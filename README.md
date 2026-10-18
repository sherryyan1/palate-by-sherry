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
  <a href="#-get-started">Get started</a> &nbsp;·&nbsp;
  <a href="#-sherrys-picks">Sherry's Picks</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">Documentation</a>
</p>

*A palate for ideas, a palette for slides.*

**palate** is a skill that helps researchers turn complex research into presentations their audience can follow.

**Start with what you have.** Share an existing deck, rough notes, an outline, or a paper. You don't need to prepare slides first. **palate** can refine a deck or develop a new one from your material.

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

### 02 | Share your material

Attach a deck or paper, or paste your notes and main ideas. In Codex, choose the request that fits:

| Starting material | Example request |
| :--- | :--- |
| Existing slides | `$palate Polish my slides.` |
| Rough text, notes or an outline | `$palate Create slides from these notes.` |
| A paper or manuscript | `$palate Create a research presentation from this paper.` |


In ChatGPT Work, type `@` and select the installed **palate** plugin or skill, then send your material with the corresponding request.

### 03 | Tell **palate** about your presentation

After you send your request, **palate** asks about four things:

- **Presentation setting:** Is this for a research meeting, a tutorial, or an external presentation?
- **Duration:** How many minutes do you plan to present?
- **Screen format:** Is the venue's screen closer to 4:3 or 16:9? If you're not sure, **palate** preserves an existing deck's proportions or starts a new deck at 16:9, clearly marking that as a design assumption until the venue is confirmed.
- **Technical depth:** How much technical detail would you like to keep? **palate** can decide if you prefer.

You can select the suggested options or answer in your own words. **palate** won't ask again for details you've already shared. If you're starting a new deck, it also confirms PowerPoint or Keynote when you haven't specified one.

**palate** uses your material to establish what the talk can support. If an essential result, definition or source is missing, it asks for that information rather than inventing findings or citations.

## <img src="assets/icons/languages.svg" width="22" height="22" align="bottom" alt="">&nbsp; Languages

This README is available in **English, 简体中文, 日本語, and 한국어**. You can switch languages using the links at the top of the page.

**palate** keeps an existing deck in its original language unless you request a translation. For a new deck, it follows the requested language or the source material; if the intended language is unclear, it asks. When translating, it preserves numerical values, units and scientific meaning.

If a technical term has plausible translations that could materially change its scientific meaning, **palate** asks you to clarify before applying one.

## <img src="assets/icons/compass.svg" width="22" height="22" align="bottom" alt="">&nbsp; Sherry's Picks

Listen with skepticism when a speaker **cherry-picks**. Present with confidence when applying **Sherry's Picks**.

It's not about choosing which evidence to show, but making thoughtful choices about how to present it. **palate** works from the big picture to the finer details, guided by four principles.

### <img src="assets/icons/users-round.svg" width="22" height="22" align="top" alt="">&nbsp; 01 | Read the room

<sub><em>Know your audience.</em></sub>

Good design begins with understanding the occasion. Who will be listening? What do they already know? What should they take away from the talk?

**palate** first establishes an overall style that suits the audience, purpose, and setting. A conference presentation, a research meeting, and a public lecture each call for a different approach. There is no one-size-fits-all design.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/git-branch.svg" width="22" height="22" align="top" alt="">&nbsp; 02 | Find the thread

<sub><em>Make the story worth following.</em></sub>

A good presentation is more than a collection of good slides. The ideas need to connect, and the reasoning should unfold naturally.

**palate** looks at the presentation as a whole, identifies its central argument, and revisits the structure. This may involve rearranging slides, reorganizing sections, or changing how ideas are introduced, so that every part has a clear place in the story.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/align-left.svg" width="22" height="22" align="top" alt="">&nbsp; 03 | Distill the message

<sub><em>Seek simplicity from complexity.</em></sub>

Clarity comes from knowing what to keep, what to explain, and what can be said more simply.

**palate** works through the slides one by one, refining dense text, removing repetition, and bringing the key message into focus. The aim is to make complex research easier to understand without losing the precision, nuance, or uncertainty that matters.

<img src="assets/icons/arrow-down.svg" width="22" height="22" alt="">

### <img src="assets/icons/palette.svg" width="22" height="22" align="top" alt="">&nbsp; 04 | Refine the visuals

<sub><em>Make every detail belong.</em></sub>

Finally, **palate** turns to the visual details: figures, typography, alignment, spacing, and colour.

For new colour choices, **palate** draws on curated reference palettes, adapting them to the content and the distinctions each figure needs to communicate while preserving existing scientific colour mappings. See the [colour guidance](references/refine-the-visuals.md#give-color-a-consistent-purpose).

Graphics should communicate, not merely decorate. Consistent formatting brings the slides together, while thoughtful variation keeps each page suited to its content. The result is a presentation that feels coherent, polished, and professional, without looking as though it came from a fixed template.

## <img src="assets/icons/files.svg" width="22" height="22" align="bottom" alt="">&nbsp; Formats and requirements

**palate** uses one design standard with separate native workflows for PowerPoint and Keynote. It keeps an existing deck's format unless a different delivery format is requested; a Keynote deck does not need to pass through PowerPoint.

| Source | What **palate** provides |
| :--- | :--- |
| PowerPoint (`.pptx`) | A new editable `.pptx`, with final review in PowerPoint. |
| Keynote (`.key`) | A new native `.key` candidate, using the supported operations in Keynote on Mac. |
| Text, notes, an outline, a paper or a manuscript | A new deck in the agreed application, using available native authoring tools. |

Python tools require Python 3.11+; `.pptx` inspection uses `lxml`, and raster-resolution diagnostics use Pillow. The agent reuses an available bundled runtime. The included Windows PowerPoint renderer is one platform-specific preview option, not a requirement for Keynote or every PowerPoint environment. **palate** reviews the result in the actual delivery application and identifies any missing tool or unfinished check. Installing the skill does not install PowerPoint or Keynote or grant application access.

Setup applies to the environment that processes the files, which may differ from the device used to chat. A web session does not automatically have access to local PowerPoint or Keynote. Without the required native review, any edited output remains a candidate. See the [installation guide](docs/installation.md) and [ChatGPT Work guide](docs/chatgpt-work.md) for their separate setup and verification steps.

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
