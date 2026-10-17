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


def docx_parts():
    return {
        "[Content_Types].xml": f'<Types xmlns="{route.CT}"><Override PartName="/word/document.xml" ContentType="{route.DOCUMENT_TYPE}"/></Types>',
        "_rels/.rels": f'<Relationships xmlns="{route.REL}"><Relationship Id="r1" Type="{route.R}/officeDocument" Target="word/document.xml"/></Relationships>',
        "word/document.xml": f'<w:document xmlns:w="{route.W}"><w:body><w:p><w:r><w:t>Synthetic confidential finding</w:t></w:r></w:p></w:body></w:document>',
    }


def pdf_bytes():
    """A small standards-shaped PDF; the routing test does not render or read pages."""
    data = b"%PDF-1.4\n"
    offsets = [0]
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] >>",
    ]
    for index, content in enumerate(objects, 1):
        offsets.append(len(data))
        data += f"{index} 0 obj\n".encode("ascii") + content + b"\nendobj\n"
    startxref = len(data)
    data += b"xref\n0 4\n0000000000 65535 f \n"
    data += b"".join(f"{offset:010d} 00000 n \n".encode("ascii") for offset in offsets[1:])
    return data + f"trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n{startxref}\n%%EOF\n".encode("ascii")


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
        self.assertEqual(result["target"], "pptx")
        self.assertEqual(result["target_origin"], "source")
        self.assertFalse(result["conversion_requested"])
        self.assertEqual(result["validation"]["content"], "pending")
        self.assertEqual(result["source"]["source_sha256"], route.file_hash(source))
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(list(self.folder.iterdir()), [source])

    def test_pptx_for_keynote_is_explicit_conversion_before_native_work(self):
        result = route.route_presentation(self.archive("source.pptx", pptx_parts()), "keynote")
        self.assertEqual(result["status"], "requires-format-conversion")
        self.assertTrue(result["conversion_requested"])
        self.assertFalse(result["can_transform_now"])
        self.assertEqual(result["native_keynote_adapter"], "experimental-mac-unverified")
        self.assertEqual(result["validation"]["keynote_runtime"], "not-run")
        self.assertTrue(any("File > Open" in step for step in result["steps"]))

    def test_keynote_default_preserves_native_source_without_conversion(self):
        source = self.archive("source.KEY", self.modern_parts())
        original = source.read_bytes()
        for target in (None, "auto", "keynote"):
            result = route.route_presentation(source, target)
            self.assertEqual(result["source"]["kind"], "keynote-modern")
            self.assertEqual(result["adapter"], "native-keynote")
            self.assertEqual(result["target"], "keynote")
            self.assertFalse(result["conversion_requested"])
            self.assertFalse(result["can_transform_now"])
            self.assertFalse(result["can_deliver_target_now"])
            self.assertEqual(result["validation"]["keynote_runtime"], "not-run")
            self.assertEqual(result["native_keynote_adapter"], "experimental-mac-unverified")
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(list(self.folder.iterdir()), [source])

    def test_native_keynote_missing_runtime_does_not_fall_back_to_pptx(self):
        environment = {"platform": "win32", "prerequisites_detected": False,
                       "automation_access": "not-probed", "native_mac_validation": "not-run"}
        with patch.object(route, "keynote_environment", return_value=environment):
            result = route.route_presentation(self.archive("source.key", self.modern_parts()))
        self.assertEqual(result["status"], "requires-keynote-runtime")
        self.assertEqual(result["adapter"], "native-keynote")
        self.assertEqual(result["target"], "keynote")
        self.assertFalse(result["conversion_requested"])

    def test_detected_mac_prerequisites_still_require_actual_preflight(self):
        environment = {"platform": "darwin", "prerequisites_detected": True,
                       "automation_access": "not-probed", "native_mac_validation": "not-run"}
        with patch.object(route, "keynote_environment", return_value=environment):
            result = route.route_presentation(self.archive("source.key", self.modern_parts()))
        self.assertEqual(result["status"], "requires-keynote-preflight")
        self.assertFalse(result["can_transform_now"])
        self.assertFalse(result["can_deliver_target_now"])
        self.assertEqual(result["keynote_environment"]["automation_access"], "not-probed")
        self.assertEqual(result["keynote_environment"]["native_mac_validation"], "not-run")

    def test_only_explicit_pptx_target_converts_keynote(self):
        result = route.route_presentation(self.archive("source.key", self.modern_parts()), "pptx")
        self.assertEqual(result["target_origin"], "explicit")
        self.assertEqual(result["target"], "pptx")
        self.assertEqual(result["status"], "requires-format-conversion")
        self.assertEqual(result["adapter"], "explicit-application-conversion")
        self.assertTrue(result["conversion_requested"])
        self.assertFalse(result["can_transform_now"])

    def test_prerequisite_detection_never_claims_automation_or_mac_validation(self):
        with patch.object(route.sys, "platform", "win32"), patch.object(route.shutil, "which") as which:
            result = route.keynote_environment()
        which.assert_not_called()
        self.assertFalse(result["prerequisites_detected"])
        self.assertIsNone(result["keynote_app"])
        self.assertEqual(result["automation_access"], "not-probed")
        self.assertEqual(result["native_mac_validation"], "not-run")

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

    def test_legacy_marker_gets_native_preflight_without_native_validity_claim(self):
        source = self.archive("legacy.key", {"index.apxl": b"synthetic legacy marker"})
        result = route.route_presentation(source)
        self.assertEqual(result["source"]["kind"], "keynote-legacy")
        self.assertEqual(result["adapter"], "native-keynote")
        self.assertFalse(result["conversion_requested"])
        self.assertIn(result["status"], {"requires-keynote-runtime", "requires-keynote-preflight"})
        self.assertIn("modern .key baseline", result["steps"][0])
        self.assertIn("does not accept legacy", result["steps"][0])

    def test_legacy_directory_native_source_has_content_bound_hash(self):
        source = self.folder / "legacy.key"
        source.mkdir()
        (source / "index.apxl").write_bytes(b"synthetic legacy document")
        result = route.route_presentation(source)
        self.assertEqual(result["source"]["kind"], "keynote-legacy")
        self.assertEqual(result["source"]["hash_kind"], "bundle-manifest-sha256")
        first_hash = result["source"]["source_sha256"]
        (source / "index.apxl").write_bytes(b"another synthetic revision")
        self.assertNotEqual(first_hash, route.inspect_presentation(source)["source_sha256"])

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

    def test_paper_pdf_requires_a_delivery_choice_without_conversion_or_source_changes(self):
        source = self.folder / "paper.pdf"
        original = pdf_bytes()
        source.write_bytes(original)
        for target in (None, "auto"):
            result = route.route_presentation(source, target, source_kind="paper")
            self.assertEqual(result["source_kind"], "paper")
            self.assertEqual(result["source"]["kind"], "pdf")
            self.assertEqual(result["status"], "requires-delivery-target")
            self.assertIsNone(result["target"])
            self.assertEqual(result["target_origin"], "pending")
            self.assertFalse(result["conversion_requested"])
            self.assertFalse(result["can_transform_now"])
            self.assertFalse(result["can_deliver_target_now"])
            self.assertEqual(result["source"]["source_sha256"], route.file_hash(source))
            self.assertEqual(set(result["validation"].values()), {"pending", "not-run"})
            self.assertIn("Source inspection may proceed", result["steps"][0])
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(list(self.folder.iterdir()), [source])
        self.assertEqual(route.route_presentation(source)["status"], "reference-only")

    def test_paper_has_no_source_application_when_target_is_selected(self):
        source = self.folder / "paper.pdf"
        source.write_bytes(pdf_bytes())
        for target in ("pptx", "keynote"):
            with self.subTest(target=target):
                result = route.route_presentation(source, target, "paper")
                self.assertEqual(result["status"], "requires-native-authoring")
                self.assertEqual(result["adapter"], "new-" + target + "-authoring")
                self.assertEqual(result["target"], target)
                self.assertEqual(result["target_origin"], "explicit")
                self.assertFalse(result["conversion_requested"])
                self.assertFalse(result["can_transform_now"])
                self.assertFalse(result["can_deliver_target_now"])
                self.assertNotIn("palate_pptx.py inspect", " ".join(result["steps"]))
                if target == "keynote":
                    self.assertEqual(result["keynote_environment"]["automation_access"], "not-probed")

    def test_explicit_text_and_paper_accept_unicode_material_without_returning_it(self):
        content = "Private draft: \u6c34\u5e93\u673a\u5236\u3002\nUncertain estimates must remain qualified."
        for index, (extension, encoding) in enumerate(((".txt", "utf-8"), (".md", "utf-8-sig"), (".markdown", "utf-16"))):
            source = self.folder / (str(index) + extension)
            source.write_text(content, encoding=encoding)
            original = source.read_bytes()
            for source_kind in ("text", "paper"):
                result = route.route_presentation(source, "pptx", source_kind)
                self.assertEqual(result["source"]["kind"], "text")
                self.assertEqual(result["status"], "requires-native-authoring")
                self.assertFalse(result["can_transform_now"])
                self.assertEqual(result["source"]["source_sha256"], route.file_hash(source))
                self.assertNotIn("Private draft", json.dumps(result))
            self.assertEqual(route.route_presentation(source)["status"], "unsupported")
            self.assertEqual(source.read_bytes(), original)

    def test_word_sources_are_inspected_as_material_and_not_as_slide_packages(self):
        source = self.archive("manuscript.docx", docx_parts())
        original = source.read_bytes()
        for source_kind in ("text", "paper"):
            result = route.route_presentation(source, "keynote", source_kind)
            self.assertEqual(result["source"]["kind"], "docx")
            self.assertEqual(result["source"]["container"], "zip")
            self.assertEqual(result["status"], "requires-native-authoring")
            self.assertFalse(result["conversion_requested"])
            self.assertFalse(result["can_transform_now"])
            self.assertNotIn("Synthetic confidential finding", json.dumps(result))
        self.assertEqual(route.route_presentation(source)["status"], "unsupported")
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(list(self.folder.iterdir()), [source])

    def test_missing_empty_binary_mislabelled_and_slide_materials_fail_closed(self):
        sources = [self.folder / "missing.txt"]
        for name, data in (("empty.md", b""), ("blank.txt", b" \n\t"), ("binary.txt", b"\x00\x01binary"),
                           ("not-pdf.pdf", b"Just a brief"), ("renamed.txt", pdf_bytes()),
                           ("fake.docx", b"Plain text is not a Word container"), ("legacy.doc", b"legacy")):
            source = self.folder / name
            source.write_bytes(data)
            sources.append(source)
        sources += [self.archive("slides.pptx", pptx_parts()), self.archive("slides.docx", pptx_parts()),
                    self.archive("slides.key", self.modern_parts())]
        directory = self.folder / "source.txt"
        directory.mkdir()
        sources.append(directory)
        for source_kind in ("paper", "text"):
            for source in sources:
                with self.subTest(source_kind=source_kind, name=source.name):
                    result = route.route_presentation(source, "pptx", source_kind)
                    self.assertEqual(result["status"], "unsupported")
                    self.assertFalse(result["can_transform_now"])
                    self.assertNotIn("source_sha256", result["source"])

    def test_paper_pdf_boundary_failures_are_not_treated_as_readable_papers(self):
        original = pdf_bytes()
        cases = [b"%PDF-1.7\nsynthetic reference", original.replace(b"%%EOF", b"missing"),
                 original.replace(b"startxref", b"notxref"), original.replace(b"xref\n0 4", b"nope\n0 4")]
        for index, data in enumerate(cases):
            source = self.folder / f"invalid-{index}.pdf"
            source.write_bytes(data)
            self.assertEqual(route.route_presentation(source, source_kind="paper")["status"], "unsupported")

    def test_word_malformed_macro_external_and_unsafe_containers_are_rejected(self):
        cases = []
        parts = docx_parts()
        del parts["word/document.xml"]
        cases.append(parts)
        parts = docx_parts()
        parts["word/document.xml"] = "<not-closed"
        cases.append(parts)
        parts = docx_parts()
        parts["word/document.xml"] = '<!DOCTYPE foo [<!ENTITY bar "Private source text">]><foo/>'
        cases.append(parts)
        parts = docx_parts()
        parts["[Content_Types].xml"] = parts["[Content_Types].xml"].replace(route.DOCUMENT_TYPE, "application/vnd.ms-word.document.macroEnabled.main+xml")
        cases.append(parts)
        parts = docx_parts()
        parts["_rels/.rels"] = parts["_rels/.rels"].replace('Target="word/document.xml"', 'Target="https://example.invalid/word.xml" TargetMode="External"')
        cases.append(parts)
        cases.append({**docx_parts(), "../outside": b"synthetic"})
        for index, parts in enumerate(cases):
            result = route.route_presentation(self.archive(f"invalid-{index}.docx", parts), source_kind="paper")
            self.assertEqual(result["status"], "unsupported")
            self.assertNotIn("Private source text", json.dumps(result))

    def test_material_credentials_are_rejected_in_head_or_later_text_without_hash_or_content(self):
        marker = "-----BEGIN " + "PRIVATE KEY" + "-----\nsynthetic-private-payload"
        for index, (prefix, encoding) in enumerate((("", "utf-8"), ("", "utf-16"), ("notes\n" * 1000, "utf-8"))):
            source = self.folder / f"credential-{index}.txt"
            source.write_text(prefix + marker, encoding=encoding)
            for source_kind in ("text", "paper"):
                result = route.route_presentation(source, "pptx", source_kind)
                self.assertEqual(result["status"], "unsupported")
                self.assertEqual(result["source"]["kind"], "credential-key")
                self.assertNotIn("source_sha256", result["source"])
                self.assertNotIn("synthetic-private-payload", json.dumps(result))
        parts = docx_parts()
        parts["word/document.xml"] = parts["word/document.xml"].replace("Synthetic confidential finding", marker)
        result = route.route_presentation(self.archive("credential.docx", parts), source_kind="paper")
        self.assertEqual(result["status"], "unsupported")
        self.assertNotIn("source_sha256", result["source"])
        self.assertNotIn("synthetic-private-payload", json.dumps(result))

    def test_material_size_limits_fail_closed(self):
        source = self.folder / "notes.txt"
        source.write_text("Synthetic research notes", encoding="utf-8")
        with patch.object(route, "MAX_TEXT_BYTES", 10):
            self.assertEqual(route.route_presentation(source, source_kind="text")["status"], "unsupported")
        with patch.object(route, "MAX_PACKAGE_BYTES", 10):
            self.assertEqual(route.route_presentation(source, source_kind="paper")["status"], "unsupported")
        source = self.archive("notes.docx", docx_parts())
        with patch.object(route, "MAX_XML_BYTES", 10):
            self.assertEqual(route.route_presentation(source, source_kind="paper")["status"], "unsupported")

    def test_invalid_source_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            route.route_presentation(self.folder / "source.md", source_kind="auto")

    def test_cli_explicit_paper_and_text_routes_do_not_create_outputs(self):
        source = self.folder / "notes.md"
        source.write_text("Private proposed research explanation", encoding="utf-8")
        for source_kind in ("paper", "text"):
            completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(source),
                                        "--source-kind", source_kind, "--target", "keynote"], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["status"], "requires-native-authoring")
            self.assertFalse(result["conversion_requested"])
            self.assertFalse(result["can_transform_now"])
            self.assertNotIn("Private proposed", completed.stdout)
        missing = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(self.folder / "missing.pdf"),
                                  "--source-kind", "paper"], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertEqual(json.loads(missing.stdout)["status"], "unsupported")
        self.assertEqual(list(self.folder.iterdir()), [source])

    def test_cli_emits_actionable_json_and_unsupported_exit_code(self):
        source = self.archive("source.key", self.modern_parts())
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(source), "--target", "keynote"], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["adapter"], "native-keynote")
        self.assertFalse(json.loads(completed.stdout)["conversion_requested"])
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(source)], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["target"], "keynote")
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/presentation_route.py"), str(self.folder / "missing.key")], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "unsupported")


if __name__ == "__main__":
    unittest.main()
