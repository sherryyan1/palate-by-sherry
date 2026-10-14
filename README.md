<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/media/palate-dark.svg">
  <img src="docs/media/palate-light.svg" alt="palate. by Sherry — Good research deserves good taste. Not just how it looks. How it thinks." width="1200">
</picture>

<p align="center">Research presentation design. With a sense of taste.</p>

<p align="center">
  <a href="#use-palate">Get started</a> &nbsp;·&nbsp;
  <a href="references/design-system.md">Design principles</a> &nbsp;·&nbsp;
  <a href="docs/usage.md">Documentation</a>
</p>

<br>

## Clear ideas. Considered slides.

**palate. by Sherry** is a Codex skill for research presentations. It brings structure, visual judgment and scientific care to an editable PowerPoint deck, shaped around the audience, the time and the depth of the talk.

A palate for ideas. A palette for slides. Yes, the name is doing a little extra work.

| You bring | Palate returns |
| :--- | :--- |
| A research PPTX | An editable redesigned deck |
| An audience, a time, a purpose | A considered reading order and level of detail |
| Scientific evidence | Preserved data, qualifications and references |
| A design brief | A concise transformation report |

<br>

## Good taste has a method.

Teal accents. Clear hierarchy. Room for the evidence. Section arrows and conceptual part markers where they help the listener follow the argument.

The design follows the research: a comparison gets comparable scales; a method gets a readable chain of reasoning; a result gets evidence and explanation together. Text, charts, tables and diagrams stay native where possible. Complex source figures stay intact when reconstruction cannot be verified.

## Use Palate

Install from the repository with Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate-by-sherry.zip --install "$env:USERPROFILE\.codex\skills\palate-by-sherry"
```

Use an existing bundled Python runtime when available. Then attach a research deck and ask:

```text
Use $palate-by-sherry to redesign this PPTX for a 10-minute internal tutorial.
The audience knows the fundamentals but is new to this method.
Explain the mechanism clearly, retain the key equations and caveats,
and return an editable PPTX with a concise transformation report.
```

PowerPoint on Windows provides the included render workflow. New or rebuilt slides use an available native presentation authoring workflow. Single-page monthly updates are outside this skill's scope.

<details>
<summary>Explore the workflow</summary>

- [Usage and requirements](docs/usage.md)
- [Design system](references/design-system.md)
- [Transformation plan](references/transform-plan.md)
- [Scientific fidelity](references/scientific-fidelity.md)
- [Validation](docs/validation.md)

</details>

<br>

<p align="center"><em>Good research deserves good taste.</em><br><sub>Not just how it looks. How it thinks.</sub></p>
