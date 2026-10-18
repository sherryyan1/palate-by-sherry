# Spacing and hierarchy

Spacing tells listeners which elements belong together, where an explanation begins and when attention should move to another idea. A slide can have aligned objects and ample empty area yet communicate the wrong relationships. **palate** judges space by the scientific reading order it creates, then checks whether the intended grouping remains clear at the actual display size.

Use this guide when composing a slide or reviewing a layout that feels crowded, disconnected or uneven. It develops the spatial decisions introduced in the [design system](design-system.md). The centered work area is a standing constraint; its dimensions and the intervals within it depend on the actual canvas and content.

## From scientific groups to a checked layout

1. **Identify what must be read together.** Keep a figure, its relevant interpretation and essential qualifications close enough to form a group. Give a separate argument a more distinct interval. A larger gap can accidentally detach a unit, label, caveat or legend from its evidence, so establish these associations before adjusting the geometry.
2. **Define the symmetric work area, then its internal intervals.** Set equal left/right margins and equal top/bottom margins before placing content, recording the bounds in the units required by the native workflow. Keep every foreground element inside this area, including titles, navigation and footnotes. Only the slide number sits outside at the bottom right, black on light slides and white on dark slides. Check object extents and visible text, including groups and rotated elements. Repeat comparable gaps across comparable relationships within the work area, varying them when the content changes. When the canvas changes, reconsider the work area and composition while keeping the type hierarchy and 10.5 pt minimum.
3. **Inspect the visible content as well as its coordinates.** Text boxes include internal margins and space beyond glyph bounds; letters, symbols and different type weights carry unequal visual mass. Compare visible edges and baselines, then make modest optical adjustments where equal coordinates appear uneven. Preserve chart-axis alignment and meaningful comparison scales while doing so.
4. **Review the final render at the intended display scale.** Judge breathing room and association together with text scale, weight and leading. Keep labels, units, legends and uncertainty readable. Dense scientific evidence can justify compact spacing when each relationship remains clear and the required detail can still be inspected.

When a section navigation bar is present, reserve a row above the slide title and keep the two roles visibly separate. Limit the ribbon to five items. For a longer argument, use meaningful higher-level sections and map the detailed topics to them, preserving every topic within the agreed scope. Within the bar, keep adjacent items close. For arrow navigation, inspect the visible seam between each tip and the next notch; a small overlap of shape frames may be needed to keep that seam narrow and consistent. Adjust segment widths, concise wording and the bar's overall placement to fit the row, keeping labels at least 12 pt after fitting and scaling. Do not spread the items apart to fill the available width or shrink labels to resolve a fit problem. Vertically center the labels within the navigation shapes, using consistent internal insets across sections and comparable slides. Check the rendered label positions and fit rather than applying the body-text top-anchor rule to navigation. Covers and self-contained pages need no navigation solely to satisfy this rule.

Inspect space inside containers as well as between them. Top-anchor unfilled body text and keep the top edge, top inset, paragraph space before and first-line typography consistent for corresponding roles across slides. Vertically center flowchart-node text and filled text boxes within their intended text region, with balanced vertical insets. Apply this to separate text-over-background objects as well as text inside a native shape. For top-anchored roles, one-line and two-line blocks should share the same visible starting position. Middle-anchored containers follow their own alignment rule; when their logical text is retained unchanged across slides, lock the container height and position as well as the text metrics. Compare successive comparable slides as well as individual pages; equal box coordinates alone do not establish that consistency. Preserve established title-layout anchoring. Table cells retain vertical middle anchoring; left-align descriptive text and center very short entries such as numbers, using right alignment only when explicitly instructed. A substantial text block also needs a deliberate visual treatment and internal hierarchy, as described in the [text-box and table guidance](design-system.md#text-boxes-and-tables). Keep those treatments within the work area and preserve the association between the explanation and its evidence.

## Keep retained text fixed across slide changes

Text should not run when a slide changes. If the same logical text element remains on consecutive slides, its words must remain in the same visible position while the new material changes around it. This applies to a repeated paragraph, heading, caption, diagram label or navigation label. Match elements by their role and source identity, not merely identical strings that happen to appear in different parts of the research.

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
