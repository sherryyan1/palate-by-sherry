# Scientific fidelity and editability

Before editing, inventory every source slide, including hidden slides, speaker notes, charts/workbooks, tables, equations, images, references and animation. Distinguish a source contradiction from a transformation defect. Flag uncertain units/legends/claims for the owner; never guess corrections.

## Preservation path

`palate_pptx.py` changes only explicitly planned presentation styling/geometry. It compares source text/run order, equations, table grids, shape identities, relationships, hidden flags and timing. Every unmodified part, including media, charts, embedded workbooks, notes, layouts, masters and themes, must remain byte-identical. Changed slide XML must match the plan; a structural pass has visual/scientific review pending.

Retaining a raster figure preserves its content but does not make interior labels editable. State this distinction. Enlarging it does not add resolution. Prefer original vector/high-resolution data or verified native reconstruction; do not invent missing pixels or read values from a blurry plot as if exact.

## Content-changing/rebuilding path

The conservative patcher intentionally cannot summarize text, split slides, reconstruct figures or recolor chart internals. Perform these with a native authoring tool when appropriate. Before authoring, create a task-local content ledger for each changed slide:

- Original file hash, one-based slide, shape ID/figure/table/equation identity.
- Source scientific statement and all numbers/units/axes/legends, uncertainty and qualifications.
- New location: output slide/object/notes/appendix and exact replacement statement.
- Change reason, any interpretation and its support; distinguish an owner's approved correction from an agent's proposal.
- Native editability before/after, dependencies such as workbook formulas and animation states.

Capture full caption/source detail before shortening. Review meaning, negation, comparison baseline, conditions, correlation/causation and uncertainty manually against the source. Numeric token matching alone is insufficient: identical numbers can be assigned to the wrong quantity. Keep essential uncertainty/conditions near the evidence, even if long derivations move elsewhere. Do not replace a formula with an unverified intuitive paraphrase.

For reconstructed diagrams, check each label and directional connection. Use native shapes/text/connectors when editability is required. For charts preserve full categories/series/errors/units, correct axis types/scales and workbook lineage. Preserve original workbook formulas when required; a cached-data snapshot is not equivalent. Native equations should remain math objects or another verified editable equation representation.

Validate the authored package with the available presentation finalizer and independently compare the ledger against output text, chart data, equations, notes and references. Render and inspect every page. Do not run the conservation validator on a rebuild and then ignore its failures; it enforces a different contract.

## Review record and delivery

Structural integrity, visual quality, scientific interpretation and editability are separate checks. Record which application rendered/opened the output. “PowerPoint checked” requires an actual PowerPoint open/inspection; static export does not establish animation playback.

For conservative output, provide a hash-bound review record as documented in the plan contract. The reviewer can be the agent; never invent human approval. Finalization requires all review statuses passed and no unresolved issues. If a source scientific contradiction prevents certification, deliver only a clearly labeled candidate plus the unresolved issue; do not assert the content is scientifically correct.

Deliver a new editable PPTX and a concise report: audience/time/depth, source/output mapping, meaningful changes and decision basis, preserved evidence, checks actually performed and material limitations. Keep detailed extracted content and validation artifacts local. No research uploads are implied by Skill invocation.
