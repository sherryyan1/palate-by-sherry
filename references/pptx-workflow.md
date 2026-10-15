# PowerPoint object preservation and validation

Use this workflow to turn a compatible PPTX source into a separately reviewed editable output. It guides the agent from source inspection through implementation and delivery, keeping the design decision separate from the evidence that the resulting file is sound. The [implementation paths](#two-implementation-paths) distinguish bounded changes to existing objects from rewriting or rebuilding; the [review sequence](#review-and-deliver) applies to both.

## Runtime and task workspace

This adapter handles compatible PowerPoint `.pptx` sources. Begin with [presentation_route.py](../scripts/presentation_route.py) so the source format and requested delivery determine the file route. Keynote sources stay in the [native Keynote workflow](keynote-workflow.md) unless the user requests conversion. A user-selected PowerPoint export from Keynote may enter this workflow only after its conversion baseline has been reviewed. The preservation checks here apply to the PPTX itself; any application conversion needs its own comparison.

Locate bundled runtimes with the desktop dependency tool. Check the tools for the operation being attempted rather than treating a successful package inspection as proof that rendering is available:

| Operation | Required environment and limit |
| --- | --- |
| Preserve and inspect PPTX objects | Python with `lxml`; neither Node nor a presentation SDK is needed by the preservation helper. |
| Raster pixel diagnostics | Pillow, in addition to the preservation runtime. |
| Render with the included Windows helper | Installed PowerPoint; scoped COM permission may be needed. |
| Review through another native PowerPoint workflow | Access to the actual delivery application, with application/version and performed checks recorded. The Windows helper is not mandatory. |

If another available renderer is used during iteration, identify it in the review record. Its render does not establish PowerPoint compatibility; complete final appearance and object checks in the requested delivery application. If that application is unavailable, the corresponding checks remain pending and the output remains a candidate. This workflow does not require Windows when a suitable native PowerPoint workflow is available elsewhere.

Create small task-local `build/` and `outputs/` directories outside the reference corpus. Keep the source immutable and retain its SHA-256, because plans and render evidence must refer to the same baseline. Fresh output names preserve that baseline through each revision. Research-bearing files stay out of version control by default; never copy the entire research corpus or install GitHub Desktop for this workflow.

## Understand before designing

The brief determines which explanation belongs on the slide and which detail the audience can use. Resolve it through [guided intake](guided-intake.md), known profiles and the current request, skipping information already supplied. Ask about purpose or subject familiarity only when the answer affects the design. Users may delegate depth; before transformation, choose that depth from the source and resolved brief and record it in the plan context. Source inspection can proceed while required choices are pending.

Inspect the actual PPTX with `palate_pptx.py inspect`, then render and view every source page. Read notes where needed to understand the evidence and qualifications. The inventory must cover embedded workbooks, native tables, charts and equations, raster-only labels, fonts, image resolution, hidden pages and animation layers. Together, the object inventory and rendered slides show what can be changed safely and what the audience actually sees. Reuse unchanged render evidence only when its source hash matches.

Preserve the source language by default. For requested translation, complete the [scientific translation preflight](scientific-fidelity.md#scientific-translation) before rewriting, recording the target, terminology decisions and protected source content in the private content ledger. A ready intake brief does not resolve pending language questions.

For each slide, connect its purpose and scientific relationship to the primary evidence and required caveats. Record any source discrepancy before identifying the design problem and a justified operation. This order keeps the change accountable to the argument: it should improve reading order, hierarchy, spacing, evidence legibility or contextual explanation. A global teal recolor alone does not satisfy that requirement. Match the requested redesign depth, and make targeted improvements when the deck already works instead of forcing uniform layouts.

Choose from the design system according to the content. Meaningful title part markers and section arrows help listeners retain their place in the argument, while stable scale and category mappings make comparisons trustworthy. Technical audit pages still need their checkable detail after any simplification. Treat palette examples as provisional and use variants of the same content to learn exact preferences.

Before planning placement, record the symmetric work area and type roles from the [design system](design-system.md#03--use-space-and-typography-to-show-relationships). Inspect actual font use and effective sizes across slides, layouts, masters, tables and charts; theme names alone do not establish the visible typography. Apply the intended Fira title family explicitly where needed, preserve script and mathematical coverage, and review the 10.5 pt floor after text fitting. Define or adjust master guides through native authoring when needed; the conservative helper preserves masters. Its canvas-bound geometry guard does not check the smaller work area, and its direct-style inventory cannot certify inherited or image-interior text. Complete those checks through appropriate native inspection and rendered review.

Apply the [text-box and table defaults](design-system.md#text-boxes-and-tables) through native authoring when alignment or padding needs to change. The conservative helper cannot set those properties. Review vertical middle anchoring separately from horizontal alignment, keeping descriptive table text left and short entries, including numbers, centered unless explicitly instructed otherwise. Give substantial text a deliberate visual treatment while preserving its reasoning and qualifications, then check internal spacing and fit in PowerPoint.

When tables are present, resolve the [two-color comparison](design-system.md#table-color-options) using the same representative content before applying final table colors. Use native authoring for table fills, borders or numeric-display changes beyond the helper's contract. Follow [numeric display](scientific-fidelity.md#numeric-display), preserving underlying values and formulas while reviewing grouped quantities, consistent comparable precision and necessary exceptions.

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
2. Open/export the candidate in the actual rendering application and inspect every final slide individually. Compare every changed slide with its source, checking text fit, wrapping, clipping, aspect ratios, alignment, connectors, figure labels, chart axes and legends, and reading order. Check the intended fonts and the 10.5 pt minimum, including effective sizes after text fitting. Review [spacing](spacing-and-hierarchy.md) through visible gaps within and between groups, the symmetric work-area boundary and the association of evidence with its labels and qualifications. Confirm that only the bottom-right slide number sits outside the work area and that it is black on light slides or white on dark slides. Contact sheets can reveal deck-wide patterns, but supplement rather than replace individual review.
3. Establish editability with native object inventories and application object inspection, testing an editable copy where necessary. Distinguish native labels from labels inside retained images. Check workbook lineage and native formulas as well as the displayed chart values; cached values alone cannot establish those dependencies.
4. Repair visual or scientific defects and render the changed slides again. Keep source contradictions explicit, and never change scientific data to make an automated layout diagnostic disappear.
5. Finalize a new PPTX with a concise report of source/output mapping, meaningful design reasons, completed checks and limitations, including translation uncertainty or unrun checks when applicable. On the preservation path, the hash-bound `finalize` command copies the reviewed file and generates the report; the review itself must already have been performed.

## Deliverables and updates

Return the editable deck and concise transformation report with the checks actually performed and any material limits. Keep source-specific evidence and detailed review artifacts private within the authorized execution environment; follow the file-handling limits in [scientific fidelity](scientific-fidelity.md#review-record-and-delivery).

### When the Skill itself changes

Maintaining the Skill is a separate task from delivering a redesigned deck. Review tracked content and run relevant tests before sharing Skill changes. Push only an authorized branch and compare its remote SHA; rebuild and reinstall explicitly when runtime files change so Git, package and installed copy do not drift.
