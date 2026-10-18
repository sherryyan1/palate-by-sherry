# Spacing and hierarchy

Spacing tells listeners which elements belong together, where an explanation begins and when attention should move to another idea. A slide can have aligned objects and ample empty area yet communicate the wrong relationships. **palate** judges space by the scientific reading order it creates, then checks whether the intended grouping remains clear at the actual display size.

Use this guide when composing a slide or reviewing a layout that feels crowded, disconnected or uneven. It develops the spatial decisions introduced in the [design system](design-system.md). The centered work area is a standing constraint; its dimensions and the intervals within it depend on the actual canvas and content.

## From scientific groups to a checked layout

1. **Identify what must be read together.** Keep a figure, its relevant interpretation and essential qualifications close enough to form a group. Give a separate argument a more distinct interval. A larger gap can accidentally detach a unit, label, caveat or legend from its evidence, so establish these associations before adjusting the geometry.
2. **Define the symmetric work area, then its internal intervals.** Apply the [work-area and typography requirements](refine-the-visuals.md#work-area-and-typography), recording the bounds in the units required by the native workflow before placing content. Repeat comparable gaps across comparable relationships within the work area, varying them when the content changes. When the canvas changes, reconsider the work area and composition while keeping the type hierarchy and 10.5 pt minimum.
3. **Inspect the visible content as well as its coordinates.** Text boxes include internal margins and space beyond glyph bounds; letters, symbols and different type weights carry unequal visual mass. Compare visible edges and baselines, then make modest optical adjustments where equal coordinates appear uneven. Preserve chart-axis alignment and meaningful comparison scales while doing so.
4. **Review the final render at the intended display scale.** Judge breathing room and association together with text scale, weight and leading. Keep labels, units, legends and uncertainty readable. Dense scientific evidence can justify compact spacing when each relationship remains clear and the required detail can still be inspected.

When a section navigation bar is present, apply the [section navigation requirements](refine-the-visuals.md#section-navigation-and-conceptual-parts). Reserve a row above the slide title and keep the two roles visibly separate. Keep the bar compact, with no more than five items and labels at least 12 pt after fitting and scaling. Group longer arguments without dropping topics. For arrow navigation, inspect the rendered seams between tips and notches; a small overlap of shape frames may be needed to keep them narrow and consistent. Check rendered label positions, fit and vertical centering under the navigation rules rather than applying the body-text top-anchor rule. Covers and self-contained pages need no navigation solely to satisfy this rule.

Inspect space inside containers as well as between them. Apply the [role-specific text-box and table requirements](refine-the-visuals.md#text-boxes-and-tables). For corresponding top-anchored roles with different content, compare the visible first-line positions across slides rather than box coordinates alone. For the same logical text retained across consecutive slides, apply the [retained-text continuity requirements](#keep-retained-text-fixed-across-slide-changes), including the fixed height of middle-anchored containers. Compare successive comparable slides as well as individual pages. For substantial text, apply the [visual treatment and internal hierarchy requirements](refine-the-visuals.md#text-boxes-and-tables). Keep those treatments within the work area and preserve the association between the explanation and its evidence.

## Keep retained text fixed across slide changes

Text should not run when a slide changes. If the same logical text element remains on consecutive slides, its words must remain in the same visible position while the new material changes around it. This applies to a repeated paragraph, heading, caption, diagram label or navigation label. Match elements by their role and source identity, not merely identical strings that happen to appear in different parts of the research.

Independent cover alternatives shown for design comparison deliberately explore different title positions and typography. They are not narrative builds and do not require the same text geometry. Once a cover is selected, any consecutive builds of that design follow the retained-text rule.

Establish a shared target position and typography for the output sequence, then reuse that object or a copy with its layout properties intact. The lock applies between output slides; it does not prevent a consistent redesign of the entire sequence. Record the retained element and its locked properties in the private slide specification:

| Property | What must remain stable |
| :--- | :--- |
| Geometry | Native x/y position, width, height, rotation and any parent-group translation, rotation or scale. |
| Text metrics | Effective font family, weight, size, character spacing, line spacing, paragraph spacing and line breaks, including the actual outcome of automatic fitting. |
| Text origin | Vertical anchoring, horizontal alignment and internal insets, so the first visible glyph and each baseline retain their position. |
| Embedded labels | Placement, scale and crop of a retained figure containing unchanged labels; equal image frames alone do not establish stable interior text. |

For a middle-anchored node or filled text box, changing the container height can move unchanged text even if its top edge stays fixed. Reuse the complete text region, anchor and balanced insets; put new content in another region if needed.

Top anchoring prevents a one-line block from sinking relative to a two-line block, but does not lock the x position, wrapping or glyph metrics. Do not move, resize or refit retained text to accommodate new neighboring content. Recompose the changing material or split the explanation around the locked element. If a marker or other text fragment changes within a persistent heading, reserve its space so unchanged words do not shift. Repeated navigation labels keep the same frames and font metrics; show the active section through fill or color rather than a size or weight change that moves the lettering. A deliberate relocation requires an explicit user instruction, not an inferred need for variety.

Review every adjacent slide pair containing retained text at the same canvas scale. Inspect native properties, then alternate the actual application renders or use an aligned overlay when helpful. Compare visible word starts, line endings and baselines as well as box coordinates. Any positional jump in a retained element remains an issue to correct. A whole-deck contact sheet, a single-slide inspection or a passed package check does not establish continuity.

## Resolve spacing problems

When a layout fails, identify the relationship at fault before changing all the gaps:

| Condition | Design response and check |
| :--- | :--- |
| Groups merge visually | Clarify the gap between groups; keep each group's labels and qualifications attached. |
| A heading feels disconnected | Reconsider its distance, weight and scale together; verify the intended parent-child relationship. |
| Evidence fills the slide | Preserve readable labels, units, legends and uncertainty. Reorganize or split with a content ledger when appropriate; never delete science or shrink all text to manufacture whitespace. |

Mandatory layouts and comparison axes can constrain rearrangement. Work within those constraints, preserving the evidence associations and scales. Neither equal gaps nor maximum empty space is a goal by itself.

## Design references and their limits

The references below explain why space changes what readers notice and associate. Their principles can inform a research slide; brand-specific logo ratios and UI pixel or rem values belong to their original systems and are not fixed slide presets.

| Reference | Relevant principle and application |
| :--- | :--- |
| [Apple identity guidelines, page 10](https://training.apple.com/content/dam/appletraining/us/en/2022/documents/Apple_ID_Guidelines_Channel_180919.pdf#page=10) | Clear space protects a signature from competing content, and more than the minimum is allowed. Give a mark room to remain distinct; Apple's numeric ratio belongs to its own identity system. |
| [IBM layout guidance](https://www.ibm.com/design/language/layout/tips-and-techniques/) | Repetition and variation create continuity and distinct roles; breathing room provides visual pauses. Repeat dimensions and alignments where relationships repeat, while allowing different content its own composition. |
| [Carbon spacing guidance](https://www.carbondesignsystem.com/building-blocks/foundations/spacing/overview) | Proximity strengthens association, recurring spacing suggests comparable importance, and surrounding space can increase prominence. Organize related elements and give the eye places to rest; dense sections can remain appropriate. |
| [IBM type basics](https://www.ibm.com/design/language/typography/type-basics/) | Alignment, leading and manageable line lengths support legibility; weight, contrast and scale establish hierarchy. Judge spacing with the typography that occupies it, without accumulating redundant emphasis. |
| [Pentagram: The Philadelphia Inquirer](https://www.pentagram.com/work/the-philadelphia-inquirer) | Controlled white space and stronger organization allow larger images and infographics. Organize the page so evidence gains clarity and presence; an editorial layout is not a mandatory slide template. |
| [Oliver Wyman webinar presentation, PDF pages 7 and 8](https://www.oliverwyman.com/content/dam/oliver-wyman/v2/publications/2025/jan/us-election-impact-supply%20chains.pdf#page=7) | A filled commentary panel separates interpretation from the table on page 7; page 8 gives an attributed quotation a panel while leaving ordinary prose open. Use fill to identify a meaningful group. |
| [Roland Berger Trend Compendium, PDF page 6](https://www.rolandberger.com/publications/publication_pdf/roland_berger_trend_compendium_2050_trend_4_economics_and_business.pdf?v=1394673#page=6) | This landscape, slide-format publication separates chart and explanatory column with a fine vertical rule. A clear boundary and aligned reading order can structure text without a fill. |
| [Bain sustainable procurement factsheet, PDF page 3](https://www.bain.com/contentassets/110ea77537cd4ebfb1aecc12d231c69d/updated-sustainable-procurement-factsheet-vfeb-2025---final.pdf#page=3) | Four light gray panels organize parallel categories through shared insets and spacing. This is a portrait factsheet, used here as a grouping reference. |

The reviewed filled panels have square corners. Slight rounding is a contextual option in palate, chosen together with the content, fill and insets. These examples support decisions about grouping; they do not prescribe the text alignment, typography, colors or geometry of a research deck.
