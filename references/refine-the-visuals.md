# Refine the visuals

Visual design gives a developed argument a form the audience can follow and inspect. Begin with the context from [Read the room](read-the-room.md), the slide roles and evidence relationships from [Find the thread](find-the-thread.md), and the wording and necessary detail from [Distill the message](distill-the-message.md). If the visual cannot explain the intended relationship without inventing evidence or hiding a qualification, return to those decisions before polishing the layout.

This is the canonical reference for typography, work area, navigation, text containers, table treatment, color and recurring branding. The specialist guides below own detailed visual composition and asset decisions. Apply the [decision library](design-decision-library.json) within each rule's trigger and exceptions; retain an effective existing design when a change offers no identifiable benefit.

Before authoring, specify the visual contribution and supporting text for each slide. Use the [outline, storyboard and construction sequence](visual-storytelling.md#outline-then-storyboard-then-build) after narrative diagnosis. Carry out changes through the selected [PowerPoint](pptx-workflow.md) or [Keynote](keynote-workflow.md) workflow, keeping a private source-to-output record and separate checks of scientific content, editability and rendered appearance.

## Section navigation and conceptual parts

Hierarchy also helps listeners follow a longer explanation. Use meaningful section arrows when orientation is needed, with no more than five items in a section navigation ribbon. When a study has more sections, choose at most five truthful higher-level groups and map every subsection to its appropriate group in the private design specification. Preserve every scientific section and its topic content; the grouping simplifies orientation rather than reducing the study's scope. Highlight the group containing the actual current section. Key takeaways do not need a separate ribbon item. The closing synthesis may sit within a truthful conclusion or discussion group, or omit navigation; do not consume a ribbon slot merely because a summary slide is required. Do not truncate the ribbon to the first five sections, hide additional sections behind an ellipsis or add a second concurrent ribbon to bypass the limit.

Whenever a section navigation bar is present, place it above the slide title so listeners encounter the broader context before the current topic. Keep navigation items compact and visually connected. Arrow segments should adjoin or interlock closely so the bar reads as one continuous strip, with only narrow, consistent separators. Do not widen the gaps to fill the row. Use native editable navigation labels at 12 pt or larger after text fitting and group scaling. Vertically center them within the navigation shapes, with consistent internal insets across sections and comparable slides. Keep repeated label frames, positions, insets, font family, size and weight fixed across slides; emphasize the active group through color or fill so its words do not move when the section changes. Resolve long labels through concise wording, adjusted segment widths or a coherent reflow of the bar within the five-item limit; do not shrink labels to fit or reduce their effective font size below 12 pt. A cover or self-contained page does not need navigation solely to satisfy this placement rule.

For a subject explained through conceptual parts, use title markers such as `(1/3)` to show progress. Count the parts of the explanation, which may span several slides; do not invent a denominator or renumber by slide count.

## Work area and typography

Define the work area before placing content. It is a rectangle centered on the slide, with equal left and right margins and equal top and bottom margins; horizontal and vertical margins need not be the same. Choose its dimensions for the actual canvas and record its bounds and units in the private design specification. A coordinate example such as horizontal and vertical half-extents does not prescribe the same physical size for every deck. Use matching master or layout guides where the native workflow supports them.

Keep titles, section navigation, figures, labels, explanations, citations and footnotes inside this area. The slide number is the only foreground-content exception: place it outside the work area at the bottom right, using black on a light background and white on a dark one. A slide background may fill the canvas. Check the visible extent of grouped and rotated objects, connectors and text overflow, rather than only their unrotated frames.

Within that boundary, apply the [scientific grouping and spacing sequence](spacing-and-hierarchy.md#from-scientific-groups-to-a-checked-layout), adapting the composition when the scientific relationship changes.

Use the following type hierarchy when applying Sherry's style. The minimum is a requirement; the usual sizes are starting points that can increase for the content and viewing conditions.

| Role | Typeface or size | Design intent |
| :--- | :--- | :--- |
| Slide title | Fira Sans family, usually Extra Condensed Bold | Retain a suitable variant from the approved reference; size the title for its role and available space. |
| Prominent subheading | Usually 16 pt | Make a meaningful secondary level easy to identify. |
| Body text | Fira Sans for Latin text, usually 12 pt | Keep the explanation readable without competing with the title. Use a suitable companion for other scripts. |
| Section navigation labels | At least 12 pt | Keep orientation readable; fit the wording and ribbon layout without shrinking labels below this size. |
| Footnote or minor supporting text | At least 10.5 pt | Reserve the smallest size for low-priority information. Essential qualifications remain prominent with their evidence. |
| All displayed text | Never below 10.5 pt | Include editable table text, chart labels, legends, units and citations in the review. |

Read actual text formatting as well as theme defaults: a deck can declare Arial in its theme while using Fira on its visible titles. Preserve useful body-font pairings, embedded fonts and the fonts needed for other scripts or mathematics. Verify availability and rendered glyphs before choosing a family; a missing registry entry alone does not establish substitution. Do not silently substitute Arial or Calibri for the intended title font, or assign Fira to text whose script it cannot render. When the intended font cannot be used, explain the limitation and resolve a suitable alternative before final delivery.

Typography and space work together: heading scale, explanatory text and the interval between them should show their roles at a glance. Check effective sizes after inheritance, group scaling and automatic text fitting. When text overflows, rearrange, enlarge its space or split the explanation with a content ledger instead of shrinking it below the minimum. Text inside a retained image needs a separate legibility review at its final placed size; a native font-size check cannot certify it. Enlarge or reconstruct that evidence only when scientific fidelity can be verified, and keep an unresolved limitation explicit.

Apply the [spacing and hierarchy guide](spacing-and-hierarchy.md#from-scientific-groups-to-a-checked-layout) to combine geometric alignment with optical judgment while preserving scientific associations and comparison scales.

## Recurring logos and watermarks

Recurring logos and watermarks should follow the deck's intended slide roles and branding variants. Compare equivalent pages and inspect their actual master and layout inheritance before treating an absence as an omission. A cover, section divider, full-bleed image or deliberately unbranded layout can have a different treatment; its role alone does not establish whether a mark belongs there.

Restore an isolated missing mark through the appropriate native master or layout, or by restoring the slide's intended inheritance. Reuse the correct existing asset and preserve its proportions and intended placement. Keep foreground marks inside the work area; an intentional full-canvas background watermark retains its background role and coverage. Avoid individual pasted copies, duplicate marks and blanket changes to master-graphics visibility. Keep an uncertain brand or intentional exception unresolved until its intended treatment is clear. Inspect every slide affected by a shared-layout change for visibility, contrast, overlap and unintended propagation. Follow the application-specific [PowerPoint](pptx-workflow.md) or [Keynote](keynote-workflow.md) workflow for the native repair and review.

## Text boxes and tables

Choose vertical anchoring by the role of the container. Unfilled body text, captions and free-standing subheadings use top anchoring so their first lines remain stable across comparable slides with different amounts of text. Flowchart nodes and filled text boxes use vertical middle anchoring, with balanced internal top and bottom clearance. This includes text placed over a separate bounded background shape; a renderer's object type must not defeat the intended composition. A whole-slide background alone does not turn unfilled body text into a filled text box. Within a large background panel containing several elements, center each designated label or text region, not the entire mixture of headings, figures and prose as one text block. Preserve the established slide-title anchoring. Navigation labels and table cells retain vertical middle anchoring. Horizontal paragraph alignment remains a separate choice.

| Content | Vertical alignment | Horizontal alignment |
| :--- | :--- | :--- |
| Unfilled body text, captions and free-standing headings | Top | Keep the paragraph alignment appropriate to the explanation. |
| Flowchart nodes and filled text boxes, including filled heading bands and callouts | Middle within the intended text region, with balanced vertical insets | Keep explanatory prose left-aligned when useful; center short labels when appropriate. |
| Section navigation labels | Middle, with consistent internal insets | Keep the established label alignment. |
| Title text-box content | Preserve the established title layout | Keep the established title paragraph alignment. |
| Descriptive table text | Middle | Left |
| Very short table entries, including numbers | Middle | Center |

For repeated top-anchored text roles, align the box's top edge and keep its top inset, paragraph space before and first-line typography consistent. Inspect automatic fitting and inherited styles as well as direct properties. Compare the visible first-line position across successive slides; a matching container boundary alone is insufficient. Text-box height may follow the content without moving that starting position. This first-line rule applies to top-anchored roles. For a flowchart node or filled text box, honor middle anchoring and keep the intended text region explicit.

For the same logical text retained across consecutive slides, follow [the retained-text continuity rule](spacing-and-hierarchy.md#keep-retained-text-fixed-across-slide-changes). The more flexible height rule above concerns corresponding roles with different content.

Apply the table choices consistently to comparable entries, including headers according to their content. Use right or decimal alignment only when explicitly instructed; a numerical data type does not supply that instruction. If table-cell centering exposes a fit problem, adjust the container, padding or composition while preserving the 10.5 pt minimum. An explicitly required layout can override the defaults, with its reason retained in the private design specification.

Substantial text needs a visible design treatment that gives the explanation a clear entry and internal hierarchy. Depending on its role, use a concise heading with an accent rule, a restrained background treatment or clearly labeled groups with deliberate spacing. Choose the treatment to reveal the argument and its relationship to nearby evidence. Keep continuous reasoning in connected prose, retain scientific qualifications, and reserve enough space for the text to remain readable. Short labels and captions can remain plain.

## Visual treatment for every slide

Follow [every-slide composition](visual-storytelling.md#review-every-slide-as-a-complete-composition) for the whole requested scope. Plan what the audience learns from each visual, preserve sufficient visible scientific explanation and retain justified typography-led exceptions. A text panel or icon is a grouping or recognition aid, not evidence that the slide explains its subject. Split a complex explanation at a coherent boundary when necessary, maintaining source coverage, qualifications and continuity.

| Visual decision | Detailed reference and purpose |
| :--- | :--- |
| Source-specific schematics | [Objects and relationships](visual-storytelling.md#build-around-objects-and-relationships): expose the relevant operation, comparison or changed condition with native labels and relationships where feasible. |
| Illustration language | [Illustration language](visual-storytelling.md#choose-the-illustration-language): choose a light editorial or infographic treatment by explanatory purpose. Preserve sufficient object detail and structure; a lightweight style does not justify an underdeveloped main visual. |
| Main visual production and finish | [Asset construction](visual-storytelling.md#select-and-construct-assets-deliberately) and [visual review](visual-storytelling.md#review-the-contribution-then-the-rendering): select a capable authoring method, develop the main asset, and verify specificity, explanatory contribution and finish. An enlarged standalone icon cannot pass as the main illustration. |
| Supporting icons | [Icon role and scale](visual-storytelling.md#keep-icons-in-a-supporting-role): compact cues in flowcharts or before subheadings and section labels; do not enlarge a lone icon into the main illustration. |
| Research Question page | [Question framing](visual-storytelling.md#frame-a-research-question): adapt illustrated motivation, dominant question and related subquestions to the actual research, without inventing a causal chain or fixed number of cards. |
| Comparisons | [Comparison patterns](comparison-patterns.md): choose a supported arrangement with shared criteria where valid; preserve unequal evidence and design another arrangement when needed. |
| Cover | [Cover art direction](cover-art-direction.md): develop the whole composition, normally using organic editorial illustration on a light ground. Preserve the guide's subject, atmosphere, typography, asset and fallback conditions. |
| Grouped figure panels | [Figure panels](figure-panels.md): separate or recompose evidence only with original identities, shared axes, legends, scales and qualifications intact. Native framing does not make image interiors editable. |
| Country identifiers and sourced assets | [Asset sourcing](asset-sourcing.md): verify small flags beside country names and any licensed icons without changing scientific encodings or assuming an available integration. |
| Presentation ending | [Plan the final audience-facing slide](visual-storytelling.md#plan-the-final-audience-facing-slide): choose, retain or explicitly omit a dedicated closing slide according to the brief and scope. Place it after the final content or conclusion slide and before appendices; a conclusion or research summary cannot serve both roles. Match the deck's visual system and keep its text and layout editable. A research summary follows [visual key takeaways](visual-storytelling.md#close-with-visual-key-takeaways); discussion or thanks pages have their own purpose. Use [closing compositions and backgrounds](closing-layouts.md) when a concrete layout or background would help, loading only the selected option. |
| Diagram edges | [Connector review](visual-storytelling.md#connect-the-intended-objects): verify meaning, source, target and visible attachment after final layout. |
| Repeated text and spacing | [Spacing and hierarchy](spacing-and-hierarchy.md): maintain semantic groups and lock retained text across consecutive slides; compare actual rendered positions. |
| Reference adaptation | [Style adaptation](style-adaptation.md): transfer supported design properties without treating reference artwork as scientific evidence or copying editing remnants. |

Illustration style does not establish source support or editability. Keep evidence, explanatory schematics and illustrative depictions distinct; retain complex figures when accurate reconstruction cannot be verified. Apply [scientific fidelity](scientific-fidelity.md) to content and [slide citations](distill-the-message.md#slide-citations-and-references) to APA 7 attribution and italic reference styling.

## Choosing a text-box treatment

A light neutral fill can make a self-contained explanation easier to distinguish from neighboring evidence. Consider a pale gray panel with gently rounded corners when the text needs that enclosure, giving it comfortable internal space and a clear heading. Treat fill, corner shape, inset spacing and type hierarchy as one composition; the enclosure should clarify a group without crowding its content or competing with the figure.

For headings that introduce distinct modules or parallel explanation blocks, normally use native text boxes with a solid accent fill and white (`FFFFFF`) text. Choose a fill from the deck's resolved palette that is dark enough for readable white lettering; match the treatment across comparable module headings. Keep the text editable, vertically centered with balanced internal insets, and size the box to fit the heading without crowding. When a sequence such as `01 / 02 / 03 / 04` already establishes the modules' order and hierarchy, keep the headings unfilled with readable dark text on a light background; a dark heading band is not required. A small relevant icon may precede the heading text, using a coherent family and the [supporting icon scale](visual-storytelling.md#keep-icons-in-a-supporting-role); Flaticon is an available option under the existing [asset-sourcing rules](asset-sourcing.md). Preserve the numbering and keep the title text editable. This treatment applies to module headings; body explanations, figure captions and slide titles retain their own roles and anchoring. A filled module heading does not change the pure-white slide background required for copied research figures.

| Relationship to explain | Treatment to consider | Check |
| :--- | :--- | :--- |
| A self-contained rationale or interpretation beside evidence | Light gray fill with slight corner rounding; restrained outline if needed | The panel reads as one explanation and stays associated with its evidence. |
| Several comparable explanations | Shared fill, corner treatment and insets, with aligned headings and gutters | Corresponding non-title text starts align even when line counts differ, without forcing equal text lengths or reducing type size. |
| A qualification or takeaway needs a distinct location | A shallow neutral or accent-tinted band, or a heading with an accent rule | Emphasis matches the statement's scientific role and strength. |
| A label or caption belongs directly to a figure | No fill, or a fine separating rule where useful | The text remains visually attached to the figure. |

Use a modest radius relative to panel height, preserve visible clearance around the text and keep the complete treatment inside the work area. On dark slides, choose a neutral tone that suits the background and preserves contrast. The [reference comparisons](spacing-and-hierarchy.md#design-references-and-their-limits) inform these choices; specific brand colors and shapes remain local examples. A panel can improve grouping, while headings and intervals still carry the explanation within it.

## Table color options

After inspecting a deck that contains tables, offer two color treatments using one representative table. Keep the content, layout, typography, numeric precision and emphasis targets identical in both previews so the choice concerns color. Use a native preview or a clearly identified design preview, and present the choices through the available question tool.

| Option | Color treatment | What remains consistent |
| :--- | :--- | :--- |
| Nature-inspired | Warm stone headers (`D8D6C2`), black header and body text, and white body cells, following Sherry's preferred journal-inspired table treatment. | Scientific category mappings, quantities, uncertainty and source precision. |
| Deck-matched | Derive headers, light fills and accents from the deck's established colors; use a coherent light-to-dark hierarchy with readable contrast. | The deck's semantic color roles and the same scientific content. |

Use a restrained table structure in both previews: black horizontal rules at the top, below the header, between meaningful body groups and at the bottom, with no visible vertical grid. A rule around 1 pt is a starting point; check its weight at the final slide size. Add grouped or multi-level headers only when the data needs them. Keep the established typography, alignment and numeric-display rules.

Myriad Pro at 12 pt is the reference face for this table treatment. Use it as a table-specific pairing when its genuine fonts and rendered glyphs can be verified, retaining the established title and body hierarchy. Resolve an available alternative if needed rather than silently substituting a font.

The Nature-inspired option names Sherry's preferred journal-like treatment, not an official Nature table standard. Nature's [scientific illustration guide](https://www.nature.com/documents/Nature_scientific_illustration_author_guide.pdf) informs color hierarchy and accessibility for conceptual figures; it does not prescribe this preset. Adapt contrast for the background and viewing conditions while retaining the chosen treatment and scientific color meanings.

Ask only when a table is present and the current request has not already supplied or delegated the palette decision. Offer exactly these two preset choices, retaining any custom-answer facility supplied by the host. Wait for a submitted choice or explicit delegation before applying final table colors; continue independent content and layout work while it is pending. Reuse the choice for comparable tables in that deck. Keep it in the private design specification rather than adding unsupported fields to a helper schema.

Color can encode a category, sign, threshold or magnitude. Preserve that mapping in both options, including heatmaps and significance markings; adjust nonsemantic headers, rules and neutral fills where necessary. Check contrast in light and dark slides, retain explicit labels, and preserve the existing alignment, 10.5 pt minimum and numeric-display rules.

For an image-only table, first establish whether an editable reconstruction can be verified. A design preview does not establish native editability; retain the original or obtain a suitable source when reconstruction cannot preserve its evidence reliably, and state the remaining limit.

## Give color a consistent purpose

Choose colors from the slide's question, scientific encodings, supplied references and resolved brief. Sherry prefers clean, identifiable hues and clear foreground/background separation. Restraint comes from purposeful emphasis and a readable hierarchy, not from making every color grayish. Both a focused highlight and a larger categorical palette can work. There is no default teal, universal palette, fixed color count or topic-to-hue assignment.

When a new palette is needed, retrieve a coordinated recipe from the single [curated library](curated-palettes.json) with [select_palette.py](../scripts/select_palette.py). Run `python <skill-root>/scripts/select_palette.py --task <task>` using the task below; `--id <palette-id>` retrieves one known recipe, and `--list` returns a compact ID/task index. Read only the matching result, then reuse its ID and HEX-to-role mapping in the private design specification. Do not repeatedly load the whole library. The helper retrieves candidates; the agent chooses and applies the roles through the actual authoring route. It does not automatically recolor a deck.

Preserve a recipe's coordinated combination and distinguish its data colors from background, text and supporting roles. A documented subset can fit fewer categories; do not mix unrelated swatches or invent extra steps to satisfy a category count. Follow the recipe's intended uses and limits. Keep chart style separate from palette semantics: an ordinal bubble scale does not identify unordered groups, while redundant size/color encoding of the same quantity can be valid when the key says so. The library contains color combinations and usage guidance, not reference documents, page indexes, preference records or source-specific scientific legends. Keep any supplied reference material and task-specific analysis private.

Give each color a role before applying it: category identity, quantitative magnitude, sign, comparison context or narrative emphasis. Keep the same identity across related slides and support it with labels, markers or line styles. Prefer very light but distinguishable grays for neutral backgrounds, grids and supporting structure; keep text clearly readable. A gray or taupe data series may be stronger when its legend gives it a specific comparison role. Avoid making gray-blue, gray-purple or muted text the whole slide's visual treatment. Red, green and teal remain available when justified by the task and its scientific encodings; no library hue is a default. Preserve source scientific mappings and follow the current brief.

### Choose the background with the evidence

Apply these preferences when designing or restyling pages, subject to explicit instructions in the current brief. Existing scientific encodings remain binding.

| Page condition | Background treatment |
| :--- | :--- |
| Contains a research-figure screenshot or a figure copied from a paper | Use a pure white (`FFFFFF`) slide background. Preserve the figure's pixels, labels and scientific mappings; recoloring its interior or placing its white rectangle on a colored slide is not a substitute. |
| Figure-free page with a light background | Use the approved clean beige (`F8F4EC`) with readable dark text and distinct accents. |
| Dark page without a copied research figure | Use a flat deep blue-gray treatment, such as `203040`, warm off-white headings, clear white body text and concentrated accents. Adapt the composition to the content. |

Native charts and conceptual diagrams can be evaluated on light or dark grounds when their scientific mappings, labels and contrast remain sound. Do not flatten or redraw evidence merely to qualify for another background.

### Match the visual encoding to the question

These are contextual choices, not a compulsory chart menu. Use an available native editable representation where it can preserve the evidence.

| Explanatory task | Useful treatment and its boundary | Recipe task |
| :--- | :--- | :--- |
| Emphasize a meaningful group | Give that group a clear color and retain other observations in a lighter comparison treatment. Reinforce membership in labels when useful. The highlighted group need not be the largest value. | `single-highlight` |
| Distinguish many categories | Choose visibly distinct hues at the actual mark size; keep identities stable and use direct or line-end labels. Separate panels when the audience cannot track the categories reliably. | `multiseries` or `categorical` |
| Compare two states or scenarios | Use paired endpoints, connectors and optional direction arrows on a common scale. Any variable connector width requires a separately defined quantity and key. Keep historical/future uncertainty bands tied to their series. | `paired-contrast` or `scenario-bands` |
| Show a relationship with an additional quantity | Consider a bubble plot with explicit axes and a size key. Encode magnitude through circle area, define any color mapping and annotate selected cases. Association or a nearby event marker does not establish causality. | `categorical-bubbles` or `ordered-bubbles` |
| Show additive contributions over time | Consider stacked area with stable category identities, direct labels and a clear distinction between observations and projections. Stronger selected layers and pale remaining layers can preserve both focus and total context. Define any overlaid aggregate separately; stacked values must be meaningfully additive. | `many-category-stack` or `stacked-area` |
| Show percentage levels or changes on a map | Use an ordered sequential scale for levels. For signed change, evaluate a diverging scale around a meaningful neutral value. Keep no-data distinct and distinguish percentage levels, relative percentage change and percentage-point differences. | `ordered-percent-map` or `diverging` |
| Compose a calm editorial illustration | Match the subject and illustration language to the explanation, then preserve the chosen combination's structural and accent roles. Coastal Clear Blues and Editorial Blue & Terracotta remain distinct positive examples, not universal coastal or blue themes. | `calm-illustration` |

For newly designed or deliberately recolored graphics, choose color-vision-friendly palettes and avoid introducing rainbow gradients. Keep concise axis and legend labels unambiguous, using stable symbols and the [unit-label convention](scientific-fidelity.md#unit-labels). Remove redundant decoration rather than data, uncertainty or essential context. These choices do not authorize recoloring or simplifying retained evidence whose scientific mappings cannot be verified.

Before changing a figure, inspect its legend and category mappings. Those mappings carry scientific meaning and take priority over the preferred palette. Reuse a concise, resolved set of color roles in the private design specification. When a consequential choice is unresolved, compare a small number of representative native renders with wording, data, layout and typography held constant. A rejected treatment calls for revisiting its use, pairing and distribution of color, rather than repeatedly substituting isolated hex codes. User approval of a reference page does not approve every hue on it.

Check contrast, label legibility and legend consistency in the final render. Inspect the HEX actually used by native/vector objects; a retrieved recipe alone does not prove application or accessibility. If a raster image model is used, condition it with the chosen combination and roles, inspect the result and disclose that exact HEX compliance is not guaranteed. Prefer editable vectors or native charts when exact values matter. A diagram also needs enough resolution for its relationships and labels to remain readable. Retain a complex source figure when reconstruction cannot be verified; upscaling cannot recover missing detail. Topic-specific illustrations, such as a lightbulb for energy, are optional choices rather than brand requirements.

## Review the design against the research

A visual decision is complete only when the resulting slide communicates the source accurately and meets the applicable visual-finish criteria. Follow the [scientific fidelity workflow](scientific-fidelity.md) to trace content changes and review scientific meaning, editability and rendered appearance separately.

When a main visual fails review, identify the concrete defect and revise the asset or composition before inspecting the native render again. Correct the source of the problem rather than merely describing it in the delivery report. Use the existing private review record for the observed defect, correction and acceptance evidence; no separate review workflow is required. A structural pass, successful image generation or completed export cannot establish visual quality. If an essential check or correction remains unresolved, state the limitation and retain candidate status.

When explaining the changes, follow the [writing style](writing-style.md): connect the decision with the audience's need, its design reason and any limiting condition. Use continuous prose to develop the argument and tables when discrete information benefits from comparison. These documentation forms explain the design; they do not prescribe the layout of a slide.
