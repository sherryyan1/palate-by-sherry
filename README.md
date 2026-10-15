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
  <a href="#get-started">Get started</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">Design principles</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">Documentation</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** is a Codex skill that helps researchers turn complex work into presentations their audience can follow.

**Start with the slides you already have.** Upload your slides, even if they're crowded, inconsistent, or still a work in progress. You don't need to redesign them first. That's what **palate** is here for.

**palate** starts by understanding your audience, purpose, and time available. It then reorganizes your content into a clearer narrative, decides what deserves emphasis, and refines each slide so the evidence and reasoning are easier to follow. Whether you're preparing a conference talk, a research meeting, or a tutorial, the design adapts to your needs while preserving the scientific meaning of your work.

You'll receive a **refined, editable slide deck** and a brief report of what changed, what was checked, and anything that still needs your attention.

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; Get started

### 01 | Install **palate**

Open Codex and paste:

```text
Install the palate Codex skill from https://github.com/sherryyan1/palate-by-sherry.

Check the environment where Codex runs, follow docs/installation.md, and verify that $palate is available. If palate is already installed, ask before replacing it.
```

Codex checks repository access, dependencies and skill discovery. If **palate** does not appear, restart Codex and check again. See the [installation guide](docs/installation.md) for setup details.

### 02 | Upload your slides

Attach the slides you already have. They can be crowded, inconsistent or unfinished. Then ask:

```text
$palate Polish my slides.
```

### 03 | Tell **palate** what you need

You can provide your audience, presentation duration and desired technical depth in your first message. A complete design brief is optional: **palate** uses what you have already shared and asks only for missing details that could materially affect the design. The [usage guide](docs/usage.md) explains the options.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; Languages

This README is available in **English, 简体中文, 日本語, and 한국어**. You can switch languages using the links at the top of the page.

**palate** keeps your slides in their original language unless you request a translation. When translating, it preserves numerical values, units and scientific meaning.

If a technical term has plausible translations that could materially change its scientific meaning, **palate** asks you to clarify before applying one.

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; Design principles

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | Start with the audience

<sub><em>What does your audience need to understand?</em></sub>

A tutorial may need a mechanism explained step by step. A research meeting may need methods and uncertainty visible for discussion. **palate** adjusts the explanation to the context and the evidence listeners need to examine.

Time shapes the **depth and pacing** of the explanation, not a fixed slide count. Supporting details can move to notes or an appendix when the main explanation remains accurate.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/chart-no-axes-combined.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | Let the evidence lead

<sub><em>How can the evidence and reasoning be easier to follow?</em></sub>

**palate** clarifies information hierarchy, aligns comparable scales and develops methods in a logical sequence. It keeps findings close to the evidence and qualifications needed to interpret them.

Space, teal accents and navigation markers help when they reveal a relationship or keep listeners oriented. Their use follows the content rather than a fixed template.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/shield-check.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | Keep the science intact

<sub><em>What should never change during a redesign?</em></sub>

**palate** preserves data, units, equations, labels, legends, uncertainty, caveats and references. It maintains native editability where the tools support it and retains complex figures when reliable reconstruction cannot be verified.

### <img src="assets/icons/package-check.svg" width="22" height="22" align="top" alt="">&nbsp; What you get

You receive a new editable slide deck in a supported format and a concise report explaining the changes, completed checks and anything that still needs attention.

**palate** checks scientific content, editability and rendered appearance separately. If an essential check cannot be completed, it labels the output as a candidate and explains what remains.

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; Formats and requirements

**palate** applies the same design principles to PowerPoint and Keynote. File handling and final review depend on the source and delivery format.

| Source | What **palate** provides | When you need to help |
| :--- | :--- | :--- |
| PowerPoint (`.pptx`) | A new editable `.pptx` deck, reviewed against the source. | Provide a compatible editable copy if the source cannot be opened. If **palate** cannot access the delivery application, it guides you through the remaining checks. |
| Keynote (`.key`) | An editable `.pptx` deck prepared from a PowerPoint export and PDF reference. Native `.key` delivery follows saving and review in Keynote on Mac. | Provide the exports and complete the native save and review if **palate** cannot access Keynote on Mac. |

Windows cannot provide native `.key` editing through this workflow. The [Keynote guide](references/keynote-workflow.md) explains the export, conversion and final native checks; the report identifies the format actually delivered and any pending Keynote work.

The Python tools require Python 3.11+, `lxml` and Pillow; Codex uses an available bundled runtime where possible. The included Windows previews require Microsoft PowerPoint. Translating or rewriting text, creating slides and rebuilding editable objects require an available presentation authoring tool. **palate** explains any missing tool or review that limits delivery.

Setup applies to the computer or remote environment where Codex runs, which may differ from the device you use to chat. This repository does not provide native iOS or iPadOS installation. The [installation guide](docs/installation.md) covers environment checks and manual setup.

Your Codex environment determines where files are stored and processed. **palate** preserves the original, saves revisions separately and asks before sending research files to another service. It covers multi-slide presentations; single-page monthly updates are outside its scope.

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; Documentation

- [Installation and environment checks](docs/installation.md)
- [Usage and presentation brief](docs/usage.md)
- [Communication design](references/communication-design.md)
- [Design system](references/design-system.md)
- [Keynote workflow](references/keynote-workflow.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Transformation plan](references/transform-plan.md)
- [Validation](docs/validation.md)
