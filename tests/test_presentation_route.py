"""Container and state tests; synthetic Keynote fixtures do not prove Mac compatibility."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("presentation_route", ROOT / "scripts/presentation_route.py")
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)


def pptx_parts():
    return {
        "[Content_Types].xml": f'<Types xmlns="{route.CT}"><Override PartName="/ppt/presentation.xml" ContentType="{route.PRESENTATION_TYPE}"/></Types>',
        "_rels/.rels": f'<Relationships xmlns="{route.REL}"><Relationship Id="r1" Type="{route.R}/officeDocument" Target="ppt/presentation.xml"/></Relationships>',
        "ppt/presentation.xml": f'<p:presentation xmlns:p="{route.P}" xmlns:r="{route.R}"><p:sldIdLst><p:sldId id="256" r:id="r1"/></p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/></p:presentation>',
        "ppt/_rels/presentation.xml.rels": f'<Relationships xmlns="{route.REL}"><Relationship Id="r1" Type="{route.R}/slide" Target="slides/slide1.xml"/></Relationships>',
        "ppt/slides/slide1.xml": f'<p:sld xmlns:p="{route.P}"><p:cSld><p:spTree/></p:cSld></p:sld>',
    }


class PresentationRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def archive(self, name, parts):
        path = self.folder / name
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for member, data in parts.items():
                archive.writestr(member, data)
        return path

    def modern_parts(self):
        return {"Index/Document.iwa": b"synthetic document", "Index/Slide-1.iwa": b"synthetic slide"}

    def test_compatible_pptx_uses_existing_workflow_without_marking_reviews_passed(self):
        source = self.archive("source.pptx", pptx_parts())
        original = source.read_bytes()
        result = route.route_presentation(source)
        self.assertEqual(result["status"], "ready-pptx")
        self.assertTrue(result["can_transform_now"])
        self.assertFalse(result["can_deliver_target_now"])
        self.assertEqual(result["adapter"], "shared-pptx-workflow")
        self.assertEqual(result["validation"]["content"], "pending")
        self.assertEqual(result["source"]["source_sha256"], route.file_hash(source))
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(list(self.folder.iterdir()), [source])

    def test_pptx_for_keynote_keeps_transform_available_but_requires_native_review(self):
        result = route.route_presentation(self.archive("source.pptx", pptx_parts()), "keynote")
        self.assertEqual(result["status"], "requires-keynote-runtime")
        self.assertTrue(result["can_transform_now"])
        self.assertEqual(result["native_keynote_adapter"], "not-implemented")
        self.assertEqual(result["validation"]["keynote_runtime"], "not-run")
        self.assertTrue(any("File > Open" in step for step in result["steps"]))

    def test_modern_keynote_zip_requires_export_for_both_targets(self):
        source = self.archive("source.KEY", self.modern_parts())
        for target in ("pptx", "keynote"):
            result = route.route_presentation(source, target)
            self.assertEqual(result["source"]["kind"], "keynote-modern")
            self.assertEqual(result["status"], "requires-export")
            self.assertFalse(result["can_transform_now"])
            self.assertTrue(any("PowerPoint" in step and "PDF" in step for step in result["steps"]))

    def test_directory_bundle_is_read_only_and_hash_changes_when_content_changes(self):
        source = self.folder / "source.key"
        for name, data in self.modern_parts().items():
            member = source / name
            member.parent.mkdir(parents=True, exist_ok=True)
            member.write_bytes(data)
        before = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
        result = route.inspect_presentation(source)
        self.assertEqual(result["kind"], "keynote-modern")
        self.assertEqual(result["container"], "directory")
        self.assertEqual(result["hash_kind"], "bundle-manifest-sha256")
        self.assertEqual(before, {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()})
        (source / "Index/Slide-1.iwa").write_bytes(b"changed synthetic slide")
        self.assertNotEqual(result["source_sha256"], route.inspect_presentation(source)["source_sha256"])

    def test_nested_index_zip_is_recognized_for_file_and_bundle(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("Document.iwa", b"synthetic")
            archive.writestr("Slide-1.iwa", b"synthetic")
        zipped = self.archive("source.key", {"Index.zip": buffer.getvalue()})
        bundle = self.folder / "bundle.key"
        bundle.mkdir()
        (bundle / "Index.zip").write_bytes(buffer.getvalue())
        for source in (zipped, bundle):
            self.assertEqual(route.inspect_presentation(source)["kind"], "keynote-modern")

    def test_iwork_document_without_slide_signature_is_not_assumed_keynote(self):
        source = self.archive("source.key", {"Index/Document.iwa": b"synthetic Pages or Numbers document"})
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_legacy_marker_gets_export_route_without_native_validity_claim(self):
        source = self.archive("legacy.key", {"index.apxl": b"synthetic legacy marker"})
        result = route.route_presentation(source)
        self.assertEqual(result["source"]["kind"], "keynote-legacy")
        self.assertEqual(result["status"], "requires-export")

    def test_private_public_and_putty_keys_are_excluded_without_returning_text(self):
        headers = [b"-----BEGIN " + kind + b"-----" for kind in (b"PRIVATE KEY", b"RSA PRIVATE KEY", b"OPENSSH PRIVATE KEY", b"PUBLIC KEY")]
        headers += [b"PuTTY-User-Key-File-3: synthetic"]
        for index, header in enumerate(headers):
            source = self.folder / f"credential-{index}.key"
            source.write_bytes(header + b"\nsynthetic-private-payload")
            result = route.route_presentation(source)
            self.assertEqual(result["source"]["kind"], "credential-key")
            self.assertEqual(result["status"], "unsupported")
            self.assertNotIn("synthetic-private-payload", json.dumps(result))
            self.assertNotIn("source_sha256", result["source"])

    def test_plain_key_text_is_not_a_presentation(self):
        source = self.folder / "unknown.key"
        source.write_text("synthetic non-presentation text", encoding="utf-8")
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_pdf_is_reference_only_even_with_misleading_extension(self):
        source = self.folder / "reference.key"
        source.write_bytes(b"%PDF-1.7\nsynthetic reference")
        result = route.route_presentation(source, "keynote")
        self.assertEqual(result["status"], "reference-only")
        self.assertFalse(result["can_transform_now"])

    def test_missing_and_empty_sources_are_unsupported(self):
        missing = self.folder / "missing.pptx"
        empty = self.folder / "empty.pptx"
        empty.touch()
        for source in (missing, empty):
            self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_random_zip_named_pptx_is_unsupported(self):
        source = self.archive("source.pptx", {"hello.txt": "synthetic"})
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_incomplete_pptx_missing_slide_is_unsupported(self):
        parts = pptx_parts()
        del parts["ppt/slides/slide1.xml"]
        self.assertEqual(route.route_presentation(self.archive("source.pptx", parts))["status"], "unsupported")

    def test_macro_enabled_package_is_not_dispatched_to_pptx_patcher(self):
        parts = pptx_parts()
        parts["[Content_Types].xml"] = parts["[Content_Types].xml"].replace(route.PRESENTATION_TYPE, "application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml")
        self.assertEqual(route.route_presentation(self.archive("source.pptx", parts))["status"], "unsupported")

    def test_external_and_traversing_slide_targets_are_unsupported(self):
        for replacement in ('Target="https://example.invalid/slide.xml" TargetMode="External"', 'Target="../outside.xml"'):
            parts = pptx_parts()
            parts["ppt/_rels/presentation.xml.rels"] = parts["ppt/_rels/presentation.xml.rels"].replace('Target="slides/slide1.xml"', replacement)
            self.assertEqual(route.route_presentation(self.archive("source.pptx", parts))["status"], "unsupported")

    def test_malformed_or_dtd_bearing_metadata_is_unsupported(self):
        declaration = '<!DOCTYPE foo [<!ENTITY bar "synthetic">]><foo/>'
        for metadata in ("<not-closed", declaration, declaration.encode("utf-16")):
            parts = pptx_parts()
            parts["[Content_Types].xml"] = metadata
            self.assertEqual(route.route_presentation(self.archive("source.pptx", parts))["status"], "unsupported")

    def test_duplicate_members_are_rejected(self):
        source = self.archive("source.key", self.modern_parts())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(source, "a") as archive:
                archive.writestr("Index/Document.iwa", b"duplicate synthetic")
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_unsafe_member_and_linked_members_are_rejected(self):
        source = self.archive("source.key", {**self.modern_parts(), "../outside": b"synthetic"})
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")
        source = self.archive("linked.key", self.modern_parts())
        with zipfile.ZipFile(source, "a") as archive:
            linked = zipfile.ZipInfo("Data/link")
            linked.create_system = 3
            linked.external_attr = (0o120777 << 16)
            archive.writestr(linked, "target")
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_package_and_metadata_limits_fail_closed(self):
        source = self.archive("source.pptx", pptx_parts())
        with patch.object(route, "MAX_PACKAGE_BYTES", 10):
            self.assertEqual(route.route_presentation(source)["status"], "unsupported")
        with patch.object(route, "MAX_XML_BYTES", 10):
            self.assertEqual(route.route_presentation(source)["status"], "unsupported")

    def test_invalid_target_is_rejected(self):
        with self.assertRaises(ValueError):
            route.route_presentation(self.folder / "source.key", "pdf")

    def test_cli_emits_actionable_json_and_unsupported_exit_code(self):
        source = self.archive("source.key", self.modern_parts())
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(source), "--target", "keynote"], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "requires-export")
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(self.folder / "missing.key")], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "unsupported")


if __name__ == "__main__":
    unittest.main()
