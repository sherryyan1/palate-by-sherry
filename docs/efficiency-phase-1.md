# Palate Efficiency Optimization · Phase 1

This change coordinates reference loading, shared analysis and review work. The four Sherry's Picks capabilities and their scientific and visual standards remain intact. It adds no dependency or external service and does not change the READMEs or the installed skill.

## Scope and baseline

The baseline is repository commit `2e5499ac34f15e34c9ddf4063a3a70e89f778679`, preserved as an allowlisted runtime package before behavioral edits. Its package contains 54 files; the optimized runtime contains 57. The installed skill has 48 managed files and differs from the repository baseline. All 49 observed installation files, including its manifest, were checked separately and left unchanged. Historical presentation and development runs are not used as comparable performance measurements.

The test environment is Windows with Python 3.12.14, Node.js and PowerPoint 16.0. The comparison uses fixed synthetic evidence, not private research. Baseline and optimized instruction evaluations use fresh bounded agents with the same model and reasoning setting, the same brief and the same three tasks in the same order. They propose decisions and validation plans; they do not author a new deck.

| Task | Fixed request | Quality criterion |
| :--- | :--- | :--- |
| A: narrow repair | Change one existing ribbon's effective label size from 10.5 pt to 12 pt. | Preserve content, order and illustration; identify fitting, inheritance and native review obligations. |
| B: six-slide improvement | Improve the narrative, writing and visual plan for a modeled replacement-generation comparison. | Connect question, assumptions, method, result and limitations; propose explanatory visuals with sufficient detail. |
| C: refined-deck review | Review an already coherent sequence under the unchanged brief. | Retain sound decisions, identify only justified changes and preserve final verification. |

The fixture has equal 1.0 TWh hydropower shortfalls, fossil replacement of 0.8 versus 0.2 TWh, and an assumed fossil factor of 0.5 tCO2/MWh. The outputs are 0.40 and 0.10 MtCO2 of replacement operational emissions. Neither evaluation may present them as measured findings, net whole-grid changes, lifecycle results or a policy ranking. Uncertainty estimates are not supplied.

## Implementation

| Files | Responsibility |
| :--- | :--- |
| [SKILL.md](../SKILL.md) | Route tasks by scope, reuse valid context and retain complete final review. |
| [Execution guidance](../references/execution-efficiency.md) | Loading matrix, shared-state contract, invalidation, bounded handoffs, selective intermediate previews and quality-based stopping. |
| [reference_query.py](../scripts/reference_query.py) | Query the maintained rule index, complete selected rules or complete reference sections with their enclosing scope. It does not maintain a second rule library. |
| [task_state.py](../scripts/task_state.py) | Validate private structured state, retrieve relevant slides and compare dependencies. It reports review freshness, not scientific or visual approval. |
| [keynote_native.js](../scripts/keynote_native.js) | Reuse the read-only inspection inventory; preserve before/after collection for edits. |
| [Intake guidance](../references/guided-intake.md), [PowerPoint plan](../references/transform-plan.md), [Keynote workflow](../references/keynote-workflow.md) | Reuse returned question states and completed equivalent checks; preserve saved-file reopening and fresh finalization. |
| [Package allowlist](../scripts/package_skill.py) and regression tests | Include the three new runtime files and verify selection, invalidation, safeguards and native boundary behavior. |

The [loading matrix](../references/execution-efficiency.md#choose-the-scope-before-loading-references) distinguishes local formatting, wording, scientific revision, visual refinement, full creation and final review. A small scientific change still loads accuracy safeguards. A full redesign still uses all four capabilities. Installation guidance, teaching examples and the other application's workflow are not blanket runtime prerequisites.

The shared state links the brief, research questions, evidence, ordered slides, narrative and established design through stable IDs. Workers receive selected slides, relevant evidence, neighboring context and review declarations. Changes to the brief, narrative, shared design or order invalidate the whole deck's relevant state. Complete source/evidence mappings permit local invalidation; incomplete or unlinked records conservatively expand it. Hidden slides and visible neighbors both remain in scope. Any relevant change makes the final deck review stale.

State files remain private. Revision values must be refreshed against real artifacts; the helper does not open referenced files or detect an unrecorded external edit. A current fingerprint proves only that recorded dependencies match. Design approval records an established decision under the authorized scope and does not add a new permission gate.

## Mechanical measurements

These measurements establish reduced payload or repeated work, not universal token savings.

| Measurement | Baseline / full path | Optimized / selected path | What was verified |
| :--- | ---: | ---: | :--- |
| Rule retrieval, Unicode characters | 52,965 for the complete library | 11,998 for the index plus complete R007 and R014 | Selected rules retain policy, exceptions and validation. This pair illustrates payload size; other tasks may require more rules. |
| Synthetic 12-slide task state, Unicode characters | 10,319 for the complete record | 5,000 for slide 6 with slides 5 and 7 as context | Shared brief, narrative, design and relevant evidence remain present. Small records may gain little or grow because of metadata. |
| Keynote read-only inventory calls | 2 | 1 | Actual adapter code in a controlled JXA host simulation returns the same inventory, with and without PDF export. |
| Keynote edit inventory calls | 2 | 2 | The expected-source guard and saved-result collection remain separate. No Mac execution is claimed. |
| PowerPoint intermediate exports | 2 PNGs for all pages | 1 PNG for the selected page | The selected PNG bytes and decoded 1920 × 1080 pixels are identical on the same synthetic source. |

The PowerPoint comparison also preserved file hashes and before/after inventories and exercised read-only open, close and reopen. The two sequential calls took 10.96 and 8.34 seconds respectively. Startup and caching differ, so this single pair does not establish latency savings. No new native save, editability, animation or aesthetic certification was performed for that renderer check.

## Controlled instruction comparison

The evaluation used `gpt-6-astra` with `ultra` reasoning. Counts below are the aggregate of A, B and C in one evaluation turn per version. The cases share a session so later tasks can reuse relevant work. The logs do not provide dependable per-case token boundaries; no per-case token savings are inferred.

| Metric | Baseline | Optimized evaluation |
| :--- | ---: | ---: |
| Input tokens | 1,293,187 | 1,311,733 |
| Cached input tokens | 1,219,328 | 1,227,264 |
| Uncached input tokens | 73,859 | 84,469 |
| Output tokens, including reasoning | 11,538 | 11,345 |
| Model responses | 17 | 17 |
| Outer tool calls | 16 | 16 |
| Returned tool-text characters | 326,594 | 370,656 |
| Elapsed seconds | 363.46 | 365.48 |
| Deck builds / renders / visual revisions | 0 / 0 / 0 | 0 / 0 / 0 |

Input totals increased 1.4%, uncached input increased 14.4%, and output decreased 1.7%. **This comparison does not demonstrate end-to-end token or latency savings.** Both runs recovered truncated batched output, and the optimized run read additional routing material. The observed reads establish redundant work; they do not isolate the exact token cost of each cause. After the evaluation, output guidance was clarified to check combined read size and recover only missing sections. That clarification has not received a second model benchmark and is not credited with savings.

Measurements sum per-response `token_usage_record.usage` records, deduplicated by thread and response ID. They exclude parent implementation work and later accounting follow-ups, and never sum cumulative counters. Cached input is a subset of input; reasoning output is a subset of output. Outer calls count model-visible orchestration calls, not every nested operation; the baseline includes one agent communication call. Tool-text counts measure returned payload strings, not the exact text remaining after host truncation. No images were supplied to these planning evaluations, and separate image-token accounting is unavailable. Cache behavior, stochastic execution and one trial per version prevent generalization or billing estimates.

| Quality dimension | Observed result in both evaluations | Limit |
| :--- | :--- | :--- |
| Scope and stability | A remains a local font repair. C retains all six refined titles and the established visual design. | No real candidate file was edited. |
| Narrative and titles | B connects equal shortfalls, replacement choice, controlled comparison, quantitative answer, inference boundary and synthesis. | This is a reasoned review of proposals, not an audience-comprehension test. |
| Scientific integrity | Both retain 0.40/0.10 MtCO2, common assumptions, modeled replacement scope and missing uncertainty. Neither claims net whole-grid change or a policy winner. | The evidence is synthetic. |
| Visual contribution | Both propose source-specific cutout scenes, a two-branch calculation, aligned mixture/emissions comparisons and a qualified visual synthesis. | Proposed detail does not prove rendered aesthetics. |
| Native delivery | Both keep content, editability, full-slide rendering and relevant playback as separate required checks. | File validity and editability are not measured by these text-only cases. |

The optimized evaluation used the frozen 57-file runtime package with SHA-256 `e2c0e72b67a8b2b4595185d9ea8a98569cd7abc743f0b35fc859bd9944508957`. The final source subsequently added selected review declarations to task-state packets and clarified output batching. Those changes have focused code checks where applicable; they are not included in the model-usage comparison. No favorable rerun has replaced the initial result.

## Validation boundaries and remaining work

Independent review caught incomplete evidence mapping that could leave local review declarations current after an unmapped evidence change. The fix treats incomplete sources and evidence as global dependencies; unlinked questions receive the same conservative handling. Regression cases also cover hidden-slide neighbors, old and new order context, deleted slides, changed assumptions, shared formatting, source revisions and stale whole-deck reviews. Reference queries retain parent scientific qualifications and fail on unknown or ambiguous selections.

The final automated suite contains 248 tests. Six are environment skips: five filesystem-link checks and the real-Mac Keynote integration test. Two packaging tests initially hit Windows `Access denied` while renaming disposable test directories; both passed unchanged when rerun in a separate writable directory outside OneDrive. The remaining 240 tests passed in the suite. The isolated rerun also passed all ten documentation-link tests. Package builders include the same 57 runtime files, and the repository-content audit found no private or generated material in the publishable set. Actual installed files were never used as test destinations.

The four canonical capability documents, scientific-fidelity rules, figure guidelines and README files remain unchanged. Code and package checks establish runtime consistency, not the aesthetic quality of every future presentation. Full final review still includes every slide, hidden content, scientific meaning, native editability and actual rendered appearance. An unavailable required check remains pending.

The source is suitable for a controlled pilot, but Phase 1 has not yet demonstrated its full presentation-quality and efficiency success criterion. Keep it on the optimization branch for review before main-branch integration or replacing an installed skill. Shared-state maintenance and selective retrieval add overhead to small tasks; conservative invalidation can correctly expand work to the whole deck. Existing successful analysis must be reusable in practice, not merely representable in a schema.

The next useful evaluation is a paired full presentation task with real native authoring and independent review of both outputs. It should measure scientific retention, narrative, visual quality and editability alongside tokens, not replace those criteria with call counts. Mac Keynote and browser ChatGPT Work execution also remain unverified. No installation update is part of this change.
