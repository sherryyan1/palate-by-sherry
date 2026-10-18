"""Retrieve a bounded color recipe; selection does not recolor or validate a slide."""
import argparse
import json
from pathlib import Path
import re

LIBRARY = Path(__file__).resolve().parents[1] / "references/curated-palettes.json"


def load_library(path=LIBRARY):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    ids = set()
    for recipe in data["palettes"]:
        if recipe["id"] in ids:
            raise ValueError("Duplicate palette ID")
        ids.add(recipe["id"])
        if not recipe.get("tasks") or not recipe.get("colors"):
            raise ValueError("A recipe needs task semantics and colors")
        roles = set()
        for color in recipe["colors"]:
            if color["role"] in roles or not re.fullmatch(r"#[0-9A-F]{6}", color["hex"]):
                raise ValueError("Invalid color role or HEX")
            roles.add(color["role"])
        if not set(recipe.get("source_pages", {})) <= set(data["sources"]):
            raise ValueError("Unknown source")
    for source, pages in data["reference_page_index"].items():
        if source not in data["sources"]:
            raise ValueError("Unknown page-index source")
        for values in pages.values():
            if any(value not in ids for value in values if not value.startswith("reference ")):
                raise ValueError("Unknown page-index recipe")
    return data


def select(data, *, recipe_id=None, task=None, source=None, page=None, limit=3, listing=False):
    if not any((recipe_id, task, source, listing)):
        raise ValueError("Select an ID, task or source; use --list for a compact index")
    if not 1 <= limit <= 10:
        raise ValueError("Limit must be between 1 and 10")
    tasks = {task for recipe in data["palettes"] for task in recipe["tasks"]}
    if task and task not in tasks:
        raise ValueError("Unknown task; choose from: " + ", ".join(sorted(tasks)))
    if source and source not in data["sources"]:
        raise ValueError("Unknown source")
    if page is not None and (not source or page < 1):
        raise ValueError("A positive physical page/slide number requires --source")
    if recipe_id and recipe_id not in {r["id"] for r in data["palettes"]}:
        raise ValueError("Unknown palette ID")
    recipes = [r for r in data["palettes"] if
               (not recipe_id or r["id"] == recipe_id) and
               (not task or task in r["tasks"]) and
               (not source or source in r["source_pages"]) and
               (page is None or page in r["source_pages"].get(source, []))]
    if listing:
        return {"recipes": [{"id": r["id"], "name": r["name"], "tasks": r["tasks"]}
                            for r in recipes]}
    fields = ("id", "name", "status", "tasks", "colors", "source", "source_pages", "provenance",
              "verification", "best_for", "avoid", "notes")
    chosen = [{key: recipe[key] for key in fields if key in recipe}
              for recipe in recipes[:limit]]
    result = {"recipes": chosen, "more_ids": [r["id"] for r in recipes[limit:]]}
    if source and page is not None:
        index = data["reference_page_index"].get(source, {}).get(str(page), [])
        result["page_notes"] = [value for value in index if value.startswith("reference ")]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", dest="recipe_id")
    parser.add_argument("--task")
    parser.add_argument("--source")
    parser.add_argument("--page", type=int)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--list", dest="listing", action="store_true")
    args = parser.parse_args()
    try:
        result = select(load_library(), **vars(args))
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
