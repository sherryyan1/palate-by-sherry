<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="docs/media/palate-dark-mobile.svg">
  <source media="(max-width: 640px)" srcset="docs/media/palate-light-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/media/palate-dark.svg">
  <img src="docs/media/palate-light.svg" alt="palate by Sherry — Good research deserves good taste." width="1200">
</picture>

<!-- language-navigation -->
<p align="center">
  <a href="README.md" lang="en">English</a> &nbsp;·&nbsp;
  <a href="README.zh-CN.md" lang="zh-CN">简体中文</a> &nbsp;·&nbsp;
  <a href="README.ja.md" lang="ja">日本語</a> &nbsp;·&nbsp;
  <a href="README.ko.md" lang="ko">한국어</a>
</p>
<!-- /language-navigation -->

<p align="center">
  <a href="#quick-start">Get started</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">Design principles</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">Documentation</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** is a Codex skill that helps researchers turn complex work into presentations their audience can follow.

**Start with the slides you already have.** Upload your slides, even if they're crowded, inconsistent, or still a work in progress. You don't need to redesign them first. That's what **palate** is here for.

**palate** starts by understanding your audience, purpose, and time available. It then reorganizes your content into a clearer narrative, decides what deserves emphasis, and refines each slide so the evidence and reasoning are easier to follow. Whether you're preparing a conference talk, a research meeting, or a tutorial, the design adapts to your needs while preserving the scientific meaning of your work.

You'll receive a **refined, editable slide deck** and a brief report of what changed, what was checked, and anything that still needs your attention.


## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; Quick start

From the repository root, install the dependencies and skill:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

Then, attach your slides and ask:

```text
Use palate to polish my slides.
```

Start with this request, or tell palate who the audience is, how long the presentation will be and how much technical detail you want. palate uses the information you have already provided and asks only for missing details that affect the design. If you want palate to choose how much detail to include, it reviews your slides and considers the audience and time available. The [usage guide](docs/usage.md) explains how these choices guide the design.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; Languages

This README is available in **English, 简体中文, 日本語, and 한국어**. You can switch languages using the links at the top of the page.

Your presentation stays in its original language unless you request a translation.

If you do, palate will help translate the content while preserving numerical values, units, and scientific meaning. If a technical term has multiple possible translations, palate will ask you to clarify rather than guess.

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; How it approaches the slides

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | Start with the audience

<sub><em>What needs to be understood?</em></sub>

For example, a tutorial may need a mechanism explained step by step. A research meeting may need methods and uncertainty visible for discussion.

Time shapes the **depth and pacing** of the explanation, not a fixed slide count. Supporting details can move to notes or an appendix.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/chart-no-axes-combined.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | Let the evidence lead

<sub><em>How should the evidence be read?</em></sub>

Clear hierarchy, teal accents and space around the evidence help make those relationships readable. Comparable results use comparable scales; methods follow a clear sequence; findings stay close to the evidence and qualifications needed to interpret them.

Section arrows and part markers can help listeners follow a longer argument when the content calls for them.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/shield-check.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | Keep the science intact

<sub><em>What must the design preserve?</em></sub>

palate preserves data, units, equations, labels, legends, uncertainty, caveats and references. Existing native objects remain editable where the tools support them, and complex figures stay intact when reconstruction cannot be verified.

### <img src="assets/icons/package-check.svg" width="22" height="22" align="top" alt="">&nbsp; What you get

You receive a new editable deck and a concise report explaining the changes, checks completed and any remaining limits. palate checks content, editability and appearance separately. If it cannot complete a required check, it identifies the remaining work and marks the deck as a candidate.

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; Formats and requirements

palate applies the same design principles to PowerPoint and Keynote. The source format determines which files it needs and where it can complete the final review.

| Source | What palate does | When you need to help |
| :--- | :--- | :--- |
| PowerPoint | Refines a compatible editable deck, preserves editable objects where supported and reviews the result against the source. | Provide a compatible editable copy if the source cannot be opened. If palate cannot access the delivery application, it guides you through the remaining checks. |
| Keynote | Compares a PowerPoint export with the source and PDF reference before design, then polishes a new PowerPoint copy and guides the final Keynote review. | If palate cannot access Keynote on Mac, provide PowerPoint and PDF exports and complete the native save and review there. |

On Windows, palate can prepare the PowerPoint copy but cannot edit a native `.key` file. If it cannot access Keynote on Mac, palate guides you through the exports and final save and review, and records any outstanding native Keynote steps in the report. The [Keynote workflow](references/keynote-workflow.md) explains these steps and the checks required before native Keynote delivery is complete.

The bundled scripts require Python 3.11+, `lxml` and Pillow; palate uses an existing bundled runtime when available. Microsoft PowerPoint must be installed for the included Windows slide previews. Translating or rewriting text, creating slides and rebuilding editable objects require an available presentation editor; palate explains the delivery limits if that editor is unavailable.

The original deck is preserved and output is saved to a new file. Research files remain local unless their upload is explicitly authorized. This skill covers multi-slide presentations; single-page monthly updates are outside its scope.

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; Documentation

- [Usage, installation and requirements](docs/usage.md)
- [Design system](references/design-system.md)
- [Keynote workflow](references/keynote-workflow.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Transformation plan](references/transform-plan.md)
- [Validation](docs/validation.md)
