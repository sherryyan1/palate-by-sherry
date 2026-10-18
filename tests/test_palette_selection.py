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

    def test_task_and_page_filters_intersect(self):
        result = select_palette.select(self.data, task="scenario-bands", source="pbl_pdf", page=20)
        self.assertEqual([r["id"] for r in result["recipes"]], ["pbl_topright_scenario"])

    def test_categorical_bubbles_do_not_receive_ordered_scale(self):
        result = select_palette.select(self.data, task="categorical-bubbles", limit=10)
        self.assertTrue(result["recipes"])
        self.assertNotIn("econ_bubble_spectrum", [r["id"] for r in result["recipes"]])
        self.assertIn("econ_bubble_spectrum", [r["id"] for r in select_palette.select(self.data, task="ordered-bubbles")["recipes"]])

    def test_numeric_level_and_signed_change_are_separate(self):
        ordered = select_palette.select(self.data, task="ordered-percent-map")
        diverging = select_palette.select(self.data, task="diverging")
        self.assertIn("econ_percent_choropleth", [r["id"] for r in ordered["recipes"]])
        self.assertNotIn("econ_percent_choropleth", [r["id"] for r in diverging["recipes"]])

    def test_sampler_page_does_not_become_a_palette(self):
        result = select_palette.select(self.data, source="economist_pdf", page=2)
        self.assertEqual(result["recipes"], [])
        self.assertTrue(result["page_notes"])

    def test_results_are_bounded_without_mutating_library(self):
        before = copy.deepcopy(self.data)
        result = select_palette.select(self.data, task="calm-illustration", limit=1)
        self.assertEqual(len(result["recipes"]), 1)
        self.assertTrue(result["more_ids"])
        self.assertEqual(before, self.data)

    def test_missing_and_incompatible_selectors_do_not_fall_back(self):
        for kwargs in ({}, {"recipe_id": "unknown"}, {"task": "unknown"},
                       {"source": "unknown"}, {"page": 20}, {"listing": True, "limit": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                select_palette.select(self.data, **kwargs)
        self.assertEqual(select_palette.select(self.data, recipe_id="econ_percent_choropleth", task="diverging")["recipes"], [])

    def test_invalid_recipe_rejected(self):
        for corruption in ("duplicate_id", "invalid_hex", "duplicate_role"):
            bad = copy.deepcopy(self.data)
            if corruption == "duplicate_id":
                bad["palettes"].append(copy.deepcopy(bad["palettes"][0]))
            elif corruption == "invalid_hex":
                bad["palettes"][0]["colors"][0]["hex"] = "blue"
            else:
                bad["palettes"][0]["colors"].append(copy.deepcopy(bad["palettes"][0]["colors"][0]))
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
