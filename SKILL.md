---
name: palate
description: "Polish research slides in Sherry's style from a short request, with guided choices for audience, time and depth. Use for PowerPoint and Keynote presentations, tutorials, research meetings, project briefings, seminars and talks. Preserve scientific evidence and native editability; route Keynote through verified interchange."
---

# palate by Sherry

*Good research deserves good taste.*

Deliver a new editable deck and a concise transformation report when redesign is requested. Respond in the user's requested language. Use **palate** consistently in prose and **palate by Sherry** for the full display name. Invoke the skill as `$palate`.

## Design judgment

Read the [design system](references/design-system.md) and relevant [decision rules](references/design-decision-library.json) before choosing a layout. Primary rules establish the style direction, while contextual rules offer ways to explain a particular scientific relationship. Evaluate those choices against the content and brief, preserving each rule's exceptions. Reference material can inform how evidence is organized without requiring adoption of its full brand palette.

Accept a short request such as “Use palate to polish my slides.” The brief should establish what listeners need to understand and inspect, because that determines the explanation and level of detail. Follow [guided intake](references/guided-intake.md) to collect missing context: begin with the setting, ask about the audience on the external branch, then resolve duration and depth. Reuse supplied fields and [context profiles](references/presentation-contexts.json), and let users delegate design choices. Preserve explicit constraints without inferring slide counts, Q&A allocations or subject familiarity. Single-page monthly updates are outside this workflow.

Follow the [writing style](references/writing-style.md) when drafting documentation, reports and explanatory prose. Develop continuous reasoning in connected sentences that explain a choice and its purpose. Use tables for discrete information that benefits from comparison, while keeping commands, ordered procedures and scientific qualifications exact.

## Execute

- **Route the source:** run [presentation_route.py](scripts/presentation_route.py) to identify the input and available path. Use the requested delivery application, or preserve the source application when unspecified; pass `--target keynote` for native Keynote delivery. For Keynote input or delivery, read the [Keynote workflow](references/keynote-workflow.md) and compare any conversion with the original before design. Inspect the actual container and runtime capability because `.key` can identify either a presentation or a credential; an extension alone is insufficient.
- **Existing editable deck:** follow the [object-preservation workflow](references/pptx-workflow.md) for PowerPoint sources and verified Keynote exports. Inspect structure and every rendered source slide. Select layouts from the scientific relationship, reading order and context. Use the conservative helper for existing-object placement and styling.
- **New or rebuilt slides:** use an available native presentation authoring workflow; with the installed presentations skill, use JavaScript `@oai/artifact-tool` and its finalizer. Keep a content ledger when summarizing, splitting slides or reconstructing figures. Never flatten a whole slide to conceal lost editability.
- **Reference-based adaptation:** follow [style adaptation](references/style-adaptation.md). Compare the same scientific content, record context and source identities privately, and apply only supported design choices. Do not copy accidental animation overlays or editing remnants.

## Protect the evidence

Read [scientific fidelity](references/scientific-fidelity.md) before changing content. Preserve conclusions, data, units, labels, legends, uncertainty, caveats, equations and references, keeping essential qualifications visible with their evidence. Supplementary detail can move to notes or an appendix when its location remains traceable and the main explanation retains its meaning. Retain complex source figures when reconstruction cannot be verified.

Review content, appearance and editability separately because a structurally intact file can still communicate the research incorrectly. Render and inspect every final slide in the delivery application, comparing changed slides with the source. Verify native text, tables, charts and diagrams remain editable; preserve chart workbooks and check fonts, equations, notes and hidden-slide behavior across conversion. Review changed animation states through playback. Finalize only after the appropriate reviews, including native Keynote inspection when that format is requested; an interchange-file check does not cover the later conversion.

## Runtime

Locate bundled runtimes with `load_workspace_dependencies` when available, then choose the tool for the operation below.

| Operation | Tool and requirements |
| :--- | :--- |
| Identify format and next step | [presentation_route.py](scripts/presentation_route.py); standard library, read-only. |
| Inspect, apply, validate or finalize preserved objects | [palate_pptx.py](scripts/palate_pptx.py); `lxml`, with Pillow for raster-resolution diagnostics. Follow the [plan contract](references/transform-plan.md). |
| Export Windows previews | [render_pptx.ps1](scripts/render_pptx.ps1); installed PowerPoint, opened read-only. |
| Import, save and review native Keynote delivery | Keynote on Mac; obtain local exports when that runtime is unavailable. |

The conservative helper preserves package parts and source content. Animation edits, nested-group geometry, table resizing, rewritten text and rebuilt evidence use the dedicated authoring path, with a content ledger and review. Stale hashes, stretched figures and existing output paths are rejected. Do not bypass a rejected operation by deleting evidence or disabling checks.

Keep research-bearing inputs, outputs, plans and review artifacts private. Skill invocation does not authorize uploading them. Use a new output file and state material limits that affect delivery.
