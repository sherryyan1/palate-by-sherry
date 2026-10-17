# From research material to slides

An existing deck is one starting point, not a prerequisite. Accept rough notes, a paragraph describing the research, an outline or a paper, and use the same audience-led design judgment to develop the presentation. Establish what material the user has supplied before asking for anything else; do not send someone away to prepare slides that palate is meant to help create.

## Choose the path from the material and the request

| Starting material | What palate does | What remains to establish |
| :--- | :--- | :--- |
| Editable slides | Inspect the source structure and rendered pages, then refine or restructure the explanation. | Reuse the source application unless another delivery was requested. |
| Rough text, notes or an outline | Identify the intended message, organize a supported argument and create the slides through native authoring. | Ask about consequential gaps in the content and the delivery application when they are unknown. |
| A paper or manuscript | Read the research and its evidence, then build a presentation around the question and contribution the audience needs to understand. | Resolve the intended focus if several materially different talks are possible; identify missing evidence or unreadable material. |

Use the request to establish a document's role. A PDF can be a paper, an exported deck or a visual reference; its file extension does not settle that question. An exported slide PDF is not an editable source, but it can support a new reconstruction when requested and when its content can be verified. Distinguish that work from preserving the original native objects.

For files, the read-only router supports explicit source intent:

```text
python scripts/presentation_route.py "existing.pptx"
python scripts/presentation_route.py "outline.md" --source-kind text --target pptx
python scripts/presentation_route.py "manuscript.pdf" --source-kind paper --target keynote
```

Use `text` or `paper` only when the supplied material and request support that interpretation. The default remains `slides`. The document routes recognize bounded file structures and report the next step; they do not extract the paper, verify its science or create a deck. Read pasted text directly in the host rather than requiring a file for the router. Other readable source formats can be handled through an available document reader, with the same content checks; do not rename unsupported files to bypass a route rejection.

## Read for the talk, not for a page-by-page conversion

For a paper, inspect the main text together with the relevant figures, tables, equations, captions, citations and supplementary material. Read rendered pages where extraction cannot establish a symbol, panel association or qualifier. If only an abstract or excerpt is available, identify that coverage and use it for the explanation it actually supports. Request the missing section or figure when it is necessary for the intended talk, rather than requesting an already prepared deck.

Organize around the research question, why it matters, the approach, the central evidence and the qualified contribution. Adapt that sequence to the audience and purpose; a tutorial can develop a mechanism before a result, while a research discussion may need methods and uncertainty close to the finding. A paper's section headings and paragraph count do not determine the slide sequence or slide count.

Rough notes may describe a completed study, proposed work or an idea that has not yet been tested. Preserve that status. Clarify the claim or missing evidence when it affects the scientific message, and continue independent organization while waiting. Do not turn an intended analysis into a completed result, fill an empty results section with plausible numbers, or invent a citation. If the supplied material supports only an outline or design proposal, identify that deliverable instead of presenting an invented finished study.

When sparse notes call for a conceptual introduction or tutorial, develop the needed background from verifiable references and preserve their attribution. Distinguish that background from the user's own study and findings. No study results are required for a conceptual explanation, but factual additions still need support; identify any unavailable evidence instead of filling the gap with plausible claims.

## Establish the delivery without assuming a source application

Reuse the shared [presentation brief](redesign-intake.md): setting, audience when relevant, duration, venue screen and depth. Keep the helper's existing context schema; record source type, delivery application, content coverage and language in the private authoring context rather than adding arbitrary intake fields.

Text and papers have no source presentation application. Reuse an explicit PowerPoint or Keynote request; otherwise ask which editable delivery the user wants. This is an authoring choice, not a conversion request. Check the available creation tools and native review path before promising that file. The bounded PowerPoint and Keynote adapters cannot create a new deck from a paper.

Use a selected 4:3 or 16:9 canvas. An explicit `not_sure` answer keeps an existing deck's canvas. When there is no source canvas, use 16:9 as a disclosed provisional design choice and keep the venue ratio unconfirmed; do not describe the default as a screen measurement. Preserve the source language unless a change was requested. If mixed-language material leaves the intended slide language unclear, ask rather than inferring it from the conversation or README language.

## Make the evidence traceable through authoring

Before summarizing, establish a private source snapshot and content ledger. For a file, record its identity and the relevant page, section, paragraph, figure, table or equation. For pasted text, retain a task-local snapshot with stable paragraph identifiers. Map each output claim, figure and important qualification back to that material, following [scientific fidelity](scientific-fidelity.md#content-changingrebuilding-path).

Create a working narrative and slide outline from that map, then author the deck. Proceed with supported design decisions without requiring approval of every outline; ask when an unresolved scientific interpretation or a consequential change needs the user's judgment. Use [explanatory illustrations and diagrams](design-system.md#visual-treatment-for-text-heavy-slides) to make difficult material intelligible, and split complex explanations where useful graphics and readable text need more room.

Retain complex figures when accurate reconstruction cannot be verified. A figure image can be placed in an otherwise editable deck, with its internal editing limit reported. Preserve its labels, legend, caption meaning, uncertainty and attribution. Rebuilding a chart requires verified data and appropriate units and scales; a plotted curve alone does not supply exact values. Seek an editable figure or data only when needed for the chosen transformation.

Use the selected [PowerPoint](pptx-workflow.md#create-a-new-deck-from-research-material) or [Keynote](keynote-workflow.md#create-a-new-deck-from-research-material) authoring path. Review content coverage, rendered appearance and native editability separately. Compare output against the supplied material; there may be no original slides to compare. Report the source coverage, material omissions or questions, actual checks and any pending native review. If creation or review is unavailable, distinguish an outline or candidate from a completed, reviewed editable deck.
