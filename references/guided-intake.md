# Guided presentation intake

The brief should settle the decisions that change how the research is explained. A request such as “Use palate to polish my slides” is enough to begin: use the supplied slides, text or paper and context, then ask only for information that affects the audience's understanding. Users can leave visual choices and technical depth to palate.

This is an agent-facing interaction reference. [Question order](#from-the-brief-to-a-design-decision) explains which answers depend on earlier ones, [language choices](#language-choices) covers translation decisions, and [runtime state](#runtime-state) defines the helper's input and output. For the design reasoning behind the brief fields, see [Presentation brief](redesign-intake.md).

Identify the starting material before asking for more. Existing slides, rough text and papers all use this brief; follow [source-to-slides](source-to-slides.md) for the new-deck paths. Read pasted text directly, and use [presentation_route.py](../scripts/presentation_route.py) for files with the appropriate explicit source role. Do not ask for a deck when the user has supplied text or a paper. If no usable content has been supplied, ask what the talk should cover; request an attachment only when a file is actually needed. The choice tool accepts text, so attachment requests belong in ordinary chat.

## From the brief to a design decision

Start with the setting because it provides context for the design decisions. On the external branch, establish the audience next so the explanation can account for what listeners know and what they need from the talk. Then collect the duration, venue screen shape and technical depth together when the host allows three questions in one call. Time and depth determine how much of the reasoning should unfold on the main slides; the screen shape establishes the canvas available to present it. These answers are independent, so the user can supply them in the same round.

| Question | Choices | Ask when |
| :--- | :--- | :--- |
| Setting | Internal tutorial, internal research, external | The setting has not been supplied. |
| External audience | Experts, C-suite/executives, general audience | The setting is external and the audience is unknown. |
| Duration | Profile suggestion, common times or custom minutes | The request gives no explicit duration. |
| Venue screen | 16:9 widescreen, 4:3 standard, not sure | The screen shape or an explicit decision to keep an existing source canvas has not been supplied. |
| Depth | Let palate choose, key takeaways, full technical detail | Neither a depth nor delegation has been supplied. |

Use [context profiles](presentation-contexts.json) to suggest a duration, while leaving the choice open until the user accepts it. Preserve explicit times, custom audiences and other constraints from the current request. An expert audience alone does not establish whether the event is a seminar or a government project briefing.

Ask which shape is closer to the venue screen, not which ratio the source file already uses. A source deck can be 16:9 even when the room has a 4:3 screen. Record an explicit ratio as `screen_aspect_ratio` and use it for the target canvas and layout. If the user is unsure or explicitly asks to keep the current slide shape, record `not_sure`. Retain an existing source canvas without treating its ratio as a confirmed venue measurement. For a new deck with no source canvas, disclose a provisional 16:9 design choice while keeping the venue ratio unconfirmed. A missing answer remains pending; do not select this option on the user's behalf.

When the requested ratio differs from the source, follow the native [PowerPoint](pptx-workflow.md#match-the-venue-screen) or [Keynote](keynote-workflow.md#match-the-venue-screen) workflow to set the new output's canvas, redefine its symmetric work area and reflow the content. A canvas change is not permission to stretch figures, crop evidence or shrink text below the type minimum. The intake helper records this decision; it does not resize slides or establish that the changed layout has been visually verified.

When users select “Let palate choose,” inspect their supplied material before deciding the depth and record that decision in the transformation context. Consider the reasoning listeners need to follow and the evidence they need to check within the available time. Keep essential qualifications beside the finding, and give supplementary detail a traceable place in notes or an appendix. Expertise does not require every equation to be displayed, just as duration does not imply a fixed slide count.

Use the request to prepare or refine the research presentation as the purpose unless a narrower goal has been supplied. For rough notes or a paper, ask about a consequential gap or materially ambiguous focus rather than requiring a complete brief or finished slides. Record source type and the chosen delivery application in the separate authoring context; these are not extra fields in the intake helper's state. Ask about a specific goal or subject familiarity when the answer would change a consequential design choice. Fonts, palettes and layouts are part of the design work; ordinary polishing should not require users to choose them in advance.

Table colors have a separate choice after source inspection or when a text-only slide is redesigned as a table. Follow the [two-option comparison](design-system.md#table-color-options): show Nature-inspired and deck-matched versions of the same representative table, keeping all other design and content decisions equal. Ask through the available question tool unless the current request already supplies or delegates that decision. Do not ask this question when no tables are present or planned, or make it a required global brief field. A pending table choice holds final table coloring, while independent inspection and layout work can continue.

## Language choices

The README version, conversation language and slide language serve different purposes. Reuse an explicit presentation-language request independently of the language used for the conversation or documentation. Preserve the supplied material's language when no change is requested, resolving an unclear slide language for mixed-language sources through the source-to-slides workflow. For a requested translation, follow the [scientific translation preflight](scientific-fidelity.md#scientific-translation), resolving an unclear target before rewriting and reusing confirmed terminology decisions. This keeps a Korean discussion of an English conference presentation from silently becoming a Korean slide deck.

Record the requested target and terminology decisions in the private content ledger alongside the brief. The choice helper does not accept extra language fields in its state or `--known` input. Its `ready` status settles audience, time, screen shape and the requested depth or delegation; it does not resolve translation questions or authorize rewriting while required language answers are pending. Translation uses the content-changing authoring and review path in [scientific fidelity](scientific-fidelity.md).

## Presenting the questions

Use the host's available input tool to keep the brief easy to answer. Translate visible questions and labels into the user's language while retaining stable field values, so the selected context reaches the runtime unchanged.

| Available tool | Presentation | Contract |
| :--- | :--- | :--- |
| `request_user_input_async` | In-chat choice cards, with a custom text answer | Prefer this tool when available. Each `questions` entry takes `title` and optional `options` strings; each set is single-choice. |
| `request_user_input` | Choice cards within the host's limits | Respect its mode and option-count restrictions; divide longer menus into follow-up choices when needed. |
| Neither | Concise numbered choices in chat | Ask for the same context without claiming that a popup was displayed. |

The host supplies these cards; the Skill does not create an operating-system modal. When the host provides custom input, use that facility instead of adding a redundant “Other” option.

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
| Screen shape | Use `screen_aspect_ratio` with `16:9`, `4:3` or `not_sure`. Normalize ratio forms such as `16 x 9` or `4 / 3`; reject unsupported ratios rather than silently selecting the closest one. |
| `--known` | Supply a JSON object of existing brief fields to skip their questions. |
| Custom audience | Use `audience` and, where supplied, `audience_expertise`. |
| Monthly single-page update | Return the out-of-scope route for this multi-slide skill. |

The helper persists canonical screen values in schema-version-1 answer states and includes the selected value in the ready context. Existing states that lack `screen_aspect_ratio` remain readable and return the missing question instead of assuming a ratio. Both a submitted choice and `--known` use the same normalization, so supplied answers are not asked again. `not_sure` is an explicit answer and completes this part of the brief while retaining an existing source canvas or using the disclosed provisional canvas for a new deck.

Once the brief and any required translation clarifications are resolved, state the audience, time, screen shape and depth briefly and begin the requested design work without another approval step. The [design system](design-system.md) and [scientific fidelity](scientific-fidelity.md) guide the choices that follow; the brief provides their context rather than selecting a fixed template.
