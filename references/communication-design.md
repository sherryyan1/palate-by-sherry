# Communication design

Make complex ideas easier to follow without making them less rigorous.

Treat writing and presentation design as decisions about the reader's attention and understanding. Establish who the audience is, what they need to understand or do, and which information makes the next idea intelligible. Then decide the order, location and depth of the explanation. Revise wording and visual treatment after those relationships are clear. Leave material that already serves its audience alone.

Keep complexity that supports interpretation, verification or action. Resolve avoidable complexity created by unclear actors, mixed information roles, unexplained shorthand or misplaced detail. Completeness, brevity and visual restraint are useful only when they help the audience do that work.

This guide explains the judgment behind those choices. [Writing style](writing-style.md) covers prose and document forms; the [design system](design-system.md) and [spacing guide](spacing-and-hierarchy.md) cover slide composition. [Scientific fidelity](scientific-fidelity.md) remains the authority for content preservation and review. A README's entry sequence, icons or heading syntax do not prescribe the structure of a slide deck.

## Identify the reader before choosing the form

A researcher deciding whether to use **palate** and an agent applying a transformation need different kinds of precision. Establish who will use the document and what they need to do before changing its structure or voice.

| Document purpose | What the reader needs | Editorial approach |
| :--- | :--- | :--- |
| Using **palate** | A useful next action, expected result and any condition requiring their help | Explain what **palate** does and when the user contributes. Link to implementation details where they become relevant. |
| Executing a workflow | Exact inputs, sequence, constraints and evidence of completion | Keep commands, identifiers, mandatory requirements and failure conditions explicit. Add context where it prevents an execution mistake. |
| Understanding and applying design | The reason for a choice and the limits of its use | Explain the relationship being communicated, then distinguish design principles, recurring preferences and implementation constraints. |

A mixed-purpose reference can serve both readers with an explanation followed by a clearly identified procedure or contract. Separate them within the existing document when that makes the transition easier to follow; create another file only when it resolves a real navigation problem. Review every edit to a runtime reference for changes to obligations, exceptions and supported operations, even when the edit appears purely editorial.

## Begin with the audience's task

**Why and when:** Readers need to recognize how the material helps them before interpreting its internal organization. In a product guide, identify the useful action, who performs it and the condition that calls for the user's help. In a talk, establish the question the audience needs to understand or evaluate.

| Before | After |
| :--- | :--- |
| Format-table headings: "Preparation" and "Final review" | "What **palate** does" and "When you need to help" |

**Boundary:** An internal execution procedure can correctly begin with a requirement or command. Naming **palate** as the actor must never imply that an unavailable tool or unfinished check has already done the work. If an essential review cannot be completed, name the limitation and describe the output as a candidate rather than a fully verified final deck.

## Follow the reader's journey

**Why and when:** Order information by the reader's next useful question and the prerequisites for understanding the answer. A researcher considering a tool needs to know how to begin and what they will receive; they need not learn its architecture first.

| Before | After |
| :--- | :--- |
| An introduction explains adaptable design before explaining how to start. | "Start with the slides you already have." Then explain audience, purpose and time, the design work, and the deliverable. |
| The design system introduces hierarchy and composition before audience and depth. | "01 \| Establish what the audience needs" comes before evidence structure, spacing and color, so visual choices follow the purpose of the explanation. |

**Boundary:** This product-entry sequence is not a fixed template. An expert methods discussion may need the model's assumptions first; a tutorial may need a concept before its result. Choose the order that supports the audience's actual task.

## Restructure before rewriting

**Why and when:** A paragraph can be difficult because it combines different jobs, even when each sentence is accurate. Separate those jobs before shortening sentences. Use connected prose for reasoning, tables for alternatives with shared criteria, and ordered steps for real dependencies.

| Before | After |
| :--- | :--- |
| One paragraph combines scientific safeguards, editable objects, the deliverable and review. | Put safeguards under "Keep the science intact" and the deliverable under "What you get." |
| Installation mixes the user's starting request, the agent's procedure and details of installer experiments. | Explain when Codex needs the user's help, identify the procedure's audience, and link to the experimental evidence in Validation. Keep the supported route and untested platforms visible in Installation. |

**Boundary:** A paragraph with one coherent purpose needs no extra heading. Tables can fragment an argument, and numbering can imply a sequence that does not exist.

## Give detail a useful location

**Why and when:** A detail earns its place by answering the current question, enabling an action or limiting a claim. Keep immediate decisions and material limitations visible; move internal mechanics or supplementary explanation to a place where readers can find and use them.

| Before | After |
| :--- | :--- |
| The Languages section explains native authoring and object-preservation helpers. | "Your presentation stays in its original language unless you request a translation." Keep authoring requirements in the formats section and technical guide. |

**Boundary:** Relocation must not hide a condition that changes a reader's decision. On a slide, an assumption necessary to interpret a finding belongs with that finding, even if the full derivation moves to notes.

## Use familiar, precise language

**Why and when:** Abstract shorthand transfers interpretation work to readers. Name the choice or action in terms the audience uses. More words can produce a clearer explanation when they remove an unnecessary inference.

| Before | After |
| :--- | :--- |
| "when you leave the depth open" | "If you want **palate** to choose how much detail to include" |

**Boundary:** Retain established scientific terms, identifiers, equations and literal commands. Explain an unfamiliar concept where necessary rather than replacing it with a familiar word that changes its meaning. Register depends on the section and audience; a casual introduction does not set vocabulary for every technical reference.

Describe the presentation separately from its application and file format. Use software-neutral terms such as slides or slide deck for the material as a whole, and natural equivalents in localized prose. Reserve PowerPoint, Keynote and format names for actual software, compatibility, conversion or technical limits. Preserve application-specific instructions when that distinction matters; replacing every application name would conceal useful information. A terminology correction to approved prose should change only the necessary words and grammar; it does not authorize regenerating the passage.

## Keep the reasoning checkable

**Why and when:** Clarity depends on preserving the conditions under which a statement is true. When summarizing, translating or moving content, retain the relationship among the claim, evidence, uncertainty and assumptions. A shorter statement that changes that relationship is not a successful edit.

| Before, an illustrative layout problem | After |
| :--- | :--- |
| A result occupies the main slide while all its qualifications move to an appendix. | Keep the result's essential conditions and uncertainty beside the evidence; move only supplementary detail to a traceable location. |

**Boundary:** A live methods review may require a complete derivation or caption. Preserve that detail when listeners need to inspect it. Follow the existing fidelity workflow; polished prose and matching numbers do not establish scientific equivalence.

## Make visual emphasis explain relationships

**Why and when:** Use proximity, whitespace, type and restrained emphasis to show where to begin, what belongs together and what deserves attention. Judge the association the viewer actually perceives, rather than applying equal gaps or accumulating visual treatments.

| Before, an illustrative layout problem | After |
| :--- | :--- |
| A figure, its qualification and an unrelated finding have identical gaps between them. | Group the figure with its qualification and give the independent finding a more distinct interval. |

**Boundary:** Dense scientific evidence can justify compact spacing. Preserve readable labels, meaningful scales and category mappings. A well-organized existing layout may need no change; empty area and decorative consistency are not goals by themselves.

## Write each language for its readers

**Why and when:** Localized prose should use the register and explanatory order familiar to researchers in that language. Preserve capabilities, responsibilities and material limits across versions; syntax, sentence length and paragraph boundaries can differ when the text is being drafted or localized.

| Before, an illustrative localization instruction | After |
| :--- | :--- |
| "Translate every sentence and retain every paragraph boundary." | "Preserve what the reader can do, when their input is needed and what they receive; express those commitments naturally in the target language." |

**Boundary:** User-approved wording remains exact when requested. Scientific terminology requires its own fidelity review. Do not infer the slide language from the README language, and do not turn a context-specific word choice into a global vocabulary ban.

## Ask when the answer changes the decision

**Why and when:** Use the supplied material and context first. Ask when missing information would materially change the explanation, scientific interpretation, user commitment or usable deliverable. Explain the choice briefly so the user can supply the answer that matters.

| Before | After |
| :--- | :--- |
| "Technical terminology and ambiguous translations require careful review." | "If a technical term has multiple plausible translations that could change its scientific meaning, **palate** asks you to clarify rather than guess." |

**Boundary:** Multiple dictionary translations alone do not establish scientific ambiguity. Use clear disciplinary meanings without excessive questions. Leave ordinary visual choices to **palate**, and reuse supplied answers. Required target-language or material terminology answers must arrive before dependent rewriting; independent inspection can continue.

## Distinguish constraints from preferences

**Why and when:** A preference records a useful direction within a context; it does not authorize changing evidence or overriding an explicit request. Preserve the existing decision library's triggers and exceptions rather than promoting one successful example into a universal rule.

| Before, an illustrative overgeneralization | After |
| :--- | :--- |
| "Use `01 \| Title` for every heading." | "Use numbered headings when they improve navigation; `01 \| Title` is a preferred form when numbering fits the material." |

**Boundary:** Exact approved text, requested formats and scientific preservation are binding in their applicable scope. A README's `01 | Title` convention does not require that heading syntax on slides. Existing primary style rules retain their triggers and exceptions; contextual layouts remain choices to evaluate. Aesthetic consistency never justifies a misleading scientific relationship.

Before accepting an edit, compare what the reader can understand or do before and after it. Explain why the new order or emphasis helps, what information was retained or moved, and what different context would justify a different choice. If that benefit cannot be identified, preserve the existing passage.
