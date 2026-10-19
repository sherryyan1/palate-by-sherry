"""Extract an ordered, unreviewed title inventory without changing a presentation.

CLI: --source DECK.pptx|INVENTORY.json --output PRIVATE_NEW_REVIEW.json
JSON input is an explicit inventory, not a native Keynote parser. Its schema is
{schema_version: 1, source_kind: keynote|outline|manual, slides:
 [{slide_id: string, title: string|null, hidden: boolean}]}.
Use native-exported or manually confirmed titles for Keynote. Keep the output
task-local and untracked: it contains original research and private review work.
Extraction cannot establish narrative coherence or validate scientific claims.
"""

from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import posixpath
import re
import stat
import zipfile

try:
    from .palate_pptx import E, NS, xml
except ImportError:
    from palate_pptx import E, NS, xml


MAX_SOURCE_BYTES = 256 * 1024 * 1024
MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_XML_BYTES = 4 * 1024 * 1024
MAX_READ_XML_BYTES = 64 * 1024 * 1024
MAX_MEMBERS = 20_000
MAX_SLIDES = 2_000
MAX_CANDIDATES = 1_000
MAX_TEXT_LENGTH = 20_000
TITLE_TYPES = {"title", "ctrTitle"}
EXCLUDED_TYPES = {"dt", "ftr", "hdr", "sldNum"}


def _path(value):
    path = Path(value).expanduser()
    if ".." in path.parts or str(path).startswith(("\\\\", "//")):
        raise ValueError("Use a local path without parent traversal")
    if path.drive and not path.is_absolute():
        raise ValueError("Drive-relative paths are unsupported")
    absolute = Path(os.path.abspath(path))
    if any(":" in part for part in absolute.parts if part != absolute.anchor):
        raise ValueError("Alternate data streams and colon-bearing path components are unsupported")
    return absolute


def _reject_links(path):
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (getattr(info, "st_file_attributes", 0)
                & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):
            raise ValueError("Symlink and reparse-point paths are unsupported")


def _read_source(path, limit):
    _reject_links(path)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError("Input must be a regular file within the size limit")
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("Input exceeds the supported size")
    return raw


def _text(value, name, allow_empty=False, maximum=MAX_TEXT_LENGTH):
    if not isinstance(value, str) or len(value) > maximum or (not allow_empty and not value.strip()):
        raise ValueError(f"Invalid {name}")
    if any((ord(c) < 32 and c not in "\n\r\t") or ord(c) == 127 for c in value):
        raise ValueError(f"Control characters are unsupported in {name}")
    return value


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON keys are unsupported")
        result[key] = value
    return result


def _inventory(raw):
    data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    if (not isinstance(data, dict) or set(data) != {"schema_version", "source_kind", "slides"}
            or type(data["schema_version"]) is not int or data["schema_version"] != 1
            or data["source_kind"] not in ("keynote", "outline", "manual")):
        raise ValueError("Expected a version-1 keynote, outline or manual title inventory")
    if not isinstance(data["slides"], list) or not 1 <= len(data["slides"]) <= MAX_SLIDES:
        raise ValueError("Inventory slide count is outside the supported range")
    slides, identities = [], set()
    for item in data["slides"]:
        if not isinstance(item, dict) or set(item) != {"slide_id", "title", "hidden"}:
            raise ValueError("Each slide needs exactly slide_id, title and hidden")
        identity = _text(item["slide_id"], "slide_id", maximum=200)
        if identity in identities or type(item["hidden"]) is not bool:
            raise ValueError("Slide IDs must be unique and hidden must be boolean")
        identities.add(identity)
        title = item["title"]
        if title is not None:
            _text(title, "title", allow_empty=True)
        slides.append({"slide_id": identity, "hidden": item["hidden"], "part": None,
                       "relationship_id": None, "original_title": title,
                       "title_status": "provided" if title and title.strip() else "missing",
                       "title_candidates": [] if title is None else [{"text": title, "basis": "explicit_inventory"}],
                       "extraction_notes": []})
    return data["source_kind"], slides


class _Package:
    """Read only relevant XML, bounded before decompression, using the shared parser."""

    def __init__(self, archive):
        self.archive, self.cache, self.total = archive, {}, 0
        members = archive.infolist()
        names = [item.filename for item in members]
        if len(names) > MAX_MEMBERS or len(set(names)) != len(names):
            raise ValueError("Too many or duplicate package members")
        if any(name.startswith("/") or "\\" in name or ":" in name or
               ".." in name.split("/") for name in names):
            raise ValueError("Unsafe package member path")
        self.members = {item.filename: item for item in members}

    def read(self, part):
        if part in self.cache:
            return self.cache[part]
        info = self.members.get(part)
        if info is None or info.is_dir() or info.file_size > MAX_XML_BYTES:
            raise ValueError("Missing or oversized XML part")
        self.total += info.file_size
        if self.total > MAX_READ_XML_BYTES:
            raise ValueError("Selected XML exceeds the total read budget")
        with self.archive.open(info) as stream:
            raw = stream.read(MAX_XML_BYTES + 1)
        if len(raw) > MAX_XML_BYTES:
            raise ValueError("XML part exceeds the read limit")
        try:
            self.cache[part] = xml(raw)
        except E.XMLSyntaxError as error:
            raise ValueError("Malformed XML part") from error
        return self.cache[part]

    def relationships(self, owner):
        folder, name = posixpath.split(owner)
        part = posixpath.join(folder, "_rels", name + ".rels")
        if part not in self.members:
            return {}
        result = {}
        for item in self.read(part):
            if item.tag != "{" + NS["rel"] + "}Relationship":
                continue
            identity, target, kind = item.get("Id"), item.get("Target"), item.get("Type")
            if not identity or identity in result or not target or not kind:
                raise ValueError("Missing or duplicate relationship identity")
            external = item.get("TargetMode") == "External"
            if not external:
                if "\\" in target or ":" in target:
                    raise ValueError("Unsafe internal relationship target")
                target = posixpath.normpath(target.lstrip("/") if target.startswith("/")
                                           else posixpath.join(folder, target))
                if target == ".." or target.startswith("../"):
                    raise ValueError("Relationship escapes the package")
            result[identity] = {"target": target, "type": kind, "external": external}
        return result


def _shape_text(shape):
    paragraphs = []
    for paragraph in shape.findall("p:txBody/a:p", NS):
        paragraphs.append("".join("\n" if element.tag == "{" + NS["a"] + "}br" else element.text or ""
                                  for element in paragraph.iter()
                                  if element.tag in {"{" + NS["a"] + "}t", "{" + NS["a"] + "}br"}))
    return _text("\n".join(paragraphs), "shape text", allow_empty=True)


def _shape_hidden(shape):
    for node in (shape, *shape.iterancestors()):
        if node.tag == "{" + NS["p"] + "}sp":
            props = node.find("p:nvSpPr/p:cNvPr", NS)
        elif node.tag == "{" + NS["p"] + "}grpSp":
            props = node.find("p:nvGrpSpPr/p:cNvPr", NS)
        else:
            continue
        hidden = props.get("hidden", "0") if props is not None else "0"
        if hidden not in ("0", "1", "false", "true"):
            raise ValueError("Invalid shape visibility flag")
        if hidden in ("1", "true"):
            return True
    return False


def _candidates(package, part, tree):
    layout_types = {}
    layout_refs = [ref for ref in package.relationships(part).values() if ref["type"].endswith("/slideLayout")]
    if len(layout_refs) > 1 or any(ref["external"] for ref in layout_refs):
        raise ValueError("Invalid slide layout relationship")
    if layout_refs:
        layout = package.read(layout_refs[0]["target"])
        if layout.tag != "{" + NS["p"] + "}sldLayout":
            raise ValueError("Invalid slide layout XML root")
        for placeholder in layout.findall("p:cSld/p:spTree/.//p:sp/p:nvSpPr/p:nvPr/p:ph", NS):
            layout_types.setdefault(placeholder.get("idx", "0"), set()).add(placeholder.get("type", "obj"))
    titles, fallback, notes, shape_ids = [], [], [], set()
    shapes = tree.findall("p:cSld/p:spTree/.//p:sp", NS)
    if len(shapes) > MAX_CANDIDATES:
        raise ValueError("Too many text shapes on one slide")
    for shape in shapes:
        text = _shape_text(shape)
        props = shape.find("p:nvSpPr/p:cNvPr", NS)
        shape_id = props.get("id") if props is not None else None
        if shape_id is None or shape_id in shape_ids:
            raise ValueError("Missing or duplicate shape identity")
        shape_ids.add(shape_id)
        if _shape_hidden(shape):
            note = "Text shapes hidden directly or by a containing group were excluded from title candidates."
            if note not in notes:
                notes.append(note)
            continue
        placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
        kind = placeholder.get("type") if placeholder is not None else None
        inherited = False
        if placeholder is not None and kind is None:
            matches = layout_types.get(placeholder.get("idx", "0"), set())
            if len(matches) == 1:
                kind = next(iter(matches))
                inherited = True
            elif len(matches) > 1:
                notes.append("Ambiguous inherited placeholder type; title needs confirmation.")
        if kind in EXCLUDED_TYPES:
            continue
        candidate = {"shape_id": shape_id, "text": text,
                     "basis": "layout_title_placeholder" if inherited else "title_placeholder"}
        if kind in TITLE_TYPES:
            if text.strip():
                titles.append(candidate)
            else:
                notes.append("An empty title placeholder is present.")
        elif text.strip():
            fallback.append({**candidate, "basis": "unconfirmed_text_shape"})
    if len(titles) == 1:
        return titles[0]["text"], "identified", titles, notes
    if titles:
        return None, "ambiguous", titles, notes
    return None, "needs_confirmation" if fallback else "missing", fallback, notes


def _pptx(raw):
    with zipfile.ZipFile(BytesIO(raw)) as archive:
        package = _Package(archive)
        presentation = package.read("ppt/presentation.xml")
        if presentation.tag != "{" + NS["p"] + "}presentation":
            raise ValueError("Invalid presentation XML root")
        relations = package.relationships("ppt/presentation.xml")
        entries = presentation.findall("p:sldIdLst/p:sldId", NS)
        if not 1 <= len(entries) <= MAX_SLIDES:
            raise ValueError("Presentation slide count is outside the supported range")
        slides, identities, parts = [], set(), set()
        for entry in entries:
            identity = entry.get("id")
            relationship_id = entry.get("{" + NS["r"] + "}id")
            ref = relations.get(relationship_id)
            if (not identity or not re.fullmatch(r"[0-9]+", identity) or identity in identities
                    or not ref or ref["external"] or not ref["type"].endswith("/slide")
                    or ref["target"] in parts):
                raise ValueError("Invalid or duplicate slide identity or relationship")
            identities.add(identity)
            parts.add(ref["target"])
            tree = package.read(ref["target"])
            if tree.tag != "{" + NS["p"] + "}sld" or tree.get("show", "1") not in ("0", "1", "true", "false"):
                raise ValueError("Invalid slide XML or visibility flag")
            title, status, candidates, notes = _candidates(package, ref["target"], tree)
            slides.append({"slide_id": identity, "relationship_id": relationship_id, "part": ref["target"],
                           "hidden": tree.get("show", "1") in ("0", "false"), "original_title": title,
                           "title_status": status, "title_candidates": candidates, "extraction_notes": notes})
    return "pptx", slides


def build_review(source):
    """Read source bytes once; return unreviewed scaffolding without writing files."""
    source = _path(source)
    suffix = source.suffix.lower()
    if suffix not in (".pptx", ".json"):
        raise ValueError("Use a PPTX or explicit JSON inventory; native Keynote conversion is not required")
    raw = _read_source(source, MAX_JSON_BYTES if suffix == ".json" else MAX_SOURCE_BYTES)
    kind, slides = _pptx(raw) if suffix == ".pptx" else _inventory(raw)
    duplicates = {}
    for index, slide in enumerate(slides, 1):
        slide["original_position"] = index
        title = slide["original_title"]
        if title and title.strip():
            duplicates.setdefault(" ".join(title.split()).casefold(), []).append(slide["slide_id"])
    previous = None
    for slide in slides:
        slide["previous_visible_slide_id"] = previous
        if not slide["hidden"]:
            previous = slide["slide_id"]
    following = None
    for slide in reversed(slides):
        slide["next_visible_slide_id"] = following
        if not slide["hidden"]:
            following = slide["slide_id"]
    for slide in slides:
        title = slide["original_title"]
        slide["same_title_slide_ids"] = [identity for identity in duplicates.get(" ".join(title.split()).casefold(), [])
                                         if identity != slide["slide_id"]] if title else []
        slide["review"] = {"narrative_role": None, "relationship_to_previous": None,
                           "relationship_to_next": None, "source_evidence": [],
                           "decision": None, "proposed_title": None, "reviewer_notes": None}
    return {"schema_version": 1, "status": "unreviewed", "narrative_validated": False,
            "source": {"filename": source.name, "sha256": hashlib.sha256(raw).hexdigest(), "kind": kind},
            "decision_options": ["retain", "revise"], "slides": slides,
            "ending_review": {"status": "unreviewed", "task_scope": None,
                              "ending_policy": None, "closing_slide_id": None,
                              "appendix_start_slide_id": None, "purpose": None,
                              "decision": None, "reason": None},
            "limitations": ["Title extraction is not narrative review or scientific validation.",
                            "Ending review requires the brief and inspected main/appendix sequence; no closing purpose or boundary is inferred.",
                            "Original order includes hidden slides; visible neighbors exclude them.",
                            "Repeated titles can be intentional progressive builds, not errors.",
                            "Custom, image-based or complex titles need native or visual confirmation.",
                            "JSON titles are supplied inventory data, not parsed native Keynote content.",
                            "No role, presentation language or proposed title is inferred."]}


def export_review(source, output):
    output = _path(output)
    if output.suffix.lower() != ".json" or not output.parent.is_dir():
        raise ValueError("Output must be a new JSON file in an existing private directory")
    _reject_links(output)
    if output.exists():
        raise FileExistsError("Output already exists; choose a new private path")
    report = build_review(source)
    payload = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(output, flags, 0o600), "wb") as stream:
        stream.write(payload)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True, help="New private, untracked JSON file; never overwritten")
    args = parser.parse_args()
    try:
        report = export_review(args.source, args.output)
    except (ValueError, OSError, UnicodeError, zipfile.BadZipFile, RuntimeError, NotImplementedError) as error:
        parser.exit(2, f"Title inventory failed: {error}\n")
    print(f"Wrote unreviewed title inventory for {len(report['slides'])} slides. Narrative review is still required.")


if __name__ == "__main__":
    main()
