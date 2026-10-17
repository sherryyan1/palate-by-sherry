# Conservative transformation contract

Use this contract after the [PPTX workflow](pptx-workflow.md#two-implementation-paths) has established that the requested changes fit the conservative helper. It applies a bounded set of changes to a known `.pptx` source, then checks that the result matches the plan. Native `.key` uses the separate [Keynote adapter contract](keynote-workflow.md#native-adapter-contract); its object identities and geometry units are different. Text rewriting, translation and reconstruction follow the appropriate authoring path instead.

The sequence is inspect, plan, apply, independently validate, then review and finalize. A successful command establishes its own part of that sequence; it does not establish scientific interpretation, visual quality or editability on its own. The sections below define the [plan fields](#plan-json) and the separate [review record](#review-and-finalization).

Run the commands with the verified Python interpreter for this session, reusing a bundled runtime when available; `python` below stands for that path. On Windows, quote absolute paths so file selection is unambiguous. Plans, inspections and receipts can contain research, so keep them in the private task build directory.

```text
python scripts/palate_pptx.py inspect input.pptx --output build/inspection.json
python scripts/palate_pptx.py apply input.pptx --plan build/plan.json --output build/candidate.pptx --receipt build/check.json
python scripts/palate_pptx.py validate input.pptx build/candidate.pptx --plan build/plan.json --receipt build/recheck.json
```

Begin with `inspect` to identify the actual objects that a plan can address. It resolves slide order through relationships and reports stable native shape IDs, hidden and animated slides, chart/workbook parts, text, notes, direct styles and local bounds. Image resolution is included when Pillow is available. Read the rendered slides alongside this inventory: the helper neither resolves every inherited style nor interprets scientific meaning.

The helper's numeric and geometry limits describe supported operations, not the full design standard. Record and review the [symmetric work area and type hierarchy](design-system.md#03--use-space-and-typography-to-show-relationships) separately: all foreground content belongs inside the work area except the bottom-right slide number, displayed text must be at least 10.5 pt, and section navigation labels must be at least 12 pt. These are native point sizes, not CSS pixels. Fractional point sizes are supported. The helper does not identify navigation roles or audit effective fonts, automatic text fitting, chart-interior labels or text inside images. Its `font_family` operation assigns one family to Latin, East Asian and complex-script declarations, so use native authoring when a target needs distinct script fonts or meaningful mixed styles.

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
| Venue screen | New intake includes `screen_aspect_ratio`: `4:3`, `16:9` or `not_sure`. The helper retains this optional field for older plan compatibility. A specified ratio must match the source canvas within rounding tolerance; otherwise use [native canvas reflow](pptx-workflow.md#match-the-venue-screen). `not_sure` keeps the source canvas and is not a guessed venue ratio. |
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
| Canvas size or new visual objects | Use native authoring to change the slide ratio or add icons, tables and diagrams. This helper preserves the source canvas and object identities; a matching ratio in context does not mean the helper resized the deck. |
| Text styling | Do not change math-bearing objects. Uniform styling must preserve meaningful emphasis. |
| Vertical anchoring, paragraph alignment, table-cell alignment or padding | Use native authoring; these are not supported `text_style` fields. Place any section navigation bar above the slide title; vertically center its labels with consistent internal insets. Top-anchor other non-title text boxes and compare corresponding first-line positions across slides. Preserve title-layout anchoring and the table-cell middle default. Follow the [text-box and table guidance](design-system.md#text-boxes-and-tables), then inspect native properties and the rendered result. |
| Numeric display, individual table-cell fills/borders or changing corner geometry | Use native authoring. Thousands separators and decimal formatting can change text or chart parts; follow [numeric display](scientific-fidelity.md#numeric-display) and preserve source values and formulas separately. A fill or line operation can restyle a supported existing shape but cannot rebuild its geometry or set individual table-cell fills/borders. Supported uniform table-text styling remains available. |
| Missing logos or watermarks, master/layout edits, layout reassignment or inherited-graphics display settings | Use the [native PowerPoint branding workflow](pptx-workflow.md#restore-consistent-branding-through-masters-and-layouts). Inspect the actual inheritance and intended exceptions before repairing the shared structure. This helper cannot add marks or change masters, layouts, relationships or display overrides. |
| Unit-label delimiters | Use native authoring for label text changes under [scientific fidelity](scientific-fidelity.md). `text_style` cannot replace parentheses with square brackets or rewrite chart, table or image labels. |

Within this contract, text, image bytes and crops, chart data and style parts, workbook formulas, captions, notes, equations, layouts, masters and relationships are immutable. That boundary makes preservation verifiable. The helper cannot translate or rewrite text; `text_style` cannot carry replacement wording. Translation, summarizing, splitting, rebuilding and chart-internal styling require the authoring path and private content ledger described in [scientific fidelity](scientific-fidelity.md), including its [translation preflight and review](scientific-fidelity.md#scientific-translation) when applicable. Keep language and glossary decisions in that ledger rather than extending this plan schema.

## Review and finalization

Render both source and candidate in the delivery application. For PowerPoint, the included `render_pptx.ps1` provides a Windows route: it uses a new directory, opens the deck read-only and leaves unrelated decks open. An available native PowerPoint workflow on another platform can supply the review instead; Windows and this script are not universal requirements. Record the application/version and actual evidence. If the delivery application is unavailable, its appearance and editability checks remain pending, regardless of another renderer's output.

Inspect every output slide individually, including hidden slides, because a layout defect may occur outside the visible presentation sequence. A selected-slide render is useful while iterating, but cannot establish complete delivery review. For requested cross-format delivery, the PPTX finalizer establishes only this contract; separately save and review the converted deliverable in its target application.

Only after reviewing the actual candidate, create the task-local review JSON. Its hash and slide coverage connect the recorded judgments to the file that will be delivered:

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
