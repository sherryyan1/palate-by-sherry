"""Validate, select and compare private task-state snapshots without editing them.

This stdlib helper checks recorded dependencies, not scientific truth or external
files. Callers must refresh source and slide revisions before reusing a snapshot.
Review fingerprints bind declarations to state; they never establish a review pass.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys


MAX_BYTES = 8 * 1024 * 1024
MAX_SLIDES = 2_000
MAX_RECORDS = 10_000
KINDS = ("content", "editability", "rendered", "narrative")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}\Z")
REQUIRED = {"schema_version", "brief", "narrative", "design", "sources",
            "questions", "evidence", "slides"}


def _digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _object(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")


def _identity(value, label):
    if not isinstance(value, str) or not ID.fullmatch(value) or value == "deck":
        raise ValueError(f"Invalid {label}; use a stable ID other than 'deck'")


def _refs(record, key, targets, label):
    refs = record.get(key)
    if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
        raise ValueError(f"{label}.{key} must be an ID list")
    if len(refs) != len(set(refs)) or any(x not in targets for x in refs):
        raise ValueError(f"{label}.{key} contains duplicate or unknown references")


def validate_state(state):
    """Validate the v1 structure and every typed reference, returning the input."""
    pending = [(state, 0)]
    while pending:
        value, depth = pending.pop()
        if depth > 64:
            raise ValueError("State exceeds 64 levels of JSON nesting")
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                raise ValueError("JSON object keys must be strings")
            pending.extend((item, depth + 1) for item in value.values())
        elif isinstance(value, list):
            pending.extend((item, depth + 1) for item in value)
        elif value is not None and type(value) not in (str, int, float, bool):
            raise ValueError("State must contain JSON values")
    _object(state, "state")
    if (set(state) - REQUIRED - {"reviews"} or not REQUIRED <= set(state)
            or type(state["schema_version"]) is not int or state["schema_version"] != 1):
        raise ValueError("Expected the version-1 task-state fields")
    for name in ("brief", "narrative", "design", "sources", "questions", "evidence"):
        _object(state[name], name)
    if type(state["design"].get("approved")) is not bool:
        raise ValueError("design.approved must be boolean")
    for name in ("sources", "questions", "evidence"):
        if len(state[name]) > MAX_RECORDS:
            raise ValueError(f"Too many {name} records")
        for identity, record in state[name].items():
            _identity(identity, f"{name} ID")
            _object(record, f"{name}.{identity}")
            if name in ("sources", "evidence") and "coverage_complete" in record and type(record["coverage_complete"]) is not bool:
                raise ValueError(f"{name}.{identity}.coverage_complete must be boolean")
    for identity, source in state["sources"].items():
        _text(source.get("revision"), f"sources.{identity}.revision")
    for identity, question in state["questions"].items():
        _text(question.get("text"), f"questions.{identity}.text")
    for identity, evidence in state["evidence"].items():
        for key, target in (("source_ids", "sources"), ("question_ids", "questions")):
            _refs(evidence, key, state[target], f"evidence.{identity}")
    slides = state["slides"]
    if not isinstance(slides, list) or not 1 <= len(slides) <= MAX_SLIDES:
        raise ValueError("slides must contain between 1 and 2000 records")
    slide_ids = set()
    for slide in slides:
        _object(slide, "slide")
        _identity(slide.get("id"), "slide ID")
        if slide["id"] in slide_ids or type(slide.get("hidden")) is not bool:
            raise ValueError("Slide IDs must be unique and hidden must be boolean")
        slide_ids.add(slide["id"])
        _text(slide.get("revision"), f"slide {slide['id']} revision")
        for key, target in (("question_ids", "questions"), ("evidence_ids", "evidence")):
            _refs(slide, key, state[target], f"slide {slide['id']}")
    reviews = state.get("reviews", [])
    if not isinstance(reviews, list) or len(reviews) > (MAX_SLIDES + 1) * len(KINDS):
        raise ValueError("reviews must be a bounded list")
    reviewed = set()
    for record in reviews:
        _object(record, "review")
        scope, kind = record.get("scope"), record.get("kind")
        if not isinstance(scope, str) or scope not in slide_ids | {"deck"} or not isinstance(kind, str) or kind not in KINDS:
            raise ValueError("Review has an unknown scope or kind")
        if (scope, kind) in reviewed:
            raise ValueError("Duplicate review scope/kind")
        reviewed.add((scope, kind))
        if record.get("status") not in ("passed", "failed", "blocked"):
            raise ValueError("Review status must be passed, failed or blocked")
        token = record.get("fingerprint")
        if not isinstance(token, str) or not re.fullmatch(r"[0-9a-f]{64}", token):
            raise ValueError("Review fingerprint must be a lowercase SHA-256 digest")
    # Reject non-JSON objects, nonfinite numbers and excessive in-memory inputs too.
    try:
        raw = json.dumps(state, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, RecursionError) as error:
        raise ValueError("State must contain finite JSON values") from error
    if len(raw) > MAX_BYTES:
        raise ValueError("State exceeds the 8 MiB limit")
    return state


class _Index:
    def __init__(self, state):
        self.state = validate_state(state)
        self.slides = {s["id"]: s for s in state["slides"]}
        self.order = list(self.slides)
        self.positions = {identity: i for i, identity in enumerate(self.order)}
        self.tokens = {name: {key: _digest(value) for key, value in state[name].items()}
                       for name in ("sources", "questions", "evidence")}
        linked = self.dependencies(self.order)
        self.unscoped_questions = {key: self.tokens["questions"][key] for key in state["questions"]
                                   if key not in linked["questions"]}
        self.unscoped_evidence = {key: self.tokens["evidence"][key] for key, record in state["evidence"].items()
                                 if not record.get("coverage_complete", False) or key not in linked["evidence"]}
        incomplete_source_ids = {source for evidence in self.unscoped_evidence
                                 for source in state["evidence"][evidence]["source_ids"]}
        self.unscoped_sources = {key: self.tokens["sources"][key] for key, record in state["sources"].items()
                                if not record.get("coverage_complete", False) or key not in linked["sources"]
                                or key in incomplete_source_ids}
        self.global_token = _digest({name: state[name] for name in ("brief", "narrative", "design")} |
                                    {"order": self.order, "unscoped_sources": self.unscoped_sources,
                                     "unscoped_evidence": self.unscoped_evidence,
                                     "unscoped_questions": self.unscoped_questions})
        self.deck_token = _digest({k: v for k, v in state.items() if k != "reviews"})
        self.payloads = {identity: self._payload(identity) for identity in self.order}

    def neighbors(self, identity):
        if identity not in self.positions:
            return []
        i = self.positions[identity]
        neighbors = set(self.order[max(0, i - 1):i] + self.order[i + 1:i + 2])
        # Preserve actual adjacency and the visible talk sequence across hidden runs.
        for direction in (-1, 1):
            position = i + direction
            while 0 <= position < len(self.order):
                candidate = self.order[position]
                if not self.slides[candidate]["hidden"]:
                    neighbors.add(candidate)
                    break
                position += direction
        return [s for s in self.order if s in neighbors]

    def dependencies(self, identities):
        evidence = {e for s in identities for e in self.slides[s]["evidence_ids"]}
        questions = {q for s in identities for q in self.slides[s]["question_ids"]}
        questions.update(q for e in evidence for q in self.state["evidence"][e]["question_ids"])
        sources = {s for e in evidence for s in self.state["evidence"][e]["source_ids"]}
        return {"evidence": evidence, "questions": questions, "sources": sources}

    def _payload(self, identity):
        deps = self.dependencies([identity])
        return _digest({"slide": self.slides[identity], **{
            name: {key: self.tokens[name][key] for key in sorted(keys)}
            for name, keys in deps.items()}})

    def fingerprint(self, scope, kind):
        if (not isinstance(kind, str) or kind not in KINDS or not isinstance(scope, str)
                or scope not in self.slides and scope != "deck"):
            raise ValueError("Unknown review scope or kind")
        payload = {"scope": scope, "kind": kind, "global": self.global_token}
        if scope == "deck":
            payload["deck"] = self.deck_token
        else:
            payload["slide"] = self.payloads[scope]
            if kind == "narrative":
                payload["neighbors"] = [(s, self.payloads[s]) for s in self.neighbors(scope)]
        return _digest(payload)

    def reviews(self):
        return [{"scope": r["scope"], "kind": r["kind"], "declared_status": r["status"],
                 "freshness": "current" if r["fingerprint"] == self.fingerprint(r["scope"], r["kind"]) else "stale"}
                for r in self.state.get("reviews", [])]

    def review_counts(self):
        reviews = self.reviews()
        total = (len(self.order) + 1) * len(KINDS)
        current = [r for r in reviews if r["freshness"] == "current"]
        passed = sum(r["declared_status"] == "passed" for r in current)
        return {"current_declarations": len(current), "stale_declarations": len(reviews) - len(current),
                "missing_declarations": total - len(reviews), "current_declared_passed": passed,
                "pending_checks": total - passed}

    def coverage(self):
        return {"complete": not (self.unscoped_sources or self.unscoped_evidence or self.unscoped_questions),
                "unscoped_source_count": len(self.unscoped_sources),
                "unscoped_evidence_count": len(self.unscoped_evidence),
                "unscoped_question_count": len(self.unscoped_questions)}

    def final_review(self):
        return {"required_before_delivery": True, "slide_ids": self.order,
                "includes_hidden": True, "review_kinds": list(KINDS), "completed_by_helper": False}


def fingerprint(state, scope, kind):
    """Return a token for an actual review to record; this performs no review."""
    return _Index(state).fingerprint(scope, kind)


def state_report(state):
    index = _Index(state)
    return {"structurally_valid": True, "slide_count": len(index.order),
            "hidden_slide_count": sum(s["hidden"] for s in state["slides"]),
            "design_approved": state["design"]["approved"], "reviews": index.reviews(),
            "review_counts": index.review_counts(), "coverage": index.coverage(),
            "unscoped_source_ids": sorted(index.unscoped_sources),
            "unscoped_evidence_ids": sorted(index.unscoped_evidence),
            "unscoped_question_ids": sorted(index.unscoped_questions),
            "fingerprints": {scope: {kind: index.fingerprint(scope, kind) for kind in KINDS}
                             for scope in ["deck", *index.order]},
            "final_deck_review": index.final_review()}


def _selection(index, requested, context):
    selected = set(requested) & set(index.order)
    identities = [s for s in index.order if s in selected | context]
    deps = index.dependencies(identities)
    result = {"brief": index.state["brief"], "narrative": index.state["narrative"],
              "design": index.state["design"], "selected_slide_ids": [s for s in identities if s in selected],
              "coverage": index.coverage(),
              "context_slide_ids": [s for s in identities if s not in selected],
              "slides": [index.slides[s] for s in identities]}
    result.update({name: {key: index.state[name][key] for key in sorted(keys)}
                   for name, keys in deps.items()})
    result["fingerprints"] = {s: {kind: index.fingerprint(s, kind) for kind in KINDS} for s in identities}
    review_scopes = set(identities) | {"deck"}
    result["reviews"] = [{**record, "freshness": "current" if record["fingerprint"] ==
                          index.fingerprint(record["scope"], record["kind"]) else "stale"}
                         for record in index.state.get("reviews", []) if record["scope"] in review_scopes]
    return result


def select_state(state, slide_ids, previous=None):
    """Select requested IDs plus adjacent and visible neighbors in both snapshots."""
    current, old = _Index(state), _Index(previous) if previous is not None else None
    if not isinstance(slide_ids, (list, tuple)) or not slide_ids:
        raise ValueError("Select at least one slide ID")
    for identity in slide_ids:
        _identity(identity, "requested slide ID")
    if len(slide_ids) != len(set(slide_ids)):
        raise ValueError("Requested slide IDs must be unique")
    known = set(current.order) | (set(old.order) if old else set())
    if set(slide_ids) - known:
        raise ValueError("Requested slide IDs are absent from both snapshots")
    context = {n for index in (current, old) if index for s in slide_ids for n in index.neighbors(s)}
    result = {"requested_slide_ids": list(slide_ids), "current": _selection(current, slide_ids, context),
              "final_deck_review": current.final_review()}
    if old:
        result["previous"] = _selection(old, slide_ids, context)
    return copy.deepcopy(result)


def compare_states(previous, current):
    """Return conservative review invalidations, keeping hidden slides in scope."""
    old, new = _Index(previous), _Index(current)
    global_reasons = [f"{name} changed" for name in ("brief", "narrative", "design")
                      if _digest(previous[name]) != _digest(current[name])]
    if old.unscoped_sources != new.unscoped_sources:
        global_reasons.append("source coverage is incomplete or changed")
    if old.unscoped_evidence != new.unscoped_evidence:
        global_reasons.append("evidence coverage is incomplete or changed")
    if old.unscoped_questions != new.unscoped_questions:
        global_reasons.append("question coverage is incomplete or changed")
    if old.order != new.order:
        global_reasons.append("slide order or membership changed")
    changed = {name: {key for key in set(old.tokens[name]) | set(new.tokens[name])
                     if old.tokens[name].get(key) != new.tokens[name].get(key)}
               for name in ("sources", "questions", "evidence")}
    affected = []
    for identity in new.order:
        kinds = [kind for kind in KINDS if identity not in old.slides
                 or old.fingerprint(identity, kind) != new.fingerprint(identity, kind)]
        if not kinds:
            continue
        reasons = list(global_reasons)
        if identity not in old.slides:
            reasons.append("slide added")
        elif _digest(old.slides[identity]) != _digest(new.slides[identity]):
            reasons.append("slide record or revision changed")
        deps = new.dependencies([identity])
        old_deps = old.dependencies([identity]) if identity in old.slides else {}
        for name, keys in changed.items():
            relevant = keys & (deps[name] | old_deps.get(name, set()))
            if relevant:
                reasons.append(f"{name} changed: {', '.join(sorted(relevant))}")
        if kinds == ["narrative"] or not reasons:
            reasons.append("neighboring narrative context changed")
        affected.append({"slide_id": identity, "hidden": new.slides[identity]["hidden"],
                         "review_kinds": kinds, "reasons": reasons})
    return {"changed": old.deck_token != new.deck_token, "affected_slides": affected,
            "removed_slide_ids": [s for s in old.order if s not in new.slides],
            "reviews": new.reviews(), "review_counts": new.review_counts(), "coverage": new.coverage(),
            "final_deck_review": new.final_review()}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON keys are unsupported")
        result[key] = value
    return result


def _local_path(value):
    path = Path(value).expanduser()
    if ".." in path.parts or str(path).startswith(("\\\\", "//")) or path.drive and not path.is_absolute():
        raise ValueError("Use a local path without parent traversal")
    path = Path(os.path.abspath(path))
    if any(":" in p for p in path.parts if p != path.anchor):
        raise ValueError("Colon-bearing path components are unsupported")
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            raise ValueError("Symlink and reparse-point paths are unsupported")
    return path


def read_state(path):
    """Read only the explicitly supplied JSON file, never its artifact references."""
    path = _local_path(path)
    with path.open("rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise ValueError("Input must be a regular file within 8 MiB")
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Input exceeds 8 MiB")
    try:
        state = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    except (UnicodeError, RecursionError) as error:
        raise ValueError("Input must be bounded UTF-8 JSON") from error
    return validate_state(state)


def _write_new(path, report):
    path = _local_path(path)
    raw = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    return str(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "select", "compare"):
        command = commands.add_parser(name)
        if name == "compare":
            command.add_argument("previous")
        command.add_argument("state")
        command.add_argument("--output", help="Write details to a new JSON file; never overwrite")
        if name == "select":
            command.add_argument("--slides", nargs="+", required=True)
            command.add_argument("--previous")
    args = parser.parse_args(argv)
    try:
        state = read_state(args.state)
        if args.command == "validate":
            report = state_report(state)
            summary = {key: report[key] for key in ("structurally_valid", "slide_count", "hidden_slide_count", "design_approved")}
        elif args.command == "select":
            report = select_state(state, args.slides, read_state(args.previous) if args.previous else None)
            summary = {"selected_slide_ids": report["current"]["selected_slide_ids"],
                       "context_slide_ids": report["current"]["context_slide_ids"],
                       "coverage": report["current"]["coverage"]}
        else:
            report = compare_states(read_state(args.previous), state)
            summary = {"changed": report["changed"], "affected_slide_count": len(report["affected_slides"]),
                       "removed_slide_ids": report["removed_slide_ids"]}
        if args.command != "select":
            summary["stale_review_count"] = sum(r["freshness"] == "stale" for r in report["reviews"])
            summary["review_counts"] = report["review_counts"]
            summary["coverage"] = report["coverage"]
            summary["final_deck_review_required"] = True
        if args.output:
            summary["details_path"] = _write_new(args.output, report)
        print(json.dumps(report if args.command == "select" and not args.output else summary, ensure_ascii=False))
    except (ValueError, OSError) as error:
        print(f"task_state: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
