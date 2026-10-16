# Writing style

Writing is part of the presentation's design: the order of the explanation should help the reader understand the research and the choices made around it. The [communication design guide](communication-design.md) explains how to decide what matters, where it belongs and how much context the audience needs. This reference covers how to express those decisions.

## Develop the explanation

Build each paragraph around a question or judgment. Explain what the audience needs to understand, how that need affects the design, and any condition that limits the choice. Let each sentence develop the previous one through a reason, consequence, example or qualification. Adding transition words to unrelated statements does not establish that relationship.

Use concrete decisions to express the style. For example, explain why an assumption belongs beside a result or why a comparison needs shared scales. Words such as clear, considered and intentional should describe an identifiable choice. Keep the voice professional and direct; do not invent first-person statements or beliefs on Sherry's behalf.

Choose familiar words and state the action or decision directly. Write for an international research audience: explain when to provide information and how much technical detail to include, rather than relying on idioms or abstract shorthand. Preserve precise scientific terms and explain unfamiliar terms where readers first need them.

## Write READMEs for researchers

Explain what **palate** does, when the user needs to contribute and what they receive. Keep essential conditions visible, and link to technical procedures rather than making readers learn the architecture before they can begin. The [communication design guide](communication-design.md) develops this reader journey and the judgment behind targeted edits; preserve passages that already serve their readers.

## Match the form to the information

| Information | Suitable form | Purpose |
| :--- | :--- | :--- |
| An argument or explanation | Connected paragraphs | Develop the reasoning and its qualifications. |
| Options, requirements or comparable cases | A table with shared criteria | Make differences easy to find and compare. |
| Actions whose order matters | Numbered steps | Preserve dependencies and a usable sequence. |
| Commands, field names or schemas | Literal code blocks and precise reference text | Keep the operational contract exact. |

A table needs a meaningful basis for comparison. Avoid splitting a continuous explanation across cells merely to shorten it. Likewise, a brief should not become a paragraph of disconnected options when a reader needs to compare them.

## Preserve the substance

For documentation and transformation reports, explain the method and its consequences before introducing implementation detail. Keep tool-specific instructions where a reader needs them to act. Preserve binding conditions, exceptions, scientific qualifications and capability limits when editing for flow.

On slides, match the amount of prose to the audience and time available. A concise interpretation can still make its reasoning explicit; this writing preference does not require paragraph-length text on every slide. Technical labels, equations and structured data keep the form that makes them easiest to understand and verify.

## Research slide wording

Begin a paragraph with its actual topic or message, then develop the evidence, explanation and qualifications the audience needs to follow it. Give each sentence a purpose within that explanation. Remove repetition and details that do not support interpretation or discussion, while retaining assumptions, uncertainty and other conditions that affect the finding. Shortening a sentence is useful when it makes the relationship easier to understand; fixed word limits and disconnected fragments are not substitutes for that judgment.

Describe what the evidence supports rather than announcing the presence of a figure. A source-backed finding or relationship usually gives the audience a more useful starting point than "Figure 2 shows...". Keep the source figure number and citation where they support identification and verification. Do not force a takeaway when the source supports only a question, method or observation, and never turn an association into a causal claim to make a heading sound decisive.

Define a research abbreviation at its first audience-visible occurrence, normally as the full term followed by the abbreviation in parentheses. Check the actual presentation order, including titles, tables, figures and build stages: a definition in later body text, speaker notes or a glossary does not explain an earlier visible abbreviation. Place the full term in the first title or an immediately associated visible explanation when that is where the abbreviation first appears. Use the abbreviation consistently within its scientific context; repeat its definition when a section or slide must stand alone or the audience needs a reminder. When distinct verified concepts share initials, make their full terms or local meaning explicit rather than merging the concepts or silently renaming protected identifiers. Avoid introducing an abbreviation that saves little repetition, and reduce unnecessary jargon according to the audience's familiarity.

Use definitions established by the source and its research context. If the full term cannot be established from the source and research context, or a material ambiguity remains, ask the user to clarify and wait for the answer before applying that expansion. Do not invent a scientific term from its initials. Symbols, chemical formulas, SI unit symbols, identifiers, codes and proper names need their appropriate explanation when unfamiliar, but are not automatically abbreviations to expand. Parentheses used to define an abbreviation remain valid; units attached to quantity labels use square brackets under the [unit-label rules](scientific-fidelity.md#unit-labels).

Review wording across the deck rather than checking body paragraphs alone:

| Check | Apply on slides |
| :--- | :--- |
| Spelling, grammar and research terms | Correct ordinary language errors, retain established scientific terms and use consistent spelling. Ask before resolving an ambiguity that could alter the research meaning. |
| Terminology and notation | Use one term for the same concept across titles, text, tables, axes, legends and notes. Preserve distinctions between different concepts; do not rotate technical synonyms for stylistic variety. |
| Quantity labels | Keep labels concise and specific, with the correct unit, symbol, case and exponent. Apply square brackets to unit-bearing labels without changing values or converting units. |
| Citations and cross-references | Keep each citation near the claim it supports. Prefer sentence-end placement when the association remains clear; keep a citation beside a particular clause when moving it would obscure that association. Preserve source figure, table and equation numbers when referring to those source objects. |
| Tone and emphasis | Report and explain the evidence with concrete nouns and precise verbs. Remove filler and unsupported praise without weakening scientific qualifications or suggesting greater certainty. |

These are slide-writing decisions. Manuscript requirements such as line numbering, fixed line spacing, submission filenames, mandatory acknowledgements or publishing data and code do not become presentation requirements. Likewise, do not number every new slide figure merely because a manuscript numbers its figures. Retain the source's references, attribution and required acknowledgements, and use figure numbers when the audience needs them to locate or discuss evidence. Rewriting follows the [content-changing workflow](scientific-fidelity.md#content-changingrebuilding-path), including a source-to-output meaning check; better prose alone does not establish scientific fidelity.

## Localized entry points

The four README versions share one set of capabilities, requirements and scientific safeguards. Write each for researchers who use that language: choose familiar terminology, develop the explanation in a natural order and adapt examples where useful. Sentence-by-sentence matching is unnecessary, but a change of language must not introduce a different promise or omit a material limit.

Keep the execution standard and detailed references in English so all entry points lead to the same design rules. Make clear that reading a localized README does not choose the language of the conversation or the presentation. Treat approved native-language wording as the source of truth and make only necessary corrections.

Choose subjects and pronouns for the language being written. Chinese, Japanese and Korean often omit reader references where English uses direct second-person sentences. Omit a subject when the context supplies it naturally, using direct verbs and the language's usual topic structure and level of politeness. Replacing every Chinese reader reference with a more formal address, adding Japanese honorifics or introducing Korean audience labels can make the prose less natural.

Keep responsibility explicit. Name **palate** or Codex when an omitted subject could leave the actor unclear, and state required files or actions directly. Retain a reader reference when it clarifies who must confirm a term or complete an application check. Judge the sentence and paragraph as a whole rather than applying a global replacement rule; literal request examples retain the speaker's intended perspective.

Describe the presentation separately from its application or file format. Choose terminology for what the sentence actually describes:

| Subject | Wording |
| :--- | :--- |
| Presentation materials | Use slides or slide deck in English, with familiar software-neutral equivalents in localized prose. Distinguish the whole deck from an individual slide where the language does so. |
| Application, compatibility or file handling | Retain PowerPoint, Keynote and exact format names when that distinction matters to the task. |

These are contextual choices, not a global replacement list. Keep the prose natural without weakening the technical distinction.

Avoid em dashes and en dashes as prose separators, while preserving literal filenames, commands and scientific notation. Write the product name as **palate** in prose; leave code, paths and invocation syntax exact.
