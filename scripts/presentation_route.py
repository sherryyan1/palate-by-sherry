"""Inspect supplied materials and select the palate presentation workflow.

Read-only, standard-library helper: no conversion, application launch or upload.
Keynote signatures recognize containers, not native validity or editable objects.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile

MAX_PACKAGE_BYTES = 1024 * 1024 * 1024
MAX_XML_BYTES = 8 * 1024 * 1024
MAX_INDEX_BYTES = 32 * 1024 * 1024
MAX_TEXT_BYTES = 8 * 1024 * 1024
MAX_MEMBERS = 100000
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PRESENTATION_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DOCUMENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}
CREDENTIAL = re.compile(
    rb"-----BEGIN (?:[A-Z0-9]+ )*(?:PRIVATE KEY|PUBLIC KEY|CERTIFICATE)-----|"
    rb"PuTTY-User-Key-File-|openssh-key-v1|(?:ssh-rsa|ssh-ed25519|ecdsa-sha2-\S+) ",
    re.IGNORECASE,
)


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_members(archive):
    infos = archive.infolist()
    names = [item.filename for item in infos]
    if len(infos) > MAX_MEMBERS or sum(item.file_size for item in infos) > MAX_PACKAGE_BYTES:
        raise ValueError("Container exceeds inspection limits")
    if len(names) != len(set(names)):
        raise ValueError("Duplicate container members")
    for item in infos:
        name = item.filename
        if not name or "\\" in name or name.startswith("/") or ":" in name or ".." in name.split("/"):
            raise ValueError("Unsafe container member")
        if stat.S_ISLNK(item.external_attr >> 16):
            raise ValueError("Linked container members are unsupported")
        if item.flag_bits & 1:
            raise ValueError("Encrypted container requires an application export")
    return {item.filename: item for item in infos if not item.is_dir()}


def bounded_read(archive, name, limit):
    if archive.getinfo(name).file_size > limit:
        raise ValueError("Container metadata exceeds inspection limits")
    with archive.open(name) as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Container metadata exceeds inspection limits")
    return data


def xml_metadata(archive, name):
    data = bounded_read(archive, name, MAX_XML_BYTES)
    # Removing NULs also exposes ASCII declarations in UTF-16/UTF-32 metadata.
    if re.search(rb"<!\s*(?:DOCTYPE|ENTITY)\b", data.replace(b"\x00", b""), re.IGNORECASE):
        raise ValueError("DTD-bearing metadata is unsupported")
    return ET.fromstring(data)


def keynote_signature(names):
    """Conservative modern Keynote signature, shared by ZIP and directory forms."""
    return "Index/Document.iwa" in names and any(
        re.fullmatch(r"Index/(?:Slide|MasterSlide)(?:[-_].+)?\.iwa", name)
        for name in names
    )


def nested_keynote_signature(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = checked_members(archive)
        return keynote_signature({"Index/" + name for name in names})


def pptx_signature(archive, names):
    """Check core OOXML structure before dispatching to full PPTX inspection."""
    required = {"[Content_Types].xml", "_rels/.rels", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"}
    if not required <= names.keys():
        return False
    types = xml_metadata(archive, "[Content_Types].xml")
    if types.tag != "{" + CT + "}Types" or not any(
        node.tag == "{" + CT + "}Override" and node.get("PartName") == "/ppt/presentation.xml"
        and node.get("ContentType") == PRESENTATION_TYPE for node in types
    ):
        return False
    roots = xml_metadata(archive, "_rels/.rels")
    if roots.tag != "{" + REL + "}Relationships" or not any(
        node.get("Type") == R + "/officeDocument" and node.get("Target", "").lstrip("/") == "ppt/presentation.xml"
        and node.get("TargetMode") != "External" for node in roots
    ):
        return False
    presentation = xml_metadata(archive, "ppt/presentation.xml")
    rels = xml_metadata(archive, "ppt/_rels/presentation.xml.rels")
    if presentation.tag != "{" + P + "}presentation" or rels.tag != "{" + REL + "}Relationships":
        return False
    size = presentation.find("{" + P + "}sldSz")
    if size is None or any(not size.get(k, "").isdigit() or int(size.get(k)) <= 0 for k in ("cx", "cy")):
        return False
    links = {node.get("Id"): node for node in rels}
    slide_ids = presentation.findall("{" + P + "}sldIdLst/{" + P + "}sldId")
    for slide in slide_ids:
        link = links.get(slide.get("{" + R + "}id"))
        if link is None or link.get("Type") != R + "/slide" or link.get("TargetMode") == "External":
            return False
        target = link.get("Target", "")
        if "\\" in target or ".." in target.split("/"):
            return False
        part = target.lstrip("/") if target.startswith("/") else str(PurePosixPath("ppt") / target)
        if part not in names or xml_metadata(archive, part).tag != "{" + P + "}sld":
            return False
    return True


def inspect_presentation(path):
    """Return container evidence without returning source text or modifying files."""
    source = Path(path).absolute()
    result = {"source_name": source.name, "kind": "unknown", "container": "unknown", "evidence": []}
    try:
        if source.is_symlink():
            raise ValueError("Linked sources are unsupported; select the original file")
        if not source.exists():
            raise ValueError("Source does not exist")
        if source.is_dir():
            result["container"] = "directory"
            if source.suffix.lower() != ".key":
                raise ValueError("Directory is not a .key presentation bundle")
            names = set()
            total = 0
            for item in source.rglob("*"):
                if item.is_symlink() or not item.resolve().is_relative_to(source.resolve()):
                    raise ValueError("Linked bundle members are unsupported")
                if item.is_file():
                    names.add(item.relative_to(source).as_posix())
                    total += item.stat().st_size
                    if total > MAX_PACKAGE_BYTES or len(names) > MAX_MEMBERS:
                        raise ValueError("Bundle exceeds inspection limits")
            modern = keynote_signature(names)
            if not modern and "Index.zip" in names:
                index = source / "Index.zip"
                if index.stat().st_size > MAX_INDEX_BYTES:
                    raise ValueError("Bundle index exceeds inspection limits")
                modern = nested_keynote_signature(index.read_bytes())
            if modern:
                result.update(kind="keynote-modern", evidence=["IWA document and slide members"])
            elif any(name.lower() in {"index.apxl", "index.apxl.gz"} for name in names):
                result.update(kind="keynote-legacy", evidence=["Legacy APXL marker; requires Keynote inspection"])
            else:
                result["evidence"] = ["No recognized Keynote document/slide signature"]
            if result["kind"] in {"keynote-modern", "keynote-legacy"}:
                # Both native package forms need a complete, read-only source identity.
                digest = hashlib.sha256()
                for name in sorted(names):
                    digest.update(json.dumps([name, file_hash(source / name)], ensure_ascii=True).encode("ascii") + b"\n")
                result.update(source_sha256=digest.hexdigest(), hash_kind="bundle-manifest-sha256")
            return result
        if not source.is_file():
            raise ValueError("Source is not a regular file")
        with source.open("rb") as stream:
            head = stream.read(4096)
        # .key is also used for credentials. Never display their text or try to convert it.
        if CREDENTIAL.search(head):
            result.update(kind="credential-key", container="text", evidence=["Credential signature; excluded from presentation workflow"])
            return result
        if head.startswith(b"%PDF-"):
            result.update(kind="pdf", container="file", source_sha256=file_hash(source), hash_kind="file-sha256",
                          evidence=["PDF signature; visual reference only"])
            return result
        if zipfile.is_zipfile(source):
            result["container"] = "zip"
            with zipfile.ZipFile(source) as archive:
                names = checked_members(archive)
                if pptx_signature(archive, names):
                    result.update(kind="pptx", evidence=["Core transitional OOXML presentation and slide structure"])
                elif keynote_signature(names) or ("Index.zip" in names and nested_keynote_signature(
                    bounded_read(archive, "Index.zip", MAX_INDEX_BYTES))):
                    result.update(kind="keynote-modern", evidence=["IWA document and slide members"])
                elif any(name.lower() in {"index.apxl", "index.apxl.gz"} for name in names):
                    result.update(kind="keynote-legacy", evidence=["Legacy APXL marker; requires Keynote inspection"])
                else:
                    result["evidence"] = ["No recognized presentation package signature"]
            if result["kind"] != "unknown":
                result.update(source_sha256=file_hash(source), hash_kind="file-sha256")
        else:
            result["container"] = "file"
            result["evidence"] = ["Unrecognized file; extension alone does not establish a presentation"]
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, ET.ParseError) as error:
        result.update(kind="unknown", evidence=[str(error)])
    return result


def docx_signature(archive, names):
    """Recognize a non-macro Word document without returning its content."""
    required = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
    if not required <= names.keys():
        return False
    types = xml_metadata(archive, "[Content_Types].xml")
    if types.tag != "{" + CT + "}Types" or not any(
        node.tag == "{" + CT + "}Override" and node.get("PartName") == "/word/document.xml"
        and node.get("ContentType") == DOCUMENT_TYPE for node in types
    ):
        return False
    rels = xml_metadata(archive, "_rels/.rels")
    if rels.tag != "{" + REL + "}Relationships" or not any(
        node.get("Type") == R + "/officeDocument" and node.get("Target", "").lstrip("/") == "word/document.xml"
        and node.get("TargetMode") != "External" for node in rels
    ):
        return False
    document = xml_metadata(archive, "word/document.xml")
    if document.tag != "{" + W + "}document" or document.find("{" + W + "}body") is None:
        return False
    if CREDENTIAL.search("".join(document.itertext()).encode("utf-8")):
        raise ValueError("Credential signature; exclude this source from the presentation workflow")
    return True


def pdf_material_signature(source):
    """Check PDF boundaries and an xref location, not page readability or validity."""
    with source.open("rb") as stream:
        if not re.match(rb"%PDF-(?:1\.[0-7]|2\.0)[\r\n]", stream.read(16)):
            return False
        size = source.stat().st_size
        stream.seek(max(0, size - 4096))
        trailer = re.search(rb"startxref\s+(\d+)\s+%%EOF\s*$", stream.read(4096))
        if trailer is None:
            return False
        offset = int(trailer.group(1))
        if offset <= 0 or offset >= size:
            return False
        stream.seek(offset)
        cross_reference = stream.read(8192)
    return bool(re.match(rb"xref(?:\s|$)", cross_reference) or (
        re.match(rb"\d+\s+\d+\s+obj\s*<<", cross_reference)
        and re.search(rb"/Type\s*/XRef\b", cross_reference.split(b"stream", 1)[0])
    ))


def inspect_material(path, source_kind):
    """Check an explicitly selected text or paper source without returning its text."""
    source = Path(path).absolute()
    result = {"source_name": source.name, "kind": "unknown", "container": "unknown", "evidence": []}
    try:
        if source.is_symlink():
            raise ValueError("Linked sources are unsupported; select the original file")
        if not source.is_file():
            raise ValueError("Select an existing regular source file")
        if not 0 < source.stat().st_size <= MAX_PACKAGE_BYTES:
            raise ValueError("Source is empty or exceeds inspection limits")
        suffix = source.suffix.lower()
        with source.open("rb") as stream:
            head = stream.read(4096)
        if CREDENTIAL.search(head.replace(b"\x00", b"")):
            result.update(kind="credential-key", container="text", evidence=["Credential signature; excluded from presentation workflow"])
            return result
        if source_kind == "paper" and suffix == ".pdf":
            if not pdf_material_signature(source):
                raise ValueError("No recognized PDF header, cross-reference and end marker; obtain a readable source")
            result.update(kind="pdf", container="file", evidence=["PDF container markers; paper purpose explicitly selected, content inspection pending"])
        elif suffix == ".docx":
            if not zipfile.is_zipfile(source):
                raise ValueError("No recognized Word document package")
            with zipfile.ZipFile(source) as archive:
                if not docx_signature(archive, checked_members(archive)):
                    raise ValueError("No recognized non-macro Word document structure")
            result.update(kind="docx", container="zip", evidence=["Core transitional OOXML Word structure; content inspection pending"])
        elif suffix in TEXT_EXTENSIONS:
            if source.stat().st_size > MAX_TEXT_BYTES:
                raise ValueError("Text source exceeds inspection limits")
            data = source.read_bytes()
            try:
                text = data.decode("utf-16" if data.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
            except UnicodeError:
                raise ValueError("Use UTF-8 text or BOM-marked UTF-16 text") from None
            if not text.strip() or any(ord(char) < 32 and char not in "\t\r\n" for char in text):
                raise ValueError("Source does not contain recognized plain text")
            if CREDENTIAL.search(text.encode("utf-8")):
                result.update(kind="credential-key", container="text", evidence=["Credential signature; excluded from presentation workflow"])
                return result
            if text.lstrip().startswith(("%PDF-", "{\\rtf")):
                raise ValueError("Container content does not match the selected text file type")
            result.update(kind="text", container="text", evidence=["Nonempty Unicode text; content inspection pending"])
        else:
            raise ValueError("Use .txt, .md or .docx material; the paper route also accepts a recognizable .pdf")
        result.update(source_sha256=file_hash(source), hash_kind="file-sha256")
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, ET.ParseError) as error:
        # Parser exceptions can refer to source content. Return only controlled messages.
        detail = str(error) if type(error) is ValueError else "Source container could not be inspected safely"
        result.update(kind="unknown", evidence=[detail])
    return result


def route_material(path, target, source_kind):
    source = inspect_material(path, source_kind)
    explicit = target not in {None, "auto"}
    result = {"schema_version": 1, "skill": "palate", "source_kind": source_kind, "source": source,
              "target": target if explicit else None, "target_origin": "explicit" if explicit else "pending",
              "conversion_requested": False, "status": "unsupported", "can_transform_now": False,
              "can_deliver_target_now": False, "adapter": None, "steps": [],
              "source_policy": "Preserve the original material and hash. Create a new deck in the chosen delivery application; a paper or text file has no source presentation application.",
              "native_keynote_adapter": json.loads((Path(__file__).resolve().parents[1] / "references/native-capabilities.json").read_text())["Keynote"]["adapter_status"],
              "validation": {"content": "pending", "appearance": "pending", "editability": "pending", "keynote_runtime": "not-run"},
              "limitations": [
                  "Material recognition is not content extraction, source verification or a completed slide deck.",
                  "Reading text, figures, equations and captions requires suitable tools; do not infer unreadable scientific content.",
                  "New slides require an available editable authoring workflow, followed by content, appearance and editability review in the delivery application.",
                  "The bounded PowerPoint and Keynote adapters do not create slides from text or papers. Native Mac integration remains untested in this repository.",
              ]}
    if source["kind"] not in {"text", "docx", "pdf"}:
        result["steps"] = ["Exclude credentials and unsupported sources. Select readable text or paper material without renaming another file to simulate its format."]
        return result
    result.update(status="requires-native-authoring" if explicit else "requires-delivery-target",
                  adapter=("new-" + target + "-authoring") if explicit else "new-deck-authoring")
    if target == "keynote":
        result["keynote_environment"] = keynote_environment()
    result["steps"] = [] if explicit else [
        "Ask whether the new deck should be delivered in PowerPoint or Keynote; do not infer the application from this material or request a format conversion. Source inspection may proceed independently."
    ]
    result["steps"] += [
        "Inspect the supplied material with suitable reading tools, resolve the missing presentation brief and keep a private source-to-output ledger using pages, sections, paragraphs and figure, table or equation identities.",
        "Organize an audience-appropriate explanation around source-supported claims and evidence. Preserve qualifications and attribution; ask about material gaps instead of inventing findings, data or references.",
        "Use an available authoring workflow to create a new editable deck in the selected application. The preservation helpers cannot build it from this source.",
        "Review scientific content against the material, then inspect rendered appearance and native editability in the delivery application. Missing authoring or review access leaves the corresponding work pending; any unchecked output remains a candidate.",
    ]
    return result


def keynote_environment():
    """Detect local prerequisites without launching Keynote or granting automation."""
    mac = sys.platform == "darwin"
    runner = shutil.which("osascript") if mac else None
    candidates = (Path("/Applications/Keynote.app"), Path.home() / "Applications/Keynote.app")
    app = next((str(p) for p in candidates if p.is_dir()), None) if mac else None
    return {"platform": sys.platform, "osascript": runner, "keynote_app": app,
            "prerequisites_detected": bool(mac and runner and app),
            "automation_access": "not-probed", "native_mac_validation": "not-run"}


def route_presentation(path, target=None, source_kind="slides"):
    """Preserve slide-source applications; route explicit material sources to authoring."""
    if target not in {None, "auto", "pptx", "keynote"}:
        raise ValueError("Target must be auto, pptx or keynote")
    if source_kind not in {"slides", "text", "paper"}:
        raise ValueError("Source kind must be slides, text or paper")
    if source_kind != "slides":
        return route_material(path, target, source_kind)
    source = inspect_presentation(path)
    kind = source["kind"]
    source_application = "pptx" if kind == "pptx" else "keynote" if kind in {"keynote-modern", "keynote-legacy"} else None
    explicit = target not in {None, "auto"}
    resolved_target = target if explicit else source_application
    conversion = bool(source_application and resolved_target != source_application)
    result = {"schema_version": 1, "skill": "palate", "source": source,
              "target": resolved_target, "target_origin": "explicit" if explicit else "source",
              "conversion_requested": conversion, "status": "unsupported", "can_transform_now": False,
              "can_deliver_target_now": False, "adapter": None, "steps": [],
              "source_policy": "Preserve the source application and original hash; work on new native copies. Convert formats only for an explicit target request.",
              "native_keynote_adapter": json.loads((Path(__file__).resolve().parents[1] / "references/native-capabilities.json").read_text())["Keynote"]["adapter_status"],
              "validation": {"content": "pending", "appearance": "pending", "editability": "pending", "keynote_runtime": "not-run"}}
    if source_application == "keynote" or resolved_target == "keynote":
        result["keynote_environment"] = keynote_environment()
    if conversion:
        result.update(status="requires-format-conversion", adapter="explicit-application-conversion")
        if resolved_target == "keynote":
            result["steps"] = [
                "The requested target differs from the PowerPoint source. Preserve the original; in Keynote on Mac open a duplicate using File > Open and save a new .key baseline.",
                "Compare the imported native baseline against the original before redesign, including scientific content, objects, fonts, notes and builds. Record conversion effects separately.",
                "Route the saved .key again with the default native Keynote path; complete native inspection, editing and review before delivery.",
            ]
        else:
            result["steps"] = [
                "The requested target differs from the Keynote source. Preserve the original; export a new PowerPoint copy from Keynote on Mac using File > Export To > PowerPoint.",
                "Compare the exported baseline against the original before redesign; record scientific content and conversion effects separately. A PDF can supplement visual comparison only.",
                "Route the exported .pptx again for the native PowerPoint workflow; review the actual delivery in PowerPoint, without requiring a particular operating system.",
            ]
    elif kind == "pptx":
        result.update(status="ready-pptx",
                      can_transform_now=True, adapter="shared-pptx-workflow")
        result["steps"] = [
            "Run scripts/palate_pptx.py inspect on the source; complete the shared intake, design and scientific-fidelity workflow.",
            "Create a new editable PPTX candidate; compare source/candidate content, rendered slides and native objects independently.",
            "Review final appearance, native editability and any playback in the delivery PowerPoint application. The included Windows renderer is one option, not a global platform requirement.",
        ]
    elif kind in {"keynote-modern", "keynote-legacy"}:
        environment = result["keynote_environment"]
        result.update(status="requires-keynote-preflight" if environment["prerequisites_detected"] else "requires-keynote-runtime",
                      adapter="native-keynote")
        result["steps"] = [
            "Keep the .key source and delivery format. In a Mac environment with Keynote, run scripts/keynote_native.py probe, then inspect a private duplicate before planning native changes.",
            "Use the native Keynote adapter for supported bounded edits and a new .key candidate; export PDF previews directly from Keynote. No PowerPoint conversion or Windows application is required for this route.",
            "Independently review scientific content, every rendered slide, native editability and any builds or media in Keynote; complete the hash-bound review before finalization.",
            "If the Mac runtime, automation permission or required operation is unavailable, keep native delivery pending and explain what is needed. Offer cross-format work only as a user-selected alternative.",
        ]
        if kind == "keynote-legacy":
            result["steps"][0] = "Keep the legacy .key original. Run scripts/keynote_native.py probe on Mac, then open a private duplicate in Keynote, review it and save a new modern .key baseline. Route that baseline again before using the native adapter, which does not accept legacy APXL containers."
    elif kind == "pdf":
        result.update(status="reference-only", adapter="visual-reference")
        result["steps"] = ["Use the PDF for visual review; obtain the editable PowerPoint or native Keynote source before polishing native slide objects."]
    elif kind == "credential-key":
        result["steps"] = ["Exclude this credential file; select the actual presentation. Do not upload it or include its contents in reports."]
    else:
        result["steps"] = ["Select the actual editable PowerPoint or Keynote source; do not rename an unknown file to simulate conversion."]
    result["limitations"] = [
        "Container recognition is not full content, render, editability or application compatibility validation.",
        "The native Keynote adapter is implemented as an experimental macOS path; Mac application integration has not been tested in this repository's Windows validation environment.",
        "Explicit cross-format conversion can change fonts, charts, connectors and builds; compare the conversion before redesign.",
        "This router detects prerequisites without launching applications, requesting automation access or uploading files. It never marks a native application review as complete.",
    ]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Presentation file, .key bundle or explicitly selected text/paper material")
    parser.add_argument("--source-kind", choices=("slides", "text", "paper"), default="slides",
                        help="Use existing slides by default; explicitly select text or paper to create a new deck")
    parser.add_argument("--target", choices=("auto", "pptx", "keynote"), default="auto",
                        help="Preserve a slide source's application; text and paper need an explicit delivery target")
    args = parser.parse_args()
    result = route_presentation(args.source, args.target, args.source_kind)
    print(json.dumps(result, indent=2))
    return 2 if result["status"] == "unsupported" else 0


if __name__ == "__main__":
    sys.exit(main())
