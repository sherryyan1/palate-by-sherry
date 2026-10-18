"""Read a reference section or complete selected rules without dumping the library."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def reference(name, root=ROOT):
    # Only maintained direct references, never arbitrary research/artifact paths.
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.(md|json)", name):
        raise ValueError("Use a reference basename, not a path")
    path = root / "references" / name
    if path.is_symlink() or not path.resolve().is_relative_to((root / "references").resolve()):
        raise ValueError("Linked reference outside the reference directory")
    return path.read_text(encoding="utf-8-sig")


def rule_query(ids=None, root=ROOT):
    library = json.loads(reference("design-decision-library.json", root))
    rules = {rule["id"]: rule for rule in library["rules"]}
    if len(rules) != len(library["rules"]):
        raise ValueError("Duplicate rule IDs")
    if ids is not None:
        unknown = set(ids) - rules.keys()
        if unknown:
            raise ValueError("Unknown rule IDs: " + ", ".join(sorted(unknown)))
    result = {key: value for key, value in library.items() if key != "rules"}
    result["mode"] = "complete_rules" if ids else "index_only"
    result["rules"] = ([rules[key] for key in dict.fromkeys(ids)] if ids else [
        {key: rule[key] for key in ("id", "name", "status", "trigger")}
        for rule in library["rules"]])
    result["notice"] = ("Selected rules are complete, including exceptions and validation."
                        if ids else "Index for selection only. Read complete applicable rules before acting.")
    return result


def headings(text):
    rows, fence = [], None
    for number, line in enumerate(text.splitlines(keepends=True)):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, tail = marker.groups()
            if fence is None:
                fence = (run[0], len(run))
            elif run[0] == fence[0] and len(run) >= fence[1] and not tail.strip():
                fence = None
            continue
        match = re.match(r"^(#{1,6})[ \t]+(.+?)\s*#*\s*$", line)
        if fence is None and match:
            rows.append({"line": number + 1, "level": len(match[1]), "heading": match[2]})
    return rows


def section_query(name, heading=None, root=ROOT):
    if not name.endswith(".md"):
        raise ValueError("Section queries require Markdown")
    text = reference(name, root)
    rows = headings(text)
    result = {"reference": name, "sha256": hashlib.sha256(text.encode()).hexdigest()}
    if heading is None:
        return {**result, "headings": rows}
    matches = [row for row in rows if row["heading"] == heading]
    if len(matches) != 1:
        raise ValueError("Heading must match exactly one listed heading")
    selected = matches[0]
    lines = text.splitlines(keepends=True)
    end = next((row["line"] - 1 for row in rows if row["line"] > selected["line"]
                and row["level"] <= selected["level"]), len(lines))
    first_section = next((row["line"] - 1 for row in rows if row["level"] >= 2), len(lines))
    # Keep the file's scope/preamble and ancestor introductions, not sibling sections.
    ancestors = []
    for row in rows:
        if row["line"] >= selected["line"]:
            break
        while ancestors and ancestors[-1]["level"] >= row["level"]:
            ancestors.pop()
        ancestors.append(row)
    ancestors = [row for row in ancestors if row["level"] < selected["level"]]
    context = [(0, min(first_section, selected["line"] - 1))]
    for row in ancestors:
        if row["level"] == 1:
            continue
        intro_end = next((r["line"] - 1 for r in rows if r["line"] > row["line"]), len(lines))
        context.append((row["line"] - 1, min(intro_end, selected["line"] - 1)))
    return {**result, "heading": heading,
            "context": "".join("".join(lines[start:stop]) for start, stop in context),
            "section": "".join(lines[selected["line"] - 1:end]),
            "notice": "Complete selected section and scope context; follow applicable linked safeguards. This is not a compliance check."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    rules = commands.add_parser("rules")
    rules.add_argument("--ids", nargs="+")
    sections = commands.add_parser("section")
    sections.add_argument("reference")
    sections.add_argument("--heading")
    args = parser.parse_args()
    try:
        result = rule_query(args.ids) if args.command == "rules" else section_query(args.reference, args.heading)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f"Reference query failed: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
