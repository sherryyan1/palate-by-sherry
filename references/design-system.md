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
| Comparison | Select a [comparison composition](comparison-patterns.md), aligning criteria, scales, labels and reading order. | Make unequal baselines or unmatched controls explicit; design a different arrangement when the listed patterns do not fit. |
| Method | Connect symbols, intuition and technical steps. | Retain the chain listeners need to verify. |
| Mechanism | Use labeled objects and meaningful connections. | Reconstruct only relationships that can be checked. |
| Reference | Give citations and supporting detail enough space. | Keep sources readable and traceable. |

Place a concise interpretation near the evidence it explains so listeners can connect the finding with the figure while hearing the argument. Keep essential qualifications visible with it. A full caption or derivation belongs on the main slide when the audience needs to examine it during the talk; supplementary detail can move to mapped notes or an appendix when its absence does not change the meaning.

Hierarchy also helps listeners follow a longer explanation. Use meaningful section arrows when orientation is needed, with no more than five items in a section navigation ribbon. When a study has more sections, choose at most five truthful higher-level groups and map every subsection to its appropriate group in the private design specification. Preserve every scientific section and its topic content; the grouping simplifies orientation rather than reducing the study's scope. Highlight the group containing the actual current section. Key takeaways do not need a separate ribbon item. The closing synthesis may sit within a truthful conclusion or discussion group, or omit navigation; do not consume a ribbon slot merely because a summary slide is required. Do not truncate the ribbon to the first five sections, hide additional sections behind an ellipsis or add a second concurrent ribbon to bypass the limit.

Whenever a section navigation bar is present, place it above the slide title so listeners encounter the broader context before the current topic. Keep navigation items compact and visually connected. Arrow segments should adjoin or interlock closely so the bar reads as one continuous strip, with only narrow, consistent separators. Do not widen the gaps to fill the row. Use native editable navigation labels at 12 pt or larger after text fitting and group scaling. Vertically center them within the navigation shapes, with consistent internal insets across sections and comparable slides. Keep repeated label frames, positions, insets, font family, size and weight fixed across slides; emphasize the active group through color or fill so its words do not move when the section changes. Resolve long labels through concise wording, adjusted segment widths or a coherent reflow of the bar within the five-item limit; do not shrink labels to fit or reduce their effective font size below 12 pt. A cover or self-contained page does not need navigation solely to satisfy this placement rule.

For a subject explained through conceptual parts, use title markers such as `(1/3)` to show progress. Count the parts of the explanation, which may span several slides; do not invent a denominator or renumber by slide count.

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
| Section navigation labels | At least 12 pt | Keep orientation readable; fit the wording and ribbon layout without shrinking labels below this size. |
| Footnote or minor supporting text | At least 10.5 pt | Reserve the smallest size for low-priority information. Essential qualifications remain prominent with their evidence. |
| All displayed text | Never below 10.5 pt | Include editable table text, chart labels, legends, units and citations in the review. |

Read actual text formatting as well as theme defaults: a deck can declare Arial in its theme while using Fira on its visible titles. Preserve useful body-font pairings, embedded fonts and the fonts needed for other scripts or mathematics. Verify availability and rendered glyphs before choosing a family; a missing registry entry alone does not establish substitution. Do not silently substitute Arial or Calibri for the intended title font, or assign Fira to text whose script it cannot render. When the intended font cannot be used, explain the limitation and resolve a suitable alternative before final delivery.

Typography and space work together: heading scale, explanatory text and the interval between them should show their roles at a glance. Check effective sizes after inheritance, group scaling and automatic text fitting. When text overflows, rearrange, enlarge its space or split the explanation with a content ledger instead of shrinking it below the minimum. Text inside a retained image needs a separate legibility review at its final placed size; a native font-size check cannot certify it. Enlarge or reconstruct that evidence only when scientific fidelity can be verified, and keep an unresolved limitation explicit.

Check visible letterforms, edges and baselines in the rendered slide. Equal text-box coordinates can look uneven because internal margins and glyph shapes differ. The [spacing and hierarchy guide](spacing-and-hierarchy.md) explains how to combine geometric alignment with optical judgment while preserving scientific associations and comparison scales.

### Recurring logos and watermarks

Recurring logos and watermarks should follow the deck's intended slide roles and branding variants. Compare equivalent pages and inspect their actual master and layout inheritance before treating an absence as an omission. A cover, section divider, full-bleed image or deliberately unbranded layout can have a different treatment; its role alone does not establish whether a mark belongs there.

Restore an isolated missing mark through the appropriate native master or layout, or by restoring the slide's intended inheritance. Reuse the correct existing asset and preserve its proportions and intended placement. Keep foreground marks inside the work area; an intentional full-canvas background watermark retains its background role and coverage. Avoid individual pasted copies, duplicate marks and blanket changes to master-graphics visibility. Keep an uncertain brand or intentional exception unresolved until its intended treatment is clear. Inspect every slide affected by a shared-layout change for visibility, contrast, overlap and unintended propagation. Follow the application-specific [PowerPoint](pptx-workflow.md) or [Keynote](keynote-workflow.md) workflow for the native repair and review.

### Text boxes and tables

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

For the same logical text retained across consecutive slides, follow [the retained-text continuity rule](spacing-and-hierarchy.md#keep-retained-text-fixed-across-slide-changes). Lock its exact target geometry and typography, including the height of any middle-anchored container, rather than independently refitting it on each page; the more flexible height rule above concerns corresponding roles with different content.

Apply the table choices consistently to comparable entries, including headers according to their content. Use right or decimal alignment only when explicitly instructed; a numerical data type does not supply that instruction. If table-cell centering exposes a fit problem, adjust the container, padding or composition while preserving the 10.5 pt minimum. An explicitly required layout can override the defaults, with its reason retained in the private design specification.

Substantial text needs a visible design treatment that gives the explanation a clear entry and internal hierarchy. Depending on its role, use a concise heading with an accent rule, a restrained background treatment or clearly labeled groups with deliberate spacing. Choose the treatment to reveal the argument and its relationship to nearby evidence. Keep continuous reasoning in connected prose, retain scientific qualifications, and reserve enough space for the text to remain readable. Short labels and captions can remain plain.

<a id="visual-treatment-for-text-heavy-slides"></a>

### Visual treatment for every slide

Give every slide in the requested work scope an intentional, polished composition of text and visual material, and review each page on its own and within the sequence. Use [visual storytelling](visual-storytelling.md) to make the research object, meaningful contrast, verified process, evidence or system structure visible at the depth the audience needs. This requirement applies to method, result, comparison, question, cover and closing pages as well as text-heavy explanations. Retain an effective existing treatment when it serves that purpose. A panel can group words, but grouping alone does not make the explanation visual. Generic icons, number badges and arrows between unchanged paragraphs do not resolve that problem, and there is no mandatory icon, picture quota or decorative treatment.

Plan the visual's contribution and the [substantive explanation that must remain visible](visual-storytelling.md#retain-the-substance-of-the-explanation) before filling the page with prose. A symbol can identify an object; a scientific schematic needs to expose the relevant operation, changed condition, interaction or comparison through source-specific components and explanatory labels. Distinguish research evidence from an explanatory schematic or an illustrative depiction, and verify the features and relationships each may convey. Reuse recognizable objects across related slides, with coherent palette, line weight and detail. Prefer native editable labels and relationships; retain complex source figures when accurate reconstruction cannot be verified. The detailed guide provides composition patterns, asset guidance and scientific boundaries, including the optional offline icon set.

Where useful graphics and readable text cannot share the work area comfortably, split at a coherent conceptual boundary. Preserve complete source-to-output coverage, reasoning order, essential qualifications and attribution, updating notes, navigation and cross-references. Do not shrink below 10.5 pt or split merely to accommodate decoration. Keep role-based anchoring, retained-text continuity and the established table alignment.

Review every in-scope slide for the contribution of its text and visual material, their hierarchy, spacing, balance and scientific associations, then check whether the visible sequence retains enough method, evidence and reasoning for this audience. Neat panels, spare wording and a complete script in notes do not establish either judgment. Retain necessary prose, exact proofs, quotations or conventional references when their purpose justifies their form, recording a slide-specific reason and still reviewing their typography and composition. An abstract diagram can depend on precise labels; it does not need a forced physical metaphor. Native editability, scientific meaning and the final application render remain separate checks. Unavailable authoring or native review leaves the relevant work pending.

### Research Question page

Use the [question-framing composition](visual-storytelling.md#frame-a-research-question) when a study benefits from showing its motivation, overarching question and related subquestions together. Start with a compact illustrated motivation at left, a dominant question callout at upper right and coordinated inquiry regions below. Give the main question the strongest emphasis and retain enough wording to distinguish the subquestions. Images and text follow the research; neither a three-step chain nor four cards are fixed requirements. Adapt the arrangement to the canvas, preserve source-supported relationships and keep the questions distinct from findings.

### Cover composition

Choose a [cover direction](cover-art-direction.md) from the central research subject, the intended introduction and the material that can be represented accurately. Use a dominant focal point, deliberate quiet space and a clear title hierarchy. A subject image, a field setting, a source-supported mechanism or a restrained conceptual composition can each work; no discipline or brand reference determines one mandatory style. Keep titles and metadata editable, retain the established typography and evaluate the composition both at full slide size and as a thumbnail.

### Grouped figure panels and country identifiers

For a composite figure, consider [separate rounded evidence regions](figure-panels.md), each with a concise native heading or badge and its relevant panel. Generous corner rounding and color can distinguish the groups while the original axes, legends, panel identities and scientific colors remain intact. Use A, B, C and D only as many times as the actual panels require; retain source labels or explicitly map any deck-local labels. H1 and related markers ordinarily identify hypotheses, so verify that meaning and distinguish any explicitly confirmed alternative group convention. Split across slides when the grouped view would make its evidence too small.

For comparisons across several countries, consider [flags beside country names](asset-sourcing.md#use-flags-to-aid-country-comparisons) on selected slides. Keep identifiers small, consistent and geographically accurate. They help recognition without replacing names, chart legends or quantitative encodings. Select additional icons through the same guide, using a coherent licensed family that serves the explanation.

### A visual ending

End a complete talk's main narrative with [visual key takeaways](visual-storytelling.md#close-with-visual-key-takeaways). Bring back the objects, relationships or evidence that make its supported messages memorable, with concise editable wording and deliberate space. Plain closing bullets or decorative text cards do not supply that synthesis. Preserve important qualifications and distinguish findings from proposed work; optional Q&A, contacts and appendices can follow.

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
