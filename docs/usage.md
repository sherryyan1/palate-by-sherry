# Usage

## Requirements

| Task | Required |
| :--- | :--- |
| Identify source format and route the workflow | Python 3.11+ |
| Inspect and preserve PowerPoint objects | Python 3.11+, lxml |
| Raster-resolution diagnostics | Pillow |
| Included Windows rendering | Microsoft PowerPoint |
| New or rebuilt native slides | Available native presentation authoring workflow |
| Native Keynote delivery and review | Keynote on Mac |

Use an existing bundled runtime when one is available. The preservation helper can inspect and adjust existing objects without a Node SDK. New or rebuilt slides require an available native authoring workflow. When the presentations skill is installed, its JavaScript `@oai/artifact-tool` workflow provides that path; the [PowerPoint workflow](../references/pptx-workflow.md) explains when it is needed.

## Install

From the repository root:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

On other systems, install to the configured Codex skills directory under `palate`. Use a fresh package filename for updates. The installer verifies the package, refuses to overwrite local edits and keeps a recoverable previous snapshot.

To migrate an earlier installation, name it explicitly:

```powershell
python scripts/package_skill.py --output dist/palate-update.zip --install "$env:USERPROFILE\.codex\skills\palate" --migrate-legacy "$env:USERPROFILE\.codex\skills\palate-by-sherry"
```

The installer verifies the complete managed installation before archiving it outside the skills directory. If it finds local edits, it stops migration and leaves the previous files intact so those changes can be resolved first.

## Start with one sentence

Attach your research slides and ask:

```text
Use palate to polish my slides.
```

You can also invoke the skill explicitly as `$palate`. A detailed brief is optional: palate uses the information already supplied and asks for the missing context that would change the design.

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

You can write your own answer or provide all the presentation details in your first message. If you select "Let palate choose," palate reviews your slides and uses your audience and available time to decide how much detail to include. The [presentation contexts](../references/presentation-contexts.md) suggest starting points, including durations; your current instructions take precedence. Slide count and Q&A time are used only when supplied, and single-page monthly updates remain outside this workflow.

The [runtime intake guide](../references/guided-intake.md) covers the host's question tools and how supplied answers are reused. You do not need to choose fonts, palettes or layouts before asking for a polish.

## Workflow

The initial review establishes what each slide contributes to the argument and where its evidence needs clearer explanation or placement. It includes the source structure and rendered slides, so the redesign can account for labels, notes, charts and other content that may be missed by a text-only inspection. Composition follows the scientific relationship and the brief, with changes recorded against the source.

When the existing objects can support the design, the conservative helper adjusts their placement, chart frames, text styling, shapes, lines and backgrounds while retaining source content and embedded workbooks. It rejects unsafe geometry and animation edits. Larger changes, such as new diagrams, summaries, slide splits, changes inside charts or table resizing, use native authoring and a content ledger that records how the source material is represented. Changes to grouped objects and animation states receive their own review.

The final review checks scientific content, native editability and rendered appearance separately. Structural checks help establish that content and package parts were retained, while inspection in the delivery application establishes whether the slides are readable and the intended objects can still be edited. Every final slide is reviewed, and changed slides are compared with the source. The deliverables are a new editable deck and a concise report explaining the changes, the checks performed and any material limits.

See the [plan contract](../references/transform-plan.md) for CLI commands and the [scientific fidelity guide](../references/scientific-fidelity.md) for work that changes content.

## PowerPoint and Keynote

The intended delivery application determines the file route; when none is specified, preserve the source application. The design brief and scientific checks remain the same for PowerPoint and Keynote, but conversion adds a separate obligation to check what survived the handoff. The read-only router identifies the source and reports the next step without converting files, launching applications or uploading research:

```text
python scripts/presentation_route.py "source.pptx" --target pptx
python scripts/presentation_route.py "source.key" --target keynote
```

For a Keynote source, preserve the original and export a PowerPoint copy plus a PDF visual reference. Compare the PowerPoint export with the source before design so that conversion defects can be distinguished from later changes. If the result will be delivered in Keynote, open the reviewed candidate there, save a new native deck and inspect every slide. Confirm native editability and review playback when the deck contains builds, transitions or media. The [Keynote workflow](../references/keynote-workflow.md) gives the export settings and conversion checks.

Windows can prepare the PowerPoint interchange deck, but native Keynote delivery and review require Keynote on Mac. If that application is unavailable, the report records the native Keynote work as pending. A PDF supplies visual evidence for comparison; it does not establish that charts, tables or labels remain editable. Renaming a file does not convert its format.

## Source files and privacy

Keep the original source intact and save exports, candidates and final deliverables as new files. Research files and task artifacts remain local unless their upload is explicitly authorized. They stay outside version control; the distributable package contains runtime instructions and code only. Git, packages and installed copies are synchronized explicitly, so a repository change does not automatically update the installed skill.
