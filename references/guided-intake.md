# Guided presentation intake

A short request such as “Use palate-by-sherry to polish my PPT” is sufficient to start. Match the skill without requiring a long brief or exact punctuation. Obtain the PPTX from supplied files/current workspace; ask for the missing file in ordinary chat when needed, not through a text-only choice tool.

## Native choice cards

Use the host's available user-input tool. Prefer `request_user_input_async` when present: its `questions` entries take `title` and optional `options` strings. Each choice set represents one single-choice question; the host also permits a custom text answer. This is an in-chat selection card, not an operating-system modal created by the skill.

Translate visible questions and labels into the user's language while preserving stable field values. Never add a redundant “Other” option when the host supplies custom input. A suggested/preselected option is not an answer until the user submits it. Do not infer answers from elapsed time. Wait for required input before the dependent transformation; source inventory and visual analysis can continue independently.

If only `request_user_input` is available, respect its mode and option-count restrictions. Group a longer menu into follow-up choices when necessary. When neither tool is available, ask the same concise numbered choices in chat. Do not claim a popup was displayed when it was not.

## Branches

| Step | Choices | Skip when |
| :--- | :--- | :--- |
| Setting | Internal tutorial, internal research, external | Already specified |
| External audience | Experts, C-suite/executives, general audience | Audience already known; internal branch |
| Duration | Profile default and common times; custom minutes | Time explicitly supplied |
| Depth | Let Palate decide, key takeaways, full technical detail | Depth or delegation already supplied |

Ask the setting first. Ask external audience only after that branch is selected. Duration and depth are independent and can share one short question-tool call. Use named profile durations as suggested choices, not silently submitted answers. Preserve current-request overrides and custom audiences, times and explicit constraints. Do not identify an external expert talk as a seminar or a government project merely from its audience.

When the user chooses “Let Palate decide,” technical depth is delegated. Choose it from the actual source, audience, available time and purpose after inspection, and record the decision in the transformation context. Do not mechanically equate expertise with every equation or duration with slide count. Keep essential qualifications visible and retain supporting detail in a traced location.

Use the polish request as the purpose when no narrower purpose is supplied. Ask an additional goal/familiarity question only when it changes a consequential design decision. Do not ask users to select fonts, palettes or layouts before ordinary polishing.

## Router and state

[guided_intake.py](../scripts/guided_intake.py) uses [choice configuration](guided-intake.json) and [context profiles](presentation-contexts.json). It returns stable question IDs, semantic option values and a ready-to-call async question payload. It does not call the UI itself; the agent invokes the available host tool. Task-local state is private and should be saved outside tracked paths.

```text
python scripts/guided_intake.py start --output build/intake-01.json
python scripts/guided_intake.py answer build/intake-01.json --field scenario --value external --output build/intake-02.json
python scripts/guided_intake.py next build/intake-02.json
```

Map the actual selected label to its semantic value; normalize custom durations without changing the user's meaning. `--known` accepts a JSON object of fields already supplied in the request. Supplied information skips its question. A custom audience uses `audience`/`audience_expertise`; arbitrary numeric times are supported. Single-page monthly update profiles route out of scope.

On completion, briefly state the resolved audience/time/depth and begin design. No extra approval is needed for the already requested polishing. Apply the [design system](design-system.md), audience priorities and [scientific fidelity](scientific-fidelity.md); the dialogue chooses the context, not a fixed template.
