# Conservative transformation contract

The conservative helper applies a bounded set of changes to a known source, then checks that the result matches the plan. Run it with the actual bundled Python executable; `python` below stands for that path. On Windows, quote absolute paths so file selection is unambiguous. Plans, inspections and receipts can contain research, so keep them in the private task build directory.

```text
python scripts/palate_pptx.py inspect input.pptx --output build/inspection.json
python scripts/palate_pptx.py apply input.pptx --plan build/plan.json --output build/candidate.pptx --receipt build/check.json
python scripts/palate_pptx.py validate input.pptx build/candidate.pptx --plan build/plan.json --receipt build/recheck.json
```

Begin with `inspect` to identify the actual objects that a plan can address. It resolves slide order through relationships and reports stable native shape IDs, hidden and animated slides, chart/workbook parts, text, notes, direct styles and local bounds. Image resolution is included when Pillow is available. Read the rendered slides alongside this inventory: the helper neither resolves every inherited style nor interprets scientific meaning.

## Plan JSON

Create the plan from the inspected objects and resolved user context. The IDs below are illustrative and must be replaced with identities from the actual source. The full current source hash binds the plan to that file; a different revision needs a new inspection and plan. Use the following conventions consistently:

| Value | Contract |
| --- | --- |
| Source SHA | Full hash of the current source. |
| Color | Hex code without `#`. |
| Geometry | Inches, regardless of the original canvas dimensions; output geometry must stay inside the actual slide size. |
| Typography | Points. |

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

Resolve the context before applying the plan. Profiles provide missing context while explicit requests retain precedence; the following conditions remain binding:

| Context condition | Required handling |
| --- | --- |
| Named profile | Fill audience class and duration only when absent. Apply specific request overrides. |
| Custom context | Supply explicit `audience`, positive `duration_minutes`, `detail_level` and `purpose`. |
| Known default | Omit the field when the default should apply; do not pass null. |
| Monthly update | Reject it as outside this skill's scope. |
| Test detail or purpose | Treat it as a test assumption, never as a learned user preference. |

Each operation must identify `slide` and `action`, give a nonempty `reason`, and supply `rule_ids`; use an empty list for engineering or task-specific choices. `shape_id` is required for every action except `background`. Reports retain primary or contextual rule IDs beside each change so the design basis stays visible. The supported actions are:

| Action | Fields | Scope |
| --- | --- | --- |
| geometry | bounds_inches | Place native objects; resize text/chart frames; preserve image proportions |
| text_style | style | Font size, family, color and bold on native text/table cells |
| fill | color | Native shape fill without protected scientific encoding |
| line | color, width_pt | Native line styling; retain arrowheads and dashes |
| background | color | Per-slide background; retain source masters |

The action limits determine when the plan must move to a native authoring workflow:

| Operation or object | Boundary |
| --- | --- |
| Geometry | Use `[x, y, width, height]` in inches. |
| Group/inherited geometry or animated slides | Use the native authoring path. |
| Table geometry | Placement only. |
| Text styling | Do not change math-bearing objects. Uniform styling must preserve meaningful emphasis. |

Within this contract, text, image bytes and crops, chart data and style parts, workbook formulas, captions, notes, equations, layouts, masters and relationships are immutable. That boundary makes preservation verifiable. The helper cannot translate or rewrite text; `text_style` cannot carry replacement wording. Translation, summarizing, splitting, rebuilding and chart-internal styling require the authoring path and private content ledger described in [scientific fidelity](scientific-fidelity.md), including its [translation preflight and review](scientific-fidelity.md#scientific-translation) when applicable. Keep language and glossary decisions in that ledger rather than extending this plan schema.

## Review and finalization

Render both source and candidate with `render_pptx.ps1` on Windows PowerPoint. The renderer uses a new directory, opens the deck read-only and leaves unrelated decks open. Inspect every output slide individually, including hidden slides, because a layout defect may occur outside the visible presentation sequence. A selected-slide render is useful while iterating, but cannot establish complete delivery review.

Only after reviewing the actual candidate, create the task-local review JSON:

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

Replace the example slide numbers and evidence with the slides and checks actually reviewed. Never copy a pass status into an unreviewed candidate. Resolve a source contradiction or failed visual check before certification; otherwise label the output as a candidate with unresolved issues. Once review is complete, `finalize` checks the plan again, binds the review to the candidate hash and requires coverage of every slide. It emits a separate final deck, a concise mapping report and a validation receipt:

```text
python scripts/palate_pptx.py finalize input.pptx build/candidate.pptx --plan build/plan.json --review build/review.json --output outputs/redesigned.pptx --report outputs/transformation-report.md
```

The finalizer verifies that the review record satisfies the contract; it cannot independently prove the reviewer's judgments. Every command refuses existing outputs and receipts, so use fresh revision filenames throughout. Original decks are never overwritten.
