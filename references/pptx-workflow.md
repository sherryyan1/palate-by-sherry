# PowerPoint object preservation and validation

## Runtime and task workspace

This adapter handles PowerPoint sources and verified Keynote exports. Begin with [presentation_route.py](../scripts/presentation_route.py) so the source format and requested delivery determine the file route. When Keynote is involved, the [Keynote workflow](keynote-workflow.md) establishes the conversion baseline and the review needed after import. The preservation checks here apply to the PPTX itself; a later application conversion needs its own comparison.

Locate bundled runtimes with the desktop dependency tool. The preservation helper uses Python with `lxml` and needs neither Node nor a presentation SDK; Pillow adds raster pixel diagnostics. The included Windows renderer requires installed PowerPoint and may need scoped COM permission. If another available renderer is used, identify it in the review record. If rendering is unavailable, visual review remains pending.

Create small task-local `build/` and `outputs/` directories outside the reference corpus. Keep the source immutable and retain its SHA-256, because plans and render evidence must refer to the same baseline. Fresh output names preserve that baseline through each revision. Research-bearing files stay out of version control by default; never copy the entire research corpus or install GitHub Desktop for this workflow.

## Understand before designing

The brief determines which explanation belongs on the slide and which detail the audience can use. Resolve it through [guided intake](guided-intake.md), known profiles and the current request, skipping information already supplied. Ask about purpose or subject familiarity only when the answer affects the design. Users may delegate depth; before transformation, choose that depth from the source and resolved brief and record it in the plan context. Source inspection can proceed while required choices are pending.

Inspect the actual PPTX with `palate_pptx.py inspect`, then render and view every source page. Read notes where needed to understand the evidence and qualifications. The inventory must cover embedded workbooks, native tables, charts and equations, raster-only labels, fonts, image resolution, hidden pages and animation layers. Together, the object inventory and rendered slides show what can be changed safely and what the audience actually sees. Reuse unchanged render evidence only when its source hash matches.

Preserve the source language by default. For requested translation, complete the [scientific translation preflight](scientific-fidelity.md#scientific-translation) before rewriting, recording the target, terminology decisions and protected source content in the private content ledger. A ready intake brief does not resolve pending language questions.

For each slide, connect its purpose and scientific relationship to the primary evidence and required caveats. Record any source discrepancy before identifying the design problem and a justified operation. This order keeps the change accountable to the argument: it should improve reading order, hierarchy, spacing, evidence legibility or contextual explanation. A global teal recolor alone does not satisfy that requirement. Match the requested redesign depth, and make targeted improvements when the deck already works instead of forcing uniform layouts.

Choose from the design system according to the content. Meaningful title part markers and section arrows help listeners retain their place in the argument, while stable scale and category mappings make comparisons trustworthy. Technical audit pages still need their checkable detail after any simplification. Treat palette examples as provisional and use variants of the same content to learn exact preferences.

## Two implementation paths

Choose the implementation from the change the slide needs:

| Required change | Implementation | Binding conditions |
| --- | --- | --- |
| Placement, size, text styling, shape fill/line or background on existing native objects | Conservative helper | Use a source-hash-bound JSON plan with native shape IDs, reasons and rule IDs. Only explicitly selected parts change; the rest are preserved. Follow the [plan contract](transform-plan.md). |
| Translated or rewritten text, different objects, slide decomposition, summaries, new native diagrams, recolored chart internals or a new deck | Available presentations workflow with JavaScript `@oai/artifact-tool`, or a verified native PowerPoint tool | Keep a content ledger and follow [scientific fidelity](scientific-fidelity.md), including its translation preflight when applicable. Use the creation tool's package/layout finalizer when supplied, then complete visual and semantic review. |

A patcher rejection identifies a boundary that the chosen operation crosses; do not disable the guard to force it through. On the authoring path, retain source objects wherever the tool can preserve them reliably. Inspect unsupported objects during import/export and compare fidelity before accepting the result. Silent flattening and a lossy python-pptx fallback are not permitted.

Animation makes reading order depend on time as well as position. The conservative helper therefore blocks animated pages to avoid changing a layout without understanding its displayed states. Prefer native PowerPoint editing for animation changes and verify playback. Retaining unchanged animation XML preserves the stored instructions, but a static export cannot establish that they play correctly.

## Review and deliver

1. Establish structural and content integrity for the chosen path. For preservation, `validate` independently inventories content and checks all nonedited parts plus planned XML. For content changes and rebuilds, compare the content ledger, labels, units, categories, equations, citations and native object presence alongside the tool's validation. Translation additionally requires the source-to-output checks in [scientific fidelity](scientific-fidelity.md#scientific-translation); structural validation cannot establish scientific equivalence.
2. Open/export the candidate in the actual rendering application and inspect every final slide individually. Compare every changed slide with its source, checking text fit, wrapping, clipping, aspect ratios, alignment, connectors, figure labels, chart axes and legends, and reading order. Review [spacing](spacing-and-hierarchy.md) through visible gaps within and between groups, outer clearance and the association of evidence with its labels and qualifications. Contact sheets can reveal deck-wide patterns, but supplement rather than replace individual review.
3. Establish editability with native object inventories and application object inspection, testing an editable copy where necessary. Distinguish native labels from labels inside retained images. Check workbook lineage and native formulas as well as the displayed chart values; cached values alone cannot establish those dependencies.
4. Repair visual or scientific defects and render the changed slides again. Keep source contradictions explicit, and never change scientific data to make an automated layout diagnostic disappear.
5. Finalize a new PPTX with a concise report of source/output mapping, meaningful design reasons, completed checks and limitations, including translation uncertainty or unrun checks when applicable. On the preservation path, the hash-bound `finalize` command copies the reviewed file and generates the report; the review itself must already have been performed.

## Deliverables and updates

Return the editable deck and concise transformation report with the checks actually performed and any material limits. Keep source-specific evidence and detailed review artifacts local. When the skill itself changes, review tracked content and run relevant tests before sharing it. Push only an authorized branch and compare its remote SHA; rebuild and reinstall explicitly when runtime files change so Git, package and installed copy do not drift.
