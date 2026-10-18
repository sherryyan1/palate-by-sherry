"""Retrieve a bounded color recipe; selection does not recolor or validate a slide."""
import argparse
import json
from pathlib import Path
import re

LIBRARY = Path(__file__).resolve().parents[1] / "references/curated-palettes.json"
RECIPE_FIELDS = {"id", "name", "tasks", "colors", "best_for", "avoid"}


def load_library(path=LIBRARY):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if set(data) != {"schema_version", "palettes"} or data["schema_version"] != 2:
        raise ValueError("Expected a color-and-usage-only library (schema 2)")
    ids = set()
    for recipe in data["palettes"]:
        if not set(recipe) <= RECIPE_FIELDS or not {"id", "name", "tasks", "colors", "best_for"} <= set(recipe):
            raise ValueError("A recipe may contain only color and usage fields")
        if recipe["id"] in ids:
            raise ValueError("Duplicate palette ID")
        ids.add(recipe["id"])
        if not recipe.get("tasks") or not recipe.get("colors"):
            raise ValueError("A recipe needs task semantics and colors")
        roles = set()
        for color in recipe["colors"]:
            if set(color) != {"role", "hex"} or color["role"] in roles or not re.fullmatch(r"#[0-9A-F]{6}", color["hex"]):
                raise ValueError("Invalid color role or HEX")
            roles.add(color["role"])
    return data


def select(data, *, recipe_id=None, task=None, limit=3, listing=False):
    if not any((recipe_id, task, listing)):
        raise ValueError("Select an ID or task; use --list for a compact index")
    if not 1 <= limit <= 10:
        raise ValueError("Limit must be between 1 and 10")
    tasks = {task for recipe in data["palettes"] for task in recipe["tasks"]}
    if task and task not in tasks:
        raise ValueError("Unknown task; choose from: " + ", ".join(sorted(tasks)))
    if recipe_id and recipe_id not in {r["id"] for r in data["palettes"]}:
        raise ValueError("Unknown palette ID")
    recipes = [r for r in data["palettes"] if
               (not recipe_id or r["id"] == recipe_id) and
               (not task or task in r["tasks"])]
    if listing:
        return {"recipes": [{"id": r["id"], "name": r["name"], "tasks": r["tasks"]}
                            for r in recipes]}
    fields = ("id", "name", "tasks", "colors", "best_for", "avoid")
    chosen = [{key: recipe[key] for key in fields if key in recipe}
              for recipe in recipes[:limit]]
    return {"recipes": chosen, "more_ids": [r["id"] for r in recipes[limit:]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", dest="recipe_id")
    parser.add_argument("--task")
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
