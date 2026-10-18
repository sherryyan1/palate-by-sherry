"""Synthetic dependency and CLI tests for immutable private task snapshots."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import task_state as helper


ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return {
        "schema_version": 1,
        "brief": {"audience": "Synthetic research group", "minutes": 12},
        "narrative": {"central_question": "Which explanation fits?"},
        "design": {"approved": True, "font": "Arial", "ratio": "16:9"},
        "sources": {f"src{i}": {"revision": "v1", "artifact": f"missing-private-{i}.pdf", "coverage_complete": True}
                    for i in range(1, 6)},
        "questions": {f"q{i}": {"text": f"Synthetic question {i}?"} for i in range(1, 6)},
        "evidence": {f"e{i}": {"source_ids": [f"src{i}"], "question_ids": [f"q{i}"], "coverage_complete": True,
                                "value": i, "units": "synthetic units", "caveat": "Illustrative only"}
                     for i in range(1, 6)},
        "slides": [{"id": f"s{i}", "revision": "v1", "hidden": i == 3,
                    "question_ids": [], "evidence_ids": [f"e{i}"],
                    "title": f"Synthetic message {i}", "role": "evidence"}
                   for i in range(1, 6)],
    }


def with_reviews(state):
    state["reviews"] = [{"scope": scope, "kind": kind, "status": "passed",
                         "fingerprint": helper.fingerprint(state, scope, kind),
                         "artifact": "private-review-not-opened.json"}
                        for scope in ["deck", *(s["id"] for s in state["slides"])]
                        for kind in helper.KINDS]
    return state


class StateTests(unittest.TestCase):
    def setUp(self):
        self.state = fixture()

    def affected(self, updated):
        return {r["slide_id"]: r for r in helper.compare_states(self.state, updated)["affected_slides"]}

    def test_local_slide_change_limits_reviews_and_includes_hidden_neighbor(self):
        updated = copy.deepcopy(self.state)
        updated["slides"][1]["revision"] = "v2"
        affected = self.affected(updated)
        self.assertEqual(set(affected), {"s1", "s2", "s3", "s4"})
        self.assertEqual(affected["s2"]["review_kinds"], list(helper.KINDS))
        self.assertEqual(affected["s1"]["review_kinds"], ["narrative"])
        self.assertEqual(affected["s3"]["review_kinds"], ["narrative"])
        self.assertTrue(affected["s3"]["hidden"])

    def test_evidence_question_and_source_changes_follow_explicit_dependencies(self):
        for name, identity, field in (("evidence", "e2", "value"),
                                      ("questions", "q2", "text"),
                                      ("sources", "src2", "revision")):
            with self.subTest(name=name):
                updated = copy.deepcopy(self.state)
                updated[name][identity][field] = "changed"
                affected = self.affected(updated)
                self.assertEqual(set(affected), {"s1", "s2", "s3", "s4"})
                self.assertEqual(affected["s2"]["review_kinds"], list(helper.KINDS))
                self.assertIn(f"{name} changed: {identity}", affected["s2"]["reasons"])
                self.assertNotEqual(helper.fingerprint(self.state, "deck", "narrative"),
                                    helper.fingerprint(updated, "deck", "narrative"))
                self.assertEqual(helper.fingerprint(self.state, "s5", "rendered"),
                                 helper.fingerprint(updated, "s5", "rendered"))

    def test_unknown_source_coverage_expands_all_current_slides(self):
        updated = copy.deepcopy(self.state)
        updated["sources"]["new-source"] = {"revision": "new"}
        affected = self.affected(updated)
        self.assertEqual(len(affected), 5)
        self.assertTrue(all(r["review_kinds"] == list(helper.KINDS) for r in affected.values()))
        self.assertIn("source coverage is incomplete or changed", affected["s5"]["reasons"])

    def test_unmapped_source_revision_change_expands_all_slides(self):
        self.state["sources"]["unmapped"] = {"revision": "v1"}
        updated = copy.deepcopy(self.state)
        updated["sources"]["unmapped"]["revision"] = "v2"
        self.assertEqual(len(self.affected(updated)), 5)

    def test_missing_coverage_assertions_default_to_global_invalidation(self):
        for name, identity, field in (("sources", "src2", "revision"), ("evidence", "e2", "value")):
            with self.subTest(name=name):
                original = fixture()
                del original[name][identity]["coverage_complete"]
                updated = copy.deepcopy(original)
                updated[name][identity][field] = "changed"
                report = helper.compare_states(original, updated)
                self.assertEqual(len(report["affected_slides"]), 5)
                self.assertTrue(all(r["review_kinds"] == list(helper.KINDS) for r in report["affected_slides"]))
                self.assertFalse(report["coverage"]["complete"])

    def test_unmapped_evidence_cannot_hide_behind_an_already_mapped_source(self):
        for complete in (False, True):
            with self.subTest(coverage_complete=complete):
                original = fixture()
                original["evidence"]["unmapped"] = {"source_ids": ["src1"], "question_ids": ["q1"],
                                                      "value": "provisional contrary finding", "coverage_complete": complete}
                with_reviews(original)
                updated = copy.deepcopy(original)
                updated["evidence"]["unmapped"]["value"] = "confirmed contrary finding"
                report = helper.compare_states(original, updated)
                self.assertEqual(len(report["affected_slides"]), 5)
                self.assertTrue(all(r["freshness"] == "stale" for r in report["reviews"]))
                packet = helper.select_state(updated, ["s5"])["current"]
                self.assertNotIn("unmapped", packet["evidence"])
                self.assertEqual(packet["coverage"]["unscoped_evidence_count"], 1)
                self.assertEqual(packet["coverage"]["unscoped_source_count"], 1)

    def test_incomplete_evidence_mapping_makes_its_source_change_global(self):
        self.state["evidence"]["e2"]["coverage_complete"] = False
        updated = copy.deepcopy(self.state)
        updated["sources"]["src2"]["revision"] = "v2"
        self.assertEqual(len(self.affected(updated)), 5)

    def test_unlinked_question_added_or_changed_invalidates_all_slides(self):
        for operation in ("added", "changed"):
            with self.subTest(operation=operation):
                original = fixture()
                if operation == "changed":
                    original["questions"]["central"] = {"text": "Initial unlinked question?"}
                with_reviews(original)
                updated = copy.deepcopy(original)
                updated["questions"]["central"] = {"text": "New unlinked research question?"}
                report = helper.compare_states(original, updated)
                self.assertEqual(len(report["affected_slides"]), 5)
                self.assertTrue(all(r["review_kinds"] == list(helper.KINDS) for r in report["affected_slides"]))
                self.assertTrue(all(r["freshness"] == "stale" for r in report["reviews"]))
                self.assertIn("question coverage is incomplete or changed", report["affected_slides"][0]["reasons"])
                self.assertEqual(report["coverage"]["unscoped_question_count"], 1)
                self.assertEqual(helper.state_report(updated)["unscoped_question_ids"], ["central"])

    def test_brief_narrative_shared_design_changes_expand_all_slides(self):
        for name in ("brief", "narrative", "design"):
            with self.subTest(name=name):
                updated = copy.deepcopy(self.state)
                updated[name]["new_requirement"] = "change"
                affected = self.affected(updated)
                self.assertEqual(len(affected), 5)
                self.assertTrue(all(r["review_kinds"] == list(helper.KINDS) for r in affected.values()))

    def test_reordering_preserves_ids_and_expands_review(self):
        updated = copy.deepcopy(self.state)
        updated["slides"] = updated["slides"][::-1]
        affected = self.affected(updated)
        self.assertEqual(list(affected), ["s5", "s4", "s3", "s2", "s1"])
        self.assertIn("slide order or membership changed", affected["s3"]["reasons"])

    def test_added_and_removed_slides_are_reported(self):
        updated = copy.deepcopy(self.state)
        updated["slides"].pop(1)
        updated["slides"].append({"id": "new", "revision": "v1", "hidden": True,
                                  "question_ids": [], "evidence_ids": []})
        report = helper.compare_states(self.state, updated)
        self.assertEqual(report["removed_slide_ids"], ["s2"])
        self.assertEqual([r["slide_id"] for r in report["affected_slides"]], ["s1", "s3", "s4", "s5", "new"])
        self.assertIn("slide added", report["affected_slides"][-1]["reasons"])
        self.assertEqual(report["final_deck_review"]["slide_ids"], ["s1", "s3", "s4", "s5", "new"])

    def test_stale_passes_cannot_be_restored_by_comparing_same_modified_state(self):
        state = with_reviews(self.state)
        updated = copy.deepcopy(state)
        updated["slides"][1]["revision"] = "v2"
        report = helper.compare_states(updated, updated)
        self.assertFalse(report["changed"])
        self.assertEqual(report["affected_slides"], [])
        reviews = {(r["scope"], r["kind"]): r for r in report["reviews"]}
        self.assertEqual(reviews[("s2", "content")]["freshness"], "stale")
        self.assertEqual(reviews[("s2", "content")]["declared_status"], "passed")
        self.assertEqual(reviews[("s5", "rendered")]["freshness"], "current")
        self.assertEqual(reviews[("deck", "rendered")]["freshness"], "stale")
        self.assertFalse(report["final_deck_review"]["completed_by_helper"])

    def test_review_declaration_changes_do_not_change_fingerprints_or_certify_review(self):
        state = with_reviews(self.state)
        updated = copy.deepcopy(state)
        updated["reviews"][0]["status"] = "failed"
        report = helper.compare_states(state, updated)
        self.assertFalse(report["changed"])
        self.assertEqual(report["reviews"][0], {"scope": "deck", "kind": "content",
                                               "declared_status": "failed", "freshness": "current"})
        self.assertTrue(report["final_deck_review"]["required_before_delivery"])

    def test_select_returns_only_needed_payload_and_hidden_context(self):
        self.state["questions"]["unrelated"] = {"text": "Unreferenced"}
        self.state["evidence"]["unrelated"] = {"source_ids": [], "question_ids": []}
        report = helper.select_state(self.state, ["s2"])
        selected = report["current"]
        self.assertEqual(selected["selected_slide_ids"], ["s2"])
        self.assertEqual(selected["context_slide_ids"], ["s1", "s3", "s4"])
        self.assertEqual(set(selected["evidence"]), {"e1", "e2", "e3", "e4"})
        self.assertEqual(set(selected["questions"]), {"q1", "q2", "q3", "q4"})
        self.assertEqual(set(selected["sources"]), {"src1", "src2", "src3", "src4"})
        self.assertEqual(selected["narrative"], self.state["narrative"])
        self.assertTrue(selected["design"]["approved"])
        self.assertTrue(selected["slides"][2]["hidden"])
        selected["slides"][0]["title"] = "Caller mutation"
        self.assertNotEqual(self.state["slides"][0]["title"], "Caller mutation")

    def test_selection_includes_current_and_old_neighbors_after_reorder(self):
        updated = copy.deepcopy(self.state)
        updated["slides"] = [updated["slides"][i] for i in (0, 2, 3, 4, 1)]
        selected = helper.select_state(updated, ["s2"], previous=self.state)
        self.assertEqual(selected["current"]["context_slide_ids"], ["s1", "s3", "s4", "s5"])
        self.assertEqual(selected["previous"]["context_slide_ids"], ["s1", "s3", "s4", "s5"])

    def test_hidden_run_keeps_actual_adjacent_and_nearest_visible_context(self):
        for slide in self.state["slides"][1:4]:
            slide["hidden"] = True
        selected = helper.select_state(self.state, ["s1"])
        self.assertEqual(selected["current"]["context_slide_ids"], ["s2", "s5"])
        self.assertEqual(set(selected["current"]["evidence"]), {"e1", "e2", "e5"})
        self.assertEqual(selected["final_deck_review"]["slide_ids"], ["s1", "s2", "s3", "s4", "s5"])
        updated = copy.deepcopy(self.state)
        updated["slides"][0]["revision"] = "v2"
        self.assertEqual(self.affected(updated)["s5"]["review_kinds"], ["narrative"])

    def test_removed_slide_can_be_selected_using_previous_snapshot(self):
        updated = copy.deepcopy(self.state)
        updated["slides"].pop(1)
        selected = helper.select_state(updated, ["s2"], previous=self.state)
        self.assertEqual(selected["current"]["selected_slide_ids"], [])
        self.assertEqual(selected["current"]["context_slide_ids"], ["s1", "s3", "s4"])
        self.assertEqual(selected["previous"]["selected_slide_ids"], ["s2"])
        with self.assertRaises(ValueError):
            helper.select_state(updated, ["s2"])

    def test_unknown_duplicate_and_missing_references_fail_closed(self):
        for location, key, value in (("slide", "evidence_ids", ["missing"]),
                                      ("slide", "question_ids", ["missing"]),
                                      ("evidence", "source_ids", ["missing"]),
                                      ("evidence", "question_ids", ["missing"]),
                                      ("slide", "evidence_ids", ["e1", "e1"]),
                                      ("slide", "revision", ""),
                                      ("source", "revision", "")):
            with self.subTest(location=location, key=key, value=value):
                updated = copy.deepcopy(self.state)
                target = {"slide": updated["slides"][0], "evidence": updated["evidence"]["e1"],
                          "source": updated["sources"]["src1"]}[location]
                target[key] = value
                with self.assertRaises(ValueError):
                    helper.validate_state(updated)
        for ids in (["missing"], ["s1", "s1"], []):
            with self.assertRaises(ValueError):
                helper.select_state(self.state, ids)

    def test_ambiguous_state_and_unknown_review_scope_fail_closed(self):
        invalid = []
        duplicate_slide = copy.deepcopy(self.state)
        duplicate_slide["slides"][1]["id"] = "s1"
        invalid.append(duplicate_slide)
        bad_version = copy.deepcopy(self.state)
        bad_version["schema_version"] = True
        invalid.append(bad_version)
        unknown_top_level = copy.deepcopy(self.state)
        unknown_top_level["shared_formatting"] = {"font": "Changed"}
        invalid.append(unknown_top_level)
        bad_review = with_reviews(copy.deepcopy(self.state))
        bad_review["reviews"][0]["scope"] = "missing"
        invalid.append(bad_review)
        duplicate_review = with_reviews(copy.deepcopy(self.state))
        duplicate_review["reviews"].append(duplicate_review["reviews"][0])
        invalid.append(duplicate_review)
        for state in invalid:
            with self.assertRaises(ValueError):
                helper.validate_state(state)

    def test_list_and_object_review_kinds_fail_with_value_error(self):
        for kind in (["content"], {"kind": "content"}):
            with self.subTest(kind=kind):
                state = with_reviews(fixture())
                state["reviews"][0]["kind"] = kind
                with self.assertRaises(ValueError):
                    helper.validate_state(state)
                with self.assertRaises(ValueError):
                    helper.fingerprint(self.state, "s1", kind)

    def test_selection_includes_direct_questions_without_importing_unrelated_evidence(self):
        self.state["slides"][1]["question_ids"] = ["q5"]
        selected = helper.select_state(self.state, ["s2"])["current"]
        self.assertIn("q5", selected["questions"])
        self.assertNotIn("e5", selected["evidence"])
        self.assertNotIn("src5", selected["sources"])

    def test_selection_filters_review_records_and_preserves_stale_declarations(self):
        state = with_reviews(self.state)
        for record in state["reviews"]:
            record["evidence_paths"] = [f"private/{record['scope']}-{record['kind']}.json"]
            record["reviewer_note"] = "Caller-supplied review evidence"
        state["slides"][0]["revision"] = "v2"
        before = copy.deepcopy(state)
        selected = helper.select_state(state, ["s1"])["current"]
        reviews = {(r["scope"], r["kind"]): r for r in selected["reviews"]}
        self.assertEqual({scope for scope, kind in reviews}, {"deck", "s1", "s2"})
        self.assertEqual(len(reviews), 12)
        stale = reviews[("s1", "content")]
        original = next(r for r in state["reviews"] if r["scope"] == "s1" and r["kind"] == "content")
        self.assertEqual({key: stale[key] for key in original}, original)
        self.assertEqual(stale["status"], "passed")
        self.assertEqual(stale["freshness"], "stale")
        self.assertEqual(stale["artifact"], "private-review-not-opened.json")
        self.assertEqual(stale["evidence_paths"], ["private/s1-content.json"])
        self.assertEqual(reviews[("deck", "content")]["freshness"], "stale")
        self.assertEqual(reviews[("s2", "rendered")]["freshness"], "current")
        stale["evidence_paths"].append("caller-mutated.json")
        self.assertEqual(state, before)

    def test_unchanged_snapshot_still_requires_full_review_including_hidden(self):
        report = helper.compare_states(self.state, self.state)
        self.assertFalse(report["changed"])
        self.assertEqual(report["affected_slides"], [])
        self.assertTrue(report["final_deck_review"]["required_before_delivery"])
        self.assertIn("s3", report["final_deck_review"]["slide_ids"])
        self.assertTrue(report["final_deck_review"]["includes_hidden"])


class CliTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / "analysis/local-only/test-temp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="task-state-", dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.source = self.folder / "state.json"
        self.source.write_text(json.dumps(fixture()), encoding="utf-8")
        self.original = self.source.read_bytes()

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/task_state.py"), *map(str, args)],
                              text=True, capture_output=True, cwd=ROOT, check=False)

    def test_validate_is_concise_and_detail_output_exposes_review_tokens(self):
        output = self.folder / "validation.json"
        result = self.run_cli("validate", self.source, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["slide_count"], 5)
        self.assertEqual(summary["hidden_slide_count"], 1)
        self.assertEqual(summary["review_counts"]["pending_checks"], 24)
        self.assertEqual(summary["details_path"], str(output))
        self.assertNotIn("fingerprints", summary)
        detail = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(len(detail["fingerprints"]["s2"]["rendered"]), 64)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_select_stdout_contains_targeted_payload_and_does_not_read_artifacts(self):
        result = self.run_cli("select", self.source, "--slides", "s1")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(set(report["current"]["sources"]), {"src1", "src2"})
        self.assertEqual(report["current"]["sources"]["src1"]["artifact"], "missing-private-1.pdf")
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_compare_stdout_is_concise_and_details_report_stale_checks(self):
        state = with_reviews(fixture())
        state["slides"][1]["revision"] = "v2"
        updated = self.folder / "new.json"
        updated.write_text(json.dumps(state), encoding="utf-8")
        before = updated.read_bytes()
        output = self.folder / "comparison.json"
        result = self.run_cli("compare", self.source, updated, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["affected_slide_count"], 4)
        self.assertGreater(summary["stale_review_count"], 0)
        self.assertEqual(summary["review_counts"]["current_declared_passed"], 13)
        self.assertEqual(summary["review_counts"]["pending_checks"], 11)
        self.assertNotIn("affected_slides", summary)
        self.assertEqual(len(json.loads(output.read_text())["affected_slides"]), 4)
        self.assertEqual(updated.read_bytes(), before)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_refuses_overwriting_input_or_existing_output(self):
        for destination in (self.source, self.folder / "already-exists.json"):
            if destination != self.source:
                destination.write_bytes(b"keep this output")
            before = destination.read_bytes()
            result = self.run_cli("validate", self.source, "--output", destination)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(destination.read_bytes(), before)
            self.assertEqual(self.source.read_bytes(), self.original)

    def test_unknown_reference_fails_before_creating_output(self):
        state = fixture()
        state["evidence"]["e1"]["source_ids"] = ["missing"]
        self.source.write_text(json.dumps(state), encoding="utf-8")
        output = self.folder / "invalid.json"
        result = self.run_cli("validate", self.source, "--output", output)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown references", result.stderr)
        self.assertFalse(output.exists())

    def test_duplicate_keys_nonfinite_values_and_large_inputs_rejected(self):
        for text in ('{"schema_version":1,"schema_version":1}',
                     json.dumps(fixture()).replace('"minutes": 12', '"minutes": NaN'),
                     " " * (helper.MAX_BYTES + 1)):
            self.source.write_text(text, encoding="utf-8")
            result = self.run_cli("validate", self.source)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
