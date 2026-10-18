"""Selective reads retain complete rules and enclosing section qualifications."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts import reference_query as query


class ReferenceQueryTests(unittest.TestCase):
    def test_selected_rules_are_identical_complete_objects(self):
        library = json.loads(query.reference("design-decision-library.json"))
        expected = {r["id"]: r for r in library["rules"]}
        result = query.rule_query(["R003", "R001", "R003"])
        self.assertEqual(result["rules"], [expected["R003"], expected["R001"]])
        self.assertEqual(result["rule_policy"], library["rule_policy"])
        self.assertTrue(all("exceptions" in r and "validation" in r for r in result["rules"]))

    def test_index_includes_every_trigger_and_rejects_unknown_ids(self):
        library = json.loads(query.reference("design-decision-library.json"))
        index = query.rule_query()
        self.assertEqual([r["trigger"] for r in index["rules"]], [r["trigger"] for r in library["rules"]])
        self.assertEqual(index["mode"], "index_only")
        with self.assertRaises(ValueError):
            query.rule_query(["R999"])

    def test_nested_section_keeps_scope_parent_and_descendants_without_siblings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "references").mkdir()
            (root / "references/test.md").write_text(
                "# Guide\nGlobal scope.\n## Parent\nParent qualification.\n"
                "### Earlier\nUnrelated earlier content.\n### Selected\nNeeded content.\n"
                "```text\n## Not a heading\n```\n#### Detail\nException.\n"
                "### Later\nUnrelated later content.\n## End\n", encoding="utf-8")
            result = query.section_query("test.md", "Selected", root)
            self.assertIn("Global scope.", result["context"])
            self.assertIn("Parent qualification.", result["context"])
            self.assertIn("Exception.", result["section"])
            self.assertNotIn("Unrelated", result["context"] + result["section"])
            self.assertNotIn("Not a heading", [r["heading"] for r in query.section_query("test.md", root=root)["headings"]])

    def test_unknown_or_duplicate_heading_and_outside_path_are_rejected(self):
        with self.assertRaises(ValueError):
            query.section_query("scientific-fidelity.md", "Missing")
        for name in ["../SKILL.md", "C:/secret.md", "other/file.md"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                query.reference(name)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "references").mkdir()
            (root / "references/test.md").write_text("# Test\n## Duplicate\nA\n## Duplicate\nB\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                query.section_query("test.md", "Duplicate", root)


if __name__ == "__main__":
    unittest.main()
