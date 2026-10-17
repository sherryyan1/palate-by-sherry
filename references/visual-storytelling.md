# Visual storytelling

A useful graphic helps the audience see something they would otherwise have to assemble from sentences: the objects involved, what changes between conditions, how a system is organized or where a method takes its inputs. A row of labeled boxes can organize that explanation without making it visual. **palate** therefore judges a graphic by the understanding it contributes, rather than by the presence of shapes, arrows or icons.

Use this guide when creating slides or reviewing explanations dominated by words, including pages that already contain a diagram or chart. The [design system](design-system.md) supplies typography, spacing and alignment requirements; [scientific fidelity](scientific-fidelity.md) governs what the visual may claim.

## Choose what the visual needs to explain

Read the source before choosing an asset. Identify the research object, the distinction or action being explained, and the evidence supporting any relationship. Record that purpose briefly in the private slide specification alongside the source-to-output ledger. For example, a comparison of operating conditions may need the same physical system shown twice, with only the relevant condition changing. A generic symbol for the research field would contribute much less.

Keep three visual roles distinct:

| Role | Contribution | Scientific boundary |
| :--- | :--- | :--- |
| Research evidence | Shows an observation, measurement, model output or source result. | Preserve data, scales, uncertainty, labels and attribution. A replacement requires verified evidence. |
| Explanatory schematic | Makes source-supported components, relationships or stages visible. | Check each connection and distinguish sequence, information flow and causality. Shape size and distance must not imply unverified quantities. |
| Illustrative depiction | Makes a source-described object, setting or intervention recognizable. | Identify a representative or conceptual depiction when it could be mistaken for an observation. It cannot establish a mechanism or result. |

An illustration may support a measured chart, but it does not replace that evidence. Likewise, adding a chart does not resolve a neighboring explanation that still asks listeners to decode a long verbal chain.

## Build around objects and relationships

Choose the composition before filling the page with prose. Use recognizable research objects where they clarify the subject, then arrange them to express the verified comparison, transformation or system structure. Keep concise labels and necessary qualifications nearby. A small number of informative objects is often more effective than a symbol attached to every sentence.

| Explanatory task | Composition to consider | What makes it useful |
| :--- | :--- | :--- |
| Explain an intervention | Show the relevant object, the intervention and its supported consequence. | The audience can identify what changes and what remains the same. Do not add an unverified causal link. |
| Compare conditions or mechanisms | Repeat a shared baseline with aligned views, changing only the relevant features. | The difference is visible without rereading two paragraphs; unequal baselines remain explicit. |
| Explain time or operating context | Pair source-supported states with a timeline, clock or environmental cue. | The cue locates the explanation without introducing invented temporal profiles. |
| Introduce a complex method | Give an overview of inputs, modules and outputs, then develop the necessary detail on subsequent slides. | Objects and module identities remain recognizable as the explanation unfolds. |
| Motivate an analytical method | Show the available observations and the question or limitation the method addresses. | The method responds to the actual evidence gap, rather than an invented idealized dataset. |
| Summarize a research argument | Reuse the objects and relationships established earlier. | The audience can recall the reasoning through a stable visual vocabulary. |

Retain a flowchart, comparison table or equation when that is the clearest representation. Abstract methods do not always have useful physical counterparts, and exact wording can matter more than an illustration. Do not force a concrete metaphor onto a mathematical relationship or add icons merely to meet a quota.

Across related slides, reuse the same symbol for the same object. Keep viewpoint, level of detail, stroke weight and color roles coherent. Change a visual feature when its meaning changes, and use labels or other cues so color is not the only distinction. A microscope, network or field setting should serve the particular explanation; no topic symbol belongs on every slide in its field.

## Select and construct assets deliberately

Native shapes, connectors, text and tables make the explanation easier to revise. Keep labels outside imported illustrations where feasible, and construct a diagram from separable components rather than embedding the whole explanation as an image. Preserve complex source figures when their reconstruction cannot be verified, reporting the limits on editing their interiors.

The optional [slide icon set](../assets/slide-icons/NOTICE.md) provides a small, coherent starting vocabulary. It is independent of the README icon system and does not prescribe a family for every presentation. Choose another consistent, appropriately licensed asset family or draw native objects when these icons cannot convey the relevant features. Before importing an SVG into a presentation application, make a private use-copy with an explicit stroke color instead of relying on `currentColor`; verify the actual import and render. Keep the distributed originals and license intact.

A suitable illustration tool can supply a more specific depiction when simple symbols are insufficient. Inspect its geometry and scientific details, use adequate resolution at the final placed size, and avoid embedded generated lettering. Do not imitate low-resolution composites, mix unrelated icon styles or reproduce a reference's incidental colors merely because its explanatory composition is useful. Follow the user's authorized environment and [host workflow](host-workflows.md) before sending research to any additional service.

Do not turn descriptive statistics into a plausible-looking density curve, draw a geographic distribution without geographic evidence, or invent trajectories to make a conceptual page look quantitative. If the source supplies only components and an unresolved relationship, show the components without a directional link and retain the uncertainty in words. Unsupported content is not repaired by labeling an otherwise misleading figure "conceptual."

## Give the explanation enough space

If useful objects, their relationships and readable text cannot share the work area comfortably, split at a conceptual boundary. An overview followed by a mechanism or module detail can preserve both orientation and depth. Give each resulting slide a clear explanatory purpose and map every claim, qualification, reference and note to its destination. Update navigation and cross-references after splitting.

Do not shrink below the 10.5 pt minimum, crowd a diagram to preserve an arbitrary slide count or split solely to make room for decoration. Keep corresponding non-title text top-anchored, navigation labels vertically centered and table alignment consistent with the [design system](design-system.md#text-boxes-and-tables).

## Review the contribution, then the rendering

Review what the audience can now understand more readily. Can they recognize the relevant objects, compare the changed condition or follow a verified relationship? Momentarily looking past the words can expose a diagram that is still only a set of text containers. This is a diagnostic, not a requirement that a scientific figure explain itself without labels. A well-designed abstract flowchart may depend on precise terms; its arrangement must still make the structure easier to follow.

For a text-dominant explanation, accept the treatment only when it contributes a clear visual distinction, object depiction, relationship or useful comparison, or when a slide-specific reason justifies retaining prose. A generic topic icon, number badge, pale panel or arrow between unchanged paragraphs does not by itself meet that standard. Record the contribution or justified exception privately, alongside source support and any split destinations.

Finally, inspect every resulting slide in the delivery application. Check scientific meaning, native editability and appearance separately, including connector endpoints, object identity, visible labels, image quality, contrast, spacing and work-area bounds. An automated asset or file check cannot establish that a graphic explains the research well, and unavailable native review remains pending.
