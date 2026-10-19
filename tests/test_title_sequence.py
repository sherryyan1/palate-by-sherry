"""Title inventory boundaries and source preservation using synthetic OOXML only."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
from xml.sax.saxutils import escape
import zipfile

from scripts import review_title_sequence as helper


ROOT = Path(__file__).resolve().parents[1]
P, A, R, REL = (helper.NS[key] for key in ("p", "a", "r", "rel"))


def shape(identity, text, placeholder="title", idx=None):
    ph = "" if placeholder is None else '<p:nvPr><p:ph' + (
        f' type="{placeholder}"' if placeholder else "") + (f' idx="{idx}"' if idx is not None else "") + '/></p:nvPr>'
    paragraphs = ''.join(f'<a:p><a:r><a:t>{escape(line)}</a:t></a:r></a:p>' for line in text.split("\n"))
    return f'<p:sp><p:nvSpPr><p:cNvPr id="{identity}" name="Synthetic shape"/>{ph}</p:nvSpPr><p:txBody>{paragraphs}</p:txBody></p:sp>'


def slide(content, show="1"):
    return f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" show="{show}"><p:cSld><p:spTree>{content}</p:spTree></p:cSld></p:sld>'.encode()


def fixture():
    return {
        "ppt/presentation.xml": f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst><p:sldId id="300" r:id="s2"/><p:sldId id="256" r:id="s1"/><p:sldId id="400" r:id="s3"/></p:sldIdLst></p:presentation>'.encode(),
        "ppt/_rels/presentation.xml.rels": f'<Relationships xmlns="{REL}"><Relationship Id="s1" Type="x/slide" Target="slides/slide1.xml"/><Relationship Id="s2" Type="x/slide" Target="slides/slide2.xml"/><Relationship Id="s3" Type="x/slide" Target="slides/slide3.xml"/></Relationships>'.encode(),
        "ppt/slides/slide1.xml": slide(shape(2, "Hidden explanation"), "false"),
        "ppt/slides/slide2.xml": slide(shape(2, "Opening question\nA second line")),
        "ppt/slides/slide3.xml": slide(shape(2, "Closing implication")),
    }


class TitleSequenceTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / "analysis/local-only/test-temp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="title-sequence-", dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.source = self.folder / "synthetic.pptx"
        self.output = self.folder / "review.json"
        self.parts = fixture()

    def write_package(self):
        with zipfile.ZipFile(self.source, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in self.parts.items():
                archive.writestr(name, content)
        return self.source.read_bytes()

    def review(self):
        self.write_package()
        return helper.export_review(self.source, self.output)

    def assert_rejected(self):
        original = self.write_package()
        with self.assertRaises((ValueError, OSError)):
            helper.export_review(self.source, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(self.source.read_bytes(), original)

    def test_presentation_order_identity_visibility_and_multiline_titles(self):
        original = self.write_package()
        report = helper.export_review(self.source, self.output)
        slides = report["slides"]
        self.assertEqual([item["slide_id"] for item in slides], ["300", "256", "400"])
        self.assertEqual([item["original_position"] for item in slides], [1, 2, 3])
        self.assertEqual([item["hidden"] for item in slides], [False, True, False])
        self.assertEqual(slides[0]["part"], "ppt/slides/slide2.xml")
        self.assertEqual(slides[0]["relationship_id"], "s2")
        self.assertEqual(slides[0]["original_title"], "Opening question\nA second line")
        self.assertEqual(slides[0]["next_visible_slide_id"], "400")
        self.assertEqual(slides[2]["previous_visible_slide_id"], "300")
        self.assertEqual((slides[1]["previous_visible_slide_id"], slides[1]["next_visible_slide_id"]), ("300", "400"))
        self.assertIsNone(slides[0]["previous_visible_slide_id"])
        self.assertIsNone(slides[2]["next_visible_slide_id"])
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(self.source.read_bytes(), original)
        self.assertEqual(json.loads(self.output.read_text(encoding="utf-8")), report)

    def test_review_fields_never_infer_narrative_or_science(self):
        report = self.review()
        self.assertEqual(report["status"], "unreviewed")
        self.assertIs(report["narrative_validated"], False)
        self.assertEqual(report["decision_options"], ["retain", "revise"])
        review = report["slides"][0]["review"]
        self.assertEqual(review["source_evidence"], [])
        self.assertTrue(all(value is None for key, value in review.items() if key != "source_evidence"))

    def test_ending_review_does_not_infer_scope_or_final_main_slide(self):
        # A last title reading "Closing implication" is insufficient evidence.
        report = self.review()
        ending = report["ending_review"]
        self.assertEqual(ending["status"], "unreviewed")
        self.assertTrue(all(value is None for key, value in ending.items() if key != "status"))
        self.assertIs(report["narrative_validated"], False)

    def test_custom_text_is_candidate_not_an_asserted_title(self):
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "Large heading", None) + shape(3, "Body detail", None))
        item = self.review()["slides"][0]
        self.assertIsNone(item["original_title"])
        self.assertEqual(item["title_status"], "needs_confirmation")
        self.assertEqual([c["text"] for c in item["title_candidates"]], ["Large heading", "Body detail"])

    def test_ambiguous_title_placeholders_are_all_preserved(self):
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "Candidate one") + shape(3, "Candidate two", "ctrTitle"))
        item = self.review()["slides"][0]
        self.assertIsNone(item["original_title"])
        self.assertEqual(item["title_status"], "ambiguous")
        self.assertEqual([c["shape_id"] for c in item["title_candidates"]], ["2", "3"])

    def test_empty_missing_and_footer_only_titles_remain_missing(self):
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "") + shape(3, "12", "sldNum") + shape(4, "Footer", "ftr"))
        item = self.review()["slides"][0]
        self.assertEqual(item["title_status"], "missing")
        self.assertEqual(item["title_candidates"], [])
        self.assertTrue(item["extraction_notes"])

    def test_hidden_title_placeholders_do_not_confirm_visible_custom_heading(self):
        for value in ("1", "true"):
            with self.subTest(hidden=value):
                hidden = shape(2, "Hidden old title").replace('id="2"', f'id="2" hidden="{value}"')
                self.parts["ppt/slides/slide2.xml"] = slide(hidden + shape(3, "Visible custom heading", None))
                self.write_package()
                item = helper.build_review(self.source)["slides"][0]
                self.assertIsNone(item["original_title"])
                self.assertEqual(item["title_status"], "needs_confirmation")
                self.assertEqual([candidate["text"] for candidate in item["title_candidates"]], ["Visible custom heading"])
                self.assertTrue(any("hidden" in note for note in item["extraction_notes"]))

    def test_hidden_duplicate_does_not_make_visible_title_ambiguous(self):
        hidden = shape(2, "Old hidden title").replace('id="2"', 'id="2" hidden="1"')
        self.parts["ppt/slides/slide2.xml"] = slide(hidden + shape(3, "Visible title"))
        item = self.review()["slides"][0]
        self.assertEqual(item["title_status"], "identified")
        self.assertEqual(item["original_title"], "Visible title")

    def test_hidden_group_ancestor_excludes_nested_title(self):
        for value in ("1", "true"):
            with self.subTest(hidden=value):
                nested = '<p:grpSp><p:nvGrpSpPr><p:cNvPr id="8" name="Inner" hidden="false"/></p:nvGrpSpPr>' + shape(2, "Nested hidden title") + '</p:grpSp>'
                outer = f'<p:grpSp><p:nvGrpSpPr><p:cNvPr id="9" name="Outer" hidden="{value}"/></p:nvGrpSpPr>{nested}</p:grpSp>'
                self.parts["ppt/slides/slide2.xml"] = slide(outer + shape(3, "Actual title"))
                self.write_package()
                item = helper.build_review(self.source)["slides"][0]
                self.assertEqual(item["original_title"], "Actual title")
                self.assertEqual(len(item["title_candidates"]), 1)
                self.assertTrue(any("containing group" in note for note in item["extraction_notes"]))

    def test_duplicate_titles_are_disclosed_without_rejection(self):
        self.parts["ppt/slides/slide3.xml"] = slide(shape(2, "  opening question  A second line "))
        report = self.review()
        self.assertEqual(report["slides"][0]["same_title_slide_ids"], ["400"])
        self.assertEqual(report["slides"][2]["same_title_slide_ids"], ["300"])
        self.assertIsNone(report["slides"][0]["review"]["decision"])

    def test_line_breaks_and_fields_preserve_visible_text(self):
        content = shape(2, "first").replace('<a:t>first</a:t>', '<a:t>first</a:t>').replace('</a:r></a:p>', '</a:r><a:br/><a:fld id="x"><a:t>field</a:t></a:fld><a:r><a:t> last</a:t></a:r></a:p>')
        self.parts["ppt/slides/slide2.xml"] = slide(content)
        self.assertEqual(self.review()["slides"][0]["original_title"], "first\nfield last")

    def test_layout_inherited_title_is_supported(self):
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "Inherited title", "", 9))
        self.parts["ppt/slides/_rels/slide2.xml.rels"] = f'<Relationships xmlns="{REL}"><Relationship Id="layout" Type="x/slideLayout" Target="../slideLayouts/layout1.xml"/></Relationships>'.encode()
        self.parts["ppt/slideLayouts/layout1.xml"] = slide(shape(6, "", "title", 9)).replace(b'p:sld', b'p:sldLayout')
        item = self.review()["slides"][0]
        self.assertEqual(item["original_title"], "Inherited title")
        self.assertEqual(item["title_candidates"][0]["basis"], "layout_title_placeholder")

    def test_malformed_layout_root_cannot_confirm_inherited_title(self):
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "Unverified inherited title", "", 9))
        self.parts["ppt/slides/_rels/slide2.xml.rels"] = f'<Relationships xmlns="{REL}"><Relationship Id="layout" Type="x/slideLayout" Target="../slideLayouts/layout1.xml"/></Relationships>'.encode()
        self.parts["ppt/slideLayouts/layout1.xml"] = f'<not-a-layout xmlns:p="{P}" xmlns:a="{A}">{shape(6, "", "title", 9)}</not-a-layout>'.encode()
        self.assert_rejected()

    def test_nonrendered_extension_shape_is_not_a_title_candidate(self):
        source = slide(shape(2, "Actual title"))
        extra = '<p:extLst><p:ext>' + shape(3, "Not a displayed title") + '</p:ext></p:extLst>'
        self.parts["ppt/slides/slide2.xml"] = source.replace(b'</p:sld>', extra.encode() + b'</p:sld>')
        item = self.review()["slides"][0]
        self.assertEqual(item["title_status"], "identified")
        self.assertEqual(item["original_title"], "Actual title")

    def test_invalid_presentation_root_is_rejected(self):
        self.parts["ppt/presentation.xml"] = self.parts["ppt/presentation.xml"].replace(b'p:presentation', b'p:notPresentation')
        self.assert_rejected()

    def test_package_absolute_slide_targets_are_resolved_inside_zip(self):
        self.parts["ppt/_rels/presentation.xml.rels"] = self.parts["ppt/_rels/presentation.xml.rels"].replace(b'Target="slides/', b'Target="/ppt/slides/')
        self.assertEqual(self.review()["slides"][0]["slide_id"], "300")

    def test_inventory_supports_keynote_and_outline_without_conversion(self):
        for kind in ("keynote", "outline", "manual"):
            with self.subTest(kind=kind):
                source = self.folder / f"{kind}.json"
                data = {"schema_version": 1, "source_kind": kind, "slides": [
                    {"slide_id": "native-stable-id", "title": "\u7814\u7a76\u95ee\u9898\nA question", "hidden": False},
                    {"slide_id": "another-id", "title": None, "hidden": True}]}
                original = json.dumps(data, ensure_ascii=False).encode("utf-8")
                source.write_bytes(original)
                result = helper.export_review(source, self.folder / f"{kind}-review.json")
                self.assertEqual(result["source"]["kind"], kind)
                self.assertEqual(result["slides"][0]["title_status"], "provided")
                self.assertEqual(result["slides"][1]["title_status"], "missing")
                self.assertIsNone(result["slides"][0]["part"])
                self.assertEqual(source.read_bytes(), original)

    def test_inventory_rejects_duplicate_keys_ids_and_invalid_types(self):
        source = self.folder / "inventory.json"
        valid = {"schema_version": 1, "source_kind": "keynote", "slides": [{"slide_id": "one", "title": "A", "hidden": False}]}
        cases = [dict(valid, schema_version=True), dict(valid, source_kind="pptx"),
                 dict(valid, slides=valid["slides"] * 2), dict(valid, slides=[]),
                 dict(valid, slides=[{"slide_id": "one", "title": ["A"], "hidden": False}]),
                 dict(valid, slides=[{"slide_id": "one", "title": "A", "hidden": "false"}])]
        for data in cases:
            with self.subTest(data=data):
                source.write_text(json.dumps(data), encoding="utf-8")
                with self.assertRaises(ValueError):
                    helper.export_review(source, self.output)
                self.assertFalse(self.output.exists())
        source.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            helper.build_review(source)

    def test_existing_output_and_source_cannot_be_overwritten(self):
        original = self.write_package()
        self.output.write_text("retain local work", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            helper.export_review(self.source, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "retain local work")
        with self.assertRaises(ValueError):
            helper.export_review(self.source, self.source)
        self.assertEqual(self.source.read_bytes(), original)

    def test_colon_paths_cannot_write_or_read_windows_alternate_data_streams(self):
        original = self.write_package()
        existing = self.folder / "existing.txt"
        existing.write_bytes(b"retain this file")
        stream = self.folder / "existing.txt:review.json"
        with self.assertRaisesRegex(ValueError, "Alternate data streams"):
            helper.export_review(self.source, stream)
        self.assertEqual(existing.read_bytes(), b"retain this file")
        self.assertFalse(stream.exists())
        with self.assertRaisesRegex(ValueError, "Alternate data streams"):
            helper.build_review(self.folder / "existing.txt:inventory.json")
        self.assertEqual(self.source.read_bytes(), original)

    def test_duplicate_or_external_slide_relationships_are_rejected(self):
        base = fixture()
        name = "ppt/_rels/presentation.xml.rels"
        for raw in (base[name].replace(b'Id="s1"', b'Id="s2"'),
                    base[name].replace(b'Id="s2"', b'Id="s2" TargetMode="External"'),
                    base[name].replace(b'Target="slides/slide2.xml"', b'Target="../../escape.xml"'),
                    base[name].replace(b'Target="slides/slide2.xml"', b'Target="slides/missing.xml"')):
            with self.subTest(raw=raw):
                self.parts = dict(base, **{name: raw})
                self.assert_rejected()

    def test_duplicate_slide_and_shape_identities_are_rejected(self):
        self.parts["ppt/presentation.xml"] = self.parts["ppt/presentation.xml"].replace(b'id="300"', b'id="256"')
        self.assert_rejected()
        self.parts = fixture()
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "One") + shape(2, "Two"))
        self.assert_rejected()

    def test_unsafe_archive_paths_and_dtd_are_rejected(self):
        self.parts["../not-allowed"] = b"no extraction"
        self.assert_rejected()
        self.parts = fixture()
        self.parts["ppt/slides/slide2.xml"] = b'<!DOCTYPE p:sld [<!ENTITY injected "synthetic">]>' + self.parts["ppt/slides/slide2.xml"]
        self.assert_rejected()

    def test_malformed_xml_duplicate_members_and_nonzip_input_create_no_output(self):
        self.parts["ppt/slides/slide2.xml"] = b"<broken>"
        self.assert_rejected()
        self.parts = fixture()
        original = self.write_package()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.source, "a") as archive:
                archive.writestr("ppt/presentation.xml", self.parts["ppt/presentation.xml"])
        with self.assertRaisesRegex(ValueError, "duplicate package"):
            helper.export_review(self.source, self.output)
        self.assertFalse(self.output.exists())
        self.source.write_bytes(b"not a zip archive")
        with self.assertRaises(zipfile.BadZipFile):
            helper.export_review(self.source, self.output)
        self.assertFalse(self.output.exists())
        self.assertNotEqual(self.source.read_bytes(), original)

    def test_size_slide_count_and_candidate_budgets(self):
        self.write_package()
        for name, limit in (("MAX_SOURCE_BYTES", 10), ("MAX_XML_BYTES", 10),
                            ("MAX_READ_XML_BYTES", 10), ("MAX_MEMBERS", 2), ("MAX_SLIDES", 2)):
            with self.subTest(limit=name), patch.object(helper, name, limit):
                with self.assertRaises(ValueError):
                    helper.export_review(self.source, self.output)
                self.assertFalse(self.output.exists())
        self.parts["ppt/slides/slide2.xml"] = slide(shape(2, "One") + shape(3, "Two"))
        with patch.object(helper, "MAX_CANDIDATES", 1):
            self.assert_rejected()

    def test_cli_requires_explicit_output_and_reports_unreviewed_state(self):
        self.write_package()
        command = [sys.executable, str(ROOT / "scripts/review_title_sequence.py"), "--source", str(self.source)]
        missing = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertFalse(self.output.exists())
        result = subprocess.run(command + ["--output", str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unreviewed", result.stdout)
        self.assertIn("still required", result.stdout)
        self.assertNotIn("Opening question", result.stdout)


if __name__ == "__main__":
    unittest.main()
