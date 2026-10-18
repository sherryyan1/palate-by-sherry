# Evaluate editorial choices in scientific titles

Audience: maintainers and scientific reviewers. Use this supplement to the existing [storytelling evaluation](storytelling-evaluation.md) when changing [editorial judgment](../references/editorial-judgment.md). It contains original synthetic evidence briefs and actual candidate title sequences prepared for this revision. These are reproducible instruction-level exercises, not real study results, rendered decks or measured audience improvements. No publisher wrote the candidates.

## Keep the comparison interpretable

Fix an international academic audience, a short research briefing, English slides and the evidence below. The original titles are deliberately generic supplied baselines. They are not outputs from an earlier model or the previous skill. Compare original and selected sequences against exactly the same evidence; do not call the comparison an old-skill/new-skill experiment. A reproducible model baseline would also need its exact skill revision, prompt, model configuration and retained outputs.

For a new evaluation, give a reviewer the raw brief and evidence before the examples. Ask for a sequence and consequential title decisions, then compare with the scientific boundaries here. Any supported wording can pass. Record actual output, evidence links, neighbor relationships, selected angle, rejected alternative and the reason for retaining or revising it. Keep real research and review records private. Use the existing title-extraction helper with an explicit `outline` inventory when no deck exists; its output remains unreviewed.

## Four full sequence exercises

Each exercise has six slide briefs: an observation, a complication, a question, a method, a quantitative result and a synthesis. This is a fixture structure, not a deck template. Bodies must show the supplied evidence and qualifications at the selected depth. A title-only inventory cannot establish that a delivered deck contains them.

### Energy: same shortfall, different replacement supply

Use Q-E and the [existing two-grid evidence E1-E4](../references/storytelling-examples.md#a-synthetic-investigation): fixed demand, 1.0 TWh loss in both grids, fossil replacements 0.8 and 0.2 TWh, fixed factor 0.5 tCO2/MWh, other replacement supply zero operational emissions by assumption. Model outputs are 0.40 and 0.10 MtCO2. There are no whole-grid baselines, lifecycle results or uncertainty estimates.

| Slide | Original title | Selected title | Role, support and next step |
| :--- | :--- | :--- | :--- |
| E-I1 | Hydropower losses | Two grids face the same hydropower shortfall | Observation, E1; introduces a matched input. |
| E-I2 | Electricity systems | Replacing 1.0 TWh leaves a choice of supply | Complication, E1-E3 and fixed demand; motivates the mix question. |
| E-Q | Research question | How does the replacement mix change modeled emissions? | Q-E; prepares the accounting comparison. |
| E-M | Methods | Hold demand and hydro loss fixed; compare replacement mixes | Method, E1-E3; prepares comparable outputs. |
| E-R | Grid comparison | Equal hydro losses yield different replacement emissions | Answer, E1/E4; annotation supplies 0.40 versus 0.10 MtCO2 and modeled status. |
| E-C | Conclusions | The same shortfall can carry different modeled replacement emissions | Synthesis of Q-E; retain operational boundary and assumptions, without a whole-grid or policy ranking. |

The opening promises an explanation of how equal inputs yield unequal replacement burdens. The method and result fulfill it. The final slide generalizes only within the simplified accounting assumptions. A source-specific breakdown belongs in the body; the ratio alone would underexplain the result.

### Medicine: the absolute size of an observed difference

Q-M asks what the trial establishes about 30-day hospitalization. Synthetic trial M1 randomly assigns 2,000 adults, 1,000 to each group, with complete 30-day outcome ascertainment. M2 records 20 hospitalizations in A and 10 in B. M3: no interval, power analysis or adverse-event results are supplied. This is a teaching fixture, not medical advice.

| Slide | Original title | Selected title | Role, support and next step |
| :--- | :--- | :--- | :--- |
| M-I1 | Treatment effects | A relative reduction needs an absolute baseline | Conceptual opening; the audience must interpret an outcome comparison. |
| M-I2 | Clinical relevance | How large is the difference in absolute terms? | Complication; gives M2 a clinically interpretable question without promising benefit. |
| M-Q | Study aim | What did the trial establish at 30 days? | Q-M; motivates design and endpoint. |
| M-M | Trial design | Compare 30-day hospitalization in two randomized groups | Method, M1; keep population, denominator and complete follow-up visible. |
| M-R | Treatment outcomes | Hospitalizations were 2% versus 1% at 30 days in this trial | Observation, M2; identify A/B, counts and the 1 percentage-point difference. |
| M-C | Clinical implications | The observed reduction leaves benefit-harm judgment open | Synthesis, M2/M3; uncertainty and missing harms prevent an assured recommendation. |

The Introduction's two questions have different jobs: absolute scale and evidential scope. The result answers the first; the ending bounds the second. Review their spoken cadence; combine or rephrase them if the actual talk makes this repetition tiring. Randomization is retained, but a lower observed incidence alone does not supply its precision, clinical value or harms.

### Computing: a lead that depends on the test

Q-C asks whether a benchmark advantage persists under a specified distribution shift. C1 evaluates the same two models on two fixed, fully labeled test sets of 1,000 cases each. C2: on the familiar set A is correct on 900 and B on 880; on the shifted set A is correct on 600 and B on 750. C3: no latency, energy, training-budget or deployment results are supplied. No universal model ranking follows.

| Slide | Original title | Selected title | Role, support and next step |
| :--- | :--- | :--- | :--- |
| C-I1 | Model performance | Model A holds a narrow lead on the familiar test | Observation, C2; identifies the starting expectation. |
| C-I2 | Distribution shift | The leading model faces a different test distribution | Complication, C1; makes the next question necessary. |
| C-Q | Research question | Does the lead survive the shifted test set? | Q-C; promises a test rather than broad deployment advice. |
| C-M | Evaluation design | Evaluate both models on the same two fixed test sets | Method, C1; prepares comparable observed accuracies. |
| C-R | Benchmark results | The benchmark lead reverses on the shifted test set | Answer, C2; show 90/88% and 60/75%, labels, denominators and set definitions. |
| C-C | Deployment | A benchmark lead does not establish robustness to this shift | Synthesis, C2/C3; no efficiency or general superiority claim. |

The comparison fulfills the opening's promise. A decline within A is 30 percentage points, not 30%; B leads A by 15 percentage points on the shifted set. That insight does not say which system is more efficient or suitable for an untested deployment.

### Social science: an aggregate advantage that reverses within groups

Q-S asks whether an observed pay advantage persists within occupation. S1 contains observational cross-sectional records, with no identification strategy: among 100 trainees, 75 work in high-pay occupation H at mean pay 130 units/hour and 25 in occupation L at 80. Among 100 non-trainees, 25 work in H at 150 and 75 in L at 90. S2 is the weighted aggregation: 117.5 versus 105 units/hour. S3: no precision estimates, longitudinal changes or causal identification are supplied.

| Slide | Original title | Selected title | Role, support and next step |
| :--- | :--- | :--- | :--- |
| S-I1 | Training and pay | Trainees earn more on average in these records | Observation, S2; defines the aggregate comparison. |
| S-I2 | Sample composition | The groups have different occupational mixes | Complication, S1; introduces a reason to inspect the aggregate. |
| S-Q | Research question | Does the pay advantage persist within occupation? | Q-S; a meaningful missing comparison, not a causal question. |
| S-M | Analysis | Compare pay within each occupation | Method, S1; prepares stratified results. |
| S-R | Wage results | Trainees earn less in both observed occupations | Answer, S1; show 130 versus 150 and 80 versus 90 units/hour alongside group counts. |
| S-C | Policy implications | Occupation changes the comparison; causality stays unresolved | Synthesis, S1-S3; the apparent paradox concerns aggregation, not a proven harmful effect of training. |

The ending resolves the apparent contradiction while keeping causality open. Dropping the pooled result would conceal the reason for the question; dropping the strata would invite a policy inference from composition. The two views must remain visible in the connected explanation.

## Candidate comparisons at consequential turns

These publisher-inspired labels are used for this requested evaluation only. Ordinary palate work selects a strategy without generating both options. Candidates are original writing, not publisher examples or exclusive publisher styles.

| Exercise / original | Accessible, BBC-inspired candidate | Analytical, Economist-inspired candidate | palate's selected choice and rejected implication |
| :--- | :--- | :--- | :--- |
| Energy / Grid comparison | Why do equal hydro losses bring different emissions? | Same shortfall, fourfold burden | E-R above. The first risks implying an unestablished total-emissions increase; the second needs the modeled replacement boundary. The selected title points toward that specific comparison. |
| Medicine / Treatment outcomes | What does a halved hospitalization rate mean here? | Half the rate, a one-point gap | M-R above. Give this audience the absolute observations immediately; neither brevity nor the valid relative calculation should displace denominators, follow-up and uncertainty. |
| Computing / Benchmark results | Which model handles this shifted test better? | A benchmark winner loses its lead | C-R above. The contrast directly answers Q-C; the question would delay an available finding, while the other candidate leaves the changed condition unstated. |
| Social science / Wage results | Why does the pay comparison reverse within occupations? | Training pays, until you split the sample | S-R above. The latter invites a causal reading of training and trivializes the confounding problem. A direct within-occupation observation prepares the qualified synthesis. |

At an Introduction turn, the same contrast can ask a question before the investigation and state a finding after it. Selection depends on what the audience has already seen, not merely which wording is more striking. The energy fixture's existing question/contrast and computing fixture's starting lead illustrate this timing.

## Boundary probes and translation

| Probe | Supplied evidence | Acceptable decision / failure to reject |
| :--- | :--- | :--- |
| Materials | A measured property differs at 4 K only; no device or room-temperature test. | Keep the tested property and 4 K condition; reject a deployable or room-temperature breakthrough. |
| Ecology | A 72-hour laboratory response in one species; no generational or field observation. | State a laboratory response; reject evolutionary adaptation, ecosystem resilience or intentional agency. |
| Uncertain rank | Two modeled point estimates with overlapping reported intervals; no rank-probability analysis. | Report the estimate comparison and uncertainty; reject a certain winner or an equivalence claim. |
| Proposed study | Design and expected diagnostics, no completed observations. | Preserve future/planned status; reject a manufactured Results section. |
| Sound over sense | A rhyming phrase changes a precise term or conceals a condition. | Retain the plain accurate term and condition even if the rhyme is lost. |
| Multilingual transfer | Re-express C-R for Chinese, Japanese and Korean academic audiences. | Preserve the two specified test contexts and reversal; adapt syntax naturally without forcing English alliteration. Check certainty and established terms in each language. |

## Assess ten dimensions without conflating them

| Dimension | Observable review evidence |
| :--- | :--- |
| Scientific accuracy | Claims and natural implications fit the evidence, scope, status, units and uncertainty. Independently recompute quantities before editorial assessment. |
| Clarity | A reviewer can paraphrase the intended comparison without decoding a device. |
| Curiosity and engagement | The opening identifies a consequential missing relationship and the sequence pays it off or bounds it. |
| Memorability | A reviewer can later recall the scientific relationship; a memorable pun alone is insufficient. This needs an actual delayed-recall exercise to measure. |
| Narrative coherence | Every slide has a specific predecessor/successor relationship and major results answer identified questions. |
| Audience appropriateness | Definitions, tone and required cultural knowledge fit the fixed brief. |
| Domain suitability | Domain-specific inference boundaries survive the rhetorical choice. |
| Quantitative insight | The meaningful comparison is supported, with denominator, magnitude, baseline and limits. |
| Linguistic naturalness | An academic reader can read the sequence aloud naturally in the delivery language. |
| Restraint | Plain titles remain where useful; no invented gap, hidden qualification, repeated teasing or exaggerated novelty. |

Use an independent scientific reviewer to examine facts and implications, and, where practical, a blind human review of shuffled candidate sets with publisher labels removed. Reveal evidence and neighboring slides, retain disagreements, and compare final sequences under the same brief. Native slide review is separate. Do not replace these judgments with regexes, title length, device counts or an aggregate automated quality score.

For this revision, the authored examples and quantitative checks provide bounded design evidence. The producing agent also reviewed its wording, so the review is unblinded and not independent. Blind human assessment, measured recall/comprehension, real-deck authoring and native appearance/editability remain unperformed. A sound alternative can remain unchanged on a second pass; new edits require an identified defect.
