---
name: palate-by-sherry
description: "Polish multi-slide research PPTs in Sherry's style from a short request, with guided choices for audience, time and depth. Preserve scientific evidence and editable PPTX objects. Use for tutorials, research meetings, project briefings, seminars and talks."
---

# palate. by Sherry

*Good research deserves good taste.*

*Not just how it looks. How it thinks.*

Deliver an editable PPTX and a concise transformation report when redesign is requested. Respond in the user's requested language.

## Design judgment

Read the [design system](references/design-system.md) and relevant [decision rules](references/design-decision-library.json). Primary rules define the style direction; contextual rules are available composition choices, evaluated against the actual content and brief. Preserve their exceptions. A report or reference can inform visual organization without importing its entire brand palette.

Accept a short request such as “Use palate-by-sherry to polish my PPT.” Follow [guided intake](references/guided-intake.md): use the available question tool for missing context, branch from setting to external audience, then collect duration and depth. Reuse [context profiles](references/presentation-contexts.json); skip supplied fields. Let users delegate depth and leave visual design to Palate. Do not require a long prompt. Do not infer slide counts from duration, assume Q&A allocations or invent subject familiarity. Single-page monthly updates are outside this workflow.

## Execute

- **Existing deck:** follow the [PPTX workflow](references/pptx-workflow.md). Inspect structure and every rendered source slide. Select layouts from the scientific relationship, reading order and context. Use the conservative helper for existing-object placement and styling.
- **New or rebuilt slides:** use an available native presentation authoring workflow; with the installed presentations skill, use JavaScript `@oai/artifact-tool` and its finalizer. Keep a content ledger when summarizing, splitting slides or reconstructing figures. Never flatten a whole slide to conceal lost editability.
- **Reference-based adaptation:** follow [style adaptation](references/style-adaptation.md). Compare the same scientific content, record context and source identities privately, and apply only supported design choices. Do not copy accidental animation overlays or editing remnants.

## Protect the evidence

Read [scientific fidelity](references/scientific-fidelity.md) before changing content. Preserve conclusions, data, units, labels, legends, uncertainty, caveats, equations and references. Keep essential qualifications visible with their evidence. Trace supplementary detail to notes or an appendix. Retain complex source figures when reconstruction cannot be verified.

Render and inspect every final slide. Compare changed slides against the source. Verify native text, tables, charts and diagrams remain editable, preserve chart workbooks and review animation states separately when changed. Structural checks do not certify appearance or scientific interpretation. Finalize only after the appropriate content, visual and editability reviews.

## Runtime

Locate bundled runtimes with `load_workspace_dependencies` when available. Python requires `lxml`; Pillow provides raster-resolution diagnostics. [palate_pptx.py](scripts/palate_pptx.py) supplies `inspect`, `apply`, `validate` and `finalize`; read the [plan contract](references/transform-plan.md). [render_pptx.ps1](scripts/render_pptx.ps1) exports read-only PowerPoint previews on Windows.

The conservative helper preserves package parts and source content. Animation edits, nested-group geometry, table resizing, rewritten text and rebuilt evidence use the dedicated authoring path, with a content ledger and review. Stale hashes, stretched figures and existing output paths are rejected. Do not bypass a rejected operation by deleting evidence or disabling checks.

Keep research-bearing inputs, outputs, plans and review artifacts private. Skill invocation does not authorize uploading them. Use a new output file and state material limits that affect delivery.
