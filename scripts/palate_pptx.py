"""Inspect and conservatively restyle editable PPTX objects without a lossy round trip.

Requires lxml; Pillow is optional for raster-resolution diagnostics. No python-pptx.
All documents, plans and reports are task-local. This module never uploads files.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import posixpath
import re
import shutil
import sys
import tempfile
import zipfile
from lxml import etree as E

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
EMU = 914400
ROOT = Path(__file__).resolve().parent.parent
MAX_UNCOMPRESSED = 1024 * 1024 * 1024
ALLOWED = {"geometry", "text_style", "fill", "line", "background"}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def xml(data):
    # Preserve prefixes/unknown extensions and forbid external entities and DTDs.
    parser = E.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False)
    tree = E.fromstring(data, parser)
    if tree.getroottree().docinfo.doctype:
        raise ValueError("DTD-bearing XML is unsupported")
    return tree


def canonical(tree):
    return E.tostring(tree, method="c14n")


def read_package(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP members")
        if sum(i.file_size for i in z.infolist()) > MAX_UNCOMPRESSED:
            raise ValueError("Package exceeds 1 GiB uncompressed safety limit")
        if any(n.startswith(("/", "\\")) or ".." in n.replace("\\", "/").split("/") for n in names):
            raise ValueError("Unsafe package path")
        return {n: z.read(n) for n in names}


def relationships(parts, owner):
    folder, name = posixpath.split(owner)
    relpath = posixpath.join(folder, "_rels", name + ".rels")
    if relpath not in parts:
        return {}
    return {el.get("Id"): {
        "type": el.get("Type"), "external": el.get("TargetMode") == "External",
        "target": el.get("Target") if el.get("TargetMode") == "External" else
            posixpath.normpath(posixpath.join(folder, el.get("Target").lstrip("/")))
            if not el.get("Target").startswith("/") else el.get("Target").lstrip("/")
    } for el in xml(parts[relpath])}


def slide_order(parts):
    tree = xml(parts["ppt/presentation.xml"])
    rels = relationships(parts, "ppt/presentation.xml")
    slides = []
    for el in tree.findall("p:sldIdLst/p:sldId", NS):
        ref = rels[el.get("{" + NS["r"] + "}id")]
        if ref["external"] or ref["target"] not in parts:
            raise ValueError("Invalid slide relationship")
        slides.append(ref["target"])
    return slides


def shape_id(shape):
    props = shape.find(".//p:cNvPr", NS)
    return int(props.get("id")) if props is not None else None


def shapes(tree):
    return tree.xpath("//p:spTree/*[self::p:sp or self::p:pic or self::p:graphicFrame or self::p:cxnSp or self::p:grpSp] | //p:grpSp/*[self::p:sp or self::p:pic or self::p:graphicFrame or self::p:cxnSp or self::p:grpSp]", namespaces=NS)


def text_of(shape):
    return "\n".join("".join(p.xpath(".//a:t/text()", namespaces=NS)) for p in shape.findall(".//a:p", NS))


def get_xfrm(shape):
    if E.QName(shape).localname == "graphicFrame":
        return shape.find("p:xfrm", NS)
    if E.QName(shape).localname == "grpSp":
        return shape.find("p:grpSpPr/a:xfrm", NS)
    return shape.find("p:spPr/a:xfrm", NS)


def bounds(shape):
    t = get_xfrm(shape)
    if t is None:
        return None
    off, ext = t.find("a:off", NS), t.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return [round(int(off.get("x")) / EMU, 6), round(int(off.get("y")) / EMU, 6),
            round(int(ext.get("cx")) / EMU, 6), round(int(ext.get("cy")) / EMU, 6)]


def analyse(path):
    parts = read_package(path)
    size = xml(parts["ppt/presentation.xml"]).find("p:sldSz", NS)
    result = {"schema_version": 1, "source_name": Path(path).name, "source_sha256": sha(path),
              "slide_size_inches": [int(size.get(k)) / EMU for k in ("cx", "cy")],
              "slides": [], "limitations": ["Inherited fonts/colors and group coordinates require visual inspection.",
                  "Static renders do not validate animation playback or scientific interpretation."]}
    for index, part in enumerate(slide_order(parts), 1):
        tree = xml(parts[part])
        rels = relationships(parts, part)
        record = {"slide": index, "part": part, "hidden": tree.get("show") == "0",
                  "animation": tree.find("p:timing", NS) is not None,
                  "transition": tree.find("p:transition", NS) is not None,
                  "shapes": [], "notes": "", "relationships": rels}
        for shape in shapes(tree):
            props = shape.find(".//p:cNvPr", NS)
            b = bounds(shape)
            kind = E.QName(shape).localname
            item = {"id": shape_id(shape), "kind": kind, "name": props.get("name") if props is not None else "",
                    "text": text_of(shape), "bounds_inches": b,
                    "group_local_coordinates": any(E.QName(a).localname == "grpSp" for a in shape.iterancestors()),
                    "math": bool(shape.xpath('.//*[local-name()="oMath" or local-name()="oMathPara"]')),
                    "native_table": bool(shape.findall(".//a:tbl", NS)),
                    "direct_text_styles": [dict(el.attrib) for el in shape.findall(".//a:rPr", NS)],
                    "image_references": [], "native_charts": []}
            for el in shape.xpath('.//*[@r:embed]', namespaces=NS):
                ref = rels.get(el.get("{" + NS["r"] + "}embed"), {})
                if ref:
                    image = {"part": ref["target"]}
                    try:
                        from PIL import Image
                        import io
                        with Image.open(io.BytesIO(parts[ref["target"]])) as im:
                            image["pixels"] = list(im.size)
                            if b and b[2] > 0 and b[3] > 0:
                                image["effective_ppi"] = round(min(im.width / b[2], im.height / b[3]))
                    except (ImportError, KeyError, OSError):
                        pass
                    item["image_references"].append(image)
            for el in shape.xpath('.//*[local-name()="chart"]'):
                ref = rels.get(el.get("{" + NS["r"] + "}id"))
                if ref:
                    item["native_charts"].append(ref["target"])
            record["shapes"].append(item)
        for ref in rels.values():
            if ref["type"].endswith("/notesSlide") and ref["target"] in parts:
                record["notes"] = "\n".join(xml(parts[ref["target"]]).xpath("//a:t/text()", namespaces=NS))
        result["slides"].append(record)
    result["slide_count"] = len(result["slides"])
    # Chart parts are relationship targets, not guaranteed to live at ppt/charts/chartN.xml.
    result["package_native_charts"] = sorted({chart for slide in result["slides"] for shape in slide["shapes"] for chart in shape["native_charts"]})
    result["embedded_workbooks"] = sorted(n for n in parts if n.startswith("ppt/embeddings/"))
    return result


def resolve_context(context):
    if not isinstance(context, dict):
        raise ValueError("Plan needs a context object")
    profiles = json.loads((ROOT / "references/presentation-contexts.json").read_text(encoding="utf-8-sig"))["profiles"]
    profile = next((p for p in profiles if p["id"] == context.get("profile")), None)
    if context.get("profile") and profile is None:
        raise ValueError("Unknown context profile")
    if profile and profile["skill_scope"] != "current_research_presentation_skill":
        raise ValueError("Single-page monthly updates are outside this multi-slide workflow")
    resolved = dict(context)
    if profile:
        for key in ("audience", "audience_expertise", "duration_minutes"):
            resolved.setdefault(key, profile[key])
    if not isinstance(resolved.get("audience"), str) or not resolved["audience"].strip():
        raise ValueError("Audience is required")
    number(resolved.get("duration_minutes"), "duration_minutes", 0.01, 1440)
    for key in ("detail_level", "purpose"):
        if not isinstance(resolved.get(key), str) or not resolved[key].strip():
            raise ValueError(f"{key} is required; do not invent it for a user redesign")
    return resolved


def number(value, name, lower, upper):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not lower <= value <= upper:
        raise ValueError(f"{name} must be a finite number in [{lower}, {upper}]")
    return value


def color(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError("Colors use six hex digits without #")
    return value.upper()


def fill(parent, value):
    for child in list(parent):
        if E.QName(child).localname in {"noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"}:
            parent.remove(child)
    node = E.Element("{" + NS["a"] + "}solidFill")
    E.SubElement(node, "{" + NS["a"] + "}srgbClr", val=color(value))
    # CT_ShapeProperties requires fill AFTER transform/geometry, BEFORE line/effects.
    following = {"ln", "effectLst", "effectDag", "scene3d", "sp3d", "extLst"}
    if E.QName(parent).localname == "rPr":
        following = {"effectLst", "effectDag", "highlight", "uLnTx", "uLn", "uFillTx", "uFill", "latin", "ea", "cs", "sym", "hlinkClick", "hlinkMouseOver", "rtl", "extLst"}
    elif E.QName(parent).localname == "ln":
        following = {"prstDash", "custDash", "round", "bevel", "miter", "headEnd", "tailEnd", "extLst"}
    insert = next((i for i, child in enumerate(parent) if E.QName(child).localname in following), len(parent))
    parent.insert(insert, node)


def apply_operation(tree, op, size):
    action = op["action"]
    if action == "background":
        common = tree.find("p:cSld", NS)
        bg = common.find("p:bg", NS)
        if bg is None:
            bg = E.Element("{" + NS["p"] + "}bg")
            common.insert(0, bg)
        # Background changes may replace bgRef, but never touch masters.
        for child in list(bg):
            bg.remove(child)
        props = E.SubElement(bg, "{" + NS["p"] + "}bgPr")
        fill(props, op["color"])
        return
    targets = [s for s in shapes(tree) if shape_id(s) == op.get("shape_id")]
    if len(targets) != 1:
        raise ValueError(f"Shape id {op.get('shape_id')} is missing or ambiguous")
    shape = targets[0]
    kind = E.QName(shape).localname
    if action == "geometry":
        if kind == "grpSp" or any(E.QName(a).localname == "grpSp" for a in shape.iterancestors()):
            raise ValueError("Group geometry needs a dedicated reconstruction; no silent coordinate conversion")
        t = get_xfrm(shape)
        b = bounds(shape)
        if t is None or b is None:
            raise ValueError("Inherited geometry must be materialized deliberately, not guessed")
        values = op["bounds_inches"]
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("bounds_inches must be [x,y,width,height]")
        x, y, w, h = [number(v, "bounds", 0, max(size) * 2) for v in values]
        if w <= 0 or h <= 0 or x + w > size[0] + 0.00001 or y + h > size[1] + 0.00001:
            raise ValueError("Target object must fit within the slide")
        if kind == "pic" and abs((w / h) / (b[2] / b[3]) - 1) > 0.002:
            raise ValueError("Image aspect ratio would change; scientific figures cannot be stretched")
        if shape.findall(".//a:tbl", NS) and (abs(w - b[2]) > 0.00001 or abs(h - b[3]) > 0.00001):
            raise ValueError("Native table resizing requires coordinated row/column geometry; this path supports table placement only")
        for node, attrs, vals in ((t.find("a:off", NS), ("x", "y"), (x, y)), (t.find("a:ext", NS), ("cx", "cy"), (w, h))):
            for attr, value in zip(attrs, vals):
                node.set(attr, str(round(value * EMU)))
    elif action == "text_style":
        styles = op["style"]
        if not styles or set(styles) - {"font_size_pt", "font_family", "color", "bold"}:
            raise ValueError("Unsupported/empty text style")
        if shape.xpath('.//*[local-name()="oMath" or local-name()="oMathPara"]'):
            raise ValueError("Equation styling is not handled by the conservative patcher")
        runs = shape.xpath(".//a:r | .//a:fld", namespaces=NS)
        if not runs:
            raise ValueError("Shape has no native text runs")
        for run in runs:
            props = run.find("a:rPr", NS)
            if props is None:
                props = E.Element("{" + NS["a"] + "}rPr")
                run.insert(0, props)
            if "font_size_pt" in styles:
                props.set("sz", str(round(number(styles["font_size_pt"], "font_size_pt", 1, 200) * 100)))
            if "bold" in styles:
                if not isinstance(styles["bold"], bool):
                    raise ValueError("bold must be boolean")
                props.set("b", "1" if styles["bold"] else "0")
            if "color" in styles:
                fill(props, styles["color"])
            if "font_family" in styles:
                family = styles["font_family"]
                if not isinstance(family, str) or not family.strip() or len(family) > 128:
                    raise ValueError("Invalid font_family")
                for tag in ("latin", "ea", "cs"):
                    node = props.find("a:" + tag, NS)
                    if node is None:
                        node = E.Element("{" + NS["a"] + "}" + tag)
                        # rPr font children precede hyperlinks and extLst.
                        following = {"latin": {"ea", "cs", "sym"}, "ea": {"cs", "sym"}, "cs": {"sym"}}[tag] | {"hlinkClick", "hlinkMouseOver", "rtl", "extLst"}
                        idx = next((i for i, c in enumerate(props) if E.QName(c).localname in following), len(props))
                        props.insert(idx, node)
                    node.set("typeface", family)
    elif action in {"fill", "line"}:
        if kind not in {"sp", "cxnSp"}:
            raise ValueError("Fill/line operations only support native shapes/connectors, not chart data or pictures")
        props = shape.find("p:spPr", NS)
        if props is None:
            raise ValueError("Shape properties missing")
        if action == "fill":
            fill(props, op["color"])
        else:
            line = props.find("a:ln", NS)
            if line is None:
                line = E.Element("{" + NS["a"] + "}ln")
                idx = next((i for i, c in enumerate(props) if E.QName(c).localname in {"effectLst", "effectDag", "scene3d", "sp3d", "extLst"}), len(props))
                props.insert(idx, line)
            if "color" in op:
                fill(line, op["color"])
            if "width_pt" in op:
                line.set("w", str(round(number(op["width_pt"], "width_pt", 0, 20) * 12700)))


def check_plan(source, plan):
    if plan.get("schema_version") != 1 or plan.get("source_sha256") != sha(source):
        raise ValueError("Plan schema/source hash mismatch: analyse the current input again")
    context = resolve_context(plan.get("context"))
    ops = plan.get("operations")
    if not isinstance(ops, list) or not ops:
        raise ValueError("A transformation needs at least one explicit operation")
    rules = {r["id"]: r for r in json.loads((ROOT / "references/design-decision-library.json").read_text(encoding="utf-8-sig"))["rules"]}
    permitted_keys = {"slide", "action", "shape_id", "reason", "rule_ids", "bounds_inches", "style", "color", "width_pt"}
    for op in ops:
        if not isinstance(op, dict) or set(op) - permitted_keys:
            raise ValueError("Unknown operation keys")
        if op.get("action") not in ALLOWED or isinstance(op.get("slide"), bool) or not isinstance(op.get("slide"), int):
            raise ValueError("Unknown action or non-integer slide")
        if not isinstance(op.get("reason"), str) or not op["reason"].strip():
            raise ValueError("Every operation needs a design reason")
        if not isinstance(op.get("rule_ids"), list):
            raise ValueError("rule_ids must be a list (empty for task-specific engineering corrections)")
        for rule in op["rule_ids"]:
            if rule not in rules or rules[rule].get("status") not in {"primary", "contextual"}:
                raise ValueError("Unknown or excluded rule")
    return context


def expected_parts(source, plan):
    context = check_plan(source, plan)
    parts = read_package(source)
    order = slide_order(parts)
    slide_size = xml(parts["ppt/presentation.xml"]).find("p:sldSz", NS)
    size = [int(slide_size.get(k)) / EMU for k in ("cx", "cy")]
    trees = {}
    for op in plan["operations"]:
        if not 1 <= op["slide"] <= len(order):
            raise ValueError("Slide number outside source deck")
        part = order[op["slide"] - 1]
        if part not in trees:
            trees[part] = xml(parts[part])
        tree = trees[part]
        if tree.find("p:timing", NS) is not None:
            raise ValueError(f"Slide {op['slide']} has animation. Use a dedicated PowerPoint-preserving edit and playback review")
        apply_operation(tree, op, size)
    for name, tree in trees.items():
        parts[name] = E.tostring(tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    return parts, context, set(trees)


def write_package(source, output, parts):
    # Repack without extracting media/large source folders; preserve ZIP metadata.
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() or output.resolve() == Path(source).resolve():
        raise ValueError("Output already exists or equals source")
    fd, temp = tempfile.mkstemp(suffix=".pptx", dir=output.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(source) as original, zipfile.ZipFile(temp, "w") as dest:
            for info in original.infolist():
                dest.writestr(info, parts[info.filename])
        # Exclusive creation avoids overwriting an output created during processing.
        with open(temp, "rb") as src, open(output, "xb") as dest:
            shutil.copyfileobj(src, dest)
    finally:
        Path(temp).unlink(missing_ok=True)


def content_signature(tree):
    # Independent content inventory, including run text, fields, formulas and table geometry.
    return {
        "text": tree.xpath("//a:t/text()", namespaces=NS),
        "math": [canonical(e).decode() for e in tree.xpath('//*[local-name()="oMath" or local-name()="oMathPara"]')],
        "shape_identity": [(shape_id(s), E.QName(s).localname) for s in shapes(tree)],
        "table_structure": [canonical(e).decode() for e in tree.xpath("//a:tblGrid", namespaces=NS)],
        "animation": [canonical(e).decode() for e in tree.findall("p:timing", NS)],
        "hidden": tree.get("show"),
        "references": sorted((E.QName(e).localname, k, v) for e in tree.iter() for k, v in e.attrib.items() if k.startswith("{" + NS["r"] + "}")),
    }


def validate(source, candidate, plan):
    expected, context, changed = expected_parts(source, plan)
    actual = read_package(candidate)
    original = read_package(source)
    errors = []
    if set(expected) != set(actual):
        errors.append("Package members added or removed")
    for name in sorted(set(expected) & set(actual)):
        if name in changed:
            if canonical(xml(expected[name])) != canonical(xml(actual[name])):
                errors.append(f"Unplanned XML change: {name}")
            if content_signature(xml(original[name])) != content_signature(xml(actual[name])):
                errors.append(f"Scientific/native content inventory changed: {name}")
        elif expected[name] != actual[name]:
            errors.append(f"Protected part changed: {name}")
    # The conservative path preserves all charts, workbooks, media, notes, layout/master parts,
    # relationships, equations, hidden flags and shape identities exactly or semantically.
    return {"schema_version": 1, "status": "passed" if not errors else "failed",
            "source_sha256": sha(source), "candidate_sha256": sha(candidate), "context": context,
            "changed_slide_parts": sorted(changed), "errors": errors,
            "protected_parts_checked": len(original) - len(changed),
            "content_inventory_preserved": not errors,
            "visual_review": "pending", "scientific_interpretation_review": "pending",
            "limitations": ["Structural/content conservation is not a visual or scientific correctness certification.",
                            "Raster labels cannot be parsed reliably; their image bytes are preserved."]}


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def finalize(source, candidate, plan, review, output, report):
    result = validate(source, candidate, plan)
    if result["status"] != "passed":
        raise ValueError("Cannot finalize: " + "; ".join(result["errors"]))
    if review.get("candidate_sha256") != result["candidate_sha256"]:
        raise ValueError("Visual review refers to a different candidate")
    count = len(slide_order(read_package(candidate)))
    if set(review.get("reviewed_slides", [])) != set(range(1, count + 1)):
        raise ValueError("Review every final slide, including hidden slides; record one-based slide numbers")
    for key in ("visual_status", "scientific_status", "editability_status"):
        if review.get(key) != "passed":
            raise ValueError(f"Cannot finalize with unresolved {key}")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        raise ValueError("Review needs reviewer identity (agent/human), not an invented user approval")
    issues = review.get("remaining_issues")
    if not isinstance(issues, list):
        raise ValueError("Review must list remaining issues, even if empty")
    if issues:
        raise ValueError("Resolve remaining issues before finalization; report blocked/unreviewed candidates separately")
    if Path(report).exists() or Path(output).exists():
        raise ValueError("Use new final/report paths")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(candidate, "rb") as src, open(output, "xb") as dest:
        shutil.copyfileobj(src, dest)
    result["visual_review"] = result["scientific_interpretation_review"] = "passed_as_recorded"
    result["review"] = review
    result["final_sha256"] = sha(output)
    library = {r["id"]: r for r in json.loads((ROOT / "references/design-decision-library.json").read_text(encoding="utf-8-sig"))["rules"]}
    rows = []
    for op in plan["operations"]:
        status = ", ".join(f"{r} ({library[r]['status']})" for r in op["rule_ids"]) or "task-specific"
        reason = op["reason"].replace("|", "/").replace("\n", " ")
        rows.append(f"| {op['slide']} | {op.get('shape_id', 'background')} | {op['action']} | {status} | {reason} |")
    text = "# palate. by Sherry — Transformation report\n\n" + \
        f"Source: `{Path(source).name}`; SHA-256 `{result['source_sha256']}`.\n\n" + \
        f"Output: `{Path(output).name}`; SHA-256 `{result['final_sha256']}`.\n\n" + \
        f"Context: {json.dumps(result['context'], ensure_ascii=False)}\n\n" + \
        "| Source/output slide | Native shape ID | Change | Decision basis | Reason |\n| --- | --- | --- | --- | --- |\n" + "\n".join(rows) + \
        "\n\nSlide order and source/output slide numbers are unchanged. Native object identities, all source text, equations, chart/workbook data, media, notes and references are retained.\n\n" + \
        f"Structural checks passed. Visual/scientific/editability review recorded by {review['reviewer']}; {count} slides reviewed.\n"
    Path(report).parent.mkdir(parents=True, exist_ok=True)
    with open(report, "x", encoding="utf-8") as f:
        f.write(text)
    save_json(str(report) + ".validation.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("inspect"); p.add_argument("source"); p.add_argument("--output", required=True)
    for command in ("apply", "validate", "finalize"):
        p = sub.add_parser(command)
        p.add_argument("source"); p.add_argument("--plan", required=True)
        if command == "apply":
            p.add_argument("--output", required=True); p.add_argument("--receipt", required=True)
        else:
            p.add_argument("candidate")
            if command == "validate":
                p.add_argument("--receipt", required=True)
            else:
                p.add_argument("--review", required=True); p.add_argument("--output", required=True); p.add_argument("--report", required=True)
    args = parser.parse_args()
    if args.command == "inspect":
        save_json(args.output, analyse(args.source))
        print("Inspection written; structural analysis only")
        return
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8-sig"))
    if args.command == "apply":
        if Path(args.receipt).exists():
            raise ValueError("Receipt already exists")
        parts, _, _ = expected_parts(args.source, plan)
        write_package(args.source, args.output, parts)
        result = validate(args.source, args.output, plan)
        save_json(args.receipt, result)
    elif args.command == "validate":
        result = validate(args.source, args.candidate, plan)
        save_json(args.receipt, result)
    else:
        review = json.loads(Path(args.review).read_text(encoding="utf-8-sig"))
        result = finalize(args.source, args.candidate, plan, review, args.output, args.report)
    print(json.dumps({"status": result["status"], "errors": result["errors"], "visual_review": result["visual_review"]}))
    if result["status"] != "passed":
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, E.XMLSyntaxError) as exc:
        print(f"palate. {exc}", file=sys.stderr)
        sys.exit(2)
