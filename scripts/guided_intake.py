"""Route short polish requests into context questions and a presentation brief.

This helper emits question payloads; Codex presents them with its available question tool.
It never opens UI, uploads data or treats a suggested/default option as a submitted answer.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "references/guided-intake.json").read_text(encoding="utf-8-sig"))
PROFILES = {p["id"]: p for p in json.loads((ROOT / "references/presentation-contexts.json").read_text(encoding="utf-8-sig"))["profiles"]}
AUDIENCES = {a["value"]: a for a in CONFIG["audiences"]}
FIELDS = {"scenario", "profile", "audience_type", "audience", "audience_expertise", "duration_minutes", "detail_level", "purpose", "slide_count", "q_and_a_minutes"}


def validate_answers(answers):
    if not isinstance(answers, dict) or set(answers) - FIELDS:
        raise ValueError("Unknown intake fields")
    for field in ("scenario", "profile", "audience_type", "audience", "audience_expertise", "detail_level", "purpose"):
        value = answers.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{field} must be nonempty text when supplied")
    if answers.get("profile") and answers["profile"] not in PROFILES:
        raise ValueError("Unknown presentation profile")
    if answers.get("scenario") and answers["scenario"] not in {"internal-tutorial", "internal-research", "external"}:
        raise ValueError("Unknown scenario; map a custom setting to the relevant presentation branch")
    for field in ("duration_minutes", "q_and_a_minutes"):
        value = answers.get(field)
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < (0 if field == "q_and_a_minutes" else 0.01) or value > 1440):
            raise ValueError(f"Invalid {field}")
    if answers.get("slide_count") is not None and (isinstance(answers["slide_count"], bool) or not isinstance(answers["slide_count"], int) or answers["slide_count"] <= 0):
        raise ValueError("Invalid slide_count")


def question(id, title, options):
    return {"id": id, "title": title, "options": options}


def pending(questions):
    return {"status": "needs_input", "can_inspect_source": True, "can_transform": False,
            "questions": questions,
            "request_user_input_async": {"questions": [{"title": q["title"], "options": [o["label"] for o in q["options"]]} for q in questions]}}


def route(answers):
    validate_answers(answers)
    answers = {k: v for k, v in answers.items() if v is not None}
    profile_id = answers.get("profile")
    if not profile_id and answers.get("scenario") in {"internal-tutorial", "internal-research"}:
        profile_id = answers["scenario"]
    profile = PROFILES.get(profile_id)
    if profile and profile["skill_scope"] != "current_research_presentation_skill":
        return {"status": "out_of_scope", "can_transform": False, "reason": "Single-page monthly updates are outside this multi-slide workflow."}
    scenario = answers.get("scenario")
    if profile:
        inferred = profile_id if profile["setting"] == "internal" else "external"
        if scenario and scenario != inferred:
            raise ValueError("Scenario conflicts with the explicit profile; resolve the correction first")
        scenario = inferred
    if not scenario:
        return pending([question("scenario", "Where will you present?", CONFIG["scenarios"])])
    audience_type = answers.get("audience_type")
    # Explicit audience content takes precedence. Profile expertise can skip an already known field.
    if not audience_type and profile and profile.get("audience_expertise"):
        audience_type = profile["audience_expertise"]
    audience = answers.get("audience")
    if scenario == "external" and not audience_type and not audience:
        return pending([question("audience_type", "Who is the external audience?", CONFIG["audiences"])])
    if audience_type and audience_type not in AUDIENCES and not audience:
        raise ValueError("Custom audience type requires an audience description")
    questions = []
    if "duration_minutes" not in answers:
        default = profile.get("duration_minutes") if profile else None
        values = list(CONFIG["duration_minutes"])
        if default is not None:
            values = [default] + [v for v in values if v != default]
        options = [{"value": value, "label": f"{value:g} minutes" + (" (profile default)" if value == default else "")} for value in values]
        questions.append(question("duration_minutes", "How many minutes do you have? You can also enter a custom duration.", options))
    if "detail_level" not in answers:
        questions.append(question("detail_level", "How much technical detail should the talk show?", CONFIG["depths"]))
    if questions:
        return pending(questions)
    context = {k: v for k, v in answers.items() if k in {"duration_minutes", "detail_level", "purpose", "slide_count", "q_and_a_minutes"}}
    if profile:
        context["profile"] = profile_id
    if profile:
        context["audience"] = profile["audience"]
        if profile.get("audience_expertise"):
            context["audience_expertise"] = profile["audience_expertise"]
    persona = AUDIENCES.get(audience_type)
    if persona:
        context["audience"] = persona["audience"]
        context["audience_expertise"] = persona["expertise"]
    if audience:
        context["audience"] = audience
    if answers.get("audience_expertise"):
        context["audience_expertise"] = answers["audience_expertise"]
    context.setdefault("audience", "research group")
    context.setdefault("purpose", "Polish the supplied research presentation for clarity and delivery.")
    context["setting"] = "external" if scenario == "external" else "internal"
    priorities = list(persona["priorities"]) if persona else [
        "Explain the learning objective and mechanism step by step." if scenario == "internal-tutorial" else
        "Support discussion of the research question, method and evidence."]
    return {"status": "ready", "can_inspect_source": True, "can_transform": True, "context": context,
            "design_priorities": priorities,
            "depth_delegated": context["detail_level"] == "automatic",
            "design_instruction": "Inspect the source before choosing layout, pacing and visible technical detail. Retain scientific evidence; do not derive slide count from minutes."}


def record(answers, field, value):
    if field not in {q["id"] for q in route(answers).get("questions", [])}:
        raise ValueError("Question is not currently pending")
    if field == "duration_minutes":
        if isinstance(value, bool):
            raise ValueError("Duration must be numeric")
        value = float(value)
    changed = dict(answers)
    changed[field] = value
    validate_answers(changed)
    return changed


def read_state(path):
    state = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if state.get("schema_version") != 1:
        raise ValueError("Unknown intake state schema")
    validate_answers(state.get("answers"))
    return state["answers"]


def save_state(path, answers):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump({"schema_version": 1, "answers": answers}, stream, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start"); p.add_argument("--output", required=True); p.add_argument("--known", help="JSON file containing already supplied intake fields")
    p = sub.add_parser("next"); p.add_argument("state")
    p = sub.add_parser("answer"); p.add_argument("state"); p.add_argument("--field", required=True); p.add_argument("--value", required=True); p.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "start":
        answers = json.loads(Path(args.known).read_text(encoding="utf-8-sig")) if args.known else {}
        validate_answers(answers); save_state(args.output, answers)
    else:
        answers = read_state(args.state)
        if args.command == "answer":
            answers = record(answers, args.field, args.value)
            save_state(args.output, answers)
    print(json.dumps(route(answers), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        parser_error = str(error)
        raise SystemExit(f"palate. intake: {parser_error}")
