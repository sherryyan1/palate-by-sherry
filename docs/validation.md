# Validation

Validation asks three different questions: did the scientific content survive, can the intended objects still be edited, and does the rendered deck communicate the evidence clearly? Each needs its own evidence. The current validation record covers the following:

| Check | Coverage |
| :--- | :--- |
| Automated regression | 82 intake, format routing, OOXML, packaging and repository-audit tests |
| Language decisions | Five independent instruction simulations, plus a terminology-confirmation follow-up |
| End-to-end transformation | Two-slide native chart, table, text and process fixture |
| Render review | Before/after PowerPoint exports, individually inspected |
| Editability | Reversible text, table-cell and chart-series edits in PowerPoint |
| Content conservation | Values, units, categories, qualifiers, media, notes and workbooks |

The integration fixture uses synthetic data only. Its authoring package, layout, chart, font and import checks passed, and transformation preserved all six chart values together with the embedded workbook. Those conservation results were followed by render and editability review before the candidate was finalized with a mapping report.

## Run regression tests

```text
python -m unittest discover -s tests -v
python scripts/audit_repository.py
```

Regression tests exercise the boundaries that keep a routine operation from silently becoming a content change or an unsafe update:

| Area | Coverage and limit |
| --- | --- |
| Object preservation | Stale hashes, unsafe image geometry, native table placement, animation/math guards, unknown actions, overwrites and review coverage. Chart identity follows relationship targets rather than assumed package locations. |
| Installation | Installed local-edit preservation, explicit name migration, complete manifest verification, archives outside skill discovery, unrelated-path protection, backup collisions and rollback after installation failure. |
| Guided intake | Scenario branching, external audience selection, executive priorities, custom durations, delegated depth, prefilled briefs, profile overrides and out-of-scope requests. |
| Format routing | PowerPoint package structure, modern and legacy Keynote containers, directory bundles, nested indexes, credential keys, reference-only PDFs and invalid inputs; read-only behavior, source hashes and pending review states. |
| Repository audit | Narrow README language exceptions and an exact allowlist for reviewed icons; credentials, private materials, unexpected binaries and local links remain checked. Staged audits inspect the exact Git index. |

The intake helper emits payloads for the available Codex question tool, which supplies their display behavior. Pending questions remain unresolved input: they cannot count as submitted answers or permit a transformation that depends on those answers. Format tests have a comparable boundary. Their synthetic Keynote containers establish detection and routing behavior, while native Keynote compatibility still requires application testing.

The language simulations used synthetic slide excerpts to exercise source-language retention, separate conversation and presentation languages, clarification of a missing translation target, preservation of scientific content and clarification of a materially ambiguous term. A follow-up checked consistent reuse of the user's confirmed terminology. Source-to-draft review compared numerical values, units, equations and references alongside assumptions, uncertainty, qualifications and claim strength. These were instruction-following and text-review checks; they did not author or render a translated deck, test its native editability or certify the underlying science.

Integration review follows the actual authoring and delivery sequence:

1. Create a fixture with `tests/create_fixture.mjs` through the bundled presentation authoring workflow.
2. Apply `tests/run_integration.py`, then render source and candidate with `scripts/render_pptx.ps1`.
3. Inspect every slide and exercise `tests/check_powerpoint_objects.ps1` to check native editability in PowerPoint.
4. Record the actual review evidence before finalization.

## Scope of a pass

A structural pass establishes package and content conservation under the tested contract. Human or agent review supplies the visual and scientific judgments recorded for the particular output. Neither result extends automatically to arbitrary scientific content or unsupported imported objects. Static exports also leave animation playback unverified, and raster interiors remain raster unless reconstruction has been performed and verified.

Content rewriting, table resizing, chart-internal styling, grouped geometry and animation changes require the native authoring path with its content ledger. Their review must follow the objects and meanings actually changed, rather than relying on a preservation pass that enforces a different contract. Every deliverable receives the checks appropriate to its own changes.

The [Keynote workflow](../references/keynote-workflow.md) adds comparisons at export and import so conversion losses can be distinguished from design changes. Native Keynote import, save, rendering, editing and playback have not been exercised in this Windows environment. A reviewed PowerPoint interchange deck therefore leaves native Keynote review pending.
