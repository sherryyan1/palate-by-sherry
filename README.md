<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/media/palate-dark.svg">
  <img src="docs/media/palate-light.svg" alt="palate by Sherry — Good research deserves good taste." width="1200">
</picture>

<p align="center">
  <a href="#quick-start">Get started</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">Design principles</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">Documentation</a>
</p>

**palate** is a Codex skill for refining research presentations in Sherry's style. It adapts structure, visual hierarchy and detail to the audience and time available, while preserving the scientific evidence.

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

palate asks for missing context through short choices: presentation setting, audience, duration and level of detail. You can provide a brief upfront or delegate the depth. Information already supplied is not asked again. Compatible Codex hosts display choice cards; other hosts use concise questions.

## What it does

- Improves reading order, spacing and the connection between evidence and explanation.
- Preserves data, units, equations, labels, uncertainty, caveats and references.
- Delivers a new editable deck and a concise report of changes, checks and any limits.

The design uses clear hierarchy, teal accents and room for the evidence. Layouts follow the content: comparable scales for comparisons, a clear sequence for methods, and results presented with their interpretation. Section arrows and part markers help listeners follow longer arguments. Complex figures remain intact when reconstruction cannot be verified.

## Formats and requirements

One design workflow serves both PowerPoint and Keynote. File handling follows the source format.

| Source | Workflow | Final review |
| :--- | :--- | :--- |
| PowerPoint | Preserve native objects; use native authoring for larger revisions. | Check content, appearance and editability in the delivery application. |
| Keynote | Export a PowerPoint copy, then use the shared design workflow. | Open the result in Keynote; check conversion, fonts, native objects and playback. |

The [format router](references/keynote-workflow.md) identifies compatible inputs and the next required step. Native Keynote delivery requires Keynote on Mac. Windows can prepare the interchange deck; Keynote review remains pending until performed there.

The bundled scripts require Python 3.11+, `lxml` and Pillow. Use an existing bundled runtime when available. The included Windows preview renderer requires Microsoft PowerPoint; new or rebuilt slides require an available native presentation authoring workflow.

Output is saved to a new file. Research files remain local unless their upload is explicitly authorized. Single-page monthly updates are outside this skill's scope.

## Documentation

- [Usage, installation and requirements](docs/usage.md)
- [Design system](references/design-system.md)
- [Keynote workflow](references/keynote-workflow.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Transformation plan](references/transform-plan.md)
- [Validation](docs/validation.md)
