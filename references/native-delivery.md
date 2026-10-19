# Equal native delivery standards

PowerPoint and Keynote share the same outcome: a new editable deck in the requested application, reviewed against its research and communication brief. Implementation differs; acceptance does not. A format name never determines final or candidate status. Use [native-capabilities.json](native-capabilities.json) as the machine-readable source of capability and validation status. Its tested scope does not certify the current document.

Use Artifact Tool plus native PowerPoint review for new PPTX, and [Keynote authoring](keynote-authoring.md) or controlled native Keynote editing for `.key`. Neither preservation helper creates complete decks. For API gaps, use controlled native editing with the same content ledger: grouping, layout/master design, chart-internal edits, equations, transitions and media. Never flatten a slide to bypass missing support. An unavailable operation remains pending in either format.

## Shared final review

Both preservation finalizers call `scripts/delivery_review.py`. Content-changing authoring must use this gate against the final inventory too; package validation is additional evidence, not a substitute. Bind the review to the candidate SHA-256, actual `native_application` (`PowerPoint` or `Keynote`), reviewer, nonempty `evidence`, every actual slide exactly once, and an empty `remaining_issues` list. Record application version and actual observations in the evidence.

Require `visual_status`, `scientific_status`, `editability_status`, `protected_content_status` and `playback_status` to be `passed`. A static deck still needs navigation/ending playback. These are recorded judgments, not machine certification of the science.

For complete decks, `ending_review` has `policy: required`, one-based `summary_slide`, `closing_slide`, and `appendix_start_slide` (null when absent). Require `separate_page_status`, `native_render_status`, `playback_status`, `skipped_appendix_status`, all `passed`, and nonempty `evidence`. Check roles against actual contents. Closing must be distinct, visible, after the summary and before any appendix; it must be the next visible slide after the summary. Confirm normal advancement does not enter skipped backups. Preserve deliberately visible appendices when appropriate to the brief.

For user-requested omission use `policy: explicitly_omitted`; for selected-slide work use `policy: out_of_scope`. Both require a specific user-grounded `reason`. Neither waives other native checks. Missing, failed or unperformed checks block final delivery for both formats.

## Paired verification

Use comparable synthetic scenarios in both applications: create multiple slides; add/edit text, a table and a chart; add, duplicate, move and delete slides; retain notes and skipped backup slides; export; save/reopen; edit chart data; inspect every slide; play from summary through closing. Separately cover layouts, groups, equations, mixed fonts, builds and media. Record passed, failed or not-run per case with application version and evidence. Mocked tests do not establish native execution. Preserve unrelated documents and owned scratch evidence on failures.
