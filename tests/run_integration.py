"""Exercise the preservation CLI on the two-slide synthetic SDK fixture.

Rendering/visual review/finalization are intentionally separate real review steps.
"""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("palate", ROOT / "scripts/palate_pptx.py")
palate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(palate)
source, task = Path(sys.argv[1]), Path(sys.argv[2])
analysis = palate.analyse(source)
if analysis["slide_count"] != 2 or not analysis["package_native_charts"] or not analysis["embedded_workbooks"]:
    raise ValueError("Expected synthetic fixture with two slides and embedded chart workbook")
def object_id(slide, name):
    return next(o["id"] for o in analysis["slides"][slide - 1]["shapes"] if o["name"] == name)
ops = []
def operation(slide, obj, action, reason, rules=None, **kwargs):
    ops.append(dict(slide=slide, shape_id=obj, action=action, reason=reason, rule_ids=rules or [], **kwargs))
for slide in (1, 2):
    operation(slide, object_id(slide, "title"), "text_style", "Strengthen title hierarchy using a provisional teal accent; keep conceptual part markers.", ["R008", "R009"], style={"font_size_pt": 24, "bold": True, "color": "217A80"})
operation(1, object_id(1, "Chart"), "geometry", "Give the native chart more readable space; retain all series, axes and the workbook.", bounds_inches=[0.4, 1.2, 5.4, 3.5])
operation(1, object_id(1, "explanation"), "geometry", "Separate evidence from its unchanged explanation and caveat.", ["R002"], bounds_inches=[6.05, 1.35, 3.4, 3.35])
operation(1, object_id(1, "explanation"), "text_style", "Increase explanation legibility without dropping qualifications.", style={"font_size_pt": 18, "color": "172B30"})
table = next(o for o in analysis["slides"][1]["shapes"] if o["native_table"])
operation(2, table["id"], "text_style", "Improve native table reading while keeping header emphasis, units and every cell.", style={"font_size_pt": 16, "color": "172B30"})
operation(2, object_id(2, "process-arrow"), "fill", "Use provisional teal for the editable data-flow arrow.", ["R008"], color="217A80")
operation(2, object_id(2, "process-arrow"), "line", "Keep a clean native connector outline without changing flow.", color="217A80", width_pt=0.5)
ops.append(dict(slide=2, action="background", color="FFFFFF", reason="Keep the native table and process on a neutral canvas.", rule_ids=[]))
plan = {"schema_version": 1, "source_sha256": analysis["source_sha256"],
        "context": {"profile": "internal-tutorial", "audience_expertise": "synthetic test: basic data interpretation", "detail_level": "synthetic test: concise with all six values visible", "purpose": "exercise editable chart/table/diagram preservation; not a user research talk"}, "operations": ops}
task.mkdir(parents=True, exist_ok=True)
palate.save_json(task / "plan.json", plan)
parts, _, _ = palate.expected_parts(source, plan)
palate.write_package(source, task / "candidate.pptx", parts)
result = palate.validate(source, task / "candidate.pptx", plan)
palate.save_json(task / "structural-check.json", result)
if result["status"] != "passed":
    raise ValueError(result["errors"])
print(json.dumps({"status": result["status"], "operations": len(ops), "visual_review": result["visual_review"]}))
