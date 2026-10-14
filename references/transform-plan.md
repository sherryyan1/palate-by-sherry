# Conservative transformation contract

Run the scripts with the actual bundled Python path; below, `python` stands for that executable. Use quoted absolute paths on Windows. Plans, inspections and receipts contain research and stay in the private task build directory.

```text
python scripts/palate_pptx.py inspect input.pptx --output build/inspection.json
python scripts/palate_pptx.py apply input.pptx --plan build/plan.json --output build/candidate.pptx --receipt build/check.json
python scripts/palate_pptx.py validate input.pptx build/candidate.pptx --plan build/plan.json --receipt build/recheck.json
```

`inspect` resolves slide order through relationships, reports stable native shape IDs, hidden/animated slides, chart/workbook parts, text, notes, direct styles, local bounds and image resolution when Pillow is available. It does not resolve all inherited styles or interpret scientific meaning. Read rendered slides alongside it.

## Plan JSON

Create the plan from actual inspected objects and the user context, not the illustrative IDs below. Source SHA is the full hash of the current source. Color codes omit `#`; geometry uses inches regardless of original canvas dimensions; typography uses points. Keep output geometry inside the actual slide size.

```json
{
  "schema_version": 1,
  "source_sha256": "FULL_CURRENT_SOURCE_SHA256",
  "context": {
    "profile": "internal-tutorial",
    "audience_expertise": "as supplied by the user",
    "detail_level": "as supplied by the user",
    "purpose": "as supplied by the user"
  },
  "operations": [
    {
      "slide": 1,
      "shape_id": 2,
      "action": "text_style",
      "style": {"font_size_pt": 28, "bold": true, "color": "217A80"},
      "rule_ids": ["R008"],
      "reason": "Give the existing title clear hierarchy with a provisional teal accent."
    },
    {
      "slide": 1,
      "shape_id": 3,
      "action": "geometry",
      "bounds_inches": [0.5, 1.2, 5.8, 3.4],
      "rule_ids": [],
      "reason": "Separate the existing figure from the explanation without stretching it."
    }
  ]
}
```

Named profiles fill audience class and duration only when absent. Custom contexts need explicit `audience`, positive `duration_minutes`, `detail_level`, `purpose`. Do not pass null for a known default. Specific request overrides apply. Monthly update is rejected as outside this Skill's scope. Detail/purpose values in a test are test assumptions, not learned user preferences.

Every operation needs `slide`, `action`, nonempty `reason`, `rule_ids` (empty for engineering/task-specific choices). `shape_id` is required except background. Reports identify primary or contextual rule IDs alongside each change. Supported actions:

| Action | Fields | Scope |
| --- | --- | --- |
| geometry | bounds_inches | Place native objects; resize text/chart frames; preserve image proportions |
| text_style | style | Font size, family, color and bold on native text/table cells |
| fill | color | Native shape fill without protected scientific encoding |
| line | color, width_pt | Native line styling; retain arrowheads and dashes |
| background | color | Per-slide background; retain source masters |

Geometry is `[x, y, width, height]` in inches. Group/inherited geometry and animated slides use the native authoring path. Table geometry supports placement only. Text styling does not change math-bearing objects; uniform styling must preserve meaningful emphasis.

Text, image bytes/crops, chart data/style parts, workbook formulas, captions, notes, equations, layouts/masters and relationships are immutable on this path. Summarizing, splitting, rebuilding and chart-internal styling use the authoring path in [scientific fidelity](scientific-fidelity.md).

## Review and finalization

Render the source and candidate using `render_pptx.ps1` on Windows PowerPoint. It uses a new directory, opens read-only and does not close unrelated decks. All output slides, including hidden ones, need individual inspection. A partial selected-slide render is useful for iteration but not complete delivery review.

Create a task-local review JSON only after actually reviewing it:

```json
{
  "candidate_sha256": "HASH_OF_REVIEWED_CANDIDATE",
  "reviewed_slides": [1, 2],
  "visual_status": "passed",
  "scientific_status": "passed",
  "editability_status": "passed",
  "reviewer": "Codex (or actual reviewer name)",
  "remaining_issues": [],
  "evidence": ["actual before/after render paths and checks"]
}
```

Record real slide numbers and actual evidence; do not copy an example pass status into an unreviewed candidate. A source contradiction or a failed visual check must be resolved or kept as an explicitly unreviewed candidate. `finalize` checks the plan again, binds review to the candidate hash, requires every slide reviewed and emits a separate final plus a concise mapping report and validation receipt:

```text
python scripts/palate_pptx.py finalize input.pptx build/candidate.pptx --plan build/plan.json --review build/review.json --output outputs/redesigned.pptx --report outputs/transformation-report.md
```

It does not independently prove the reviewer's judgments. All commands refuse existing outputs and receipts; use new revision filenames. Original decks are never overwritten.
