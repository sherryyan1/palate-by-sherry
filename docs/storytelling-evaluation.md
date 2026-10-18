# Evaluate scientific storytelling

This guide is for maintainers and reviewers assessing the behavior described in [Find the thread](../references/find-the-thread.md). Use the [synthetic storytelling examples](../references/storytelling-examples.md) for reproducible, public exercises and authorized task-local sources for real-deck evaluation. Keep original research, extracted titles and detailed review records private and untracked.

For angle selection, rhetorical choices and cross-domain title sequences, use the [editorial evaluation supplement](editorial-evaluation.md). It includes four synthetic scientific briefs, actual candidate decisions, quantitative boundaries and ten review dimensions. It separates these exercises from a measured comparison of model versions or audience outcomes.

The purpose is to establish whether the proposed narrative helps an audience understand and evaluate the research. A larger number of edits, more sentence headlines or a stronger claim is not evidence of improvement. Separate what a script can verify from what requires editorial, scientific or native-application review.

## Prepare an ordered title inventory

The helper reads a PPTX or an explicit JSON inventory and creates a new JSON review record. It does not change the presentation, rewrite titles or certify scientific or narrative quality.

```text
python scripts/review_title_sequence.py --source deck.pptx --output existing-private-dir/new.json
python scripts/review_title_sequence.py --source inventory.json --output existing-private-dir/new.json
```

The output parent directory must already exist in an authorized private workspace, and the output file must not exist. Choose a new filename for each run; the helper refuses to overwrite an earlier record. Use local paths without parent traversal, symbolic links or reparse points. The helper uses the repository's existing `lxml` dependency through the shared PPTX parser; it does not require a new language-model or presentation-application dependency.

For Keynote, obtain titles through an available native route or a manually confirmed inventory. For a paper or rough text, use the provisional outline. Supply the exact input schema below, with no additional fields:

```json
{
  "schema_version": 1,
  "source_kind": "outline",
  "slides": [
    {
      "slide_id": "I1",
      "title": "Two grids lose the same 1.0 TWh of hydropower",
      "hidden": false
    },
    {
      "slide_id": "M1",
      "title": "Hold demand and hydro loss fixed; compare replacement mixes",
      "hidden": false
    },
    {
      "slide_id": "R1",
      "title": null,
      "hidden": false
    }
  ]
}
```

| Input field | Contract |
| :--- | :--- |
| `schema_version` | Integer `1`. |
| `source_kind` | Exactly `keynote`, `outline` or `manual`. This describes the supplied inventory; it does not enable native parsing. |
| `slides` | Ordered, nonempty array. Preserve the intended source order. |
| `slide_id` | Nonempty, unique string identifying a source slide or outline item. Keep it stable during review. |
| `title` | String or `null`. Use `null` when a title is missing or unconfirmed; do not invent one merely to complete extraction. |
| `hidden` | Boolean, supplied explicitly for every item. |

The input limits and rejection conditions are enforced by [review_title_sequence.py](../scripts/review_title_sequence.py). A PPTX is read in its presentation relationship order, not filename order. The helper identifies explicit title placeholders and supported layout-inherited title placeholders. If a title is absent, ambiguous or stored as ordinary text, it records candidates for confirmation rather than guessing from font size or page position. Image-based titles require native or visual inspection.

### Interpret the generated record

Every generated record starts with `status: "unreviewed"` and `narrative_validated: false`. Preserve that extraction baseline. Add the agent's assessment in a private working copy or companion review; do not treat a changed status field as evidence that review occurred.

| Output | Meaning and limitation |
| :--- | :--- |
| `source.filename`, `source.kind` | Input filename and route used. A JSON inventory retains its declared source kind. |
| `source.sha256` | Digest of the exact bytes read. For JSON input, it identifies the JSON inventory, not a native Keynote file or the paper behind an outline. |
| `original_position`, `slide_id` | Original ordered position and identity. PPTX records also retain the slide part and relationship ID. |
| `original_title`, `title_status`, `title_candidates` | Extracted or supplied wording and confirmation needs. `provided` means supplied through JSON, not independently verified. |
| `hidden`, `previous_visible_slide_id`, `next_visible_slide_id` | Hidden slides remain in the inventory; visible-neighbor fields skip them. Review the actual intended delivery sequence separately. |
| `same_title_slide_ids` | Titles matching after whitespace normalization and case folding. Repetition may be a deliberate progressive build, not an error. |
| `review` | Initially empty fields for role, neighboring relationships, evidence, decision, proposed title and notes. They require a reviewer. |
| `decision_options` | The helper advertises `retain` and `revise`. Record structural changes such as moves, splits or merges in the narrative map and reviewer notes, retaining original IDs and output lineage. |

The helper neither parses `.key` files nor exports Keynote through PowerPoint. Processing a Keynote inventory therefore provides no evidence of Mac rendering, native editability or save/reopen compatibility.

## Review the narrative against the evidence

Establish the audience, purpose, duration and depth before comparison. Keep these conditions fixed for a before-and-after evaluation, and retain both the original and proposed title sequence. A reviewer should be able to inspect the source associated with every consequential change.

| Dimension | Evidence of a useful improvement | Failure to investigate |
| :--- | :--- | :--- |
| Narrative coherence | Each major slide has a recognizable role and an explainable link to its neighbors. The title sequence reveals the argument at an appropriate level. | Unexplained topic changes, missing prerequisites, redundant claims or unanswered promises. |
| Introduction engagement | A supported observation, tension or consequential uncertainty gives the audience a reason to follow the scientific question. | Generic background, invented novelty, unsupported surprise or a question with a false presupposition. |
| Methodological reasoning | Major steps explain why they are necessary, what they hold fixed or change, their assumptions and what inference they permit. | A tool list, a decorative flowchart, invented validation or a model treated as empirical causal identification. |
| Question-to-result traceability | Each major finding maps to an earlier question or is clearly identified as exploratory; its evidence and qualifications remain available. | An isolated chart, an unsupported answer or an exploratory result presented as a planned test. |
| Insight quality | The title or annotation identifies a specific, supported comparison and its importance within the study's scope. | Dramatic wording without analysis, an unverified ratio, incompatible comparisons or an unjustified recommendation. |
| Scientific integrity | Values, units, boundaries, uncertainty, contrary evidence and the force of the conclusion are preserved. | Causality added to association, assumptions presented as findings, null results treated as equivalence or omitted caveats. |
| Visual communication | The actual graphic helps inspect the relationship claimed by the title, with readable evidence and correct connections. | A large icon replacing explanation, misleading scales or emphasis, decorative charts or an unreadable method. |
| Decision stability | A second pass under the same conditions retains sound decisions and changes only identifiable remaining defects. | Equivalent titles rotated for novelty, arbitrary reordering or removal of qualifications to simplify the story. |

Use a short verdict for each dimension: supported, needs revision or not assessed. Explain the evidence behind the verdict. A numeric score can help a local comparison, but no aggregate score should hide a scientific error or turn subjective engagement into an automated claim.

## Exercise the difficult cases

Run the [two-grid fixture and boundary cases](../references/storytelling-examples.md) through an independent agent review where available. Give the reviewer the raw evidence and brief before showing the expected examples. The examples establish scientific boundaries and reasonable decisions, not one required title wording.

| Exercise | What a successful response must preserve |
| :--- | :--- |
| Connected Introduction | The equal-shortfall observation leads to the replacement mechanism and Q1 without inventing a literature gap or causal finding. |
| Method comparison | Demand and hydropower shortfall remain fixed between cases; replacement mix differs. Assumptions and modeled status remain explicit. |
| Results insight | The 0.40 and 0.10 MtCO2 outputs, operational boundary and fourfold ratio are correctly supported and linked to Q1. |
| Uncertain difference | The interval remains visible; the response does not invent its method, declare a winner or infer equivalence. |
| Null result | Failure to reject a null is not converted into proof of no effect or equivalence. |
| Proposal without results | Planned analysis stays planned. Any illustrative future pattern is identified as hypothetical and does not become a completed finding. |
| Already refined sequence | The agent evaluates the argument and retains good choices unless it identifies a specific remaining defect. |
| Hidden slide or repeated build | Delivery order and source provenance remain distinct; repeated titles are inspected in context rather than automatically rewritten. |

For the stability exercise, provide the refined output again with the same brief and evidence. Compare the reasoning and scientific force, not only exact string equality. A justified correction to a missed error is an improvement; swapping equally accurate phrasing without a reader benefit is not.

## Keep validation layers separate

| Layer | What it can establish | What it cannot establish |
| :--- | :--- | :--- |
| Automated helper tests | Input validation, extraction order, title candidates, hidden status, stable identities, provenance, safe output handling and unchanged source files. | Interest, coherent inference, scientific truth, readable layouts or native application behavior. |
| Agent or human editorial review | Explainable slide roles, transitions, audience fit, supported headline choices and justified retention. | An experimental improvement in audience comprehension, or native rendering that was not inspected. |
| Scientific source review | Traceable results, valid calculations, preserved qualifications and an appropriate interpretation of the supplied evidence. | The truth of unavailable source data or unperformed analyses. |
| Native presentation review | Rendered text, graphics, connector endpoints, continuity, editability and save/reopen behavior in the application actually tested. | Compatibility with another untested application or operating system. |

Run the focused helper tests with the repository's supported Python environment:

```text
python -m unittest discover -s tests -p test_title_sequence.py
```

Complete the relevant packaging, link and repository-content checks when changing runtime files. Record the actual commands, outcomes and environment rather than copying a historical test count. Helper tests and a synthetic editorial exercise do not demonstrate a completed PowerPoint or Keynote workflow. When no native deck has been produced and inspected, report native visual and editability validation as not performed.

For a real deck, follow the existing [validation procedure](validation.md) after the narrative review. Report the principal narrative changes, any unresolved source questions, the checks completed and their limits. Keep detailed research-bearing evidence local; publish only synthetic fixtures or material explicitly suitable for the repository.
