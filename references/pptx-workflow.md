# PPTX analysis, design, transformation and validation

## Runtime and task workspace

Locate bundled runtimes with the desktop dependency tool. Use Python with `lxml`; Pillow adds raster pixel diagnostics. The preservation helper does not need Node or a presentation SDK. Rendering on Windows requires installed PowerPoint and may need scoped COM permission. Use another available renderer if necessary and state which one; an unavailable renderer means visual review remains pending.

Create small task-local `build/` and `outputs/` directories outside the reference corpus. Never copy the entire research corpus or install GitHub Desktop. Keep source immutable, retain its SHA-256 and use fresh output names. Keep research-bearing files out of version control by default.

## Understand before designing

Resolve context through the known profiles and current request. Obtain missing detail/purpose/expertise only where consequential. Inspect the actual PPTX using `palate_pptx.py inspect`, render and view every source page. Read source notes when needed. Inventory embedded workbooks, native tables/charts/equations, raster-only labels, fonts, image resolution, hidden pages and animation layers. Reuse unchanged render evidence only if its source hash matches.

For each slide record its purpose, scientific relationship, primary evidence, required caveats, source discrepancy, design problem and a justified operation. A transformation should improve reading order, hierarchy, spacing, evidence legibility or contextual explanation; a global teal recolor is insufficient. Match the request's redesign depth. When the whole deck already works, make targeted improvements rather than forcing uniform layouts.

Choose from the design system conditionally. Retain meaningful title part markers and section arrows. Keep scale/category mappings stable across comparisons. Do not turn technical audit pages into “minimal” slides without preserving checkable details. Palette examples are provisional; use same-content variants to learn exact preferences.

## Two implementation paths

**Preserve existing native objects.** Write a source-hash-bound JSON plan with native shape IDs, operation reasons and rule IDs. Use the conservative helper for placement, size, text styling, shape fill/line and background. It changes only explicitly selected parts and preserves the rest. Read [plan contract](transform-plan.md). A patcher rejection is actionable information, not a request to disable the guard.

**Author/rebuild or change content.** When requested quality needs different objects, slide decomposition, summaries, new native diagrams, recolored chart internals or a new deck, use the available presentations authoring workflow with JavaScript `@oai/artifact-tool`, or a verified native PowerPoint tool. Preserve source objects whenever the tool can do so reliably. For import/export inspect unsupported objects and compare fidelity; do not silently flatten them. Keep a content ledger and read [scientific fidelity](scientific-fidelity.md). The creation tool's own package/layout finalizer is required when that workflow supplies it; supplement with actual visual/semantic review. Do not use python-pptx as a lossy fallback.

For animation changes prefer native PowerPoint editing and verify playback. The conservative helper blocks animated pages to avoid incorrect final-state layout changes. Unchanged animation XML can be retained, but static export alone does not prove it plays correctly.

## Review and deliver

1. Run structural/content checks appropriate to the chosen path. For preservation, `validate` independently inventories content and checks all nonedited parts plus planned XML. For rebuilds, verify content ledger, labels/units/categories, equations, citations and native object presence, alongside tool validation.
2. Open/export the candidate in the actual rendering application. Inspect every final slide individually; compare every changed slide with source. Check text fit/wrap/clipping, aspect ratios, alignment, connectors, figure labels, chart axes/legend and reading order. Contact sheets supplement individual review.
3. Verify editability through native object inventories and application object inspection; test an editable copy if necessary. Distinguish native editable labels from labels inside retained images. Check workbook lineage and native formulas, not merely cached chart values.
4. Resolve visual/scientific defects and render changed slides again. Do not modify scientific data to make an automated layout diagnostic disappear. Report source contradictions explicitly.
5. Finalize a new PPTX and concise report, with source/output mapping, meaningful design reasons and checks/limitations. For preservation, the hash-bound `finalize` command handles copying/report generation. It does not replace actual review.

## Deliverables and updates

Return the editable deck and concise transformation report. State which checks were performed and any material limits. Keep source-specific evidence and detailed review artifacts local. When updating the Skill, review tracked content, run relevant tests, push only authorized branches and compare the remote SHA. Rebuild and reinstall the package explicitly when runtime files change.
