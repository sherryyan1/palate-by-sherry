# Usage

Ask Codex to install **palate** using the [installation guide](installation.md). It checks the execution environment, dependencies and skill discovery, and asks before replacing an existing installation. Manual commands and update procedures are documented there.

## Start with one sentence

Attach your research slides and ask:

```text
$palate Polish my slides.
```

A detailed brief is optional: **palate** uses the information already supplied and asks for missing context that could materially change the design. You do not need to choose fonts, palettes or layouts first. For a Keynote source, the [format workflow](#powerpoint-and-keynote) explains when export files are needed.

## Shape the brief

The audience determines how much context a listener needs to follow the evidence. A tutorial may need definitions and a mechanism developed in stages, while a research group may need assumptions, methods and uncertainty available for discussion. An executive audience may need the supported implications made clear early; a general audience may need the finding connected to a familiar question before encountering technical detail.

Time then shapes how fully that explanation can unfold during the talk. A shorter presentation needs a clear path through the central result, with supporting detail placed where it can still be consulted. A longer talk allows more development, but its length alone does not justify extra density. Essential qualifications stay with the evidence they qualify, and material moved to notes or an appendix remains traceable to its source.

The brief uses these choices to establish the setting and the level of explanation:

| Part of the brief | Choices | Effect on the presentation |
| :--- | :--- | :--- |
| Setting | Internal tutorial, internal research, external presentation | Establishes whether the deck should primarily teach, support research discussion or explain work to an outside audience. |
| External audience | Experts, C-suite/executives, general audience | Guides terminology, conceptual support and the order in which evidence and implications are introduced. |
| Duration | Suggested times or custom minutes | Sets the pace and the amount of explanation that can be developed during the talk. |
| Depth | Let palate choose, key takeaways, full technical detail | Determines how much derivation and supporting detail should be visible, while preserving the evidence needed for interpretation. |

You can write your own answer or provide all the presentation details in your first message. If you select "Let palate choose," **palate** reviews your slides and uses your audience and available time to decide how much detail to include. The [presentation contexts](../references/presentation-contexts.md) suggest starting points, including durations; your current instructions take precedence. Slide count and Q&A time are used only when supplied, and single-page monthly updates remain outside this workflow.

Your slides stay in their original language unless you request a translation; the language of this guide or the conversation does not change that choice. If you request translation without naming the target language, **palate** asks for it before rewriting. It also asks when a technical term has plausible translations that could materially change the scientific meaning, and reuses the terminology you confirm. See the [scientific translation safeguards](../references/scientific-fidelity.md#scientific-translation) for the content checks behind that process.

The [runtime intake guide](../references/guided-intake.md) explains question order, the host's question tools and answer handling for agents implementing the interview.

## What happens after you attach a deck

### Review the source and the argument

**palate** first establishes what each slide contributes to the argument and where its evidence needs clearer explanation or placement. It inspects the source structure and rendered slides together, so the redesign can account for labels, notes, charts and other content that a text-only inspection may miss. If a source cannot be opened or a required application is unavailable, **palate** explains what file or review is needed before it can complete the task.

### Make the changes the content needs

Composition follows the scientific relationship and the brief. **palate** records changes against the source and chooses an editing route that can preserve the objects and meaning involved:

| Your slides need | How **palate** handles the change |
| :--- | :--- |
| Placement or supported styling of existing objects | Adjusts placement, chart frames, text styling, shapes, lines and backgrounds while retaining source content and embedded workbooks. This preservation route rejects unsafe geometry and animation edits. |
| New diagrams, summaries, slide splits, changes inside charts or table resizing | Uses an available presentation authoring tool that supports native, editable objects and records how the revised content represents the source. |

Grouped objects and animation states receive their own review. Translation and rewritten text also use the authoring path, with the [scientific translation safeguards](../references/scientific-fidelity.md#scientific-translation).

The [design system](../references/design-system.md) explains why audience, evidence and scientific integrity guide these choices. The [plan contract](../references/transform-plan.md) provides exact commands and fields for the existing-object route; the [scientific fidelity guide](../references/scientific-fidelity.md) covers work that changes content.

### Review the result and explain what remains

**palate** checks scientific content, native editability and rendered appearance separately. It reviews every final slide in the delivery application and compares changed slides with the source. You receive a new editable deck in a supported format and a concise report of the changes, completed checks and material limits. If an essential check cannot be completed, **palate** identifies the remaining work and labels the output as a candidate.

The [validation guide](validation.md) explains the evidence behind each kind of check and the scope of the repository's existing tests. A report distinguishes completed review from remaining work so you can decide whether the candidate is ready for your intended use.

## PowerPoint and Keynote

**palate** uses the requested delivery application, or preserves the source application when none is specified. The brief and scientific checks remain the same for PowerPoint and Keynote; conversion adds a separate comparison so losses during the handoff can be identified.

For a Keynote source, **palate** follows this sequence. If it cannot access Keynote on Mac, it guides you through the exports and the native save and review:

1. Preserve the original and obtain a PowerPoint export plus a PDF visual reference.
2. Compare the PowerPoint export with the source before design so conversion defects can be distinguished from later changes.
3. After design, if delivery is in Keynote, open the reviewed candidate there and save a new native deck. Inspect every slide, confirm native editability, and review playback when the deck contains builds, transitions or media.

The [Keynote workflow](../references/keynote-workflow.md) gives the export settings and conversion checks.

Windows can prepare the PowerPoint interchange deck, but native Keynote delivery and review require Keynote on Mac. If that application is unavailable, the report records the native Keynote work as pending. A PDF supplies visual evidence for comparison; it does not establish that charts, tables or labels remain editable. Renaming a file does not convert its format.

## Requirements

Requirements apply where Codex executes commands, which may differ from the device used to send the request. The [installation guide](installation.md) covers Windows, macOS, Linux and remote environments, including their untested or application-dependent limits.

| Task | Required |
| :--- | :--- |
| Identify source format and route the workflow | Python 3.11+ |
| Inspect and preserve objects in `.pptx` files | Python 3.11+, lxml |
| Raster-resolution diagnostics | Pillow |
| Included Windows rendering | Microsoft PowerPoint |
| New or rebuilt native slides, including translated or rewritten text | Available native presentation authoring workflow |
| Native Keynote delivery and review | Keynote on Mac |

Reuse an existing bundled runtime where available. Installing the skill does not install a presentation editor or establish application access. **palate** reports missing tools and checks rather than claiming those operations succeeded.

## Source files and privacy

**palate** preserves the original and saves exports, candidates and final deliverables as new files. File storage and processing follow the user's authorized Codex execution environment, which may be local or cloud-based. **palate** asks before publishing research or sending it to another service. Research files and task artifacts stay outside version control; the package contains only allowlisted runtime instructions and code. Git, packages and installed copies are synchronized explicitly, so a repository change does not automatically update the installed skill.
