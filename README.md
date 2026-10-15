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

**palate** is a Codex skill for refining research presentations in Sherry's style. It shapes the explanation around the audience, purpose and time available, then arranges the slides so the evidence and reasoning are easy to follow. Throughout the redesign, it preserves the meaning and qualifications of the research.

A palate for ideas, a palette for slides.

## Quick start

From the repository root, install the dependencies and skill:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

Attach your slides and ask:

```text
Use palate to polish my slides.
```

You can provide a brief upfront or begin with this sentence. palate uses what you have already shared and asks for the context that would change the design; when you leave the depth open, it reviews your slides before deciding how much explanation the talk needs. The [usage guide](docs/usage.md) explains the choices that shape the brief.

## Language choices

You can read this README in Korean, discuss the brief in Korean and still ask for an English conference presentation. Those choices serve different purposes: documentation should be easy to read, while the slides should use the language your audience needs. palate preserves the source language unless you request a change, and clarifies an uncertain target before rewriting.

Translation is a content revision. It requires an available native authoring workflow and scientific review to preserve terminology, numerical values, units and qualifications. The object-preservation helper adjusts existing objects; it does not translate their text.

## How it approaches the slides

The design begins with what listeners need to understand. A tutorial may need a mechanism explained in stages, while a research meeting may need methods and uncertainty visible for discussion. The time available determines how much of that explanation can be developed during the talk and which supporting material belongs in notes or an appendix. It does not determine a fixed slide count.

Clear hierarchy, teal accents and space around the evidence help make those relationships readable. Comparable results use comparable scales; methods follow a clear sequence; findings stay close to the evidence and qualifications needed to interpret them. Section arrows and part markers can help listeners follow a longer argument when the content calls for them.

palate preserves data, units, equations, labels, uncertainty, caveats and references. Existing native objects remain editable where the tools support them, and complex figures stay intact when reconstruction cannot be verified. The result is a new editable deck and a concise report explaining the changes, the checks performed and any remaining limits. Content, editability and rendered appearance are reviewed separately.

## Formats and requirements

PowerPoint and Keynote use the same design principles, with different preparation and review requirements.

| Source | Preparation | Final review |
| :--- | :--- | :--- |
| PowerPoint | Inspect a compatible editable deck, preserving native objects or using native authoring for larger revisions. | Check content, appearance and editability in the delivery application. |
| Keynote | Export a PowerPoint copy and PDF reference, then compare the export with the source before design. | Open and save the result in Keynote; check conversion, fonts, native editability and any playback. |

The [Keynote workflow](references/keynote-workflow.md) explains the export and conversion checks. Windows can prepare the PowerPoint interchange deck. Native Keynote delivery requires Keynote on Mac, where the final deck must be saved and reviewed; that work remains pending until it has been performed there.

The bundled scripts require Python 3.11+, `lxml` and Pillow. Use an existing bundled runtime when available. The included Windows preview renderer requires Microsoft PowerPoint; new or rebuilt slides require an available native presentation authoring workflow.

The original deck is preserved and output is saved to a new file. Research files remain local unless their upload is explicitly authorized. This skill covers multi-slide presentations; single-page monthly updates are outside its scope.

## Documentation

- [Usage, installation and requirements](docs/usage.md)
- [Design system](references/design-system.md)
- [Keynote workflow](references/keynote-workflow.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Transformation plan](references/transform-plan.md)
- [Validation](docs/validation.md)
