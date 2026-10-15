# Scientific fidelity and editability

Scientific fidelity depends on preserving the relationship between a claim, its evidence and the conditions under which it holds. Before editing, inventory every source slide, including hidden slides, speaker notes, charts and workbooks, tables, equations, images, references and animation. This baseline allows a later review to distinguish a source contradiction from a defect introduced during transformation. Flag uncertain units, legends or claims for the owner; never guess a correction.

## Preservation path

`palate_pptx.py` changes only the presentation styling and geometry explicitly named in the plan. Its comparisons cover source text and run order, equations, table grids, shape identities, relationships, hidden flags and timing. Every unmodified part must remain byte-identical, including media, charts, embedded workbooks, notes, layouts, masters and themes; changed slide XML must match the plan. These checks establish that the stored evidence survived the operation. A structural pass still leaves visual and scientific review pending, because unchanged content can become unreadable or misleading in a different arrangement.

A retained raster figure keeps its original content, while its interior labels remain part of the image. State that editability limit explicitly. Enlarging the figure adds no resolution, so prefer an original vector or high-resolution source, or a native reconstruction whose accuracy can be verified. Never invent missing pixels or report values read from a blurry plot as exact.

## Content-changing/rebuilding path

Summarizing text, splitting slides, reconstructing figures and recoloring chart internals can change what the evidence communicates. These operations sit outside the conservative patcher's contract and require an appropriate native authoring tool. Before authoring, create a task-local ledger that traces each changed slide from its source to the proposed output:

| Ledger field | Required record |
| --- | --- |
| Source identity | Original file hash, one-based slide and shape ID or figure/table/equation identity. |
| Scientific content | Source statement; all numbers, units, axes and legends; uncertainty and qualifications. |
| Destination | Output slide, object, notes or appendix, with the exact replacement statement. |
| Reason and interpretation | Why the change is needed and the support for any interpretation. Distinguish an owner's approved correction from an agent's proposal. |
| Editability and dependencies | Native editability before/after, workbook formulas, animation states and other relevant dependencies. |

Capture the full caption and source detail before shortening anything. Then compare the proposed wording with the source for meaning, negation, comparison baseline, conditions, correlation or causation, and uncertainty. Matching numeric tokens cannot establish fidelity: the same numbers may have been attached to different quantities. Essential uncertainty and conditions must remain near the evidence even when a long derivation moves to notes or an appendix. A formula may be replaced only by an explanation whose equivalence has been verified; an intuitive paraphrase alone is insufficient.

Reconstruction needs checks matched to the object being rebuilt:

| Object | Required preservation and review |
| --- | --- |
| Diagram | Check every label and directional connection. Use native shapes, text and connectors when editability is required. |
| Chart | Preserve all categories, series, errors and units, correct axis types and scales, and workbook lineage. Retain original workbook formulas when required; cached data are not equivalent. |
| Equation | Retain a math object or another verified editable equation representation. |

After authoring, use the available presentation finalizer to validate the package and independently compare the ledger with output text, chart data, equations, notes and references. Render and inspect every page to check how that content appears. The conservation validator enforces the preservation contract, so its failures cannot be ignored to approve a rebuild that follows a different contract.

## Review record and delivery

The review record must distinguish structural integrity, visual quality, scientific interpretation and editability, because evidence for one does not establish the others. Name the application that actually opened or rendered the output. “PowerPoint checked” or “Keynote checked” requires opening and inspecting the file in that application, and playback requires more than a static export. When conversion is involved, compare the converted file with the original separately, including chart data, formulas, equations, notes, fonts and build stages. Follow the [Keynote workflow](keynote-workflow.md) for that format.

For conservative output, use the hash-bound review record specified in the plan contract so the judgments apply to the exact candidate being delivered. The reviewer may be the agent; never invent human approval. Finalization requires every review status to pass and no unresolved issues. If a source scientific contradiction prevents certification, deliver only a clearly labeled candidate with the unresolved issue and do not assert that its content is scientifically correct.

Deliver a new editable deck with a concise account of the audience, time and depth, the source/output mapping, meaningful changes and their design basis, preserved evidence, checks performed and material limitations. Certify a requested native Keynote deliverable only after saving and reviewing it in Keynote; otherwise describe the remaining handoff. Detailed extracted content and validation artifacts stay local. Invoking the skill does not authorize research uploads.
