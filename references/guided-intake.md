# Guided presentation intake

The brief should settle the decisions that change how the research is explained. A request such as “Use palate to polish my slides” is enough to begin: use the supplied deck and context, then ask only for information that affects the audience's understanding. Users can leave visual choices and technical depth to palate.

Identify the supplied file with [presentation_route.py](../scripts/presentation_route.py). If the deck is missing, ask for it in ordinary chat because the choice tool accepts text rather than attachments. The [Keynote workflow](keynote-workflow.md) covers native Keynote sources and delivery; both formats use the same presentation brief.

## From the brief to a design decision

Start with the setting because it provides context for the design decisions. On the external branch, establish the audience next so the explanation can account for what listeners know and what they need from the talk. Time and depth then help decide how much of the reasoning should unfold on the main slides. They can share a question-tool call because neither depends on the other's answer.

| Question | Choices | Ask when |
| :--- | :--- | :--- |
| Setting | Internal tutorial, internal research, external | The setting has not been supplied. |
| External audience | Experts, C-suite/executives, general audience | The setting is external and the audience is unknown. |
| Duration | Profile suggestion, common times or custom minutes | The request gives no explicit duration. |
| Depth | Let palate choose, key takeaways, full technical detail | Neither a depth nor delegation has been supplied. |

Use [context profiles](presentation-contexts.json) to suggest a duration, while leaving the choice open until the user accepts it. Preserve explicit times, custom audiences and other constraints from the current request. An expert audience alone does not establish whether the event is a seminar or a government project briefing.

When users select “Let palate choose,” inspect their slides before deciding the depth and record that decision in the transformation context. Consider the reasoning listeners need to follow and the evidence they need to check within the available time. Keep essential qualifications beside the finding, and give supplementary detail a traceable place in notes or an appendix. Expertise does not require every equation to be displayed, just as duration does not imply a fixed slide count.

Use the polish request as the purpose unless a narrower goal has been supplied. Ask about a specific goal or subject familiarity when the answer would change a consequential design choice. Fonts, palettes and layouts are part of the design work; ordinary polishing should not require users to choose them in advance.

## Language choices

The README version, conversation language and slide language serve different purposes. Reuse an explicit presentation-language request independently of the language used for the conversation or documentation. Preserve the source language when no change is requested; when the intended language is ambiguous, clarify it before rewriting. This keeps a Korean discussion of an English conference presentation from silently becoming a Korean slide deck.

Record language preferences in the private brief alongside the helper's audience, time and depth context. The choice helper does not accept extra language fields in its state or `--known` input. Translation is content-changing work, so use the native authoring path and review its scientific meaning against the source as described in [scientific fidelity](scientific-fidelity.md).

## Presenting the questions

Use the host's available input tool to keep the brief easy to answer. Translate visible questions and labels into the user's language while retaining stable field values, so the selected context reaches the runtime unchanged.

| Available tool | Presentation | Contract |
| :--- | :--- | :--- |
| `request_user_input_async` | In-chat choice cards, with a custom text answer | Prefer this tool when available. Each `questions` entry takes `title` and optional `options` strings; each set is single-choice. |
| `request_user_input` | Choice cards within the host's limits | Respect its mode and option-count restrictions; divide longer menus into follow-up choices when needed. |
| Neither | Concise numbered choices in chat | Ask for the same context without claiming that a popup was displayed. |

These cards are supplied by the host, rather than an operating-system modal created by the skill. When the host provides custom input, use that facility instead of adding a redundant “Other” option.

A suggested or preselected option becomes an answer only when the user submits it. Elapsed time does not supply consent or missing context. Wait for required answers before the dependent transformation, while continuing source inventory and visual analysis where those tasks are independent. Follow the [writing style](writing-style.md) when explaining the resulting design choices.

## Runtime state

[guided_intake.py](../scripts/guided_intake.py) reads the [choice configuration](guided-intake.json) and [context profiles](presentation-contexts.json), then returns question IDs, semantic option values and an async question payload. The agent calls the host tool; the helper itself does not display UI. Save task state outside tracked paths because it contains the presentation brief.

```text
python scripts/guided_intake.py start --output build/intake-01.json
python scripts/guided_intake.py answer build/intake-01.json --field scenario --value external --output build/intake-02.json
python scripts/guided_intake.py next build/intake-02.json
```

| Input | Handling |
| :--- | :--- |
| Selected label | Map the submitted label to its semantic value. |
| Custom duration | Normalize the number without changing the requested time. |
| `--known` | Supply a JSON object of existing brief fields to skip their questions. |
| Custom audience | Use `audience` and, where supplied, `audience_expertise`. |
| Monthly single-page update | Return the out-of-scope route for this multi-slide skill. |

Once the brief is resolved, state the audience, time and depth briefly and begin the requested design work without another approval step. The [design system](design-system.md) and [scientific fidelity](scientific-fidelity.md) guide the choices that follow; the brief provides their context rather than selecting a fixed template.
