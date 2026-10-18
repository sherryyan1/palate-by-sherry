# Repository guidance

Use SKILL.md as the single English runtime entrypoint. Keep references, detailed documentation, code comments, examples and metadata in English; respond to users in their requested conversation language. The root README.zh-CN.md, README.ja.md and README.ko.md are localized human-facing entry points. README.md remains English apart from the shared language navigation and approved language-name list. Keep the four READMEs aligned on capabilities and requirements while adapting their prose naturally; do not create translated execution rules.

Treat the four README files, including their links and navigation, as approved copy. Before changing them, show the exact proposed Markdown and any applicable localized versions, explain the need, and obtain explicit approval. Keep detailed design capabilities in the existing documentation entry route rather than expanding the READMEs.

Identify whether a document serves researchers, agents or both before choosing its structure and voice. Write connected explanations that make the design judgment and its reasoning explicit. Use tables for discrete options, requirements and comparisons, and ordered steps when sequence matters. Preserve sufficient context, exact technical contracts and scientific qualifications; brevity alone is not the goal. Follow references/communication-design.md for the reasoning behind communication choices and references/writing-style.md for prose and document forms. Keep README conventions distinct from slide-design decisions, and retain explicit requirements in operational specifications.

Preserve scientific meaning, numerical results, units, labels, legends, uncertainty, equations, caveats and references. Work on new output files. Validate content, editability and rendered appearance separately. Use native objects where feasible; retain complex figures when reconstruction cannot be verified.

Primary rules define the design direction. Contextual rules are layout choices to evaluate against the content and brief; do not turn them into universal personal preferences. Single-page monthly updates are outside this multi-slide workflow.

Keep original research, derived evidence, task plans, credentials and private notes untracked. Package only the explicit runtime allowlist. Before committing, run relevant tests and the repository-content audit. Push only the intended branch when authorized and verify the remote SHA. Do not force-push or change repository visibility without explicit authorization.

Update the package allowlist and documentation when runtime references change. Preserve local edits to installed skills; managed updates retain a recoverable snapshot. Git, packages and installed skills are synchronized explicitly.

For installation, follow docs/installation.md in the environment where Codex runs. Ask before replacing an existing skill, preserve local edits and verify actual discovery as well as runtime files and dependencies.
