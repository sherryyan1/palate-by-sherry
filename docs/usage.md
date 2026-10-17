# Usage

Choose the [Codex installation](installation.md#codex-setup) or the experimental [ChatGPT Work web setup](chatgpt-work.md). Both use the same design rules. The web plugin's installation and end-to-end behavior have not yet been tested; its guide explains how to check discovery, resources and available tools before relying on it.

## Start with one sentence

In Codex, share the material you have and choose a request that fits:

| Starting material | Example request |
| :--- | :--- |
| Existing slides | `$palate Polish my slides.` |
| Rough text, an outline or notes | `$palate Create slides from these notes.` |
| A paper or manuscript | `$palate Create a research presentation from this paper.` |

You can attach a file or paste text directly. You do not need to prepare slides first. For an existing deck, the request can be as short as:

```text
$palate Polish my slides.
```

In ChatGPT Work, type `@`, select the installed **palate** plugin or skill, share the material and send the corresponding request. A typed plugin name does not replace selection or confirm installation.

A detailed brief is optional: **palate** uses the information already supplied and asks for missing context that could materially change the design. You do not need to choose fonts, palettes or layouts first. The [format workflow](#powerpoint-and-keynote) explains which native application handles the deck and when an optional conversion needs additional files. When creating a new deck, **palate** asks whether to use PowerPoint or Keynote if you have not specified the delivery application.

## Shape the brief

The audience determines how much context a listener needs to follow the evidence. A tutorial may need definitions and a mechanism developed in stages, while a research group may need assumptions, methods and uncertainty available for discussion. An executive audience may need the supported implications made clear early; a general audience may need the finding connected to a familiar question before encountering technical detail.

Time then shapes how fully that explanation can unfold during the talk. A shorter presentation needs a clear path through the central result, with supporting detail placed where it can still be consulted. A longer talk allows more development, but its length alone does not justify extra density. Essential qualifications stay with the evidence they qualify, and material moved to notes or an appendix remains traceable to its source.

The brief uses these choices to establish the setting and the level of explanation:

| Part of the brief | Choices | Effect on the presentation |
| :--- | :--- | :--- |
| Setting | Internal tutorial, internal research, external presentation | Establishes whether the deck should primarily teach, support research discussion or explain work to an outside audience. |
| External audience | Experts, C-suite/executives, general audience | Guides terminology, conceptual support and the order in which evidence and implications are introduced. |
| Duration | Suggested times or custom minutes | Sets the pace and the amount of explanation that can be developed during the talk. |
| Venue screen | 4:3, 16:9 or not sure | Fits the layout to the chosen proportions. If unknown, **palate** preserves an existing deck's proportions. With no source canvas, it uses a provisional 16:9 layout and states that the venue ratio is unconfirmed. |
| Depth | Let palate choose, key takeaways, full technical detail | Determines how much derivation and supporting detail should be visible, while preserving the evidence needed for interpretation. |

You can write your own answer or provide all the presentation details in your first message. If you select "Let palate choose," **palate** reviews your material and uses your audience and available time to decide how much detail to include. The [presentation contexts](../references/presentation-contexts.md) suggest starting points, including durations; your current instructions take precedence. Slide count and Q&A time are used only when supplied, and single-page monthly updates remain outside this workflow.

An existing deck stays in its original language unless you request a translation; the language of this guide or the conversation does not change that choice. For a new deck, **palate** follows the requested language or the source material and asks if the intended language is unclear. If you request translation without naming the target language, **palate** asks for it before rewriting. It also asks when a technical term has plausible translations that could materially change the scientific meaning, and reuses the terminology you confirm. See the [scientific translation safeguards](../references/scientific-fidelity.md#scientific-translation) for the content checks behind that process.

The [runtime intake guide](../references/guided-intake.md) explains question order, the host's question tools and answer handling for agents implementing the interview.

<a id="what-happens-after-you-attach-a-deck"></a>

## How palate develops the presentation

### Review the source and the argument

For an existing deck, **palate** establishes what each slide contributes to the argument and where its evidence needs clearer explanation or placement. It inspects the source structure and rendered slides together, so the redesign can account for labels, notes, charts and other content that a text-only inspection may miss.

For a paper or manuscript, **palate** reads the argument alongside its methods, figures, tables, equations and qualifications, then selects and sequences material for the talk. It does not simply turn each paper section into a slide. For rough text, notes or an outline, it organizes the supplied ideas and separates established findings from questions and proposed work. In both cases, claims and visuals remain traceable to the material provided. If an essential result, definition or source is missing, **palate** asks only for information needed to proceed without inventing findings, citations or relationships.

If a source cannot be read reliably or a required application is unavailable, **palate** explains what file, tool or review is needed before it can complete the task. An unreadable figure needs a usable source, not an inferred reconstruction.

If your slides contain tables or **palate** proposes one, it shows two color treatments of the same representative table: Nature-inspired and deck-matched. The content, layout and numeric precision stay the same so you can compare the colors directly. Choose one, supply a preference or ask **palate** to decide; it reuses that decision for comparable tables while preserving meaningful scientific color mappings. No table-color choice is needed when no tables are present or planned.

### Make the changes the content needs

Composition follows the scientific relationship and the brief. **palate** records how each slide uses the source material and chooses an authoring or editing route that can preserve the objects and meaning involved.

When the chosen screen ratio differs from the original, **palate** uses native authoring to change the canvas and rearrange the content. It checks text fit, figure proportions and the new work area instead of stretching the existing layout. This requires access to the appropriate authoring tools; if that access is missing, **palate** explains that the ratio change remains pending.

Text-only pages receive a visual treatment suited to their content. A comparison may become a table, a verified sequence a flowchart, or a set of concepts an illustrated grouping with labeled icons. Continuous explanations retain their reasoning within a designed composition. **palate** preserves the scientific qualifications and does not invent data or relationships for a graphic; an exact quotation or another page that needs to retain its form can be a documented exception.

New decks start in the agreed application using an available tool that can create native, editable slides. The included object-preservation helpers work on existing decks; they do not create slides from a paper or notes by themselves. Without a suitable authoring tool, **palate** can develop the narrative and slide content, but leaves file creation pending.

For existing decks, the editing route depends on the objects and changes involved:

| Your slides need | How **palate** handles the change |
| :--- | :--- |
| Placement or supported styling of existing PowerPoint objects | Uses the `.pptx` preservation helper for supported placement, chart frames, text styling, shapes, lines and backgrounds while retaining source content and embedded workbooks. It rejects unsafe geometry and animation edits. |
| Placement or text styling of existing Keynote text boxes and shapes | Uses the experimental native Keynote adapter on Mac within its limited operation set. It does not automatically rewrite text, create slides or edit chart internals. The adapter has not yet been exercised in Keynote on Mac. |
| New diagrams, summaries, slide splits, changes inside charts or table resizing | Uses an available presentation authoring tool that supports native, editable objects and records how the revised content represents the source. |

Grouped objects and animation states receive their own review. Translation and rewritten text also use the authoring path, with the [scientific translation safeguards](../references/scientific-fidelity.md#scientific-translation).

**palate** also makes displayed quantities easier to compare with thousands separators and consistent decimal places where scientifically appropriate. It preserves underlying values and formulas, keeps years and identifiers intact, and retains the precision needed for small values, uncertainty and meaningful differences. The [numeric display guide](../references/scientific-fidelity.md#numeric-display) explains those exceptions and the checks behind them.

The [design system](../references/design-system.md) explains why audience, evidence and scientific integrity guide these choices. The [PowerPoint plan contract](../references/transform-plan.md) and [Keynote workflow](../references/keynote-workflow.md) define their respective operations and checks; the [scientific fidelity guide](../references/scientific-fidelity.md) covers work that changes content. A supported native file format does not mean the included helper can perform every requested edit. If an appropriate authoring method is unavailable, **palate** identifies the blocked change rather than converting the deck without agreement.

### Review the result and explain what remains

**palate** checks scientific content, native editability and rendered appearance separately. It reviews every final slide in the delivery application and compares revised or newly authored slides with the source material. You receive a new editable deck in a supported format and a concise report of the changes, completed checks and material limits. If an essential check cannot be completed, **palate** identifies the remaining work and labels the output as a candidate.

The [validation guide](validation.md) explains the evidence behind each kind of check and the scope of the repository's existing tests. A report distinguishes completed review from remaining work so you can decide whether the candidate is ready for your intended use.

## PowerPoint and Keynote

**palate** uses one design standard and separate native workflows. It preserves an existing deck's application unless a different delivery format is requested. For a new deck, it confirms the delivery application when that choice has not been supplied. A Keynote deck stays in Keynote; neither a PowerPoint export nor Windows PowerPoint is a prerequisite.

| Delivery application | Native workflow | Current limit |
| :--- | :--- | :--- |
| PowerPoint | Edit a new `.pptx` and review it in PowerPoint. Use an available PowerPoint rendering method; the included Windows renderer is one option. | Native editing and review require actual application access. The supplied Windows script is not a renderer for macOS or Linux. |
| Keynote | Edit and save a new `.key` in Keynote on Mac, then review it there. The included adapter supports bounded placement and text styling of existing text boxes and shapes. | Experimental implementation; no Mac application execution has been tested. It requires macOS, Keynote, `osascript` and permission to control Keynote. |

The native Keynote route keeps the source and the candidate separate:

1. Check the Mac runtime and required automation access. Inspect a private copy of the source, retaining its hash and the application/version evidence.
2. Apply only supported changes to a new native candidate. Translation, rewritten text, new slides and unsupported objects need another available native authoring method with the same scientific safeguards; otherwise the relevant work remains pending.
3. Compare scientific content against the source, confirm editability in Keynote, and inspect every final slide. Review playback separately when builds, transitions or media are present. The included adapter's limited snapshots cannot establish all of these results.

The [Keynote workflow](../references/keynote-workflow.md) gives the commands, supported operations and review requirements. Python and script-level checks on Windows do not establish that this adapter works in Keynote on Mac. Until the native operations and required reviews have actually succeeded, the report identifies the untested or pending work and the output remains a candidate.

If the execution environment lacks Keynote, **palate** explains the Mac handoff and leaves native `.key` work pending. It does not automatically replace the requested format with `.pptx` or use a cloud service. Conversion is an option when the user requests another format or explicitly chooses that route. Compare the exported baseline with the source before redesign, then inspect any later import in the delivery application so conversion losses remain distinguishable from design changes. PDF is visual evidence, not proof of native editability, and renaming a file does not convert its format.

## Requirements

Requirements apply where the agent executes the work, which may differ from the device used to send the request. The [installation guide](installation.md) covers Codex environments; the [ChatGPT Work guide](chatgpt-work.md) covers the experimental web entry and its access checks.

| Task | Required |
| :--- | :--- |
| Identify source format and route the workflow | Python 3.11+ |
| Inspect and preserve objects in `.pptx` files | Python 3.11+, lxml |
| Raster-resolution diagnostics | Pillow |
| Included Windows PowerPoint rendering option | Windows and Microsoft PowerPoint |
| New or rebuilt native slides, including translated or rewritten text | Available native presentation authoring workflow |
| Experimental native Keynote adapter | macOS, Keynote, `osascript`, Python 3.11+ and automation permission; no Node or PowerPoint dependency |
| Native Keynote delivery and review | Successful native save plus content, editability, visual and applicable playback review in Keynote on Mac |

Reuse an existing bundled runtime where available. Installing the skill does not install a presentation editor or establish application access. **palate** reports missing tools and checks rather than claiming those operations succeeded.

In a web session, available file tools may support analysis, authoring and previews without access to the native delivery application. **palate** can perform the supported work, but any essential native review remains pending and the output is a candidate. Native Keynote editing itself still needs an authorized Mac environment. See the [host workflow](../references/host-workflows.md) for capability checks and private handoffs.

## Source files and privacy

**palate** preserves the original and saves exports, candidates and final deliverables as new files. File storage and processing follow the user's authorized execution environment, which may be local or cloud-based. A ChatGPT upload is processed in the selected workspace. **palate** asks before publishing research or sending it to an additional service. Research files and task artifacts stay outside version control; the packages contain only allowlisted runtime instructions and code. Git, packages and installed copies are synchronized explicitly, so a repository change does not automatically update either installed distribution.
