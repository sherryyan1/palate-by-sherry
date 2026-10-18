"""Check retrieval boundaries, recipe integrity and scientific encoding separation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import package_skill, select_palette

TEST_TEMP = Path(__file__).resolve().parents[1] / "analysis/local-only/test-temp"


class PaletteSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        cls.data = select_palette.load_library()

    def test_exact_recipe_preserves_coordinated_roles(self):
        original = next(r for r in self.data["palettes"] if r["id"] == "editorial_blue_terracotta")
        result = select_palette.select(self.data, recipe_id=original["id"])
        self.assertEqual(result["recipes"][0]["colors"], original["colors"])
        self.assertEqual(result["recipes"][0]["name"], "Editorial Blue & Terracotta")
        self.assertEqual(result["more_ids"], [])
        self.assertNotIn("palettes", result)

    def test_task_and_id_filters_intersect(self):
        result = select_palette.select(self.data, task="scenario-bands", recipe_id="blue_taupe_bands")
        self.assertEqual([r["id"] for r in result["recipes"]], ["blue_taupe_bands"])

    def test_categorical_bubbles_do_not_receive_ordered_scale(self):
        result = select_palette.select(self.data, task="categorical-bubbles", limit=10)
        self.assertTrue(result["recipes"])
        self.assertNotIn("ordered_bubble_spectrum", [r["id"] for r in result["recipes"]])
        self.assertIn("ordered_bubble_spectrum", [r["id"] for r in select_palette.select(self.data, task="ordered-bubbles")["recipes"]])

    def test_numeric_level_and_signed_change_are_separate(self):
        ordered = select_palette.select(self.data, task="ordered-percent-map")
        diverging = select_palette.select(self.data, task="diverging")
        self.assertIn("orange_percent_scale", [r["id"] for r in ordered["recipes"]])
        self.assertNotIn("orange_percent_scale", [r["id"] for r in diverging["recipes"]])

    def test_library_and_results_contain_only_color_and_usage_fields(self):
        self.assertEqual(set(self.data), {"schema_version", "palettes"})
        self.assertEqual(len(self.data["palettes"]), 27)
        for recipe in self.data["palettes"]:
            self.assertLessEqual(set(recipe), select_palette.RECIPE_FIELDS)
            self.assertEqual(select_palette.select(self.data, recipe_id=recipe["id"])["recipes"], [recipe])
            for color in recipe["colors"]:
                self.assertEqual(set(color), {"role", "hex"})

    def test_document_lookup_flags_are_not_supported(self):
        script = str(select_palette.LIBRARY.parents[1] / "scripts/select_palette.py")
        for flag, value in (("--source", "fixture"), ("--page", "1")):
            result = subprocess.run([sys.executable, script, flag, value], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"unrecognized arguments", result.stderr)
            self.assertEqual(result.stdout, b"")

    def test_results_are_bounded_without_mutating_library(self):
        before = copy.deepcopy(self.data)
        result = select_palette.select(self.data, task="calm-illustration", limit=1)
        self.assertEqual(len(result["recipes"]), 1)
        self.assertTrue(result["more_ids"])
        self.assertEqual(before, self.data)

    def test_missing_and_incompatible_selectors_do_not_fall_back(self):
        for kwargs in ({}, {"recipe_id": "unknown"}, {"task": "unknown"},
                       {"listing": True, "limit": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                select_palette.select(self.data, **kwargs)
        self.assertEqual(select_palette.select(self.data, recipe_id="orange_percent_scale", task="diverging")["recipes"], [])

    def test_invalid_recipe_rejected(self):
        for corruption in ("duplicate_id", "invalid_hex", "duplicate_role", "library_metadata", "recipe_metadata", "color_metadata"):
            bad = copy.deepcopy(self.data)
            if corruption == "duplicate_id":
                bad["palettes"].append(copy.deepcopy(bad["palettes"][0]))
            elif corruption == "invalid_hex":
                bad["palettes"][0]["colors"][0]["hex"] = "blue"
            elif corruption == "duplicate_role":
                bad["palettes"][0]["colors"].append(copy.deepcopy(bad["palettes"][0]["colors"][0]))
            elif corruption == "library_metadata":
                bad["private_reference"] = "fixture"
            elif corruption == "recipe_metadata":
                bad["palettes"][0]["private_reference"] = "fixture"
            else:
                bad["palettes"][0]["colors"][0]["private_reference"] = "fixture"
            with tempfile.TemporaryDirectory(dir=TEST_TEMP) as directory:
                path = Path(directory) / "library.json"
                path.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaises(ValueError):
                    select_palette.load_library(path)

    def test_packaged_selector_works_without_repository_or_yaml(self):
        import zipfile
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as directory:
            root = Path(directory)
            package_skill.build(root / "skill.zip")
            with zipfile.ZipFile(root / "skill.zip") as package:
                package.extractall(root / "installed")
            script = root / "installed/palate/scripts/select_palette.py"
            output = subprocess.check_output([sys.executable, str(script), "--id", "coastal_clear_blues"], cwd=root)
            result = json.loads(output)
            self.assertEqual(result["recipes"][0]["colors"][0]["hex"], "#28A3CF")


if __name__ == "__main__":
    unittest.main()
