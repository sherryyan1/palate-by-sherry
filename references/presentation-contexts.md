# Presentation contexts

Different talks ask different things of their listeners. A research meeting may need methods available for discussion; a tutorial may need a mechanism developed step by step. These profiles help **palate** turn a named setting into a starting brief, then adapt the explanation to the supplied slides and current request. They do not select a fixed template.

## Starting points for the brief

The durations below are suggestions when the user names the corresponding context and has not supplied a time. The [JSON profiles](presentation-contexts.json) hold the runtime values; the design emphasis describes choices to evaluate against the actual research.

| Context and suggested duration | Audience and design emphasis |
| :--- | :--- |
| Internal research, 60 min | For a research group, make the research question, methods and evidence easy to examine and discuss. |
| Internal tutorial, 10 min | For a research group, develop the concept or mechanism in a sequence that makes the connection between steps clear. |
| Government project briefing, 30 min | For project meeting participants, use the meeting's stated purpose to decide which results, implications and qualifications need attention. |
| Expert seminar, 60 min | For an expert audience, make the contribution clear and provide enough methods, assumptions and uncertainty to assess the evidence. |
| General-audience talk, 30 min | For a general audience, define the terms and explain the mechanisms needed to understand the finding and its significance. |

Single-page monthly progress updates are outside this multi-slide workflow. Their profile is marked out of scope in the runtime configuration.

## What the profile settles, and what still needs an answer

Use the context named by the user rather than inferring a specific event from audience expertise alone. An external expert audience, for example, does not by itself establish that the presentation is a seminar or a government project briefing. Relevant familiarity, technical depth and purpose still come from the brief and source.

| Information | How to use it |
| :--- | :--- |
| Named setting and audience class | Reuse the corresponding profile without inventing more detailed subject familiarity. |
| Explicit duration or other current constraint | Keep the user's instruction; it overrides the profile. |
| Missing duration | Offer the profile duration as a suggestion and obtain the user's answer before the dependent design work. |
| Technical depth | Resolve from the user's answer or delegated judgment after inspecting the slides; the profile does not set it. |
| Slide count and Q&A allocation | Use them when supplied; do not derive them from duration. |

Available time guides pacing and how fully the reasoning can be developed. An expert talk can still need conceptual support, and a longer presentation can still benefit from a selective account of the research. Keep the qualifications needed to interpret a result regardless of the suggested emphasis.

The [guided intake](guided-intake.md) defines how to collect missing answers. Once the brief is resolved, use the [design system](design-system.md) to choose a structure that serves the audience and preserves the evidence.
