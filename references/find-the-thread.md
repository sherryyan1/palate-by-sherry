# Find the thread

A research presentation needs an argument that listeners can follow, question and remember. This capability develops that argument before slide-level writing and visual construction. It owns whole-deck diagnosis, the relationship between neighboring slides, research-question-to-result mapping and title strategy. [Distill the message](distill-the-message.md) refines the selected explanation; [Refine the visuals](refine-the-visuals.md) makes it visible. Neither should compensate for a missing scientific connection.

## Diagnose the story before rearranging it

Read the complete material with the resolved [audience brief](read-the-room.md). For an existing deck, inspect its bodies, notes, figures, hidden slides and rendered pages as well as its titles. For a paper or notes, use [source-to-slides](source-to-slides.md) to establish source coverage and a provisional outline. Preserve the original sequence and source identities before proposing changes.

Identify the central scientific question, actual contribution, strongest supported findings, prior knowledge the audience can use, unresolved problem and evidence required to understand the answer. Look for a consequential comparison, trade-off, exception or tension within the supplied material. Establish the basis for anything described as new or surprising; novelty requires a defensible comparison with existing knowledge, not stronger adjectives.

Create a private narrative map linking motivation, question, approach, evidence, findings and implications. These are reasoning roles, not mandatory sections or a prescribed slide order. Give questions and evidence stable local identifiers so every major finding can be traced to the question it addresses and the source that supports it. Record contradictory evidence and unanswered questions as part of the map.

| Record | What it establishes |
| :--- | :--- |
| Audience purpose and central question | What this talk should help listeners understand or examine |
| Contribution and selected scope | What the work adds, and what this presentation can responsibly cover |
| Question → approach → evidence → finding | How an answer is obtained and supported, including comparator and scientific status |
| Assumptions, uncertainty and contrary evidence | What constrains the inference or prevents a tidy resolution |
| Implication and final synthesis | What has become clearer, what remains unresolved and why that matters for this audience |

When the source supports only a proposal, conceptual explanation or partial result, build the appropriate talk and keep that status explicit. Do not invent findings to complete an arc. A useful contribution may be a null result, a boundary condition or a better-defined uncertainty.

## Slide Title Sequence Review

Complete this review before changing slide order, rewriting page content or choosing new layouts. For a new deck, review provisional outline titles before construction. A narrowly scoped typography or single-object correction does not authorize a wholesale story rewrite; inspect the relevant context and preserve the requested scope.

1. **Capture the original sequence.** Extract titles in actual presentation order with stable slide IDs, hidden status and original wording. Inspect ambiguous or missing title candidates in the rendered source. Review the intended visible sequence separately from hidden or appendix material, while retaining the complete inventory.
2. **Read titles alone.** Describe the argument they imply without relying on the bodies. Locate unexplained subject changes, missing prerequisites, repeated claims, premature conclusions and promises that never receive an answer. Topic labels can be appropriate for dividers, definitions or lookup pages; their presence is not an automatic failure.
3. **Explain each slide's position.** Identify its narrative job and what it inherits from the previous slide. State what it adds and why the next slide follows. Use a real relationship such as motivation, complication, test, mechanism, comparison, qualification or synthesis, rather than writing a generic transition word.
4. **Check against the science.** Open the bodies and sources again. Verify that every proposed title is supported by the slide, with the appropriate population, condition, comparison and certainty. Record where the title-only impression would overstate or conceal the evidence.
5. **Explore, then select.** At important turns, consider genuinely different title strategies or orders. Retain a good sequence when alternatives bring no identifiable benefit. For a rewrite, move, split or merge, record the communication improvement and preserve the source-to-output mapping.
6. **Re-read the revised sequence.** Check backward and forward connections, then compare each title with its slide again after writing and visual construction. A split, merged page or stronger visual emphasis can change the argument even when most words remain unchanged.

Keep the working review private. It should contain original/proposed titles and IDs, narrative role, question/evidence references, the relationship to each neighbor, scientific qualifications, decision and reason. Record proposed order separately from the original; preserve lineage for split or merged slides. Repeated titles may be deliberate builds and should retain [text continuity](spacing-and-hierarchy.md#keep-retained-text-fixed-across-slide-changes). Stable wording can be a good editorial decision.

The success criterion is an explainable progression: a reader can locate the question, understand how the investigation addresses it and see why the findings matter. It is not a required number of questions, full-sentence headings, rhetorical devices or changed slides. Word overlap and title length cannot certify coherence.

### Extract titles without changing the deck

Use [review_title_sequence.py](../scripts/review_title_sequence.py) to prepare a private review record from a compatible PPTX or an explicit ordered JSON inventory. It extracts candidates and scaffolds judgment; it does not write better titles, assess interest, verify claims or edit slides. Inspect the native source when placeholders are absent or ambiguous. For Keynote, use a confirmed native or manually reviewed title inventory without exporting through PowerPoint. This route does not establish Mac application compatibility.

```text
python scripts/review_title_sequence.py --source input.pptx --output private/title-review.json
python scripts/review_title_sequence.py --source private/title-inventory.json --output private/title-review.json
```

The private output directory must already exist; the output file must be new. Both routes use the existing `lxml` dependency. For an ordered inventory, supply this schema with no additional fields:

```json
{"schema_version": 1, "source_kind": "outline", "slides": [{"slide_id": "I1", "title": "Original or provisional title", "hidden": false}]}
```

Use `source_kind` of `keynote`, `outline` or `manual`; each slide has a unique nonempty string ID, a string or `null` title and an explicit boolean `hidden`. Obtain a Keynote inventory from native inspection or a confirmed manual record. The helper does not inspect a `.key` file. Its `source.sha256` identifies the exact input PPTX or JSON bytes, not the Keynote deck or paper behind a JSON inventory.

The generated record stays `unreviewed`, with `narrative_validated: false`. It retains all slides, gives visible-neighbor pointers that skip hidden slides, and flags repeated titles without judging them. It does not infer appendix roles or whether a native-title placeholder is the intended audience-visible heading; confirm candidates against the slide. Complete narrative judgments in a private working record, preserving the original extraction. Record moves, splits, merges, question IDs and output lineage there; they are not populated by extraction.

Do not add these research-bearing records to Git or to an installed skill. The [evaluation guide](storytelling-examples.md#evaluate-the-sequence) explains how to use the record alongside qualitative review.

## Introduction: earn interest in the question

Search for the most compelling supported angle in the material instead of asking the researcher to invent a hook. An observation that conflicts with an expectation, a neglected mechanism, a consequential uncertainty or an unresolved trade-off can motivate the next question. Show the basis for the expectation or contrast. A useful opening makes the scientific question matter; it does not merely add drama to background facts.

Build the connection among introductory titles as carefully as each title itself. One study may move from an observation to a complication, then to an unknown mechanism and a question worth answering. Another may open with a qualified finding before explaining how it was established. Choose the sequence that the source and audience justify, and retain the definitions and evidence needed to follow it.

The audience should know what is unresolved and why the next slide helps. Do not withhold an essential qualification for suspense, invent conflict, exaggerate novelty or select only convenient evidence. Questions also have factual implications: "Why does X cause Y?" presupposes causality. An unverified causal claim does not become safe when followed by a question mark. Query the researcher privately or use a genuinely open question supported by the study's aims.

Pass the selected motivation, gap and question to the [illustrated introduction workflow](visual-storytelling.md#outline-then-storyboard-then-build). A carefully framed title needs a substantive explanation and source-specific visuals, rather than a large topic icon or a decorative scene.

## Methodology: earn confidence in the inference

Organize methods around the reasoning that connects the question to a defensible answer. Software names and historical task order rarely explain that reasoning by themselves. For each major step, identify why it is necessary, what it changes or holds fixed, what it permits the study to infer, what assumption it introduces and how its output supports the next step.

| Scientific need | Explain when relevant |
| :--- | :--- |
| Define the investigation | System boundary, population, timescale, outcome and research question |
| Establish a fair comparison | Baseline, counterfactual, controls, scenario differences and shared conditions |
| Connect data and mechanisms | Inputs, variables, measured or assumed relationships and computational transformations |
| Interpret outputs | What is observed, simulated, assumed, estimated or causally identified, and the limits of that status |
| Assess confidence | Validation, sensitivity, uncertainty and what each check actually tests |

Select only the elements the supplied study contains; do not invent controls, validation or sensitivity analysis to make it look rigorous. Keep assumptions distinct from findings and a model comparison distinct from empirical causal identification. A chronological order remains appropriate when the temporal sequence itself is the method's logic.

Use titles that explain the scientific purpose of an operation, such as what a paired comparison holds fixed, rather than merely naming a tool. Translate that reasoning into [method mini-scenes and analytical diagrams](visual-storytelling.md#choose-the-illustration-language) with accurate connections. The actual inputs, operations, constraints and interpretation must remain visible at the audience's chosen depth.

## Results: turn evidence into findings

Every major result needs a role in the investigation. Link it to a research question or identify a clearly supported exploratory finding without retroactively presenting it as a planned test. Inspect the figure, values, definitions, comparator and uncertainty before writing the headline or commentary.

| Establish for each finding | What to record or show |
| :--- | :--- |
| Question answered | The relevant question ID, including partial or negative answers |
| Finding and comparison | What changed, differed or remained unresolved, compared with what and under which conditions |
| Supporting evidence | Source figure/table/data, calculation where needed, and relationship to the displayed graphic |
| Scientific status | Observed, modeled, estimated or causally identified; time period and population |
| Interpretation and limits | Why the result matters, the uncertainty, alternative explanation or boundary that constrains it |

State a supported finding in the title when one is established. A descriptive technical heading may remain appropriate when the slide presents an unresolved distribution, diagnostic or exploratory result. Never force a winner, threshold, ranking or causal mechanism onto evidence that does not establish it. Preserve negative results and exceptions that affect the answer.

Use a concise analytical statement near the chart when it helps listeners see the decisive comparison. Verify calculations from source values, including denominator, units, rounding and interval meaning. Make the comparison legible with direct labels, restrained annotations or matched scales; do not emphasize only a convenient point estimate while hiding overlap or uncertainty. A difference between scenarios does not automatically justify a policy recommendation.

Order findings so each adds to the answer. An overall pattern may motivate a subgroup comparison, followed by an explanatory test and robustness check, but those roles can appear in another order or be absent. Do not turn each figure into an isolated miniature talk or force an attractive mechanism explanation that the study has not tested.

## Discussion and ending: synthesize what has become clearer

Return to the original question and explain what the evidence collectively establishes. A conclusion should connect findings into a larger understanding, not simply repeat several Results headlines. Keep what remains uncertain and what the study does not establish visible. Distinguish implications supported by the investigation from speculative applications or possible next studies.

Adapt the ending to the audience's purpose. A group meeting may need a focused unresolved question for discussion; a tutorial may close by applying the concept; a conference talk may emphasize a qualified contribution. Do not automatically create separate Discussion, Conclusion and Future Work sections. If future work belongs, connect each proposed step to a specific unresolved inference and explain why that step could address it.

End the complete main narrative with [visual key takeaways](visual-storytelling.md#close-with-visual-key-takeaways), reusing meaningful evidence, comparisons or research objects. A memorable formulation must remain scientifically defensible; a slogan is not a substitute for synthesis. Q&A, contact details and appendices may follow, and the closing takeaway needs no separate navigation-ribbon item.

## Write titles for their narrative role

First draft the plain, accurate message. Then consider whether another strategy would make its role easier to understand or remember. At important turning points, explore alternatives that differ in reasoning or emphasis rather than swapping adjectives. Choose selectively and check the complete sequence afterward. Technical definitions and equation walkthroughs can retain direct, precise headings.

| Technique | Useful contribution | Check before choosing it |
| :--- | :--- | :--- |
| Framing or concrete observation | Identifies the consequential question or object | The frame fits the actual scope and does not hide contrary evidence. |
| Contrast or antithesis | Makes a supported tension or trade-off visible | Compared cases have clear units, baselines and conditions; grammatical contrast does not manufacture a false binary. |
| Open question | Creates a legitimate reason to follow the investigation | No unsupported presupposition; later slides answer it or explicitly retain the uncertainty. |
| Claim or quantitative comparison | Directs attention to a supported result | Comparator, scientific status, magnitude and uncertainty can be verified. |
| Parallelism and rhythm | Connects related cases and makes the sequence easier to follow | Verbal symmetry does not imply equivalent evidence or erase exceptions. |
| Metaphor | Makes an unfamiliar relationship intelligible | Its mapped relationship is defensible and cannot be mistaken for a literal mechanism or agency. |
| Alliteration, wordplay or a double meaning | Adds a memorable reading to an already clear message | The meaning is recoverable without obscure cultural knowledge; precision and tone survive the device. |
| Curiosity followed by explanation | Motivates the next scientific step | The audience receives the promised explanation; essential context is not withheld for suspense. |

Use familiar subjects or concepts to connect backward and place the new distinction where it receives emphasis. This is a diagnostic for information flow, not a mandatory word-order rule. Repeated technical terms can strengthen continuity; replacing them with decorative synonyms can obscure the science. A pun that requires explanation or a headline that overclaims is worse than the plain accurate version.

When an attractive claim cannot be verified, record a specific private question for the researcher. Do not publish it as a finding, and do not use rhetorical wording to conceal the gap. Follow [scientific fidelity](scientific-fidelity.md) for discrepancies and content-changing work.

## Review improvement and decision stability

Compare the original and proposed narrative maps, title sequences and evidence associations. Explain the benefit of each consequential change; retained slides need a genuine assessment, not a blanket declaration that nothing needs improvement. Revisit a previous design when new evidence, an unresolved defect or a changed brief warrants it. Under an unchanged brief and evidence base, do not rotate among equivalent titles, reorder sound slides for novelty or undo a good decision merely to produce edits.

Use the [synthetic examples and evaluation procedure](storytelling-examples.md) to distinguish extraction checks from judgment of coherence, engagement, inference and insight. The helper does not automate that judgment. Preserve source coverage and scientific force, then review the actual delivered title sequence and its bodies. Native visual and editability review remain separate requirements.

## Editorial foundations

These sources inform specific decisions rather than prescribing a universal presentation formula. The adaptation to palate's workflow remains design judgment.

| Source | What informs this capability | Limit |
| :--- | :--- | :--- |
| [MIT EECS: Slide Presentation](https://mitcommlab.mit.edu/eecs/commkit/slideshow/) | Read titles as a sequence and make their messages contribute to the talk. | Teaching guidance; not every technical slide needs an assertion headline. |
| [MIT/Broad: Results](https://mitcommlab.mit.edu/broad/commkit/journal-article-results/) | Connect rationale, evidence and conclusions in a logical progression. | Adapt written-paper guidance to an audience and a spoken explanation. |
| [Gopen and Swan: The Science of Scientific Writing](https://inpp.ohio.edu/~meisel/PHYS6751/file/ScientificWriting_GGopenJSwanAmSci1990.pdf) | Familiar information can connect backward while new emphasis moves the explanation forward. | Applying this principle across slide titles is an editorial inference, not an automated rule. |
| [Garner and Alley: How the Design of Presentation Slides Affects Audience Comprehension](https://writing.engr.psu.edu/ae_comprehension.pdf) | Couple a message headline with explanatory visual evidence. | A bounded engineering-student experiment compared a bundle of slide choices; it does not prove that any headline technique works universally. |
| [Nature Methods: Should scientists tell stories?](https://www.nature.com/articles/nmeth.2726) | Use narrative without suppressing scientific nuance or inconvenient evidence. | Narrative coherence does not establish scientific truth. |
| [BBC: Reporting Statistics](https://downloads.bbc.co.uk/rmhttp/guidelines/editorialguidelines/pdfs/ReportingStatistics.pdf) | Verify statistics, context and comparisons; distinguish correlation from causation. | This accessible guidance is dated 10 March 2017, not presented as current BBC policy. |
| [Economist Education: Writing with Style](https://education.economist.com/blog/what-to-read/writing-with-style) | Use familiar language and carefully chosen metaphors to explain unfamiliar material. | Preserve necessary scientific terms rather than applying editorial preferences mechanically. |
| [Boggio and Parini: What's in a headline?](https://research.uniupo.it/en/publications/whats-in-a-headline-learning-and-teaching-the-use-of-rhetorical-s/) | Distinguish rhetorical devices rather than treating every memorable title as a pun. | The institutional abstract identifies techniques; it does not establish scientific-presentation benefits. |
