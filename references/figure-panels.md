# Recompose a multi-panel figure

A dense figure can become easier to explain when its panels are separated and given distinct places in the argument. Treat this as a change in presentation, not a change in evidence. First establish what each panel shows and how it depends on the others, then decide whether to retain the whole figure, make a grouped overview or develop the panels across several slides.

The rounded-panel treatment is a contextual option. Consider generous rounded color regions, a compact native heading badge and a retained source panel within each region when they help listeners connect an idea with its evidence. Use a pale fill behind a plot where contrast permits, reserving stronger color for a heading or badge. Match the number of regions to the actual content; the example of four panels does not require a four-card template.

## Establish the panel identities before cropping

Read the complete figure, caption and associated source explanation. Inventory the panel letters, axes, units, legends, color bars, scale bars, annotations, uncertainty, statistical labels and references. Identify any shared item needed to interpret an individual panel. A crop that retains the data marks but loses their coordinate system or legend is incomplete.

| Element | How to preserve it |
| :--- | :--- |
| Source panel labels | Retain the original labels and record their relationship to each destination. A new deck-local A, B, C or D label must remain distinguishable from a source label. |
| Hypothesis identifiers | Use H1, H2 or a sub-hypothesis such as H2b only when the source establishes that identity. Do not turn arbitrary evidence groups into hypotheses through decoration. |
| Shared axes, legends and scales | Keep the relevant shared context visible with each interpretation, or retain the original connected layout when separation would be misleading. Verify any native reconstruction against the source. |
| Captions and qualifications | Keep the conditions needed for interpretation near the relevant panel. Map extended caption detail and source attribution to readable notes or an appendix without detaching essential meaning. |
| Source identity | Preserve the original figure and panel citation. Record any new presentation label separately so reordering cannot silently change a cross-reference. |

Separate figures from different studies may be grouped around a question, but the composition must not imply shared controls, a common experiment or comparable scales without support. Retain each source's own identity and qualification. Color can link a heading to its evidence, while the evidence's scientific color mapping stays protected.

Distinguish a request for the rounded H-badge appearance from a request for exact H identifiers. The appearance can use ordinary panel letters. If exact H labels are requested without an established meaning, clarify what they identify before treating them as hypotheses. An explicitly confirmed presentation-group convention can be retained with that role made clear and the original source-panel map intact; it must not silently create scientific hypotheses.

## Extract only what can be checked

Prefer the original vector or high-resolution figure over a screenshot. For an existing editable deck, inspect whether its panels are already separate objects. Reuse those objects when feasible. If the figure is one image, use reversible native picture crops or extract lossless panel copies from the source image; preserve the original privately. Retained panel interiors remain images even when the surrounding labels and layout are editable.

Do not crop away an inconvenient observation, truncate an error bar, hide a legend category or alter the aspect ratio to fit equal cards. Record each panel's source bounds and destination in the private content ledger. Review the complete source alongside the separated panels to verify that all required context remains available. Cropping is not automatic panel detection, figure reconstruction or validation of the underlying study.

The optional [panel extraction helper](../scripts/extract_figure_panels.py) makes bounded pixel crops from a static raster image. It checks source identity and crop bounds, writes PNG copies without resizing and records their identities in a private extraction manifest. It does not decide where a panel ends or which shared legend it needs. Use the available native authoring path to place the extracted images and editable framing; the conservative object-preservation helper cannot perform this reconstruction.

Prepare the plan after inspecting the source. Coordinates are integer pixels with exclusive right and bottom bounds:

```json
{
  "schema_version": 1,
  "source_sha256": "<SHA-256 of the source image>",
  "panels": [
    {"id": "A", "source_panel": "Figure 2a", "box": [0, 0, 800, 600]},
    {"id": "shared-legend", "source_panel": "Figure 2 shared legend", "box": [800, 0, 1000, 600]}
  ]
}
```

The coordinates illustrate the plan structure, not a safe crop for an actual figure. Include shared context crops where needed, then place them visibly with the panels they explain. Keep the plan, source, extracted images and manifest private.

```text
python scripts/extract_figure_panels.py --source figure.png --plan panel-plan.json --output-dir new-panel-output
```

The helper requires Pillow and a fresh output directory whose parent exists. It accepts static PNG, JPEG, TIFF and WebP images only when their decoded pixel mode can be saved as PNG without conversion. Coordinates refer to raw decoded pixels; EXIF rotation is not applied. Orient a private source copy deliberately before selecting coordinates if its displayed orientation differs, then hash that exact copy.

The operation is bounded to 64 panels, a 256 MiB source, a 1 MiB plan and 64 million source pixels or combined crop pixels. Plans reject unknown fields, unsafe or case-colliding IDs, stale hashes and out-of-bounds boxes. Inputs and output paths must not use symlinks or reparse points, and source files must not be hard-linked. Existing output directories are not reused. These guards establish an unambiguous extraction; its output still needs semantic review and native placement before it can establish a scientifically faithful slide.

## Compose the explanation and review it

Keep badges, headings, colored regions, connectors and added labels native and editable. Place each concise interpretation close to its supporting panel, using a consistent reading order and clear internal spacing. Rounded containers should explain grouping rather than force every plot into an identical crop or reduce its usable area. Follow role-based anchoring: center text vertically in filled badges and text regions, and top-anchor unfilled explanations. Preserve retained-text continuity, the 10.5 pt minimum and the symmetric work area.

When several panels need more room, show an overview and then focused details. Reuse the same panel identity and visual grouping across that sequence, with the relevant shared context repeated where necessary. Update every panel reference, note and navigation state affected by reordering or splitting. Keep a whole-figure reference in the appendix when useful for inspection; it does not replace essential context on the main slides.

Compare scientific content, editability and appearance separately. Check each extracted panel against its source bounds and complete figure, then inspect the delivery application's render for legible axes, legends, color bars, captions and panel identities. Verify that the rounded frame obscures no image content and that the reordered composition implies no unsupported relationship. If extraction, attribution or shared-context preservation cannot be verified, retain the whole figure or obtain a usable source instead of claiming a completed reconstruction.
