# Scientific fidelity and editability

Scientific fidelity depends on preserving the relationship between a claim, its evidence and the conditions under which it holds. This reference defines what the agent must preserve and what evidence is needed before an output can be called reviewed. Follow the [preservation path](#preservation-path) for bounded styling and geometry changes, or the [content-changing path](#content-changingrebuilding-path) for rewriting, translation and reconstruction. Both lead to a separate [review record and delivery](#review-record-and-delivery).

Before editing, inventory every source slide, including hidden slides, speaker notes, charts and workbooks, tables, equations, images, references and animation. This baseline allows a later review to distinguish a source contradiction from a defect introduced during transformation. Flag uncertain units, legends or claims for the owner; never guess a correction.

## Preservation path

`palate_pptx.py` changes only the presentation styling and geometry explicitly named in the plan. Its comparisons cover source text and run order, equations, table grids, shape identities, relationships, hidden flags and timing. Every unmodified part must remain byte-identical, including media, charts, embedded workbooks, notes, layouts, masters and themes; changed slide XML must match the plan. These checks establish that the stored evidence survived the operation. A structural pass still leaves visual and scientific review pending, because unchanged content can become unreadable or misleading in a different arrangement.

That package-preservation guarantee belongs to the PPTX helper. The [native Keynote adapter](keynote-workflow.md#native-adapter-contract) works through Keynote and compares the application inventory it can observe. Saving may re-encode a `.key` package, so neither unchanged bytes nor complete native-object fidelity can be inferred from a successful command. Inspect charts, formulas, equations, builds and other incompletely exposed objects directly in Keynote. The Mac implementation remains experimental and has not been tested on Mac in this development environment.

A retained raster figure keeps its original content, while its interior labels remain part of the image. State that editability limit explicitly. Enlarging the figure adds no resolution, so prefer an original vector or high-resolution source, or a native reconstruction whose accuracy can be verified. Never invent missing pixels or report values read from a blurry plot as exact.

## Content-changing/rebuilding path

Summarizing text, splitting slides, reconstructing figures and recoloring chart internals can change what the evidence communicates. These operations sit outside the conservative patcher's contract and require an appropriate native authoring tool.

Translation also follows this path, even when the layout is retained. Complete the [scientific translation preflight](#scientific-translation) before rewriting and use its source-to-output checks during review. The preservation helper cannot rewrite or translate text.

Before authoring, create a task-local ledger that traces each changed slide from its source to the proposed output:

| Ledger field | Required record |
| --- | --- |
| Source identity | Original file hash, one-based slide and shape ID or figure/table/equation identity. |
| Scientific content | Source statement and protected content: numbers, units, axes, legends, equations, quantitative relationships, uncertainty, assumptions, limitations, caveats, claim strength, references, citations and identifiers. |
| Destination | Output slide, object, notes or appendix, with the exact replacement statement. |
| Reason and interpretation | Why the change is needed and the support for any interpretation. Distinguish an owner's approved correction from an agent's proposal. |
| Editability and dependencies | Native editability before/after, workbook formulas, animation states and other relevant dependencies. |

For added schematics, record the source support for each meaningful component, label and connection, and distinguish explanatory illustration from observed evidence. For a split, map each source item to all relevant output slides, preserving reasoning order, essential qualifications, citations, notes and cross-references. Check the sequence as well as each individual slide so nothing is lost or detached from its claim.

For translation, keep the target language, established terminology glossary and source-backed or user-confirmed interpretation decisions with this same private ledger. Link decisions to the affected source and destination objects so a confirmed choice can be applied consistently without adding fields to the intake helper or conservative plan schema.

For [first-use abbreviation definitions and editorial changes](writing-style.md#research-slide-wording), record the verified full term, abbreviation and first audience-visible destination with the same ledger. Establish the definition from the source and research context; a material ambiguity needs clarification before that expansion is applied. An abbreviation inside a retained figure can be defined in an adjacent visible explanation without claiming its image text was edited. Review the actual reading order and relevant build stages so an earlier unexplained use is not hidden by a later definition.

Preserve attribution and the link between each reference and its supported statement when paraphrasing or restructuring. Keep source figure, table, equation and panel identities traceable. When deck-local numbering is needed, check its sequence and cross-references separately from the original source numbering; do not relabel a published figure as if its identity had changed. Clearer prose is not evidence of originality or a completed plagiarism check.

Capture the full caption and source detail before shortening anything. Then compare the proposed wording with the source for meaning, negation, comparison baseline, conditions, correlation or causation, and uncertainty. Matching numeric tokens cannot establish fidelity: the same numbers may have been attached to different quantities. Essential uncertainty and conditions must remain near the evidence even when a long derivation moves to notes or an appendix. A formula may be replaced only by an explanation whose equivalence has been verified; an intuitive paraphrase alone is insufficient.

Reconstruction needs checks matched to the object being rebuilt:

| Object | Required preservation and review |
| --- | --- |
| Diagram | Check every label and directional connection. Use native shapes, text and connectors when editability is required. |
| Chart | Preserve all categories, series, errors and units, correct axis types and scales, and workbook lineage. Retain original workbook formulas when required; cached data are not equivalent. |
| Equation | Retain a math object or another verified editable equation representation. |

After authoring, use the available presentation finalizer to validate the package and independently compare the ledger with output text, chart data, equations, notes and references. Render and inspect every page to check how that content appears. The conservation validator enforces the preservation contract, so its failures cannot be ignored to approve a rebuild that follows a different contract.

### Numeric display

Numeric formatting should make comparisons easier while preserving the source data, formulas and unrounded values. Treat the source value and its displayed string as separate records. Use native number formatting where the object supports it; when changing plain text, record the original string, numeric meaning, unit, chosen precision and replacement string in the private content ledger.

| Decision | Default | Exceptions and checks |
| :--- | :--- | :--- |
| Thousands grouping | Use comma separators when a quantity's integer part has four or more digits: `1000` becomes `1,000`, and `12345.67` becomes `12,345.67`. Preserve signs and the fractional part. | Keep years, dates, identifiers, reference numbers, codes, versions and mathematical notation intact. Four digits after a decimal point do not trigger integer grouping. Respect an explicitly required locale convention. |
| Decimal places | Use consistent decimal places for directly comparable values in the same table. One precision can serve a whole table of the same quantity and unit. | Mixed quantities or units can justify different precision by column or measurement. Keep counts integral and respect supported significant figures, measurement resolution and disciplinary conventions. |
| Small values and uncertainty | Retain signs, inequalities, uncertainty, interval bounds, significance marks and missing-value meanings. Choose coherent precision for an estimate and its interval where scientifically appropriate. | Never round a small nonzero value or p value to an apparent zero, invent a threshold, or hide a meaningful difference. Retain appropriate scientific notation or source-supported precision. |
| Rounding and trailing zeros | Base display precision on the source and the comparison the audience needs to make. | Preserve unrounded data; do not add zeros that imply unsupported measurement precision or change a conclusion, ordering or threshold interpretation. Record a justified exception when uniform decimals would mislead. |

Review displayed quantities across text, tables, chart labels and notes within the task scope. This is a semantic formatting decision, not a global text replacement. Text within a retained image cannot be reformatted automatically; use a verified reconstruction or retain and disclose the remaining formatting limit.

Changing a numeric string or a chart's display format follows the authoring path, because the bounded preservation helper keeps text and chart parts immutable. Compare source values and formulas separately from display strings, then inspect the actual output for units, rounding, missing values, interpretation and fit. Formatting consistency does not certify scientific equivalence.

### Unit labels

Use square brackets when a displayed quantity label explicitly carries a unit: `Capacity [MW]`, `Gain [%]` and `Temperature [°C]`. Apply this convention to table headers, chart axes and legends, and textual quantity labels within the editing scope. Ordinary inline values such as `25 MW` keep their natural form; do not invent brackets around every unit occurrence.

This is a delimiter choice, not a unit conversion. Preserve the unit symbol, case, exponent, scale factor, currency basis and denominator, along with the associated value and quantity. For example, replacing `Capacity (MW)` with `Capacity [MW]` does not authorize converting MW to GW or changing a label's scientific meaning. Do not apply a global parenthesis replacement: mathematical grouping, uncertainty and confidence intervals, citations, years and navigation markers such as `(1/3)` retain their intended notation.

Before changing a label, record its source identity, exact source and replacement strings, associated quantity and value, and unchanged unit meaning in the private content ledger. Compare the actual output with that record, then inspect fit and legibility in the delivery application. Label rewriting follows the native authoring path because the bounded preservation helper cannot rewrite text or chart interiors. Labels inside retained raster or complex figures require an available editable source or a reconstruction whose accuracy can be verified; otherwise retain the figure and report the remaining label-formatting limit. Never conceal that limit or infer that a structural check has reformatted the figure.

### Scientific translation

Translation changes the expression of the research, so establish the following before rewriting any source text:

1. **Establish the target language.** Preserve the source language unless the user explicitly requests a language change, regardless of the README or conversation language. Reuse a supplied target. If translation is requested but its target is unclear, ask which language the output should use and wait for the actual answer before rewriting; neither elapsed time nor a completed audience brief supplies that answer.
2. **Resolve scientific meaning before choosing wording.** Inspect the source wording and research context, including relevant notes, captions, labels and equations, before choosing scientific terms. Use established terminology and the source's definitions to resolve clear cases without questioning ordinary terms.

   When multiple plausible interpretations remain and the choice could materially change scientific meaning, briefly explain the alternatives and their difference, ask the user to choose or clarify, and wait for the answer before applying that term. Record the confirmed choice in the ledger and reuse it throughout the output. Do not invent a specialist translation or silently select an unresolved interpretation. Independent source inventory and layout analysis may continue while the answer is pending.
3. **Establish an editable authoring and review route.** Confirm that an available authoring path can produce and inspect the requested editable output. If the source cannot be read reliably or no supported authoring/application path is available, explain the limit and obtain a supported editable source or arrange the required application handoff. A translation draft or plan does not establish that a translated presentation has been authored and checked.

Before applying translated wording, record the source statements and protected content in the existing ledger. Preserve their scientific role as well as their surface form:

| Protected content | Source-to-output check |
| --- | --- |
| Values, units and mathematics | Preserve numerical values, signs, units, equations, mathematical notation and variable identifiers. Keep each value attached to the same quantity; preserve ratios, baselines, thresholds and other quantitative relationships. |
| Claims and qualifications | Preserve negation, comparison direction, uncertainty, assumptions, limitations and caveats. Retain the source's claim strength and distinction between association and causation; a tentative finding must not become a demonstrated conclusion. |
| Labels and terminology | Use the established glossary consistently across titles, text, tables, axes, legends, captions and notes within the translation scope. Keep translated labels attached to the same evidence, categories and scientific concepts. |
| References and identity | Preserve references, citation markers and identifiers, including their association with the supported claim. Translate surrounding explanation without substituting a different source or changing an identifier. |

After authoring, compare each translated source object with the actual output using the ledger, including notes and figure labels within scope. Check both extracted content and the rendered presentation: a preserved qualification can still be obscured by clipping or moved away from its evidence. Retained figures with untranslated interior labels need an explicit scope and editability limit; they must not be reported as fully translated figures.

Scientific equivalence requires agent or disciplinary review of the source and translation. Matching numeric tokens, package validation and the authoring finalizer cannot certify it automatically. Report the target language, material terminology decisions, source-to-output checks actually performed, unresolved scientific uncertainty and checks that remain unrun. Do not report a completed translation review when required clarification, authoring or application inspection is still pending; use the candidate and delivery limits below.

## Review record and delivery

The review record must distinguish structural integrity, visual quality, scientific interpretation and editability, because evidence for one does not establish the others. Name the application that actually opened or rendered the output. “PowerPoint checked” or “Keynote checked” requires opening and inspecting the file in that application, and playback requires more than a static export. Use each application's native path; Windows PowerPoint is not a prerequisite for Keynote. When the user requests conversion, compare the converted file with the original separately, including chart data, formulas, equations, notes, fonts and build stages. Follow the [Keynote workflow](keynote-workflow.md) for that format.

For bounded-helper output, use the hash-bound review record specified in that adapter's contract so the judgments apply to the exact candidate being delivered. The reviewer may be the agent; never invent human approval. Finalization requires every required review status to pass and no unresolved issues. If an essential content, editability or appearance check cannot be completed, identify what remains unresolved and treat any output as a clearly labeled candidate. Record playback as unrun when required application playback is unavailable; do not substitute a PDF or a package check. A source scientific contradiction also prevents certification; retain the unresolved issue and do not assert that the content is scientifically correct.

### Deliver the result and explain its limits

Deliver a new editable deck with a concise account of the audience, time, screen choice, target canvas and depth, the source/output mapping, meaningful changes and their design basis, preserved evidence, checks performed and material limitations. Certify a requested native Keynote deliverable only after saving and reviewing it in Keynote; otherwise describe the remaining handoff.

Keep detailed extracted content and validation artifacts private within the authorized execution environment. That environment may process files locally or in an authorized cloud workspace; do not imply that every task runs on the user's own computer. Invoking the Skill does not authorize publishing research or sending it to additional third-party services.
