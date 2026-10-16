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

**palate** is a skill that helps researchers turn complex work into presentations their audience can follow.

**Start with the slides you already have.** Upload your slides, even if they're crowded, inconsistent, or still a work in progress. You don't need to redesign them first. That's what **palate** is here for.

**palate** starts by understanding your audience, purpose, and time available. It then reorganizes your content into a clearer narrative, decides what deserves emphasis, and refines each slide so the evidence and reasoning are easier to follow. Whether you're preparing a conference talk, a research meeting, or a tutorial, the design adapts to your needs while preserving the scientific meaning of your work.

Once finished, you'll receive a **refined, editable slide deck** and a brief report of what changed, what was checked, and anything that still needs your attention.

## <img src="assets/icons/square-terminal.svg" width="22" height="22" align="bottom" alt="">&nbsp; Get started

### 01 | Install **palate**

Choose where to work. Both routes use the same design rules.

| Environment | Get started |
| :--- | :--- |
| Codex | Use the installation request below. |
| ChatGPT Work on the web | Follow the [private plugin setup](docs/chatgpt-work.md). This route is experimental; browser installation and end-to-end editing have not been tested. |

For Codex, paste:

```text
Install the palate Codex skill from https://github.com/sherryyan1/palate-by-sherry.

Check the environment where Codex runs, follow docs/installation.md, and verify that $palate is available. If palate is already installed, ask before replacing it.
```

Codex checks repository access, dependencies and skill discovery. If **palate** does not appear, restart Codex and check again. See the [installation guide](docs/installation.md) for setup details.

For ChatGPT Work, the web guide starts with Plugin Creator and a private plugin. Availability depends on the account and workspace. Setup remains pending until **palate** appears in the `@` picker and its runtime files are accessible; a local Codex installation does not transfer automatically.

### 02 | Upload your slides

Attach the slides you already have. In Codex, ask:

```text
$palate Polish my slides.
```

In ChatGPT Work, type `@` and select the installed **palate** plugin or skill, then ask `Polish my slides.`

### 03 | Tell **palate** about your presentation

After you send your request, **palate** asks about three things:

- **Presentation setting:** Is this for a research meeting, a tutorial, or an external presentation?
- **Duration:** How many minutes do you plan to present?
- **Technical depth:** How much technical detail would you like to keep? **palate** can decide if you prefer.

You can select the suggested options or answer in your own words. **palate** won't ask again for details you've already shared.

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

**palate** uses one design standard with separate native workflows for PowerPoint and Keynote. It keeps the source format unless a different delivery format is requested; a Keynote deck does not need to pass through PowerPoint.

| Source | What **palate** provides |
| :--- | :--- |
| PowerPoint (`.pptx`) | A new editable `.pptx`, with final review in PowerPoint. |
| Keynote (`.key`) | A new native `.key` candidate, using the supported operations in Keynote on Mac. |

If the source cannot be opened, **palate** asks for a compatible editable copy. Keynote work needs the required Mac automation permission. If the delivery application is unavailable, **palate** leaves that application work pending and explains the handoff and remaining checks.

The included native Keynote workflow is **experimental and has not been tested on a Mac**. It requires macOS, Keynote and permission for the execution process to control the application. Automated edits cover placement and text styling of existing text boxes and shapes. Other changes need an available native authoring method or remain pending. The [Keynote guide](references/keynote-workflow.md) describes the operations and review requirements. Conversion is a separate option when requested or explicitly chosen, with additional checks for conversion loss.

Python tools require Python 3.11+; `.pptx` inspection uses `lxml`, and raster-resolution diagnostics use Pillow. The agent reuses an available bundled runtime. The included Windows PowerPoint renderer is one platform-specific preview option, not a requirement for Keynote or every PowerPoint environment. **palate** reviews the result in the actual delivery application and identifies any missing tool or unfinished check. Installing the skill does not install PowerPoint or Keynote or grant application access.

Setup applies to the environment that processes the files, which may differ from the device used to chat. A web session does not automatically have access to local PowerPoint or Keynote. Without the required native review, any edited output remains a candidate. See the [installation guide](docs/installation.md) and [ChatGPT Work guide](docs/chatgpt-work.md) for their separate setup and verification steps.

The selected execution environment determines where files are stored and processed. ChatGPT uploads are processed in the selected workspace. **palate** preserves the original, saves revisions separately and asks before sending research files to another service. It covers multi-slide presentations; single-page monthly updates are outside its scope.

## <img src="assets/icons/book-open.svg" width="22" height="22" align="bottom" alt="">&nbsp; Documentation

- [Installation and environment checks](docs/installation.md)
- [ChatGPT Work web setup, experimental](docs/chatgpt-work.md)
- [Usage and presentation brief](docs/usage.md)
- [Communication design](references/communication-design.md)
- [Design system](references/design-system.md)
- [Keynote workflow](references/keynote-workflow.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Transformation plan](references/transform-plan.md)
- [Validation](docs/validation.md)
