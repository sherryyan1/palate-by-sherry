# Storytelling examples

Use these examples to practice the judgments in [Find the thread](find-the-thread.md). They show how a title can explain a slide's purpose and connect it to its neighbors without making a stronger scientific claim. They are teaching examples, not templates to insert into a research presentation.

Every grid, value and result below is synthetic. None describes a country, a supplied paper or an established repository finding. Use the actual research evidence when applying the method to a real task; do not borrow illustrative numbers as research facts.

## A synthetic investigation

The question is how the replacement mix affects operational emissions from replacement supply when two grids face the same hydropower shortfall. In this simplified fixture, demand is fixed and each grid replaces all lost generation. Grid A and Grid B have different replacement mixes. Fossil replacement generation has a fixed operational emissions factor of 0.5 tCO2/MWh; the other replacement generation has zero operational emissions by assumption.

| Evidence ID | Quantity | Grid A | Grid B |
| :--- | :--- | ---: | ---: |
| E1 | Hydropower shortfall [TWh] | 1.0 | 1.0 |
| E2 | Fossil replacement [TWh] | 0.8 | 0.2 |
| E3 | Zero-operational-emission replacement [TWh] | 0.2 | 0.8 |
| E4 | Replacement operational emissions [MtCO2] | 0.40 | 0.10 |

The accounting is explicit: fossil replacement [TWh] multiplied by 1,000,000 [MWh/TWh] and 0.5 [tCO2/MWh] gives emissions [tCO2]. Dividing by 1,000,000 converts that result to [MtCO2]. The ratio 0.40 / 0.10 is 4.0. The table contains modeled replacement-supply quantities under fixed assumptions. It does not supply whole-grid baseline totals or the displaced hydropower emission factor, so these values are not established net increases in total grid emissions. It provides no empirical causal identification, lifecycle comparison, uncertainty estimate or policy ranking.

Give this investigation the local question ID Q1. Its reasoning map is: equal hydropower shortfalls → replacement mix → operational-emissions accounting → comparison under the stated assumptions. This map establishes dependencies, not a requirement to use one slide for each arrow.

## Introduction: create a reason to follow

The initial titles name subjects but leave the audience to infer their connection. The revised sequence introduces the shared problem, identifies what remains unexplained and arrives at Q1. It withholds neither an essential qualification nor a known contradictory finding.

| ID | Original title | Diagnosis | Revised title | Support and relationship |
| :--- | :--- | :--- | :--- | :--- |
| I1 | Hydropower losses | Names the input without showing why the comparison matters. | Two grids lose the same 1.0 TWh of hydropower | E1 establishes the common starting point. The next slide asks how each grid fills that gap. |
| I2 | Electricity systems | Changes subjects without explaining the connection. | The shortfall leaves a replacement question | The fixture holds demand fixed and replaces all lost generation. This develops I1 and introduces the variable examined in I3. |
| I3 | Carbon emissions | Gives a topic without connecting electricity replacement to the outcome. | Replacement emissions depend on what fills the gap | The stated accounting links fossil replacement to operational emissions. This explains why the mix belongs in Q1. |
| I4 | Research gap | Announces a category instead of the question this study can answer. | How does the replacement mix change the modeled outcome? | Q1 follows from I3. The next slide must explain a comparison that holds demand and the shortfall fixed. |

The improvement is the chain of reasoning, not the presence of a question mark. A real study may require more background, introduce a different unresolved problem, or begin with a qualified finding. Do not invent a literature gap from this synthetic comparison. A title such as "Why does drought increase emissions?" would additionally assume an emissions increase and a causal interpretation that the fixture alone does not establish.

## Methodology: explain what the comparison permits

| Original title | Diagnosis | Revised title |
| :--- | :--- | :--- |
| Scenarios and model | Lists a category but leaves the comparison and controls unstated. | Hold demand and hydro loss fixed; compare replacement mixes |

This title follows I4 by explaining how the simplified investigation addresses Q1. Both cases have the same 1.0 TWh shortfall; the title must not say that hydropower changes between them. The visible method should show the common conditions, two replacement mixes and the same emissions-accounting operation. Label the factor as an assumption and the outputs as modeled quantities.

The method prepares the next slide to compare outputs on a shared basis. An appropriate explanatory graphic can place the shared shortfall above two native branches, each containing its replacement components and calculation. Small icons may identify components, but the comparison depends on quantities, operations and constraints, not the icons. Keep labels and connectors editable where feasible and follow the existing [visual guidance](refine-the-visuals.md).

This is a transparent scenario comparison, not proof that changing a real grid's replacement mix would cause exactly the displayed change. The simplified assumptions must remain visible at the audience's required depth.

## Results: state what the evidence establishes

| Original title | Diagnosis | Revised title |
| :--- | :--- | :--- |
| Grid comparison | Describes the figure without identifying its contribution to Q1. | Equal hydro losses yield different replacement emissions |

E1 and E4 support this contrast: the same 1.0 TWh shortfall accompanies 0.40 MtCO2 in Grid A and 0.10 MtCO2 in Grid B. A nearby annotation can state the fourfold ratio, with the same operational boundary and modeled status. Do not replace this with a broader claim that one grid is cleaner, more resilient or a policy winner.

This slide follows the controlled comparison and answers Q1 within its stated scope. It should then lead to the replacement breakdown, which explains the difference through E2 and E3 and the fixed factor. A later sensitivity question could ask whether the contrast persists when the factor or other system conditions change, but the fixture contains no sensitivity result to report.

Use a common scale and direct labels to make the contrast inspectable. The supporting graphic should preserve the equal shortfall and unequal replacement shares rather than showing only a large ratio. If adding a second panel makes the mechanism clearer, explain its relationship to the emissions panel. Do not treat an attractive chart as a substitute for that reasoning.

## When the story does not resolve neatly

These independent cases test whether an appealing narrative can remain accurate. They do not extend the two-grid fixture unless explicitly stated.

| Case and supplied evidence | Appropriate title or narrative decision | Unacceptable revision |
| :--- | :--- | :--- |
| Uncertain comparison: a synthetic estimated difference is 0.04 MtCO2 with a 95% interval from -0.03 to 0.11 MtCO2. The interval method is not supplied. | "The estimated difference remains uncertain." Show the estimate and interval, and obtain the interval definition before making a statistical claim. This follows the comparison and motivates the uncertainty discussion. | Declare a winner, infer a precise probability from the unspecified interval, or call the outcomes equivalent. |
| Null result: a supplied test fails to reject its null; the study provides no equivalence test or bound establishing a negligible effect. | "The test does not establish a difference." Keep the tested contrast, estimate, uncertainty and study limitations together. The next slide can examine what the design can detect. | "The treatments are identical" or "There is no effect." |
| Proposal: the material specifies a question, planned controls and an analysis, but contains no completed observations or model runs. | "Paired cases will test how replacement mix affects emissions." Distinguish planned methods, expected diagnostic patterns and decisions they would inform. End with the unresolved question or next test. | Invent a Results section or label an expected pattern as a finding. |
| Already coherent sequence: the equal-shortfall observation, fixed-condition comparison, qualified result and replacement explanation are supported and correctly ordered. | Retain the sequence after checking source support and neighboring relationships. Improve only a specific unresolved defect. | Replace accurate titles with puns, reverse the order for novelty or make wording changes only to increase the edit count. |

For an unresolved finding, the narrative can end with a better-defined uncertainty and an appropriate next investigation. A missing answer does not justify completing the story with a stronger claim.

## Evaluate the sequence

Use the title inventory as a starting point, then compare the original and proposed sequence with the source evidence. The extraction helper returns `status: "unreviewed"` and `narrative_validated: false`; those values correctly describe what the helper has done. It has not judged the argument.

1. Confirm title candidates and actual reading order, including the intended role of hidden slides and appendices. Preserve original titles and stable IDs.
2. Read the visible titles alone. Explain the question and progression they suggest; identify what cannot be inferred without the bodies.
3. Check each slide's role, source support and relationship to both neighbors. Record the benefit of a proposed change, or the reason to retain a sound decision.
4. Map major findings to the question they answer, including partial answers, null results and exploratory findings. Check that no title claims more than its evidence.
5. Re-read the complete sequence after writing and visual construction. Compare the resulting emphasis with the narrative map and scientific qualifications.
6. Repeat the assessment with the same brief and evidence. Retain sound choices unless a specific defect remains; record why any additional change improves the explanation.

An acceptable review names the real transitions and evidential limits rather than declaring the deck "engaging." The story should explain why this slide belongs after the previous one and before the next. It need not maximize questions, assertive headlines, changed slides or rhetorical devices.

Keep task-specific title inventories, narrative maps and review records private and untracked. Extraction tests, editorial judgment, scientific review and native presentation validation establish different things. A successful title extraction cannot establish that a presentation is coherent, accurate, editable or visually polished.
