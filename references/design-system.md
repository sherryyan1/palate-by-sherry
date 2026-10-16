# Design system

A research slide should help listeners follow an explanation and inspect the evidence behind it. **palate** begins with what the audience needs to understand, gives that relationship a visible structure, and then uses typography, space and color to make the structure easier to read. Scientific meaning limits every design choice: a cleaner composition is useful only if the evidence and its qualifications remain intact.

This guide connects the design reasoning to the choices used on slides. The [communication design guide](communication-design.md) develops the reasoning behind explanation and reading order; the [decision library](design-decision-library.json) records the rules, their triggers and their exceptions.

| Kind of guidance | Purpose and example |
| :--- | :--- |
| Design principles | Help the audience understand the research, for example by keeping a finding close to its evidence and essential qualifications. |
| Design preferences | Give the deck a recognizable identity through recurring choices such as teal emphasis, meaningful section arrows and conceptual part markers. |
| Implementation rules | Make changes reliable and review traceable, for example by preserving scientific color mappings and checking content, editability and appearance separately. |

These categories explain the purpose of the guidance. The library's **primary** and **contextual** statuses determine how to apply its rules: apply a primary rule within its trigger and exceptions, and evaluate a contextual composition option against the content and brief. A recurring preference does not belong on every page, and a contextual layout does not become a universal personal preference.

## 01 | Establish what the audience needs

Resolve the audience, available time, purpose and technical depth before choosing how much information to show. A tutorial may need to introduce a mechanism before its formal expression; a specialist discussion may need assumptions and uncertainty close to the result. The brief determines what listeners need during the talk and what they may need to inspect afterward.

| Context | Emphasis to consider |
| :--- | :--- |
| Internal tutorial | Build toward the learning objective through a guided explanation. |
| Internal research | Make the question, method and evidence available for discussion. |
| External experts | Explain the contribution through comparable evidence, assumptions and uncertainty. |
| C-suite / executives | Connect supported implications to relevant decisions, evidence and risk. |
| General audience | Introduce the concepts needed to understand the qualified finding. |

These priorities guide judgment within the brief. An expert audience may not need every derivation, and a short talk still needs the qualifications that make its result accurate. Financial or operational claims require source support; an audience category does not supply an ROI, a decision or a scientific conclusion. Duration guides pacing and depth rather than a fixed slide count. Use [presentation contexts](presentation-contexts.md) for starting points and confirmation of missing context, not as fixed templates.

## 02 | Give the evidence a readable structure

Choose the composition from the relationship the slide explains. Comparisons need shared dimensions so differences can be assessed fairly; a method needs a sequence that connects its symbols, assumptions and steps. For mechanisms, grouping and connections must reflect verified relationships in the source. Retain a source layout when it already explains the material well.

| Content | Design choice | Scientific condition |
| :--- | :--- | :--- |
| Result | Keep evidence beside its interpretation. | Preserve the finding's scope and uncertainty. |
| Comparison | Align scales, labels and reading order. | Make unequal baselines or unmatched controls explicit. |
| Method | Connect symbols, intuition and technical steps. | Retain the chain listeners need to verify. |
| Mechanism | Use labeled objects and meaningful connections. | Reconstruct only relationships that can be checked. |
| Reference | Give citations and supporting detail enough space. | Keep sources readable and traceable. |

Place a concise interpretation near the evidence it explains so listeners can connect the finding with the figure while hearing the argument. Keep essential qualifications visible with it. A full caption or derivation belongs on the main slide when the audience needs to examine it during the talk; supplementary detail can move to mapped notes or an appendix when its absence does not change the meaning.

Hierarchy also helps listeners follow a longer explanation. Use meaningful section arrows when orientation is needed, highlighting the actual current section. Whenever a section navigation bar is present, place it above the slide title so listeners encounter the broader context before the current topic. Vertically center its labels within the navigation shapes, with consistent internal insets across sections and comparable slides. A cover or self-contained page does not need navigation solely to satisfy this placement rule. For a subject explained through conceptual parts, use title markers such as `(1/3)` to show progress. Count the parts of the explanation, which may span several slides; do not invent a denominator or renumber by slide count.

## 03 | Use space and typography to show relationships

Define the work area before placing content. It is a rectangle centered on the slide, with equal left and right margins and equal top and bottom margins; horizontal and vertical margins need not be the same. Choose its dimensions for the actual canvas and record its bounds and units in the private design specification. A coordinate example such as horizontal and vertical half-extents does not prescribe the same physical size for every deck. Use matching master or layout guides where the native workflow supports them.

Keep titles, section navigation, figures, labels, explanations, citations and footnotes inside this area. The slide number is the only foreground-content exception: place it outside the work area at the bottom right, using black on a light background and white on a dark one. A slide background may fill the canvas. Check the visible extent of grouped and rotated objects, connectors and text overflow, rather than only their unrotated frames.

Within that boundary, group the scientific content before choosing gaps. A figure and its interpretation need enough proximity to read together, while a separate argument needs a clearer interval. Space should give the evidence room without detaching its labels, units, legend or qualifications. Keep the rhythm coherent across related pages, adapting the composition when the scientific relationship changes.

Use the following type hierarchy when applying Sherry's style. The minimum is a requirement; the usual sizes are starting points that can increase for the content and viewing conditions.

| Role | Typeface or size | Design intent |
| :--- | :--- | :--- |
| Slide title | Fira Sans family, usually Extra Condensed Bold | Retain a suitable variant from the approved reference; size the title for its role and available space. |
| Prominent subheading | Usually 16 pt | Make a meaningful secondary level easy to identify. |
| Body text | Fira Sans for Latin text, usually 12 pt | Keep the explanation readable without competing with the title. Use a suitable companion for other scripts. |
| Footnote or minor supporting text | At least 10.5 pt | Reserve the smallest size for low-priority information. Essential qualifications remain prominent with their evidence. |
| All displayed text | Never below 10.5 pt | Include editable table text, chart labels, legends, units and citations in the review. |

Read actual text formatting as well as theme defaults: a deck can declare Arial in its theme while using Fira on its visible titles. Preserve useful body-font pairings, embedded fonts and the fonts needed for other scripts or mathematics. Verify availability and rendered glyphs before choosing a family; a missing registry entry alone does not establish substitution. Do not silently substitute Arial or Calibri for the intended title font, or assign Fira to text whose script it cannot render. When the intended font cannot be used, explain the limitation and resolve a suitable alternative before final delivery.

Typography and space work together: heading scale, explanatory text and the interval between them should show their roles at a glance. Check effective sizes after inheritance, group scaling and automatic text fitting. When text overflows, rearrange, enlarge its space or split the explanation with a content ledger instead of shrinking it below the minimum. Text inside a retained image needs a separate legibility review at its final placed size; a native font-size check cannot certify it. Enlarge or reconstruct that evidence only when scientific fidelity can be verified, and keep an unresolved limitation explicit.

Check visible letterforms, edges and baselines in the rendered slide. Equal text-box coordinates can look uneven because internal margins and glyph shapes differ. The [spacing and hierarchy guide](spacing-and-hierarchy.md) explains how to combine geometric alignment with optical judgment while preserving scientific associations and comparison scales.

### Recurring logos and watermarks

Recurring logos and watermarks should follow the deck's intended slide roles and branding variants. Compare equivalent pages and inspect their actual master and layout inheritance before treating an absence as an omission. A cover, section divider, full-bleed image or deliberately unbranded layout can have a different treatment; its role alone does not establish whether a mark belongs there.

Restore an isolated missing mark through the appropriate native master or layout, or by restoring the slide's intended inheritance. Reuse the correct existing asset and preserve its proportions and intended placement. Keep foreground marks inside the work area; an intentional full-canvas background watermark retains its background role and coverage. Avoid individual pasted copies, duplicate marks and blanket changes to master-graphics visibility. Keep an uncertain brand or intentional exception unresolved until its intended treatment is clear. Inspect every slide affected by a shared-layout change for visibility, contrast, overlap and unintended propagation. Follow the application-specific [PowerPoint](pptx-workflow.md) or [Keynote](keynote-workflow.md) workflow for the native repair and review.

### Text boxes and tables

Default to vertical top anchoring for non-title text boxes, except section navigation labels. Corresponding body text, explanations and captions should begin at a stable position across comparable slides, even when one box contains one line and another contains two. Centering those blocks vertically can move their first lines despite matching box coordinates. Preserve the established slide-title anchoring; subheadings and panel headings still follow the top-anchor rule. Navigation labels are vertically centered within their shapes, and the navigation bar always sits above the slide title. Table cells retain their vertical middle default. Horizontal paragraph alignment remains a separate choice.

| Content | Vertical alignment | Horizontal alignment |
| :--- | :--- | :--- |
| Body text, explanations, captions, subheadings and panel headings | Top | Keep the paragraph alignment appropriate to the explanation. |
| Section navigation labels | Middle, with consistent internal insets | Keep the established label alignment. |
| Title text-box content | Preserve the established title layout | Keep the established title paragraph alignment. |
| Descriptive table text | Middle | Left |
| Very short table entries, including numbers | Middle | Center |

For repeated top-anchored text roles, align the box's top edge and keep its top inset, paragraph space before and first-line typography consistent. Inspect automatic fitting and inherited styles as well as direct properties. Compare the visible first-line position across successive slides; a matching container boundary alone is insufficient. Text-box height may follow the content without moving that starting position. Do not move a shorter block downward to center it within a shared panel.

Apply the table choices consistently to comparable entries, including headers according to their content. Use right or decimal alignment only when explicitly instructed; a numerical data type does not supply that instruction. If table-cell centering exposes a fit problem, adjust the container, padding or composition while preserving the 10.5 pt minimum. An explicitly required layout can override the defaults, with its reason retained in the private design specification.

Substantial text needs a visible design treatment that gives the explanation a clear entry and internal hierarchy. Depending on its role, use a concise heading with an accent rule, a restrained background treatment or clearly labeled groups with deliberate spacing. Choose the treatment to reveal the argument and its relationship to nearby evidence. Keep continuous reasoning in connected prose, retain scientific qualifications, and reserve enough space for the text to remain readable. Short labels and captions can remain plain.

### Visual treatment for text-only slides

A text-only slide still needs a visual idea. Inspect each such page and give it a content-appropriate graphic treatment that helps the audience understand the explanation. A list with a decorative icon beside every line is not sufficient: the treatment should make a genuine distinction, grouping or relationship easier to see. Retain a successful existing treatment when it already does this work.

| Content relationship | Visual treatment | Condition |
| :--- | :--- | :--- |
| Alternatives described along shared dimensions | An editable comparison table or aligned comparison composition | Compare only dimensions supported by the source; do not imply that unmatched evidence is equivalent. |
| A verified sequence, process or decision path | A labeled flowchart with native shapes and connectors | Every step, connection and direction must be supported; arrows must not invent causality, chronology or decision logic. |
| Distinct concepts or categories | A labeled infographic or a restrained set of meaningful outline icons | Labels carry the meaning, icons remain consistent and no invented size or count suggests a quantity. |
| Continuous reasoning or a qualified interpretation | A composed explanation with a clear heading, aligned text groups and a restrained panel, rule or meaningful visual cue | Keep the argument in connected prose and keep each qualification attached to the statement it limits. |

Choose the simplest treatment that makes the content easier to follow, then apply it using native editable text, tables, shapes and connectors where feasible. Reuse suitable existing assets or choose a coherent icon family with consistent stroke weight and recognizable meanings. Avoid decorative imagery, invented mechanisms, pseudo-data charts and graphics that suggest evidence the source does not contain. Scientific terms, qualifications, references and source attribution remain readable and editable; a diagram is not permission to shorten away their meaning.

The text-box treatments below support this rule, while their specific fills and corner shapes remain contextual choices under R018. A panel or accent rule should reveal the structure of an explanation rather than merely enclose an unchanged wall of text. Keep all foreground content inside the symmetric work area, preserve the 10.5 pt minimum and top-anchor body text and explanations so corresponding starts remain stable across slides. Tables retain their own alignment and color-choice rules.

Record each text-only slide's chosen treatment in the private design specification and compare it with the source during visual and scientific review. A title, exact quotation or reference page may need its conventional form; required source wording and attribution must stay intact. If an essential relationship cannot be verified, retain the evidence, use a nonrelational composition where possible and identify the unresolved limit. Record a necessary exception and its reason for that slide rather than treating it as permission to leave other text-only pages undesigned. When the available tools cannot author or verify the selected treatment, keep that work explicitly pending instead of claiming a completed graphic redesign.

### Choosing a text-box treatment

A light neutral fill can make a self-contained explanation easier to distinguish from neighboring evidence. Consider a pale gray panel with gently rounded corners when the text needs that enclosure, giving it comfortable internal space and a clear heading. Treat fill, corner shape, inset spacing and type hierarchy as one composition; the enclosure should clarify a group without crowding its content or competing with the figure.

| Relationship to explain | Treatment to consider | Check |
| :--- | :--- | :--- |
| A self-contained rationale or interpretation beside evidence | Light gray fill with slight corner rounding; restrained outline if needed | The panel reads as one explanation and stays associated with its evidence. |
| Several comparable explanations | Shared fill, corner treatment and insets, with aligned headings and gutters | Corresponding non-title text starts align even when line counts differ, without forcing equal text lengths or reducing type size. |
| A qualification or takeaway needs a distinct location | A shallow neutral or accent-tinted band, or a heading with an accent rule | Emphasis matches the statement's scientific role and strength. |
| A label or caption belongs directly to a figure | No fill, or a fine separating rule where useful | The text remains visually attached to the figure. |

Use a modest radius relative to panel height, preserve visible clearance around the text and keep the complete treatment inside the work area. On dark slides, choose a neutral tone that suits the background and preserves contrast. The [reference comparisons](spacing-and-hierarchy.md#design-references-and-their-limits) inform these choices; specific brand colors and shapes remain local examples. A panel can improve grouping, while headings and intervals still carry the explanation within it.

### Table color options

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

## 04 | Give color a consistent purpose

Use teal for emphasis or a requested scientific palette for the distinctions the audience needs to follow. A restrained palette can make categories and relationships easier to track when each color has a consistent role across related slides. Support that role with labels, markers or line styles rather than relying on color alone.

For newly designed or deliberately recolored graphics, choose color-vision-friendly palettes and avoid introducing rainbow gradients. Keep concise axis and legend labels unambiguous, using stable symbols and the [unit-label convention](scientific-fidelity.md#unit-labels). Remove redundant decoration rather than data, uncertainty or essential context. These choices do not authorize recoloring or simplifying retained evidence whose scientific mappings cannot be verified.

Before changing a figure, inspect its legend and category mappings. Those mappings carry scientific meaning and take priority over the preferred palette. The values below are adjustable working defaults; they do not prescribe a journal's palette or authorize recoloring scientific figures without checking the result.

| Role | Hex |
| :--- | :--- |
| Text | `172B30` |
| Teal emphasis | `217A80` |
| Light teal | `7CBEC1` |
| Background | `FFFFFF` |
| Supporting text | `58686C` |
| Comparison blue | `3B6F9B` |
| Comparison ochre | `B77932` |
| Comparison purple | `80669D` |

Check contrast, label legibility and legend consistency in the final render. A diagram also needs enough resolution for its relationships and labels to remain readable. Prefer native editable relationships when reconstruction can be verified, and retain a complex source figure otherwise. Upscaling cannot recover missing detail. Topic-specific illustrations, such as a lightbulb for energy, are optional choices rather than brand requirements.

## 05 | Check the result against the research

A visual decision is complete only when the resulting slide still communicates the source accurately. Use the [scientific fidelity workflow](scientific-fidelity.md) to trace content changes and review scientific meaning, editability and rendered appearance separately. A successful structural check does not establish that a rearranged figure is legible or that a shortened explanation preserves its meaning. If an essential check cannot be completed, state the limit and describe the output as a candidate.

When explaining the changes, follow the [writing style](writing-style.md): connect the decision with the audience's need, its design reason and any limiting condition. Use continuous prose to develop the argument and tables when discrete information benefits from comparison. These documentation forms explain the design; they do not prescribe the layout of a slide.
