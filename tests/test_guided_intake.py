"""Branching intake behavior, independent of a particular Codex UI layout."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / "analysis/local-only/test-temp"
TEST_TEMP.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("guided", ROOT / "scripts/guided_intake.py")
guided = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guided)


class GuidedIntakeTests(unittest.TestCase):
    def test_short_prompt_starts_with_all_setting_choices(self):
        result = guided.route({})
        self.assertEqual(result["status"], "needs_input")
        self.assertFalse(result["can_transform"])
        self.assertTrue(result["can_inspect_source"])
        self.assertEqual([q["id"] for q in result["questions"]], ["scenario"])
        self.assertEqual(len(result["request_user_input_async"]["questions"][0]["options"]), 3)

    def test_external_branches_to_audience_before_time(self):
        result = guided.route({"scenario": "external"})
        self.assertEqual([q["id"] for q in result["questions"]], ["audience_type"])
        self.assertEqual({a["value"] for a in result["questions"][0]["options"]}, {"expert", "executive", "general"})

    def test_executive_route_supports_custom_time_and_delegated_depth(self):
        answers = guided.record({}, "scenario", "external")
        answers = guided.record(answers, "audience_type", "executive")
        result = guided.route(answers)
        self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "screen_aspect_ratio", "detail_level"])
        answers = guided.record(answers, "duration_minutes", "17.5")
        answers = guided.record(answers, "screen_aspect_ratio", "4:3")
        answers = guided.record(answers, "detail_level", "automatic")
        result = guided.route(answers)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["context"]["duration_minutes"], 17.5)
        self.assertEqual(result["context"]["screen_aspect_ratio"], "4:3")
        self.assertEqual(result["context"]["audience_expertise"], "executive")
        self.assertTrue(result["depth_delegated"])
        self.assertNotIn("profile", result["context"])
        self.assertNotIn("slide_count", result["context"])

    def test_internal_skips_external_question_but_does_not_accept_defaults(self):
        result = guided.route({"scenario": "internal-tutorial"})
        self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "screen_aspect_ratio", "detail_level"])
        self.assertEqual(result["questions"][0]["options"][0]["value"], 10)
        self.assertEqual([o["value"] for o in result["questions"][1]["options"]], ["16:9", "4:3", "not_sure"])
        self.assertFalse(result["can_transform"])
        self.assertNotIn("context", result)

    def test_prefilled_context_skips_questions_and_preserves_overrides(self):
        result = guided.route({"profile": "external-expert-seminar", "duration_minutes": 25, "screen_aspect_ratio": "16 x 9", "detail_level": "explanatory", "purpose": "Compare two supplied methods"})
        self.assertEqual(result["status"], "ready")
        self.assertNotIn("questions", result)
        self.assertEqual(result["context"]["duration_minutes"], 25)
        self.assertEqual(result["context"]["purpose"], "Compare two supplied methods")
        self.assertEqual(result["context"]["screen_aspect_ratio"], "16:9")

    def test_custom_mixed_audience_is_not_forced_into_a_persona(self):
        result = guided.route({"scenario": "external", "audience": "Mixed specialist and policy audience", "duration_minutes": 35, "screen_aspect_ratio": "4:3", "detail_level": "overview"})
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["context"]["audience"], "Mixed specialist and policy audience")
        self.assertNotIn("audience_expertise", result["context"])

    def test_unknown_screen_is_an_explicit_answer_without_a_ratio_assumption(self):
        answers = {"scenario": "internal-research", "duration_minutes": 60, "detail_level": "automatic"}
        pending = guided.route(answers)
        self.assertEqual([q["id"] for q in pending["questions"]], ["screen_aspect_ratio"])
        self.assertFalse(pending["can_transform"])
        answers = guided.record(answers, "screen_aspect_ratio", "Not sure")
        self.assertEqual(answers["screen_aspect_ratio"], "not_sure")
        result = guided.route(answers)
        self.assertEqual(result["status"], "ready")
        self.assertTrue(result["can_transform"])
        self.assertEqual(result["context"]["screen_aspect_ratio"], "not_sure")
        self.assertNotIn("questions", result)

    def test_supplied_screen_does_not_skip_other_questions(self):
        result = guided.route({"scenario": "internal-research", "screen_aspect_ratio": "4 / 3"})
        self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "detail_level"])
        self.assertFalse(result["can_transform"])

    def test_ratios_normalize_but_unsupported_or_mistyped_values_are_rejected(self):
        for submitted, expected in (("16 : 9", "16:9"), ("4 × 3", "4:3"), ("16：9", "16:9"), ("UNKNOWN", "not_sure")):
            with self.subTest(submitted=submitted):
                self.assertEqual(guided.normalize_answers({"screen_aspect_ratio": submitted})["screen_aspect_ratio"], expected)
        for value in ("", "16:10", "automatic", True, 16 / 9, ["4:3"]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                guided.route({"screen_aspect_ratio": value})
        result = guided.route({"scenario": "internal-research", "duration_minutes": 60, "detail_level": "automatic", "screen_aspect_ratio": None})
        self.assertEqual([q["id"] for q in result["questions"]], ["screen_aspect_ratio"])

    def test_legacy_state_asks_for_screen_and_preserves_existing_answers(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            legacy = Path(temp) / "legacy.json"
            original = {"scenario": "internal-research", "duration_minutes": 60, "detail_level": "technical"}
            legacy.write_text(json.dumps({"schema_version": 1, "answers": original}), encoding="utf-8")
            restored = guided.read_state(legacy)
            self.assertEqual(restored, original)
            self.assertEqual([q["id"] for q in guided.route(restored)["questions"]], ["screen_aspect_ratio"])
            revised = guided.record(restored, "screen_aspect_ratio", "16 x 9")
            output = Path(temp) / "revised.json"
            guided.save_state(output, revised)
            self.assertEqual(guided.read_state(output), {**original, "screen_aspect_ratio": "16:9"})
            self.assertEqual(guided.route(guided.read_state(output))["status"], "ready")
            self.assertEqual(json.loads(legacy.read_text(encoding="utf-8"))["answers"], original)

    def test_known_cli_persists_canonical_screen_and_skips_its_question(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            known, state = Path(temp) / "known.json", Path(temp) / "state.json"
            known.write_text(json.dumps({"scenario": "internal-tutorial", "screen_aspect_ratio": "4 x 3"}), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "scripts/guided_intake.py"), "start", "--known", str(known), "--output", str(state)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "detail_level"])
            self.assertEqual(json.loads(state.read_text(encoding="utf-8"))["answers"]["screen_aspect_ratio"], "4:3")

    def test_invalid_known_screen_does_not_create_a_state(self):
        with tempfile.TemporaryDirectory(dir=TEST_TEMP) as temp:
            known, state = Path(temp) / "known.json", Path(temp) / "state.json"
            known.write_text(json.dumps({"screen_aspect_ratio": "16:10"}), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "scripts/guided_intake.py"), "start", "--known", str(known), "--output", str(state)], capture_output=True, text=True)
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("Unsupported screen_aspect_ratio", process.stderr)
            self.assertFalse(state.exists())

    def test_invalid_duration_and_out_of_scope_profile(self):
        for value in (0, -1, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError): guided.route({"duration_minutes": value})
        self.assertEqual(guided.route({"profile": "internal-monthly-update"})["status"], "out_of_scope")

    def test_incompatible_profile_and_out_of_order_answer(self):
        with self.assertRaises(ValueError): guided.route({"profile": "internal-tutorial", "scenario": "external"})
        with self.assertRaises(ValueError): guided.record({}, "audience_type", "expert")


if __name__ == "__main__":
    unittest.main()
