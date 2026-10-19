"""Bounded native Keynote automation. Experimental: single-slide smoke-tested on macOS 27.0.1 / Keynote 13.1.

Only the fixed JXA companion is executed. Source containers are inspected and copied
before Keynote opens them. Native content/style inventory is deliberately incomplete:
chart internals, equation semantics, builds and editability still require native review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile

try:
    from presentation_route import inspect_presentation
except ImportError:
    import importlib.util
    _spec = importlib.util.spec_from_file_location("presentation_route", Path(__file__).with_name("presentation_route.py"))
    _route = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_route)
    inspect_presentation = _route.inspect_presentation

SIDECAR = Path(__file__).with_suffix(".js")
STATUS = "experimental-mac-smoke-tested"
MAX_JSON_BYTES = 32 * 1024 * 1024
MAX_OPERATIONS = 1000
LIMITATIONS = [
    "Only a synthetic single-slide inspect/edit/save/export/reopen smoke test has passed on macOS 27.0.1 with Keynote 13.1.",
    "Exposed inventory comparisons do not prove chart data, equation semantics, builds, fonts or native editability.",
    "Native content, appearance, editability and playback review remain required; no PowerPoint conversion is performed.",
]


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def load_json(path):
    path = Path(path)
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError("JSON exceeds the native adapter limit")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def linked(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def checked_path(value):
    path = Path(value).absolute()
    if any(linked(parent) for parent in (path, *path.parents)):
        raise ValueError("Linked paths are unsupported; use a regular local path")
    return path


def source_identity(value):
    path = checked_path(value)
    result = inspect_presentation(path)
    if path.suffix.lower() != ".key" or result["kind"] != "keynote-modern" or not result.get("source_sha256"):
        raise ValueError("Use a recognized modern .key file or bundle; credentials, unknown and legacy containers are excluded")
    return path, result["source_sha256"]


def fresh_paths(*values):
    paths = [checked_path(value) for value in values if value is not None]
    if len({str(path.resolve()) for path in paths}) != len(paths):
        raise ValueError("Output paths must be distinct")
    for path in paths:
        if path.exists():
            raise ValueError("Output already exists; choose fresh revision paths")
    for left in paths:
        if any(left.resolve().is_relative_to(right.resolve()) for right in paths if left != right):
            raise ValueError("Outputs must not be nested inside one another")
    return paths


def outputs_outside_sources(sources, outputs):
    for source in sources:
        source = checked_path(source).resolve()
        for output in outputs:
            output = checked_path(output).resolve()
            if output == source or output.is_relative_to(source):
                raise ValueError("Keep outputs outside the immutable source or candidate bundle")


def remember_created(path, created):
    if created is not None:
        identity = Path(path).stat()
        created.append((Path(path), identity.st_dev, identity.st_ino))


def remove_created(created):
    """Rollback only paths exclusively created by this call, never source/existing paths."""
    for path, device, inode in reversed(created):
        if linked(path) or not path.exists():
            continue
        identity = path.stat()
        if (identity.st_dev, identity.st_ino) != (device, inode) or path.resolve() != path.absolute():
            continue
        if stat.S_ISDIR(identity.st_mode):
            shutil.rmtree(path)
        else:
            path.unlink()


def save_json(path, value, created=None):
    path = checked_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        remember_created(path, created)
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def copy_new(source, destination, created=None):
    source, destination = Path(source), checked_path(destination)
    if destination.exists():
        raise ValueError("Destination already exists")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        # The route inspector has already refused links and unsafe bundle entries.
        destination.mkdir()
        remember_created(destination, created)
        shutil.copytree(source, destination, symlinks=False, dirs_exist_ok=True)
    else:
        with source.open("rb") as origin, destination.open("xb") as target:
            remember_created(destination, created)
            shutil.copyfileobj(origin, target)


def invoke_native(request, workspace, timeout=180):
    if platform.system() != "Darwin":
        raise ValueError("Native Keynote automation requires macOS; no conversion fallback was run")
    executable = Path("/usr/bin/osascript")
    if not executable.is_file() or not SIDECAR.is_file():
        raise ValueError("osascript or the packaged Keynote JXA companion is unavailable")
    request_path = Path(workspace) / "request.json"
    save_json(request_path, request)
    try:
        completed = subprocess.run(
            [str(executable), "-l", "JavaScript", str(SIDECAR), str(request_path)],
            capture_output=True, text=True, encoding="utf-8", timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ValueError("Keynote automation timed out; inspect the retained private scratch copy before retrying") from error
    if completed.returncode:
        # Native errors can quote source text; keep them out of terminal output.
        raise ValueError("Keynote automation failed; check installation, Automation permission and the private scratch request")
    if len(completed.stdout.encode("utf-8")) > MAX_JSON_BYTES:
        raise ValueError("Native response exceeds the adapter limit")
    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError("Keynote did not return the expected JSON contract") from error
    if isinstance(response, dict) and response.get("schema_version") == 1 and response.get("status") == "error":
        detail = response.get("error", {})
        stages = {"request", "application-resolution", "application-access", "document-access", "open",
                  "document-identity", "inventory", "modify", "save", "inventory-after", "export", "close"}
        stages.update("inventory-" + field for field in (
            "position", "text", "character-sizes", "character-fonts", "character-colors", "locked",
            "object-width", "object-height", "slides", "canvas-width", "canvas-height", "skipped", "notes",
            "textitems", "shapes", "tables", "iworkitems", "groups", "images", "charts", "lines", "movies", "audioclips"))
        stage = detail.get("stage") if isinstance(detail, dict) else None
        code = detail.get("code") if isinstance(detail, dict) else None
        safe_stage = stage if isinstance(stage, str) and stage in stages else "unknown"
        safe_code = code if type(code) is int else 0
        if safe_code == -1743:
            hint = " Check macOS Automation permission for this execution process."
        elif safe_code == -1700:
            hint = " Keynote rejected a scripting value or object specifier; inspect the adapter call at this stage."
        else:
            hint = " Check this execution environment's application access; Terminal and a sandboxed host can differ."
        raise ValueError(f"Keynote automation failed at {safe_stage} (Apple event {safe_code})." + hint)
    if not isinstance(response, dict) or type(response.get("schema_version")) is not int or response.get("schema_version") != 1 or response.get("status") != "ok":
        raise ValueError("Keynote refused the native operation; no requested delivery was created")
    # Retained only inside the owned scratch directory; successful callers remove it.
    # A failed inventory check must remain diagnosable without printing document text.
    save_json(Path(workspace) / "native-response.json", response)
    return response


def require_native_environment():
    if platform.system() != "Darwin":
        raise ValueError("Native Keynote automation requires macOS; no conversion fallback was run")
    if not Path("/usr/bin/osascript").is_file() or not SIDECAR.is_file():
        raise ValueError("osascript or the packaged Keynote JXA companion is unavailable")


def scratch_call(request, parent=None, keep_failure=True):
    parent = checked_path(parent) if parent else Path(tempfile.gettempdir()).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="palate-keynote-", dir=parent)).resolve()
    try:
        return invoke_native(request, workspace)
    finally:
        if (not keep_failure or sys.exc_info()[0] is None) and workspace.is_relative_to(parent.resolve()):
            shutil.rmtree(workspace)


def probe():
    result = {"schema_version": 1, "adapter_status": STATUS, "platform": platform.system(),
              "available": False, "native_automation": "not-run", "limitations": LIMITATIONS}
    if platform.system() != "Darwin":
        result["reason"] = "macOS and Keynote are required for the native path"
        return result
    try:
        response = scratch_call({"command": "probe"})
        result.update(available=True, native_automation="responded", keynote_version=response["keynote_version"])
    except (ValueError, OSError, KeyError) as error:
        result.update(native_automation="failed", reason=str(error))
    return result


def validate_inventory(inventory):
    if not isinstance(inventory, dict) or set(inventory) != {"width", "height", "slides"}:
        raise ValueError("Invalid native inventory")
    for key in ("width", "height"):
        finite_number(inventory[key], positive=True)
    slides = inventory["slides"]
    if not isinstance(slides, list) or not slides or len(slides) > 10000:
        raise ValueError("Invalid native slide inventory")
    for index, slide in enumerate(slides, 1):
        if not isinstance(slide, dict) or set(slide) != {"slide", "skipped", "notes", "counts", "text_items", "shapes", "tables"}:
            raise ValueError("Incomplete native slide inventory")
        if type(slide["slide"]) is not int or slide["slide"] != index or type(slide["skipped"]) is not bool or not isinstance(slide["notes"], str):
            raise ValueError("Invalid native slide metadata")
        count_fields = {"iwork_items", "text_items", "shapes", "images", "tables", "charts", "lines", "movies", "audio_clips"}
        if not isinstance(slide["counts"], dict) or set(slide["counts"]) != count_fields or any(type(v) is not int or v < 0 for v in slide["counts"].values()):
            raise ValueError("Invalid native object counts")
        for kind in ("text_items", "shapes"):
            if not isinstance(slide[kind], list):
                raise ValueError("Invalid native objects")
            for ordinal, item in enumerate(slide[kind], 1):
                if not isinstance(item, dict) or set(item) != {"index", "text", "locked", "bounds_points", "style", "uniform_style"}:
                    raise ValueError("Incomplete native text/shape inventory")
                if type(item["index"]) is not int or item["index"] != ordinal or not isinstance(item["text"], str) or type(item["locked"]) is not bool or type(item["uniform_style"]) is not bool:
                    raise ValueError("Invalid native object metadata")
                bounds = item["bounds_points"]
                if not isinstance(bounds, list) or len(bounds) != 4:
                    raise ValueError("Invalid native bounds")
                for coordinate in bounds:
                    finite_number(coordinate)
                if not isinstance(item["style"], dict) or set(item["style"]) != {"font_size_pt", "font_family", "color"}:
                    raise ValueError("Invalid native style inventory")
                if item["text"]:
                    finite_number(item["style"]["font_size_pt"], positive=True)
                    if not isinstance(item["style"]["font_family"], str) or not isinstance(item["style"]["color"], str) or not re.fullmatch(r"[0-9A-F]{6}", item["style"]["color"]):
                        raise ValueError("Invalid exposed native font/color")
        if not isinstance(slide["tables"], list):
            raise ValueError("Invalid native table inventory")
        for ordinal, table in enumerate(slide["tables"], 1):
            if not isinstance(table, dict) or set(table) != {"index", "rows", "columns", "cells"} or type(table["index"]) is not int or table["index"] != ordinal:
                raise ValueError("Incomplete native table inventory")
            if any(type(table[key]) is not int or table[key] < 1 for key in ("rows", "columns")) or not isinstance(table["cells"], list) or len(table["cells"]) != table["rows"] * table["columns"]:
                raise ValueError("Native table cells are incomplete")
            for cell in table["cells"]:
                if not isinstance(cell, dict) or set(cell) != {"name", "value", "formula"} or not isinstance(cell["name"], str) or not isinstance(cell["formula"], str) or cell["value"] is not None and not isinstance(cell["value"], str):
                    raise ValueError("Invalid native table cell")
        if any(slide["counts"][key] != len(slide[key]) for key in ("text_items", "shapes", "tables")):
            raise ValueError("Native object collections and counts disagree")
    return inventory


def finite_number(value, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value) or (positive and value <= 0):
        raise ValueError("Use finite numeric geometry and positive dimensions")
    return value


def inspect_native(source, pdf=None):
    source, digest = source_identity(source)
    require_native_environment()
    if pdf is not None:
        fresh_paths(pdf)
        outputs_outside_sources([source], [pdf])
    parent = checked_path(pdf).parent if pdf else Path(tempfile.gettempdir()).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="palate-keynote-", dir=parent)).resolve()
    try:
        working = workspace / "inspection.key"
        copy_new(source, working)
        request = {"command": "inspect", "document": str(working), "pdf": str(workspace / "preview.pdf") if pdf else None}
        response = invoke_native(request, workspace)
        inventory = validate_inventory(response["inventory"])
        if source_identity(source)[1] != digest:
            raise ValueError("Source changed during native inspection")
        if pdf:
            copy_pdf(workspace / "preview.pdf", pdf)
        result = {"schema_version": 1, "adapter_status": STATUS, "source_sha256": digest,
                  "inspection_sha256": canonical_hash(inventory), "inventory": inventory,
                  "keynote_version": response["keynote_version"], "limitations": LIMITATIONS,
                  "content_review": "pending", "visual_review": "pending", "editability_review": "pending", "playback_review": "pending"}
        shutil.rmtree(workspace)
        return result
    except Exception:
        # Own scratch only; retain it if Keynote is blocked or still handling an event.
        raise


def check_pdf(source):
    source = Path(source)
    if not source.is_file():
        raise ValueError("Keynote did not produce a PDF reference")
    with source.open("rb") as stream:
        header = stream.read(5)
    if header != b"%PDF-":
        raise ValueError("Keynote did not produce a PDF reference")


def copy_pdf(source, destination):
    check_pdf(source)
    copy_new(source, destination)


def review_coverage(review, digest, count):
    if not isinstance(review, dict) or review.get("source_sha256") != digest:
        raise ValueError("Source review is absent or stale")
    slides = review.get("reviewed_slides")
    if not isinstance(slides, list) or any(type(v) is not int for v in slides) or sorted(slides) != list(range(1, count + 1)):
        raise ValueError("Record actual review of every slide, including skipped slides")
    if not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip():
        raise ValueError("Name the actual reviewer")
    if not isinstance(review.get("evidence"), list) or not review["evidence"] or any(not isinstance(v, str) or not v.strip() for v in review["evidence"]):
        raise ValueError("Record actual native review evidence")


def planned_inventory(source_hash, inventory, plan):
    if not isinstance(plan, dict) or set(plan) != {"schema_version", "source_sha256", "inspection_sha256", "source_review", "operations"} or type(plan["schema_version"]) is not int or plan["schema_version"] != 1:
        raise ValueError("Unsupported native plan schema or fields")
    if plan["source_sha256"] != source_hash or plan["inspection_sha256"] != canonical_hash(inventory):
        raise ValueError("Native plan is stale; reinspect this exact source and object order")
    review_coverage(plan["source_review"], source_hash, len(inventory["slides"]))
    if plan["source_review"].get("target_safety_status") != "passed":
        raise ValueError("Review target animation, equations, emphasis and scientific encoding before applying native changes")
    operations = plan["operations"]
    if not isinstance(operations, list) or not operations or len(operations) > MAX_OPERATIONS:
        raise ValueError("Supply a bounded nonempty native operation list")
    expected = copy.deepcopy(inventory)
    for operation in operations:
        common = {"slide", "object_kind", "object_index", "action", "reason", "rule_ids"}
        action = operation.get("action") if isinstance(operation, dict) else None
        extra = {"bounds_points"} if action == "geometry" else {"style"} if action == "text_style" else set()
        if action not in {"geometry", "text_style"} or set(operation) != common | extra:
            raise ValueError("Unsupported native operation or extra fields")
        if not isinstance(operation["reason"], str) or not operation["reason"].strip():
            raise ValueError("Every operation needs a reason")
        if not isinstance(operation["rule_ids"], list) or any(not isinstance(v, str) or not re.fullmatch(r"R\d{3}", v) for v in operation["rule_ids"]):
            raise ValueError("Use decision rule identifiers or an empty list")
        slide, ordinal = operation["slide"], operation["object_index"]
        if type(slide) is not int or not 1 <= slide <= len(expected["slides"]) or type(ordinal) is not int or ordinal < 1 or operation["object_kind"] not in {"text_item", "shape"}:
            raise ValueError("Use inspected one-based native selectors")
        objects = expected["slides"][slide - 1][{"text_item": "text_items", "shape": "shapes"}[operation["object_kind"]]]
        if ordinal > len(objects):
            raise ValueError("Native selector does not exist")
        item = objects[ordinal - 1]
        if item["locked"]:
            raise ValueError("Locked objects require native authoring and review")
        if action == "geometry":
            bounds = operation["bounds_points"]
            if not isinstance(bounds, list) or len(bounds) != 4:
                raise ValueError("Geometry uses [x, y, width, height] in native points")
            for value in bounds:
                finite_number(value)
            x, y, width, height = bounds
            if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > expected["width"] or y + height > expected["height"]:
                raise ValueError("Native object must fit the actual canvas")
            if operation["object_kind"] == "shape" and bounds[2:] != item["bounds_points"][2:]:
                raise ValueError("Shape geometry is placement only; do not resize scientific diagrams")
            item["bounds_points"] = bounds
        else:
            style = operation["style"]
            if not isinstance(style, dict) or not style or not set(style) <= {"font_size_pt", "font_family", "color"}:
                raise ValueError("Only native font size, family and color styling is supported")
            if not item["text"] or not item["uniform_style"] or re.search(r"[=∑∫√±^_]|\\(?:frac|sum|int|sqrt)", item["text"]):
                raise ValueError("Mixed styles or math-bearing text require native authoring")
            if "font_size_pt" in style:
                size = style["font_size_pt"]
                if type(size) not in (int, float) or not 1 <= size <= 512 or not math.isfinite(size):
                    raise ValueError("Native font size must be a finite number between 1 and 512 points")
            if "font_family" in style and (not isinstance(style["font_family"], str) or not style["font_family"].strip() or len(style["font_family"]) > 128 or any(ord(c) < 32 for c in style["font_family"])):
                raise ValueError("Use a plain native font family name")
            if "color" in style and (not isinstance(style["color"], str) or not re.fullmatch(r"[0-9A-Fa-f]{6}", style["color"])):
                raise ValueError("Native color uses six hexadecimal digits without #")
            item["style"].update({k: v.upper() if k == "color" else v for k, v in style.items()})
    return expected


def compare_inventory(expected, actual):
    return [] if expected == actual else ["Exposed native inventory differs from the source plus approved operations"]


def apply(source, plan, output, receipt, pdf):
    source, digest = source_identity(source)
    fresh_paths(output, receipt, pdf)
    outputs_outside_sources([source], [output, receipt, pdf])
    if Path(output).suffix.lower() != ".key" or Path(pdf).suffix.lower() != ".pdf":
        raise ValueError("Use new .key and .pdf output names")
    inspection = inspect_native(source)
    expected = planned_inventory(digest, inspection["inventory"], plan)
    parent = checked_path(output).parent
    parent.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="palate-keynote-", dir=parent)).resolve()
    working, preview = workspace / "candidate.key", workspace / "candidate.pdf"
    copy_new(source, working)
    response = invoke_native({"command": "apply", "document": str(working), "pdf": str(preview),
                              "expected_inventory": inspection["inventory"], "operations": plan["operations"]}, workspace)
    actual = validate_inventory(response["inventory"])
    errors = compare_inventory(expected, actual)
    if source_identity(source)[1] != digest:
        errors.append("Source changed during native apply")
    if errors:
        raise ValueError("; ".join(errors))
    # Reopen the saved native file independently, rather than trusting in-memory state.
    reinspection = inspect_native(working)
    if compare_inventory(expected, reinspection["inventory"]):
        raise ValueError("Saved Keynote inventory changed on reopen")
    check_pdf(preview)
    result = {"schema_version": 1, "status": "candidate", "adapter_status": STATUS, "source_sha256": digest,
              "candidate_sha256": source_identity(working)[1], "plan_sha256": canonical_hash(plan),
              "exposed_inventory_status": "passed", "errors": [], "limitations": LIMITATIONS,
              "visual_review": "pending", "scientific_review": "pending", "editability_review": "pending", "playback_review": "pending"}
    created = []
    try:
        copy_new(working, output, created)
        copy_new(preview, pdf, created)
        save_json(receipt, result, created)
    except Exception:
        remove_created(created)
        raise
    shutil.rmtree(workspace)
    return result


def validate(source, candidate, plan):
    source, digest = source_identity(source)
    candidate, candidate_digest = source_identity(candidate)
    if source.resolve() == candidate.resolve():
        raise ValueError("Candidate must be a separate new file")
    source_inventory = inspect_native(source)["inventory"]
    expected = planned_inventory(digest, source_inventory, plan)
    actual = inspect_native(candidate)["inventory"]
    errors = compare_inventory(expected, actual)
    if source_identity(source)[1] != digest or source_identity(candidate)[1] != candidate_digest:
        errors.append("Source or candidate changed during validation")
    return {"schema_version": 1, "status": "candidate" if not errors else "failed", "adapter_status": STATUS,
            "source_sha256": digest, "candidate_sha256": candidate_digest, "plan_sha256": canonical_hash(plan),
            "slide_count": len(source_inventory["slides"]), "exposed_inventory_status": "passed" if not errors else "failed",
            "errors": errors, "limitations": LIMITATIONS,
            "visual_review": "pending", "scientific_review": "pending", "editability_review": "pending", "playback_review": "pending"}


def finalize(source, candidate, plan, review, output, report):
    fresh_paths(output, report, str(report) + ".validation.json")
    outputs_outside_sources([source, candidate], [output, report, str(report) + ".validation.json"])
    result = validate(source, candidate, plan)
    if result["errors"]:
        raise ValueError("Cannot finalize a failed exposed-inventory check")
    review_coverage(review, result["source_sha256"], result["slide_count"])
    if review.get("candidate_sha256") != result["candidate_sha256"] or review.get("native_application") != "Keynote":
        raise ValueError("Review must identify this candidate and actual native Keynote inspection")
    for field in ("visual_status", "scientific_status", "editability_status", "playback_status", "protected_content_status"):
        if review.get(field) != "passed":
            raise ValueError("Cannot finalize with unresolved " + field)
    if review.get("remaining_issues") != []:
        raise ValueError("Resolve remaining issues; otherwise retain the candidate label")
    if Path(output).suffix.lower() != ".key":
        raise ValueError("Native delivery must use a fresh .key path")
    final_digest = result["candidate_sha256"]
    result.update(status="finalized-as-reviewed", final_sha256=final_digest, review=review,
                  visual_review="passed_as_recorded", scientific_review="passed_as_recorded",
                  editability_review="passed_as_recorded", playback_review="passed_as_recorded")
    lines = ["# palate by Sherry: transformation report", "",
             f"Source SHA-256: `{result['source_sha256']}`.", "", f"Output SHA-256: `{final_digest}`.", "",
             "The source slide order and exposed text, notes, skipped flags and object counts were compared with the approved native plan.", "",
             "| Slide | Native selector | Change | Decision basis | Reason |", "| --- | --- | --- | --- | --- |"]
    for operation in plan["operations"]:
        reason = operation["reason"].replace("|", "/").replace("\n", " ")
        basis = ", ".join(operation["rule_ids"]) or "task-specific"
        lines.append(f"| {operation['slide']} | {operation['object_kind']} {operation['object_index']} | {operation['action']} | {basis} | {reason} |")
    lines += ["", f"Native Keynote review recorded by {review['reviewer']}; all {result['slide_count']} slides covered.", "",
              "The finalizer checks hash-bound review records. It does not independently prove the reviewer's scientific, visual, playback or editability judgments.", "", "Adapter validation status: experimental; bounded single-slide smoke test passed on macOS 27.0.1 / Keynote 13.1.", ""]
    created = []
    try:
        copy_new(candidate, output, created)
        if source_identity(output)[1] != final_digest:
            raise ValueError("Final copy changed; retain the candidate and investigate")
        checked_path(report).parent.mkdir(parents=True, exist_ok=True)
        with checked_path(report).open("x", encoding="utf-8", newline="\n") as stream:
            remember_created(checked_path(report), created)
            stream.write("\n".join(lines))
        save_json(str(report) + ".validation.json", result, created)
    except Exception:
        remove_created(created)
        raise
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("probe")
    inspection = sub.add_parser("inspect")
    inspection.add_argument("source"); inspection.add_argument("--output", required=True); inspection.add_argument("--pdf")
    for command in ("apply", "validate", "finalize"):
        item = sub.add_parser(command)
        item.add_argument("source"); item.add_argument("--plan", required=True)
        if command != "apply":
            item.add_argument("candidate")
        if command == "apply":
            item.add_argument("--output", required=True); item.add_argument("--receipt", required=True); item.add_argument("--pdf", required=True)
        elif command == "validate":
            item.add_argument("--receipt", required=True)
        else:
            item.add_argument("--review", required=True); item.add_argument("--output", required=True); item.add_argument("--report", required=True)
    args = parser.parse_args()
    if args.command == "probe":
        result = probe()
    elif args.command == "inspect":
        fresh_paths(args.output, args.pdf)
        outputs_outside_sources([args.source], [args.output] + ([args.pdf] if args.pdf else []))
        result = inspect_native(args.source, args.pdf)
        save_json(args.output, result)
    else:
        plan = load_json(args.plan)
        if args.command == "apply":
            result = apply(args.source, plan, args.output, args.receipt, args.pdf)
        elif args.command == "validate":
            fresh_paths(args.receipt)
            outputs_outside_sources([args.source, args.candidate], [args.receipt])
            result = validate(args.source, args.candidate, plan)
            save_json(args.receipt, result)
        else:
            result = finalize(args.source, args.candidate, plan, load_json(args.review), args.output, args.report)
    print(json.dumps({k: v for k, v in result.items() if k not in {"inventory", "review"}}, ensure_ascii=False))
    return 1 if result.get("status") == "failed" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print("palate Keynote: " + str(error), file=sys.stderr)
        sys.exit(2)
