"""Scientific content preservation and rejection tests using synthetic OOXML only."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / "analysis/local-only/test-temp"
TEST_TEMP.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("palate", ROOT / "scripts/palate_pptx.py")
palate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(palate)
spec2 = importlib.util.spec_from_file_location("packager", ROOT / "scripts/package_skill.py")
packager = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(packager)


def fixture():
    # Deliberately synthetic values, native text/math/table/chart references, no research.
    a, p, r = palate.NS["a"], palate.NS["p"], palate.NS["r"]
    slide = f'''<p:sld xmlns:p="{p}" xmlns:a="{a}" xmlns:r="{r}" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><p:cSld><p:spTree>
    <p:sp><p:nvSpPr><p:cNvPr id="2" name="title"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="457200"/><a:ext cx="7315200" cy="685800"/></a:xfrm><a:prstGeom prst="rect"/><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:spPr><p:txBody><a:p><a:r><a:rPr sz="1200"><a:latin typeface="Arial"/><a:ea typeface="Arial"/></a:rPr><a:t>Synthetic result: 12 ± 2 mg/L (1/3)</a:t></a:r></a:p></p:txBody></p:sp>
    <p:pic><p:nvPicPr><p:cNvPr id="3" name="figure"/></p:nvPicPr><p:blipFill><a:blip r:embed="img"/><a:srcRect l="0" t="0" r="0" b="0"/></p:blipFill><p:spPr><a:xfrm><a:off x="914400" y="1828800"/><a:ext cx="3657600" cy="1828800"/></a:xfrm></p:spPr></p:pic>
    <p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="4" name="chart"/></p:nvGraphicFramePr><p:xfrm><a:off x="4572000" y="1828800"/><a:ext cx="3657600" cy="1828800"/></p:xfrm><a:graphic><a:graphicData><c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" r:id="chart"/></a:graphicData></a:graphic></p:graphicFrame>
    <p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="5" name="table"/></p:nvGraphicFramePr><p:xfrm><a:off x="914400" y="3657600"/><a:ext cx="914400" cy="457200"/></p:xfrm><a:graphic><a:graphicData><a:tbl><a:tblGrid><a:gridCol w="914400"/></a:tblGrid><a:tr h="457200"><a:tc><a:txBody><a:p><a:r><a:t>12 mg/L</a:t></a:r></a:p></a:txBody></a:tc></a:tr></a:tbl></a:graphicData></a:graphic></p:graphicFrame>
    <p:sp><p:nvSpPr><p:cNvPr id="6" name="formula"/></p:nvSpPr><p:txBody><a:p><m:oMath><m:r><m:t>x=12</m:t></m:r></m:oMath></a:p></p:txBody></p:sp>
    </p:spTree></p:cSld></p:sld>'''
    relns = palate.NS["rel"]
    return {
        "ppt/presentation.xml": f'<p:presentation xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst><p:sldId id="300" r:id="s2"/><p:sldId id="256" r:id="s1"/></p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/></p:presentation>'.encode(),
        "ppt/_rels/presentation.xml.rels": f'<Relationships xmlns="{relns}"><Relationship Id="s1" Type="x/slide" Target="slides/slide1.xml"/><Relationship Id="s2" Type="x/slide" Target="slides/slide2.xml"/></Relationships>'.encode(),
        "ppt/slides/slide1.xml": slide.replace('<p:sld ', '<p:sld show="0" ', 1).encode(),
        "ppt/slides/slide2.xml": slide.encode(),
        "ppt/slides/_rels/slide2.xml.rels": f'<Relationships xmlns="{relns}"><Relationship Id="img" Type="x/image" Target="../media/image1.png"/><Relationship Id="chart" Type="x/chart" Target="../charts/chart1.xml"/><Relationship Id="notes" Type="x/notesSlide" Target="../notesSlides/notesSlide2.xml"/></Relationships>'.encode(),
        "ppt/media/image1.png": b"synthetic-image-bytes",
        "ppt/charts/chart1.xml": b'<chart><unit>mg/L</unit><value>12</value></chart>',
        "ppt/embeddings/workbook.xlsx": b"synthetic-formula-workbook",
        "ppt/notesSlides/notesSlide2.xml": f'<p:notes xmlns:p="{p}" xmlns:a="{a}"><a:t>Synthetic caveat: simulated data only. Reference: test fixture.</a:t></p:notes>'.encode(),
        "ppt/theme/theme1.xml": b"<theme/>",
    }


class PreserveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TEMP)
        self.folder = Path(self.temp.name)
        self.source = self.folder / "source.pptx"
        self.parts = fixture()
        self.write(self.source, self.parts)
        self.plan = {"schema_version": 1, "source_sha256": palate.sha(self.source),
                     "context": {"profile": "internal-tutorial", "detail_level": "synthetic test", "purpose": "test preservation"},
                     "operations": [{"slide": 1, "shape_id": 2, "action": "text_style", "style": {"font_size_pt": 24, "color": "217A80", "font_family": "Arial", "bold": True}, "rule_ids": ["R008"], "reason": "Synthetic test hierarchy"},
                                    {"slide": 1, "shape_id": 3, "action": "geometry", "bounds_inches": [0.5, 1.5, 5, 2.5], "rule_ids": [], "reason": "Synthetic test layout"}]}

    def tearDown(self):
        self.temp.cleanup()

    def write(self, target, parts):
        with zipfile.ZipFile(target, "w") as z:
            for name, data in parts.items():
                z.writestr(name, data)

    def candidate(self):
        parts, _, _ = palate.expected_parts(self.source, self.plan)
        path = self.folder / "candidate.pptx"
        palate.write_package(self.source, path, parts)
        return path, parts

    def test_slide_order_hidden_native_inventory_and_notes(self):
        analysis = palate.analyse(self.source)
        self.assertEqual(analysis["slides"][0]["part"], "ppt/slides/slide2.xml")
        self.assertTrue(analysis["slides"][1]["hidden"])
        self.assertIn("simulated data", analysis["slides"][0]["notes"])
        self.assertEqual(analysis["slides"][0]["shapes"][2]["native_charts"], ["ppt/charts/chart1.xml"])

    def test_preserves_all_science_and_native_objects(self):
        before = palate.sha(self.source)
        candidate, parts = self.candidate()
        result = palate.validate(self.source, candidate, self.plan)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["visual_review"], "pending")
        self.assertEqual(palate.sha(self.source), before)
        self.assertEqual(parts["ppt/charts/chart1.xml"], self.parts["ppt/charts/chart1.xml"])
        self.assertEqual(parts["ppt/embeddings/workbook.xlsx"], self.parts["ppt/embeddings/workbook.xlsx"])
        self.assertEqual(parts["ppt/slides/slide1.xml"], self.parts["ppt/slides/slide1.xml"])
        tree = palate.xml(parts["ppt/slides/slide2.xml"])
        props = tree.find(".//a:rPr", palate.NS)
        self.assertEqual([palate.E.QName(c).localname for c in props], ["solidFill", "latin", "ea", "cs"])

    def test_rejects_changed_units_captions_and_equations(self):
        _, parts = self.candidate()
        for before, after in ((b"mg/L", b"g/L"), (b"12", b"13"), (b"x=12", b"x=21")):
            changed = dict(parts)
            changed["ppt/slides/slide2.xml"] = changed["ppt/slides/slide2.xml"].replace(before, after)
            path = self.folder / ("tampered" + str(len(after)) + str(len(before)) + ".pptx")
            self.write(path, changed)
            self.assertEqual(palate.validate(self.source, path, self.plan)["status"], "failed")

    def test_fractional_size_and_fira_family_preserve_source_content(self):
        self.plan["operations"] = [{
            "slide": 1, "shape_id": 2, "action": "text_style",
            "style": {"font_size_pt": 10.5, "font_family": "Fira Sans"},
            "rule_ids": ["R014"], "reason": "Check fractional point sizes without changing evidence",
        }]
        candidate, parts = self.candidate()
        self.assertEqual(palate.validate(self.source, candidate, self.plan)["status"], "passed")
        tree = palate.xml(parts["ppt/slides/slide2.xml"])
        props = tree.find(".//a:rPr", palate.NS)
        self.assertEqual(props.get("sz"), "1050")
        self.assertEqual(props.find("a:latin", palate.NS).get("typeface"), "Fira Sans")
        original = palate.xml(self.parts["ppt/slides/slide2.xml"])
        self.assertEqual(palate.text_of(tree), palate.text_of(original))
        for name, data in self.parts.items():
            if name != "ppt/slides/slide2.xml":
                self.assertEqual(parts[name], data, name)

    def test_rejects_media_workbook_notes_and_chart_tampering(self):
        _, parts = self.candidate()
        for name in ("ppt/media/image1.png", "ppt/charts/chart1.xml", "ppt/embeddings/workbook.xlsx", "ppt/notesSlides/notesSlide2.xml"):
            modified = dict(parts); modified[name] += b"changed"
            path = self.folder / "tampered.pptx"; self.write(path, modified)
            self.assertEqual(palate.validate(self.source, path, self.plan)["status"], "failed")

    def test_requires_current_hash_and_missing_depth(self):
        for field in ("hash", "detail"):
            plan = copy.deepcopy(self.plan)
            if field == "hash": plan["source_sha256"] = "stale"
            else: del plan["context"]["detail_level"]
            with self.assertRaises(ValueError): palate.expected_parts(self.source, plan)

    def test_context_defaults_overrides_and_scope(self):
        context = palate.resolve_context(self.plan["context"])
        self.assertEqual(context["duration_minutes"], 10)
        custom = dict(self.plan["context"], duration_minutes=15)
        self.assertEqual(palate.resolve_context(custom)["duration_minutes"], 15)
        with self.assertRaises(ValueError):
            palate.resolve_context(dict(custom, profile="internal-monthly-update"))

    def test_matching_or_unsure_screen_preserves_canvas_and_context(self):
        for ratio in ("16:9", "not_sure"):
            with self.subTest(ratio=ratio):
                plan = copy.deepcopy(self.plan)
                plan["context"]["screen_aspect_ratio"] = ratio
                parts, context, _ = palate.expected_parts(self.source, plan)
                self.assertEqual(context["screen_aspect_ratio"], ratio)
                self.assertEqual(parts["ppt/presentation.xml"], self.parts["ppt/presentation.xml"])

    def test_screen_mismatch_requires_native_reflow_in_both_directions(self):
        plan = copy.deepcopy(self.plan)
        plan["context"]["screen_aspect_ratio"] = "4:3"
        with self.assertRaisesRegex(ValueError, "native authoring"):
            palate.expected_parts(self.source, plan)
        standard = dict(self.parts)
        standard["ppt/presentation.xml"] = standard["ppt/presentation.xml"].replace(b'cy="5143500"', b'cy="6858000"')
        self.write(self.source, standard)
        plan["source_sha256"] = palate.sha(self.source)
        parts, context, _ = palate.expected_parts(self.source, plan)
        self.assertEqual(context["screen_aspect_ratio"], "4:3")
        self.assertEqual(parts["ppt/presentation.xml"], standard["ppt/presentation.xml"])
        plan["context"]["screen_aspect_ratio"] = "16:9"
        with self.assertRaisesRegex(ValueError, "native authoring"):
            palate.expected_parts(self.source, plan)

    def test_screen_context_rejects_invalid_choices_and_allows_canvas_rounding(self):
        for value in (None, True, 16 / 9, "16:10", [], {}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                palate.resolve_context(dict(self.plan["context"], screen_aspect_ratio=value))
        rounded = dict(self.parts)
        rounded["ppt/presentation.xml"] = rounded["ppt/presentation.xml"].replace(b'cy="5143500"', b'cy="5143501"')
        self.write(self.source, rounded)
        plan = copy.deepcopy(self.plan)
        plan["source_sha256"] = palate.sha(self.source)
        plan["context"]["screen_aspect_ratio"] = "16:9"
        parts, _, _ = palate.expected_parts(self.source, plan)
        self.assertEqual(parts["ppt/presentation.xml"], rounded["ppt/presentation.xml"])

    def test_refuses_stretch_offslide_and_nan(self):
        for box in ([0, 0, 5, 1], [9, 1, 5, 2.5], [0, float("nan"), 5, 2.5]):
            plan = copy.deepcopy(self.plan); plan["operations"][1]["bounds_inches"] = box
            with self.assertRaises(ValueError): palate.expected_parts(self.source, plan)

    def test_native_table_placement_preserves_grid_but_resize_is_rejected(self):
        op = {"slide": 1, "shape_id": 5, "action": "geometry", "bounds_inches": [2, 4, 1, 0.5], "reason": "Move synthetic native table", "rule_ids": []}
        self.plan["operations"] = [op]
        candidate, _ = self.candidate()
        self.assertEqual(palate.validate(self.source, candidate, self.plan)["status"], "passed")
        op["bounds_inches"] = [2, 4, 2, 0.5]
        with self.assertRaises(ValueError): palate.expected_parts(self.source, self.plan)

    def test_nonstandard_chart_part_location(self):
        parts = dict(self.parts)
        parts["ppt/slides/charts/chart-special.xml"] = parts.pop("ppt/charts/chart1.xml")
        rel = "ppt/slides/_rels/slide2.xml.rels"
        parts[rel] = parts[rel].replace(b"../charts/chart1.xml", b"charts/chart-special.xml")
        self.write(self.source, parts)
        analysis = palate.analyse(self.source)
        self.assertEqual(analysis["package_native_charts"], ["ppt/slides/charts/chart-special.xml"])

    def test_animation_and_math_guard(self):
        parts = dict(self.parts)
        parts["ppt/slides/slide2.xml"] = parts["ppt/slides/slide2.xml"].replace(b"</p:sld>", b"<p:timing/></p:sld>")
        self.write(self.source, parts); self.plan["source_sha256"] = palate.sha(self.source)
        with self.assertRaises(ValueError): palate.expected_parts(self.source, self.plan)
        self.write(self.source, self.parts); self.plan["source_sha256"] = palate.sha(self.source)
        self.plan["operations"][0]["shape_id"] = 6
        with self.assertRaises(ValueError): palate.expected_parts(self.source, self.plan)

    def test_unknown_action_rule_and_keys(self):
        for key, value in (("action", "rewrite_science"), ("rule_ids", ["R006"]), ("ignore_checks", True)):
            plan = copy.deepcopy(self.plan); plan["operations"][0][key] = value
            with self.assertRaises(ValueError): palate.expected_parts(self.source, plan)

    def test_refuses_overwrites(self):
        candidate, parts = self.candidate()
        with self.assertRaises(ValueError): palate.write_package(self.source, candidate, parts)
        with self.assertRaises(ValueError): palate.write_package(self.source, self.source, parts)

    def test_review_must_bind_hash_and_all_slides(self):
        candidate, _ = self.candidate()
        review = {"candidate_sha256": palate.sha(candidate), "reviewed_slides": [1, 2], "visual_status": "passed", "scientific_status": "passed", "editability_status": "passed", "reviewer": "unit test synthetic reviewer", "remaining_issues": [], "native_application": "PowerPoint", "playback_status": "passed", "protected_content_status": "passed", "evidence": ["Synthetic review only"], "ending_review": {"policy": "out_of_scope", "reason": "Bounded fixture modification"}}
        for key, value in (("candidate_sha256", "stale"), ("reviewed_slides", [1]), ("remaining_issues", ["unresolved"]), ("scientific_status", "pending")):
            invalid = dict(review); invalid[key] = value
            with self.assertRaises(ValueError): palate.finalize(self.source, candidate, self.plan, invalid, self.folder / "final.pptx", self.folder / "report.md")
        result = palate.finalize(self.source, candidate, self.plan, review, self.folder / "final.pptx", self.folder / "report.md")
        self.assertEqual(result["final_sha256"], palate.sha(candidate))
        self.assertIn("R008 (primary)", (self.folder / "report.md").read_text(encoding="utf-8"))

    def test_duplicate_zip_and_dtd_rejected(self):
        path = self.folder / "duplicate.pptx"
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("x", b"1"); z.writestr("x", b"2")
        with self.assertRaises(ValueError): palate.read_package(path)
        with self.assertRaises(ValueError): palate.xml(b'<!DOCTYPE a [<!ENTITY x "secret">]><a>&x;</a>')


class PackagingTests(unittest.TestCase):
    def legacy_install(self, root):
        installed = root / "skills/palate-by-sherry"
        payload = {"SKILL.md": b"Synthetic legacy managed skill", "references/retired.md": b"Synthetic legacy runtime"}
        for name, data in payload.items():
            path = installed / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        manifest = {"name": "palate-by-sherry", "schema_version": 1,
                    "files": {name: packager.digest(data) for name, data in payload.items()}}
        (installed / "package-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return installed

    def tree(self, directory):
        return {path.relative_to(directory).as_posix(): path.read_bytes()
                for path in directory.rglob("*") if path.is_file()}

    def test_managed_update_retains_removed_runtime_files_in_backup(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            installed = root / "skills/palate"
            packager.install(package, installed)
            retired = installed / "references/retired-reference.md"
            retired.write_text("Former managed runtime reference", encoding="utf-8")
            marker = installed / "package-manifest.json"
            old = json.loads(marker.read_text())
            old["files"]["references/retired-reference.md"] = packager.digest(retired.read_bytes())
            marker.write_text(json.dumps(old), encoding="utf-8")
            packager.install(package, installed)
            self.assertFalse((installed / "references/retired-reference.md").exists())
            backups = list((root / ".palate-backups").glob("*/palate/references/retired-reference.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "Former managed runtime reference")
            self.assertFalse((installed.parent / ".palate-backups").exists())

    def test_allowlist_install_and_local_edit_preservation(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            manifest = packager.build(package)
            self.assertEqual(manifest["name"], "palate")
            with zipfile.ZipFile(package) as z:
                closing_assets = {"assets/closing-backgrounds/NOTICE.md",
                                  "assets/closing-backgrounds/coastal-panorama.png",
                                  "assets/closing-backgrounds/transmission-tower.png",
                                  "assets/closing-backgrounds/solar-diagonal.png"}
                runtime_assets = {"palate/" + name for name in packager.FILES
                                  if name.startswith("assets/slide-icons/") or name in closing_assets}
                self.assertTrue(all("assets/" not in name or name in runtime_assets for name in z.namelist()))
                self.assertFalse(any("analysis/" in name or ".git/" in name for name in z.namelist()))
                self.assertTrue(all(name.startswith("palate/") for name in z.namelist()))
            installed = root / "skills/palate"
            packager.install(package, installed)
            self.assertEqual(palate.sha(installed / "SKILL.md"), manifest["files"]["SKILL.md"])
            (installed / "SKILL.md").write_text("local unfinished edit", encoding="utf-8")
            with self.assertRaises(ValueError): packager.install(package, installed)
            self.assertEqual((installed / "SKILL.md").read_text(), "local unfinished edit")

    def test_old_install_target_is_refused_without_touching_existing_tree(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            legacy = self.legacy_install(root)
            before = self.tree(legacy)
            with self.assertRaises(ValueError): packager.install(package, legacy)
            self.assertEqual(self.tree(legacy), before)

    def test_explicit_migration_archives_unchanged_legacy_outside_discovery(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            package_before = package.read_bytes()
            legacy = self.legacy_install(root)
            legacy_before = self.tree(legacy)
            unrelated = root / "skills/unrelated"
            unrelated.mkdir()
            (unrelated / "SKILL.md").write_text("Unrelated skill", encoding="utf-8")
            installed = root / "skills/palate"
            result = packager.install(package, installed, migrate_legacy=legacy)
            self.assertEqual(result, str(installed.resolve()))
            self.assertFalse(legacy.exists())
            self.assertEqual(json.loads((installed / "package-manifest.json").read_text())["name"], "palate")
            backups = list((root / ".palate-backups").glob("*/palate-by-sherry"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(self.tree(backups[0]), legacy_before)
            self.assertFalse(backups[0].is_relative_to(installed.parent))
            self.assertEqual((unrelated / "SKILL.md").read_text(), "Unrelated skill")
            self.assertEqual(package.read_bytes(), package_before)

    def test_legacy_sibling_requires_explicit_migration_flag(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            legacy = self.legacy_install(root)
            before = self.tree(legacy)
            installed = root / "skills/palate"
            with self.assertRaisesRegex(ValueError, "explicitly"):
                packager.install(package, installed)
            self.assertEqual(self.tree(legacy), before)
            self.assertFalse(installed.exists())

    def test_changed_and_extra_legacy_files_are_preserved_and_refused(self):
        for modification in ("edit", "extra"):
            with self.subTest(modification=modification), tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
                root = Path(temp)
                package = root / "skill.zip"
                packager.build(package)
                legacy = self.legacy_install(root)
                if modification == "edit":
                    (legacy / "SKILL.md").write_text("Local unfinished legacy edit", encoding="utf-8")
                else:
                    (legacy / "notes.md").write_text("Local private legacy note", encoding="utf-8")
                before = self.tree(legacy)
                installed = root / "skills/palate"
                with self.assertRaises(ValueError):
                    packager.install(package, installed, migrate_legacy=legacy)
                self.assertEqual(self.tree(legacy), before)
                self.assertFalse(installed.exists())
                self.assertFalse((root / ".palate-backups").exists())

    def test_migration_cannot_target_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            unrelated = self.legacy_install(root / "unrelated")
            before = self.tree(unrelated)
            installed = root / "skills/palate"
            with self.assertRaisesRegex(ValueError, "exact sibling"):
                packager.install(package, installed, migrate_legacy=unrelated)
            self.assertEqual(self.tree(unrelated), before)
            self.assertFalse(installed.exists())

    def test_migration_requires_a_valid_old_name_manifest(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            legacy = self.legacy_install(root)
            marker = legacy / "package-manifest.json"
            manifest = json.loads(marker.read_text())
            manifest["name"] = "unrelated"
            marker.write_text(json.dumps(manifest), encoding="utf-8")
            before = self.tree(legacy)
            with self.assertRaises(ValueError):
                packager.install(package, root / "skills/palate", migrate_legacy=legacy)
            self.assertEqual(self.tree(legacy), before)

    def test_migration_refuses_unsafe_manifest_paths_without_touching_other_files(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            legacy = self.legacy_install(root)
            marker = legacy / "package-manifest.json"
            manifest = json.loads(marker.read_text())
            outside = legacy.parent / "outside.txt"
            outside.write_text("Unrelated content", encoding="utf-8")
            manifest["files"]["../outside.txt"] = packager.digest(outside.read_bytes())
            marker.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(ValueError):
                packager.install(package, root / "skills/palate", migrate_legacy=legacy)
            self.assertEqual(outside.read_text(), "Unrelated content")
            self.assertTrue(legacy.exists())

    def test_migration_can_update_an_existing_unchanged_new_install(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            installed = root / "skills/palate"
            packager.install(package, installed)
            current_before = self.tree(installed)
            legacy = self.legacy_install(root)
            legacy_before = self.tree(legacy)
            packager.install(package, installed, migrate_legacy=legacy)
            self.assertEqual(self.tree(installed), current_before)
            self.assertFalse(legacy.exists())
            archives = root / ".palate-backups"
            self.assertEqual(self.tree(next(archives.glob("*/palate"))), current_before)
            self.assertEqual(self.tree(next(archives.glob("*/palate-by-sherry"))), legacy_before)

    def test_migration_refuses_backup_collisions_before_moving_either_install(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            installed = root / "skills/palate"
            packager.install(package, installed)
            legacy = self.legacy_install(root)
            backup = packager.snapshot_path(legacy, (legacy / "package-manifest.json").read_bytes())
            backup.mkdir(parents=True)
            (backup / "keep.txt").write_text("Existing archive", encoding="utf-8")
            new_before, old_before = self.tree(installed), self.tree(legacy)
            with self.assertRaisesRegex(ValueError, "Previous snapshot"):
                packager.install(package, installed, migrate_legacy=legacy)
            self.assertEqual(self.tree(installed), new_before)
            self.assertEqual(self.tree(legacy), old_before)
            self.assertEqual((backup / "keep.txt").read_text(), "Existing archive")

    def test_failed_new_install_rolls_back_both_managed_directories(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            packager.build(package)
            installed = root / "skills/palate"
            packager.install(package, installed)
            legacy = self.legacy_install(root)
            new_before, old_before = self.tree(installed), self.tree(legacy)
            original_rename = Path.rename

            def fail_staged_rename(path, target):
                if path.parent.name.startswith("palate-stage-") and path.name == "palate":
                    raise OSError("Synthetic install failure")
                return original_rename(path, target)

            with patch.object(Path, "rename", fail_staged_rename):
                with self.assertRaisesRegex(OSError, "Synthetic install failure"):
                    packager.install(package, installed, migrate_legacy=legacy)
            self.assertEqual(self.tree(installed), new_before)
            self.assertEqual(self.tree(legacy), old_before)

    def test_cli_explicit_migration_reports_the_preserved_archive(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            installed = root / "skills/palate"
            legacy = self.legacy_install(root)
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_skill.py"), "--output", str(package),
                 "--install", str(installed), "--migrate-legacy", str(legacy)],
                capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(Path(result["installed"]), installed)
            self.assertTrue(Path(result["legacy_archived"]).is_dir())
            self.assertFalse(Path(result["legacy_archived"]).is_relative_to(installed.parent))
            self.assertFalse(legacy.exists())

    def test_cli_migration_requires_an_install_target_before_building(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            root = Path(temp)
            package = root / "skill.zip"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_skill.py"), "--output", str(package),
                 "--migrate-legacy", str(root / "skills/palate-by-sherry")],
                capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("requires --install", completed.stderr)
            self.assertFalse(package.exists())


if __name__ == "__main__":
    unittest.main()
