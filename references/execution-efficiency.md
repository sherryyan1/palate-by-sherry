# Execute with shared context

Efficiency comes from reusing sound work and inspecting the right evidence. It does not change the four design capabilities, the scientific standards or the requirement to inspect every final slide. This guide coordinates their execution; the canonical capability and native-workflow references still own their decisions.

## Choose the scope before loading references

Start with the request, existing brief and actual delivery application. Select a row below; broaden it when a consequential change crosses its boundary. Read necessary scope paragraphs and complete relevant sections, including exceptions. A Markdown link is a route to consult when relevant, not an instruction to recursively load all linked documents.

| Task | Read or reuse | Broaden when |
| :--- | :--- | :--- |
| Typography, alignment or one-object repair | Existing brief and source inventory; the relevant typography/spacing/container guidance; scientific-fidelity scope, preservation and delivery requirements; the selected native workflow. | Reflow, shared styles or prominence affect other slides or interpretation. Do not rewrite the narrative without an identified need and appropriate scope. |
| Title or wording revision | Existing brief and narrative map; Find the thread's title review and relevant section role; Distill the message; content-changing scientific safeguards. | The title changes scientific force, order, scope or evidence associations. Do not load illustration or other-application workflows by default. |
| Method or result revision, even a small one | Relevant Find the thread method/results guidance, complete applicable accuracy/interpretation safeguards, evidence and comparator, wording guidance and actual native route. | Changed assumptions or findings affect questions, conclusions, diagrams or other dependent slides. Small visual scope does not mean small scientific scope. |
| Visual refinement of an established argument | Reuse the brief and narrative; Refine the visuals and the specialist sections the actual objects need; scientific preservation/content-changing requirements as applicable. | A split, new visual relationship, crop or emphasis changes the explanation. Recheck the affected narrative and scientific dependencies. |
| New presentation or substantial redesign | All four capabilities at their respective stages, source-to-slides when needed, scientific fidelity and the chosen native workflow. | Load covers, tables, panels, translation, asset sourcing and other specialists when their features occur. All capabilities remain available. |
| Review an already refined deck | Existing source-bound plan and review evidence, the criteria for the requested review, plus the necessary scientific and native checks. | A real defect, changed requirement or stale dependency calls for a targeted correction. Do not reopen settled design decisions merely to produce changes. |

Use [reference_query.py](../scripts/reference_query.py) to retrieve an index or complete material. It uses the maintained files directly, so there is no second hand-maintained rule summary to synchronize.

```text
python scripts/reference_query.py rules
python scripts/reference_query.py rules --ids R001 R003
python scripts/reference_query.py section find-the-thread.md
python scripts/reference_query.py section find-the-thread.md --heading "Slide Title Sequence Review"
```

Rule selection returns complete objects, including exceptions and validation. A section query returns the complete selected section, descendants, file scope and enclosing introductions. Follow any additional safeguards the selected content requires. A heading index or rule index alone is never sufficient instruction. The helper's normalized-text hash identifies its reference text, not a research artifact or a completed quality check.

Keep already-read instructions available through the current phase; reread when their content changed or a lost context leaves a necessary rule uncertain. Teaching examples and repeated unchanged-brief stability assessments are optional learning/regression tools, not a required extra production pass. Documentation and installation references belong to those tasks, not every slide edit. Only load the selected PowerPoint or Keynote route unless conversion was explicitly requested.

## Reuse presentation-level analysis

Treat the brief, evidence ledger, narrative map and storyboard as linked parts of one private task record, not separate essays to regenerate at every stage. Use stable source, evidence, question and slide IDs. Preserve the original title extraction and source-to-output lineage, and link to detailed artifacts rather than copying their full text into every slide packet. Keep exact data, uncertainty, equations and qualifications where the scientific ledger requires them; a compact state is an index to that evidence, not a substitute for it.

Use [task_state.py](../scripts/task_state.py) for selective retrieval and dependency comparison. It does not analyze research, author slides or approve checks. For a very small repair, reuse an existing record or make a small record for the actual scope rather than manufacturing an entire new analysis. A substantial deck needs the shared narrative and evidence relationships before local work begins.

Before reuse, confirm actual source/candidate identities, the brief, slide order and relevant shared styles. Caller-supplied revisions must be updated from those checks; an unchanged string is not proof that a file is unchanged. Keep the current complete record private, retrieve only the necessary slice, and preserve prior versions in new files.

The version-1 record has the following contract. Existing intake and transformation-plan files keep their own schemas; link to them rather than adding state fields to those files.

| Field | Required content |
| :--- | :--- |
| `schema_version` | `1` |
| `brief`, `narrative`, `design` | Objects for the agreed brief, central argument and established design. `design.approved` is a boolean indicating an established design under the authorized scope, including delegated choices; it does not introduce an extra approval step. Record unresolved issues in the relevant narrative or slide record. |
| `sources` | Map of stable IDs to objects with nonempty `revision` and source locations. Verify revisions against the actual material before reuse. |
| `questions` | Map of stable IDs to objects with nonempty `text`. |
| `evidence` | Map of stable IDs to objects with `source_ids` and `question_ids` lists. Keep source-linked findings, assumptions, qualifications and detailed artifact paths here. |
| `slides` | Ordered records with `id`, nonempty `revision`, boolean `hidden`, and `question_ids` and `evidence_ids` lists. Include each slide's role, title, design decisions, lineage and outstanding issues as needed. |
| `reviews` (optional) | Declarations with `scope` (slide ID or `deck`), `kind` (`content`, `editability`, `rendered` or `narrative`), `status` (`passed`, `failed` or `blocked`) and `fingerprint` from the helper. Link to actual review evidence. |

Source and evidence records can declare `coverage_complete: true` only after all their dependencies have been mapped. Omitted or false coverage is conservative: changing that record invalidates all slide checks. A source also remains unscoped if any of its evidence is incomplete or unlinked. Selection reports incomplete coverage so a local worker knows when its packet is insufficient. Do not set completeness merely to obtain a smaller packet.

```text
python scripts/task_state.py validate build/state-02.json --output build/state-02-report.json
python scripts/task_state.py select build/state-02.json --slides s3 --previous build/state-01.json
python scripts/task_state.py compare build/state-01.json build/state-02.json --output build/state-diff.json
```

`validate` and `compare` print concise summaries; `select` returns the requested slides, relevant evidence and neighboring context, including hidden-slide adjacency and the visible sequence. It includes relevant review declarations with their evidence paths and computed freshness. `--output` writes details to a new file and reports its path. Existing outputs and inputs cannot be overwritten. Reuse review declarations only when both their fingerprints and underlying evidence remain valid; the helper neither opens external artifacts nor performs those reviews.

| Change | Required refresh |
| :--- | :--- |
| Research source or evidence changes | Recheck its claims, dependent slides and qualifications; revisit the deck's argument and final approval. Expand when evidence coverage is incomplete. |
| Audience, objective, duration, depth or language changes | Reassess the brief, narrative scope and dependent writing/design choices. A language change retains the scientific translation preflight. |
| Slide order, split, merge or removal changes | Refresh the narrative sequence, neighbor relationships, first-use terminology, numbering and source-to-output lineage. |
| Theme, font, master/layout, canvas or shared visual decision changes | Review every affected slide, including hidden slides; a global change expands visual/editability coverage to the whole deck. |
| One slide or one shared figure changes | Refresh its content, visible output and native checks as appropriate, plus dependent slides and adjacent builds. |
| Renderer/application version, font availability or linked resources change | Invalidate relevant render/editability evidence; record the new environment in the task's shared design/review context. |

The structured helper conservatively expands some changes to the whole deck. Do not narrow that result without establishing the complete dependency scope. Its freshness flags mean only that declared inputs match; inspect the evidence behind a claimed review. A valid state or current fingerprint never certifies scientific accuracy, native editability or a passed visual review.

## Hand off a bounded task

When delegation genuinely helps, send the responsible agent a compact packet containing its exact task, relevant reference sections, selected slides and neighbors, supporting evidence, protected scientific qualifications, existing narrative/design decisions, output location and acceptance criteria. Include the central research question and the slide's role so a local improvement cannot undermine the whole argument. Use a fresh bounded context where supported rather than copying project-development discussions and unrelated presentation history.

Do not add agents solely to make each context look smaller. Separate workers only when their responsibilities can be coordinated without duplicated whole-deck analysis. The coordinating agent owns the narrative and resolves conflicting local proposals. A worker returns changed IDs, reasons, evidence, checks and unresolved issues, not a new independent story for the entire deck. After context compression or a host handoff, resume from the verified task record and necessary instructions rather than automatically rereading all source files.

## Preview the changes and their consequences

Plan a coherent group of edits before rebuilding. Preserve detailed conceptual illustrations and necessary design exploration; do not impose an arbitrary build or image-generation quota. During intermediate repairs, preview changed slides plus affected neighbors and any shared dependencies. For example:

```powershell
& ./scripts/render_pptx.ps1 -Source build/candidate.pptx -OutputDirectory build/review-02 -Slides @(3,4,5)
```

Run this in a PowerShell session so `-Slides` receives an integer array. Keep each render in a new directory. Record candidate identity, native application/version, slide IDs and preview paths. The [PowerPoint renderer](../scripts/render_pptx.ps1) already supports selected slides; Keynote's current native PDF export remains whole-deck and Mac-unverified. Do not invent selective Keynote support.

Inspect full slides at a readable scale; use crops for a specific detail and contact sheets for cross-slide patterns. Contact sheets cannot replace individual final-page review. Reuse an identical, already inspected screenshot only when its artifact and environment are unchanged and the review question is already settled. A new scientific or design question can justify inspecting the same image again. Do not infer image identity from a filename alone.

Before delivery, inspect every final slide, including hidden slides, in the actual application and complete the required content, editability and playback checks separately. Intermediate selected previews do not establish complete coverage. Global changes require broader review even if only one source object was edited. Keep the final title-sequence and question-to-result review.

## Keep outputs concise and stop for the right reason

Keep inventories, XML, long logs and evidence in private files. Return status, actionable errors/warnings, affected IDs, pending checks and paths. Retrieve the needed slide/object fields or diagnostic excerpt instead of printing a full report. Do not silently truncate relevant evidence; when a summary is incomplete, say what remains and retrieve it. Existing helpers already save detailed output and usually return short summaries.

Before batching reference reads, check their sizes against the combined tool-output allowance. Retrieve complete necessary sections in manageable groups; batching several large files only to truncate and reread them is redundant work. If truncation occurs, retrieve the missing section, not the entire batch again. This output check governs how material is returned, never which scientific qualifications may be discarded.

Use successful `apply` receipts for checks already performed inside that operation. A separate identical validation immediately afterward supplies no new evidence unless the input changed or an independent checkpoint serves a distinct purpose. Preserve finalization's fresh checks, saved-file reopening, actual native review and all source/target safeguards. An intake `answer` already returns the next question state; `next` resumes a saved state rather than repeating that result.

Maintain an issue list with affected IDs and required verification. Continue when a substantive scientific, narrative, visual or native defect remains, or a justified improvement is still required to meet the brief. After the relevant checks pass and no such issue remains, deliver. Do not stop because an iteration quota expired or keep making equivalent changes to demonstrate activity. An unavailable required check remains pending and prevents a verified-delivery claim.
