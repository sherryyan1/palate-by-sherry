"""Verify scientific crop fidelity and fail-closed export boundaries."""

import hashlib
import importlib.util
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("figure_panel_helper", ROOT / "scripts/extract_figure_panels.py")
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class FigurePanelTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / "analysis/local-only/test-temp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="palate-panels-", dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.source = self.folder / "source.png"
        self.plan_path = self.folder / "plan.json"
        self.output = self.folder / "crops"
        image = Image.new("RGBA", (12, 9))
        image.putdata([(x * 19, y * 27, (x + y) * 11, 90 + x * 8) for y in range(9) for x in range(12)])
        image.save(self.source)
        self.original = self.source.read_bytes()
        self.plan = {
            "schema_version": 1,
            "source_sha256": hashlib.sha256(self.original).hexdigest(),
            "panels": [
                {"id": "A", "source_panel": "original panel (a)", "box": [1, 2, 7, 8]},
                {"id": "shared-legend", "source_panel": "shared legend", "box": [9, 0, 12, 9]},
            ],
        }

    def write_plan(self):
        self.plan_path.write_text(json.dumps(self.plan), encoding="utf-8")

    def run_extract(self):
        self.write_plan()
        return helper.extract(self.source, self.plan_path, self.output)

    def assert_rejected(self, exception=ValueError):
        self.write_plan()
        with self.assertRaises(exception):
            helper.extract(self.source, self.plan_path, self.output)
        self.assertFalse(self.output.exists(), "Rejected plans must not create output")
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_exact_pixels_source_identity_and_manifest(self):
        manifest = self.run_extract()
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertEqual(manifest["source"], {
            "filename": "source.png", "sha256": self.plan["source_sha256"],
            "format": "PNG", "width": 12, "height": 9, "mode": "RGBA",
        })
        saved_manifest = json.loads((self.output / helper.MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(saved_manifest, manifest)
        self.assertEqual({path.name for path in self.output.iterdir()}, {"A.png", "shared-legend.png", helper.MANIFEST_NAME})
        with Image.open(self.source) as source:
            for supplied, record in zip(self.plan["panels"], manifest["panels"]):
                png = (self.output / record["file"]).read_bytes()
                with Image.open(BytesIO(png)) as crop:
                    expected = source.crop(supplied["box"])
                    self.assertEqual(crop.size, expected.size)
                    self.assertEqual(crop.mode, expected.mode)
                    self.assertEqual(crop.tobytes(), expected.tobytes())
                self.assertEqual(record["box"], supplied["box"])
                self.assertEqual(record["source_panel"], supplied["source_panel"])
                self.assertEqual(record["sha256"], hashlib.sha256(png).hexdigest())
                self.assertEqual(record["semantic_crop_review"], "pending")
                self.assertEqual(record["native_editability"], "raster interior is not native editable")

    def test_supported_static_formats_preserve_decoded_pixels(self):
        for format_name, suffix in (("PNG", ".png"), ("JPEG", ".jpg"), ("TIFF", ".tiff"), ("WEBP", ".webp")):
            with self.subTest(format=format_name):
                self.source = self.folder / ("source" + suffix)
                Image.new("RGB", (12, 9), (38, 102, 173)).save(self.source, format=format_name)
                self.original = self.source.read_bytes()
                self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
                self.output = self.folder / ("crops-" + format_name)
                self.run_extract()
                with Image.open(self.source) as source, Image.open(self.output / "A.png") as crop:
                    self.assertEqual(crop.tobytes(), source.crop((1, 2, 7, 8)).tobytes())

    def test_palette_transparency_is_preserved(self):
        source = Image.new("P", (12, 9), 1)
        source.putpalette([0, 0, 0, 140, 120, 100] + [0] * (768 - 6))
        source.putpixel((2, 3), 0)
        source.save(self.source, transparency=0)
        self.original = self.source.read_bytes()
        self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
        self.run_extract()
        with Image.open(self.source) as source, Image.open(self.output / "A.png") as crop:
            self.assertEqual(crop.mode, "P")
            self.assertEqual(crop.getpalette(), source.getpalette())
            self.assertEqual(crop.info["transparency"], 0)
            self.assertEqual(crop.convert("RGBA").tobytes(), source.crop((1, 2, 7, 8)).convert("RGBA").tobytes())

    def test_sixteen_bit_pixels_are_not_clipped_or_quantized(self):
        source = Image.new("I;16", (12, 9))
        for y in range(9):
            for x in range(12):
                source.putpixel((x, y), (x + y * 12) * 601)
        source.save(self.source)
        self.original = self.source.read_bytes()
        self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
        self.run_extract()
        with Image.open(self.source) as source, Image.open(self.output / "A.png") as crop:
            self.assertEqual(crop.mode, source.mode)
            self.assertEqual(crop.tobytes(), source.crop((1, 2, 7, 8)).tobytes())

    def test_exif_orientation_does_not_rotate_raw_pixel_coordinates(self):
        source = Image.new("RGB", (12, 9), (24, 74, 133))
        source.putpixel((2, 3), (220, 40, 20))
        exif = Image.Exif()
        exif[274] = 6
        source.save(self.source, exif=exif)
        self.original = self.source.read_bytes()
        self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
        manifest = self.run_extract()
        with Image.open(self.output / "A.png") as crop:
            self.assertEqual(crop.size, (6, 6))
            self.assertEqual(crop.getpixel((1, 1)), (220, 40, 20))
            self.assertNotIn(274, crop.getexif())
        self.assertIn("no EXIF rotation", manifest["coordinate_system"])

    def test_invalid_bounds_types_and_dimensions_are_rejected(self):
        for box in ([-1, 0, 2, 2], [0, 0, 13, 2], [3, 2, 3, 4], [0, 8, 2, 3], [0, 0, 2.0, 3], [False, 0, 2, 3], [0, 2, 4], "0,0,2,3"):
            with self.subTest(box=box):
                self.plan["panels"][0]["box"] = box
                self.assert_rejected()

    def test_stale_hash_unknown_fields_and_duplicate_json_keys_are_rejected(self):
        self.plan["source_sha256"] = "0" * 64
        self.assert_rejected()
        self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
        self.plan["unexpected"] = True
        self.assert_rejected()
        del self.plan["unexpected"]
        self.plan["panels"][0]["resize"] = [40, 40]
        self.assert_rejected()
        del self.plan["panels"][0]["resize"]
        self.write_plan()
        self.plan_path.write_text(self.plan_path.read_text(encoding="utf-8").replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            helper.extract(self.source, self.plan_path, self.output)
        self.assertFalse(self.output.exists())

    def test_schema_and_resource_limits_are_enforced_before_output(self):
        self.plan["schema_version"] = True
        self.assert_rejected()
        self.plan["schema_version"] = 1
        saved_panels = self.plan["panels"]
        self.plan["panels"] = []
        self.assert_rejected()
        self.plan["panels"] = saved_panels
        self.write_plan()
        for limit_name in ("MAX_SOURCE_BYTES", "MAX_PLAN_BYTES", "MAX_SOURCE_PIXELS", "MAX_TOTAL_CROP_PIXELS", "MAX_PANELS"):
            with self.subTest(limit=limit_name), patch.object(helper, limit_name, 1):
                with self.assertRaises(ValueError):
                    helper.extract(self.source, self.plan_path, self.output)
                self.assertFalse(self.output.exists())

    def test_filename_collisions_traversal_and_reserved_names_are_rejected(self):
        for identifier in ("a", "../A", "C:stream", "A.png", "CON", "lpt9", "x" * 65, "A ", ""):
            with self.subTest(identifier=identifier):
                self.plan["panels"][1]["id"] = identifier
                self.assert_rejected()

    def test_empty_or_controlled_source_identity_is_rejected(self):
        for identity in ("", " ", "panel\nA", "x" * 201):
            with self.subTest(identity=identity):
                self.plan["panels"][0]["source_panel"] = identity
                self.assert_rejected()

    def test_existing_output_is_untouched(self):
        self.output.mkdir()
        sentinel = self.output / "A.png"
        sentinel.write_bytes(b"existing private content")
        self.write_plan()
        with self.assertRaises(FileExistsError):
            helper.extract(self.source, self.plan_path, self.output)
        self.assertEqual(sentinel.read_bytes(), b"existing private content")
        self.assertEqual(list(self.output.iterdir()), [sentinel])

    def test_output_file_and_traversal_paths_are_rejected(self):
        self.output.write_bytes(b"existing")
        self.write_plan()
        with self.assertRaises(FileExistsError):
            helper.extract(self.source, self.plan_path, self.output)
        self.assertEqual(self.output.read_bytes(), b"existing")
        with self.assertRaisesRegex(ValueError, "traversal"):
            helper.extract(self.folder / "unused" / ".." / "source.png", self.plan_path, self.folder / "other")

    def test_source_or_plan_inside_output_is_rejected(self):
        self.write_plan()
        with self.assertRaisesRegex(ValueError, "inside"):
            helper.extract(self.output / "source.png", self.plan_path, self.output)
        with self.assertRaisesRegex(ValueError, "inside"):
            helper.extract(self.source, self.output / "plan.json", self.output)
        self.assertFalse(self.output.exists())

    def test_symlinks_are_rejected_when_platform_permits_them(self):
        link = self.folder / "linked.png"
        try:
            link.symlink_to(self.source)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation is unavailable for this account")
        self.write_plan()
        with self.assertRaisesRegex(ValueError, "Symlink"):
            helper.extract(link, self.plan_path, self.output)
        self.assertFalse(self.output.exists())

    def test_hard_link_inputs_are_rejected(self):
        link = self.folder / "hardlinked.png"
        try:
            os.link(self.source, link)
        except (OSError, NotImplementedError):
            self.skipTest("Hard-link creation is unavailable for this account")
        self.assert_rejected()

    def test_animated_multipage_and_nonpreservable_inputs_are_rejected(self):
        for format_name, mode in (("PNG", "RGB"), ("TIFF", "RGB"), ("JPEG", "CMYK"), ("TIFF", "F"), ("BMP", "RGB")):
            with self.subTest(format=format_name, mode=mode):
                image = Image.new(mode, (12, 9))
                options = {"save_all": True, "append_images": [Image.new(mode, (12, 9), 1)]} if format_name in {"PNG", "TIFF"} and mode == "RGB" else {}
                image.save(self.source, format=format_name, **options)
                self.original = self.source.read_bytes()
                self.plan["source_sha256"] = hashlib.sha256(self.original).hexdigest()
                self.assert_rejected()

    def test_encoding_failure_does_not_create_output(self):
        self.write_plan()
        with patch.object(Image.Image, "save", side_effect=OSError("synthetic encoding failure")):
            with self.assertRaisesRegex(OSError, "encoding failure"):
                helper.extract(self.source, self.plan_path, self.output)
        self.assertFalse(self.output.exists())

    def test_write_failure_removes_only_created_files(self):
        self.write_plan()
        original_write = helper._write_new
        count = 0
        def racing_write(path, data, owned, directory_fd=None):
            nonlocal count
            count += 1
            if count == 2:
                path.write_bytes(b"competing content")
            original_write(path, data, owned, directory_fd)
        with patch.object(helper, "_write_new", side_effect=racing_write):
            with self.assertRaises(FileExistsError):
                helper.extract(self.source, self.plan_path, self.output)
        self.assertEqual({file.name for file in self.output.iterdir()}, {"shared-legend.png"})
        self.assertEqual((self.output / "shared-legend.png").read_bytes(), b"competing content")

    def test_failed_write_removes_owned_files_and_empty_directory(self):
        self.write_plan()
        original_write = helper._write_new
        def failing_write(path, data, owned, directory_fd=None):
            original_write(path, data, owned, directory_fd)
            raise OSError("synthetic write failure")
        with patch.object(helper, "_write_new", side_effect=failing_write):
            with self.assertRaisesRegex(OSError, "write failure"):
                helper.extract(self.source, self.plan_path, self.output)
        self.assertFalse(self.output.exists())

    def test_fresh_directory_race_cannot_overwrite_another_run(self):
        self.write_plan()
        original_mkdir = Path.mkdir
        def racing_mkdir(path, *args, **kwargs):
            if path == self.output:
                original_mkdir(path)
                (path / "sentinel").write_bytes(b"another run")
            return original_mkdir(path, *args, **kwargs)
        with patch.object(Path, "mkdir", racing_mkdir):
            with self.assertRaises(FileExistsError):
                helper.extract(self.source, self.plan_path, self.output)
        self.assertEqual((self.output / "sentinel").read_bytes(), b"another run")

    def test_cli_exports_and_reports_pending_review(self):
        import sys
        self.write_plan()
        result = subprocess.run([
            sys.executable, "-B", str(ROOT / "scripts/extract_figure_panels.py"),
            "--source", str(self.source), "--plan", str(self.plan_path), "--output-dir", str(self.output),
        ], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["semantic_crop_review"], "pending")
        self.assertTrue((self.output / "A.png").is_file())


if __name__ == "__main__":
    unittest.main()
