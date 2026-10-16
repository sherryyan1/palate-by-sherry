# Validation

Validation asks three different questions: did the scientific content survive, can the intended objects still be edited, and does the rendered deck communicate the evidence clearly? Each needs its own evidence. **palate** records those outcomes separately so a passed file check cannot conceal an unfinished visual or scientific review.

## Read the report for your deck

The transformation report explains what changed, what was checked and what still needs attention. Look for evidence that matches the actual changes and requested delivery format:

| Review | What it establishes |
| :--- | :--- |
| Scientific content | The revised explanation preserves the source's claims, data, units, equations, uncertainty, assumptions, caveats and references. Matching stored values is only part of this review. |
| Slide wording | Research abbreviations are expanded at first visible use, terminology is consistent and labels are proofread. Shortening retains scientific qualifications, attribution and accurate cross-references. |
| Native editability | The text, tables, charts and diagrams intended to remain editable can still be edited in the delivery application. A retained raster figure's interior labels remain part of the image. |
| Rendered appearance | Every final slide has been inspected in the delivery application, with changed slides compared against the source. Corresponding non-title text starts stay aligned across slides with different line counts; inspect top anchoring, insets, paragraph spacing and first-line typography. Preserve established title alignment and the table-cell middle default. Review includes intended logo and watermark inheritance, unit-label formatting and fit. Changed animation states also need playback review. |

If an essential check cannot be completed, **palate** identifies the remaining work and labels the output as a candidate. Checks follow the actual delivery application: PowerPoint for `.pptx`, Keynote for `.key`. Neither the included Windows renderer nor a PowerPoint conversion is required for a native Keynote task. The [Keynote workflow](../references/keynote-workflow.md) explains the native checks and the additional comparisons needed only when conversion is chosen.

The checks below describe the repository's tested behavior. They do not replace review of your own deck or certify its underlying science. For the task sequence and deliverables, see the [usage guide](usage.md#what-happens-after-you-attach-a-deck).

## Repository validation record

The current record covers the following:

| Check | Coverage |
| :--- | :--- |
| Automated regression | Intake, format routing, OOXML, native Keynote boundary checks, packaging and repository-audit tests |
| Language decisions | Seven independent instruction simulations, plus a terminology-confirmation follow-up |
| Installation and discovery | Allowlisted package installed in a disposable Windows project and listed as enabled by Codex |
| End-to-end transformation | Two-slide PowerPoint native chart, table, text and process fixture |
| Render review | Before/after PowerPoint exports, individually inspected |
| Editability | Reversible text, table-cell and chart-series edits in PowerPoint |
| Content conservation | Values, units, categories, qualifiers, media, notes and workbooks |
| Native Keynote implementation | Experimental Python/JXA adapter; script-level and mocked boundary checks only. No Mac application execution or end-to-end Keynote result has been tested. |
| ChatGPT Work distribution | Plugin packaging and runtime-source parity can be checked locally. Browser installation, activation, file-tool access, question cards and end-to-end editing have not been tested. |

### ChatGPT Work distribution

The plugin builder packages the same runtime allowlist as the Codex builder under `skills/palate/`, with a portable root `plugin.json`. Regression checks compare runtime bytes and hashes, resolve relative references and reject extra development files and overwrites. These are local package checks. They do not establish that a ChatGPT workspace accepts the package or exposes its scripts and resources to a running skill.

The [web setup guide](chatgpt-work.md) provides an experimental private-plugin path and an explicit verification sequence. No browser installation, `@` activation, native question-card display, workspace resource access, complete slide transformation or native application handoff has been exercised for this distribution. No public directory listing or OpenAI review approval is claimed. Record those results separately when they are actually tested; Windows Codex results do not establish web compatibility.

### Language decisions

The language simulations used synthetic slide excerpts to exercise source-language retention, separate conversation and presentation languages, clarification of a missing translation target, preservation of scientific content and clarification of a materially ambiguous term. They also checked that clear statistical terms receive no unnecessary terminology question and that an unavailable native Keynote workflow is reported as pending. A follow-up checked consistent reuse of the user's confirmed terminology.

Source-to-draft review compared numerical values, units, equations and references alongside assumptions, uncertainty, qualifications and claim strength. These were instruction-following and text-review checks; they did not author or render a translated deck, test its native editability or certify the underlying science.

### Installation and discovery

Installation checks built the allowlisted package, compared every installed file with its manifest and confirmed actual enabled discovery through the local Codex skill-listing interface. An unchanged managed update retained its recoverable snapshot; modified and unmanaged installations were refused without altering them. The test used a disposable repository-scoped `.agents/skills/palate` directory and did not replace a user's existing installation or invoke a model. It ran on Windows; macOS and Linux installation remain untested.

The standard Codex Skill Installer was also tested against the repository root. It needs the root path and destination name explicitly. In the isolated Windows test, its Git method with `--path . --name palate` produced a directory containing `SKILL.md` and Git metadata but omitted the runtime subdirectories because of its sparse checkout. Its download method copies the selected tree without applying this repository's package allowlist. These observations support the managed package route in the [installation guide](installation.md); they do not establish the behavior of every future installer version.

### Native-object transformation fixture

The two-slide integration fixture uses synthetic data only. Its authoring package, layout, chart, font and import checks passed, and transformation preserved all six chart values together with the embedded workbook. Those conservation results were followed by before/after render review and reversible text, table-cell and chart-series edits in PowerPoint before the candidate was finalized with a mapping report.

### Native Keynote validation status

The native Keynote adapter is an implemented experimental path for inspecting a private copy and making bounded placement or text-style changes to existing text boxes and shapes. It uses Python, macOS `osascript` and a fixed JXA script to control Keynote; it does not require Node or PowerPoint. Automated rewriting, slide creation and chart-internal editing are outside this helper's operation set.

The current development environment is Windows. Tests can check routing decisions, plan validation, platform refusal, subprocess boundaries, mocked application responses and JXA syntax. They cannot establish that Keynote accepts the automation calls or that a native document opens, saves, exports or retains its objects. Native Keynote installation, automation permission, import, export, rendering, editability and playback have not been tested on a Mac. Those checks must be performed in the actual Mac environment before claiming a verified native result.

A runtime probe or a matching snapshot does not complete the scientific, visual or native-editability review. Unsupported and uninspected objects need appropriate application review, and animations need playback review. An unavailable Keynote runtime leaves native work pending; tests must not treat it as permission to switch automatically to PowerPoint or a cloud service.

## Reproduce the repository checks

Run the automated suite and content audit from the repository root:

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
| Format routing | PowerPoint package structure, modern and legacy Keynote containers, directory bundles, nested indexes, credential keys, reference-only PDFs and invalid inputs; source-format defaults, separate native routes, read-only behavior, source hashes and pending review states. |
| Native Keynote adapter | Platform and automation boundaries, source/output safeguards and bounded operation validation with mocked responses. These checks do not establish native Mac compatibility or the scientific correctness of a transformation. |
| Repository audit | Narrow README language exceptions and an exact allowlist for reviewed icons; credentials, private materials, unexpected binaries and local links remain checked. Staged audits inspect the exact Git index. |

The intake helper emits payloads for the available host question tool, which supplies their display behavior. Pending questions remain unresolved input: they cannot count as submitted answers or permit a transformation that depends on those answers. Format tests have a comparable boundary. Their synthetic Keynote containers establish detection and routing behavior, while native Keynote compatibility still requires application testing.

The existing PowerPoint integration review follows its authoring and delivery sequence. The Windows renderer below belongs to this fixture, not to every supported workflow:

1. Create a fixture with `tests/create_fixture.mjs` through the bundled presentation authoring workflow.
2. Apply `tests/run_integration.py`, then render source and candidate with `scripts/render_pptx.ps1`.
3. Inspect every slide and exercise `tests/check_powerpoint_objects.ps1` to check native editability in PowerPoint.
4. Record the actual review evidence before finalization.

The native Keynote integration test is opt-in. On a Mac with Keynote and automation access, prepare a private `.key` fixture and a plan based on its current native inspection and actual target-safety review. Set `PALATE_KEYNOTE_FIXTURE` to the source path and `PALATE_KEYNOTE_PLAN` to the plan path, then run:

```text
python -m unittest discover -s tests -p test_keynote_native.py -v
```

The integration case inspects, edits, saves, exports PDF and reopens a separate native candidate while checking the original hash. It leaves visual, scientific, editability and playback review pending. Without the Mac prerequisites and both environment variables, the case is skipped, not passed. This integration case has not been run in the Windows development environment.

## Scope of a pass

A structural pass establishes package and content conservation under the tested contract. Human or agent review supplies the visual and scientific judgments recorded for the particular output. Neither result extends automatically to arbitrary scientific content or unsupported imported objects. Static exports also leave animation playback unverified, and raster interiors remain raster unless reconstruction has been performed and verified.

Content rewriting, table resizing, chart-internal styling, grouped geometry and animation changes require the native authoring path with its content ledger. Their review must follow the objects and meanings actually changed, rather than relying on a preservation pass that enforces a different contract. Every deliverable receives the checks appropriate to its own changes.

The [Keynote workflow](../references/keynote-workflow.md) keeps native `.key` work in Keynote. If a different format is explicitly requested or conversion is chosen, it adds comparisons at export and import so conversion losses can be distinguished from design changes. A reviewed `.pptx` does not establish a reviewed `.key`; native Keynote work and its required checks remain pending until actually performed on a Mac.
