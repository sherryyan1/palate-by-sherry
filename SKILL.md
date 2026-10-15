---
name: palate
description: "Polish research slides in Sherry's style from a short request, with guided choices for audience, time and depth. Use for PowerPoint and Keynote presentations, tutorials, research meetings, project briefings, seminars and talks. Preserve scientific evidence and native editability with application-specific workflows."
---

# palate by Sherry

*Good research deserves good taste.*

Deliver a new editable deck and a concise transformation report when redesign is requested. Respond in the user's requested conversation language. Use **palate** consistently in prose and **palate by Sherry** for the full display name. Invoke the skill as `$palate`.

## Design judgment

Use [communication design](references/communication-design.md) to identify what the audience needs to understand, organize the explanation and make its reasoning visible. README navigation, icon choices and heading syntax do not prescribe slide layouts. Read the [design system](references/design-system.md) and relevant [decision rules](references/design-decision-library.json) before choosing a layout. Primary rules establish the style direction, while contextual rules offer ways to explain a particular scientific relationship. Evaluate those choices against the content and brief, preserving each rule's exceptions. Reference material can inform how evidence is organized without requiring adoption of its full brand palette.

Treat [spacing and hierarchy](references/spacing-and-hierarchy.md) as part of the explanation. Define a symmetric work area before placing content, keeping all foreground content inside it except the bottom-right slide number. Follow the [type hierarchy](references/design-system.md#03--use-space-and-typography-to-show-relationships): Fira Sans titles, a 10.5 pt minimum, usually 12 pt body text and 16 pt prominent subheadings. Establish groups and reading order before choosing gaps, then judge type scale, visible edges and outer margins together in the final render. Keep evidence associated with its labels and qualifications, and adapt spacing to the actual canvas and viewing conditions.

Accept a short request such as “Use palate to polish my slides.” The brief should establish what listeners need to understand and inspect, because that determines the explanation and level of detail. Follow [guided intake](references/guided-intake.md) to collect missing context: begin with the setting, ask about the audience on the external branch, then resolve duration and depth. Reuse supplied fields and [context profiles](references/presentation-contexts.json), and let users delegate design choices. Preserve explicit constraints without inferring slide counts, Q&A allocations or subject familiarity. Single-page monthly updates are outside this workflow.

Follow the [writing style](references/writing-style.md) when drafting documentation, reports and explanatory prose. Develop continuous reasoning in connected sentences that explain a choice and its purpose. Use tables for discrete information that benefits from comparison, while keeping commands, ordered procedures and scientific qualifications exact.

Keep README language, conversation language and presentation language independent. Preserve the source presentation language unless the user requests a change. All README versions use this one English execution standard.

## Execute

- **Route the source:** run [presentation_route.py](scripts/presentation_route.py) to identify the input and available path. Preserve the source application unless the user requests another delivery application. PowerPoint uses its native workflow; Keynote uses the [native Keynote workflow](references/keynote-workflow.md) on Mac without a PowerPoint conversion. Inspect the actual container and probe application access because `.key` can identify either a presentation or a credential, and an installed application does not establish automation permission. If the required runtime is unavailable, keep that native route pending and explain the available handoff or ask whether the user wants a different format. Do not silently substitute a conversion.
- **Resolve requested translation:** complete the [scientific translation preflight](references/scientific-fidelity.md#scientific-translation) before rewriting. An unclear target or a remaining term ambiguity that could materially change scientific meaning requires an actual user answer. Record language, terminology decisions and protected source content in the private content ledger.
- **Existing editable deck:** follow the [PowerPoint object-preservation workflow](references/pptx-workflow.md) for `.pptx` and the [Keynote workflow](references/keynote-workflow.md) for `.key`. Inspect structure and every rendered source slide. Select layouts from the scientific relationship, reading order and context. Each bounded helper has its own operation and identity contract; use a native authoring path for changes beyond that contract.
- **New or rebuilt slides:** use an available authoring workflow for the chosen application. For PowerPoint authoring with the installed presentations skill, use JavaScript `@oai/artifact-tool` and its finalizer; for Keynote, use available native Keynote authoring or controlled application editing. The bundled Keynote adapter only adjusts supported existing objects and does not translate text or rebuild evidence. Keep a content ledger when translating, summarizing, splitting slides or reconstructing figures, and complete the source-to-output review in [scientific fidelity](references/scientific-fidelity.md). Never flatten a whole slide to conceal lost editability.
- **Reference-based adaptation:** follow [style adaptation](references/style-adaptation.md). Compare the same scientific content, record context and source identities privately, and apply only supported design choices. Do not copy accidental animation overlays or editing remnants.

## Protect the evidence

Read [scientific fidelity](references/scientific-fidelity.md) before changing content. Preserve conclusions, data, units, labels, legends, uncertainty, caveats, equations and references, keeping essential qualifications visible with their evidence. Supplementary detail can move to notes or an appendix when its location remains traceable and the main explanation retains its meaning. Retain complex source figures when reconstruction cannot be verified.

Review content, appearance and editability separately because a structurally intact file can still communicate the research incorrectly. Render and inspect every final slide in the delivery application, comparing changed slides with the source. Verify native text, tables, charts and diagrams remain editable; preserve chart data and formulas, and check fonts, equations, notes and hidden-slide behavior. Review animation and media through playback where present. Finalize only after the appropriate application reviews; PowerPoint review does not establish Keynote behavior, and Keynote review does not establish PowerPoint behavior. A cross-format delivery needs a separate conversion comparison. If an essential check cannot be completed, identify the limitation and treat any output as a candidate, with no claim that the unsupported review was performed.

## Runtime

Locate bundled runtimes with `load_workspace_dependencies` when available, then choose the tool for the operation below.

| Operation | Tool and requirements |
| :--- | :--- |
| Identify format and next step | [presentation_route.py](scripts/presentation_route.py); standard library, read-only. |
| Inspect, apply, validate or finalize preserved objects | [palate_pptx.py](scripts/palate_pptx.py); `lxml`, with Pillow for raster-resolution diagnostics. Follow the [plan contract](references/transform-plan.md). |
| Export PowerPoint previews with the provided Windows helper | [render_pptx.ps1](scripts/render_pptx.ps1); installed Windows PowerPoint, opened read-only. Other available native PowerPoint workflows can perform the application review without this script. |
| Inspect, adjust supported objects, export and save native Keynote candidates | [keynote_native.py](scripts/keynote_native.py) with [keynote_native.js](scripts/keynote_native.js); macOS, Keynote and automation access. Experimental implementation, not yet tested on Mac. Follow the [native Keynote contract](references/keynote-workflow.md#native-adapter-contract). |

The PPTX conservative helper preserves package parts and source content; it cannot translate or rewrite text. The native Keynote adapter checks the application inventory it can observe and does not establish byte-identical package preservation or complete chart/equation fidelity. Animation edits, nested-group geometry, table resizing, changed text and rebuilt evidence use the appropriate native authoring path, with a content ledger and review. Follow each helper's source-hash, operation and output guards. Do not bypass a rejected operation by deleting evidence or disabling checks.

Keep research-bearing inputs, outputs, plans and review artifacts private within the user's authorized execution environment, which may be local or cloud-based. Do not publish them or transfer them to additional third-party services without explicit authorization. Use a new output file and state material limits that affect delivery.
