---
name: palate-by-sherry
description: "Polish research slides in Sherry's style from a short request, with guided choices for audience, time and depth. Use for PowerPoint and Keynote presentations, tutorials, research meetings, project briefings, seminars and talks. Preserve scientific evidence and native editability; route Keynote through verified interchange."
---

# palate. by Sherry

*Good research deserves good taste.*

Deliver a new editable deck and a concise transformation report when redesign is requested. Respond in the user's requested language. Use **palate.** consistently in prose; retain **palate-by-sherry** for invocation and technical identifiers.

## Design judgment

Read the [design system](references/design-system.md) and relevant [decision rules](references/design-decision-library.json). Primary rules define the style direction; contextual rules are available composition choices, evaluated against the actual content and brief. Preserve their exceptions. A report or reference can inform visual organization without importing its entire brand palette.

Accept a short request such as “Use palate-by-sherry to polish my slides.” Follow [guided intake](references/guided-intake.md): use the available question tool for missing context, branch from setting to external audience, then collect duration and depth. Reuse [context profiles](references/presentation-contexts.json); skip supplied fields. Let users delegate depth and leave visual design to palate. Do not require a long prompt. Do not infer slide counts from duration, assume Q&A allocations or invent subject familiarity. Single-page monthly updates are outside this workflow.

## Execute

- **Route the source:** run [presentation_route.py](scripts/presentation_route.py) on the source. Use the requested delivery application, or preserve the source application when unspecified; pass `--target keynote` for native Keynote delivery. For Keynote input or delivery, read the [Keynote workflow](references/keynote-workflow.md). Inspect format and runtime capabilities; an extension alone does not establish a valid presentation. Preserve original files and compare conversions before design. A credential `.key` file must never be treated as a deck.
- **Existing editable deck:** follow the [object-preservation workflow](references/pptx-workflow.md) for PowerPoint sources and verified Keynote exports. Inspect structure and every rendered source slide. Select layouts from the scientific relationship, reading order and context. Use the conservative helper for existing-object placement and styling.
- **New or rebuilt slides:** use an available native presentation authoring workflow; with the installed presentations skill, use JavaScript `@oai/artifact-tool` and its finalizer. Keep a content ledger when summarizing, splitting slides or reconstructing figures. Never flatten a whole slide to conceal lost editability.
- **Reference-based adaptation:** follow [style adaptation](references/style-adaptation.md). Compare the same scientific content, record context and source identities privately, and apply only supported design choices. Do not copy accidental animation overlays or editing remnants.

## Protect the evidence

Read [scientific fidelity](references/scientific-fidelity.md) before changing content. Preserve conclusions, data, units, labels, legends, uncertainty, caveats, equations and references. Keep essential qualifications visible with their evidence. Trace supplementary detail to notes or an appendix. Retain complex source figures when reconstruction cannot be verified.

Render and inspect every final slide in the delivery application. Compare changed slides against the source. Verify native text, tables, charts and diagrams remain editable, preserve chart workbooks and review animation states separately when changed. Check fonts, equations, notes and hidden-slide behavior across conversion. Structural checks do not certify appearance or scientific interpretation. Finalize only after the appropriate content, visual and editability reviews; a reviewed interchange deck does not certify a native Keynote deliverable.

## Runtime

Locate bundled runtimes with `load_workspace_dependencies` when available. [presentation_route.py](scripts/presentation_route.py) is a read-only format/capability router with no external dependencies. The object-preservation helper requires `lxml`; Pillow provides raster-resolution diagnostics. [palate_pptx.py](scripts/palate_pptx.py) supplies `inspect`, `apply`, `validate` and `finalize`; read the [plan contract](references/transform-plan.md). [render_pptx.ps1](scripts/render_pptx.ps1) exports read-only PowerPoint previews on Windows. Native Keynote import, save and playback review require Keynote on Mac; obtain local exports when that runtime is unavailable.

The conservative helper preserves package parts and source content. Animation edits, nested-group geometry, table resizing, rewritten text and rebuilt evidence use the dedicated authoring path, with a content ledger and review. Stale hashes, stretched figures and existing output paths are rejected. Do not bypass a rejected operation by deleting evidence or disabling checks.

Keep research-bearing inputs, outputs, plans and review artifacts private. Skill invocation does not authorize uploading them. Use a new output file and state material limits that affect delivery.
