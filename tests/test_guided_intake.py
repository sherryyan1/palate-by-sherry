"""Branching intake behavior, independent of a particular Codex UI layout."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
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
        self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "detail_level"])
        answers = guided.record(answers, "duration_minutes", "17.5")
        answers = guided.record(answers, "detail_level", "automatic")
        result = guided.route(answers)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["context"]["duration_minutes"], 17.5)
        self.assertEqual(result["context"]["audience_expertise"], "executive")
        self.assertTrue(result["depth_delegated"])
        self.assertNotIn("profile", result["context"])
        self.assertNotIn("slide_count", result["context"])

    def test_internal_skips_external_question_but_does_not_accept_defaults(self):
        result = guided.route({"scenario": "internal-tutorial"})
        self.assertEqual([q["id"] for q in result["questions"]], ["duration_minutes", "detail_level"])
        self.assertEqual(result["questions"][0]["options"][0]["value"], 10)
        self.assertFalse(result["can_transform"])
        self.assertNotIn("context", result)

    def test_prefilled_context_skips_questions_and_preserves_overrides(self):
        result = guided.route({"profile": "external-expert-seminar", "duration_minutes": 25, "detail_level": "explanatory", "purpose": "Compare two supplied methods"})
        self.assertEqual(result["status"], "ready")
        self.assertNotIn("questions", result)
        self.assertEqual(result["context"]["duration_minutes"], 25)
        self.assertEqual(result["context"]["purpose"], "Compare two supplied methods")

    def test_custom_mixed_audience_is_not_forced_into_a_persona(self):
        result = guided.route({"scenario": "external", "audience": "Mixed specialist and policy audience", "duration_minutes": 35, "detail_level": "overview"})
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["context"]["audience"], "Mixed specialist and policy audience")
        self.assertNotIn("audience_expertise", result["context"])

    def test_invalid_duration_and_out_of_scope_profile(self):
        for value in (0, -1, True, float("nan"), float("inf")):
            with self.assertRaises(ValueError): guided.route({"duration_minutes": value})
        self.assertEqual(guided.route({"profile": "internal-monthly-update"})["status"], "out_of_scope")

    def test_incompatible_profile_and_out_of_order_answer(self):
        with self.assertRaises(ValueError): guided.route({"profile": "internal-tutorial", "scenario": "external"})
        with self.assertRaises(ValueError): guided.record({}, "audience_type", "expert")


if __name__ == "__main__":
    unittest.main()
