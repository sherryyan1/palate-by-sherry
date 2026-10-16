# Native Keynote workflow

PowerPoint and Keynote need the same design judgment: the audience must be able to follow the argument and read the evidence without losing its qualifications. **palate** shares intake, design decisions and scientific fidelity across both applications, then uses the chosen application's native workflow. A Keynote source remains `.key` by default. Windows PowerPoint and a `.pptx` export are not prerequisites.

This reference guides the agent through native Keynote inspection, bounded changes and delivery on Mac. The bundled adapter is implemented but experimental: its JXA application calls have not been executed on Mac in this development environment. Routing, Python guard tests and simulated application responses do not establish native compatibility. Complete the actual application's preflight and reviews before making any claim about a particular deck.

Begin with [routing and access](#route-the-source-and-check-access), then [inspect the native source](#inspect-before-designing). Use the [adapter contract](#native-adapter-contract) only for changes it supports. Requested conversion follows a separate [optional path](#optional-cross-format-delivery).

## Route the source and check access

Run the read-only container router before launching an application:

```text
python scripts/presentation_route.py "input.key"
python scripts/presentation_route.py "input.pptx"
```

The default preserves the recognized source application. Pass `--target pptx` or `--target keynote` only when that different delivery format was requested. The router does not edit, convert, launch an application or upload a file.

| Source and requested delivery | Route | Next action |
| :--- | :--- | :--- |
| Compatible PPTX, PowerPoint delivery | `ready-pptx` | Enter the [PowerPoint workflow](pptx-workflow.md). All review remains pending. |
| Recognized Keynote, native delivery, Mac prerequisites detected | `requires-keynote-preflight` | Probe and inspect an isolated copy in Keynote before planning native changes. Static detection does not establish automation access. |
| Recognized Keynote, native delivery, required runtime unavailable | `requires-keynote-runtime` | Keep `.key` delivery pending. Arrange access to Keynote on Mac or ask whether the user wants an alternative format. |
| Different delivery application explicitly requested | `requires-format-conversion` | Establish a conversion baseline in the applications concerned before design or delivery. |
| PDF | `reference-only` | Inspect appearance; obtain a supported editable source before changing native objects. |
| Credential `.key`, unknown, malformed or unsupported container | `unsupported` | Exclude credentials and select the actual presentation. Do not simulate conversion by changing an extension. |

The router's exit code reports whether it emitted a recognized route, not whether a deliverable exists. `can_deliver_target_now` remains false and review fields remain pending. A native Keynote route does not set `can_transform_now` true on the strength of an application path; live preflight and inventory are still required.

Container recognition is intentionally conservative. Modern `.key` ZIP and directory bundles need document and slide/master-slide IWA signatures, with a bounded nested `Index.zip` variant. Legacy APXL markers need application inspection. The bundled native adapter accepts recognized modern `.key` only; for a legacy source, open a duplicate in available Keynote, review it and save a new modern native copy before re-routing and inspecting. Recognition does not decode IWA, validate native objects or prove that Keynote can open the file. The helper excludes credential signatures without printing their contents, rejects unsafe ZIP members and linked sources, and hashes recognized presentation files or directory manifests. Preserve a directory bundle intact.

For native work, run:

```text
python scripts/keynote_native.py probe
```

The adapter requires macOS, Keynote, `/usr/bin/osascript` and permission for the execution process to automate Keynote. Follow the actual permission prompt rather than changing unrelated system settings. A missing application, denied permission or failed preflight leaves native work pending; do not fall back to PowerPoint or iCloud without the user's choice. A PDF supplied by the owner can support design discussion while application access is arranged, but cannot establish a finished editable `.key`.

## Inspect before designing

1. Preserve the original and retain its source hash. The adapter opens a private copy because Keynote can save changes during application work. Keep source, scratch, inventory, PDF, plan, candidate and delivery paths separate; do not open the original for automated repairs. Record the actual macOS and Keynote versions and any application warnings.
2. Inspect through Keynote and export a source PDF using fresh paths:

   ```text
   python scripts/keynote_native.py inspect input.key --output build/keynote-inspection.json --pdf build/keynote-source.pdf
   ```

   The resulting inventory contains only what the application interface exposes. Read the source PDF and inspect the actual presentation, including skipped slides, notes, charts, equations, native tables, media and builds. Neither an object count nor a successful export establishes complete scientific or editability review.
3. Resolve the brief through [guided intake](guided-intake.md) and choose design changes from the scientific relationship and reading order. Preserve the source language unless translation is requested. Complete the [scientific translation preflight](scientific-fidelity.md#scientific-translation) before rewriting; the native bounded adapter cannot translate text.
4. Review the safety of each proposed target in Keynote before applying a plan. Check builds, grouping, equations, mixed emphasis and meaningful color encoding that the inventory may not expose. Use the native application for unsupported changes rather than widening the adapter's contract.

Use the shared [text-box and table guidance](design-system.md#text-boxes-and-tables): place any section navigation bar above the slide title and vertically center its labels within the navigation shapes, keeping internal insets consistent. Top-anchor other non-title text boxes and compare the first-line position across corresponding slides with different line counts. Match top edges, top insets, paragraph space before and first-line typography, and inspect automatic fitting. Preserve established title-layout anchoring. Table cells retain vertical middle anchoring; left-align descriptive table text and horizontally center short entries such as numbers. Right alignment requires an explicit instruction. Give substantial text a deliberate visual treatment and readable hierarchy. The bounded adapter cannot change anchoring, paragraph alignment, table-cell alignment or padding; use controlled native Keynote authoring for those changes and inspect both the actual properties and rendered fit. An unavailable native workflow leaves these changes pending.

For a deck with tables, offer the [Nature-inspired and deck-matched color comparison](design-system.md#table-color-options) using identical representative content, then reuse the resolved choice. Table fills, borders, corner treatments and numeric-display changes need suitable controlled native authoring; they are outside the bounded adapter. Apply the shared [numeric display](scientific-fidelity.md#numeric-display) rules, preserving raw values and formulas and separately reviewing their display. Native Keynote work remains pending when Mac application access is unavailable.

A native PDF export supplies visual evidence. Inspect its actual coverage: include skipped slides and notes where needed and obtain build-stage exports or playback evidence separately. Apple documents PDF settings for presenter notes, skipped slides and individual build stages; one PDF page does not always correspond to one source slide. ([Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac))

### Match the venue screen

Use the shared intake answer `screen_aspect_ratio`: `4:3` or `16:9` sets the target canvas, while `not_sure` keeps the source dimensions. Record the source size, confirmed answer and target size privately. A matching ratio needs no change of physical size. Never infer the venue's screen from the source document.

When a different ratio is chosen, use controlled native Keynote authoring on a private copy to change the document's slide size and recompose the slides. Redefine the symmetric work area and appropriate slide-layout guides, then reflow text and reposition or proportionally resize figures, tables, diagrams and recurring elements. Preserve scientific content, labels, essential qualifiers and the 10.5 pt floor. Do not distort or crop evidence, flatten a slide or convert through PowerPoint to perform this change.

The bounded Keynote adapter cannot change the document canvas, add objects or split slides. Use appropriate native authoring for the resize and for [visual treatments of text-heavy explanations](design-system.md#visual-treatment-for-text-heavy-slides), including conceptual illustrations, schematics, icons and tables. Review pages with existing figures as well as text-only pages, and split a complex explanation when the content and useful graphics cannot fit legibly with comfortable spacing. Resolve the two table-color alternatives for any newly created table unless supplied or delegated already. Keep the original-to-output content ledger, inspect native editability and review every affected rendered slide, including layout inheritance and builds where relevant. If the required native editing is unavailable, keep those changes pending.

This native resize and reflow path has not been tested on Mac in this development environment. Python tests, a route decision or successful package generation do not verify it; record the application actions and checks actually performed.

### Restore consistent branding through slide layouts

Use the same branding judgment as the [PowerPoint workflow](pptx-workflow.md#restore-consistent-branding-through-masters-and-layouts), implemented through Keynote's native slide layouts. Inspect which layout each slide uses and how logos or watermarks are inherited or locally overridden, then compare slides with matching roles and brand variants. An isolated omission may need repair; covers, section dividers, blank or full-bleed slides and co-branded pages can have intentional exceptions. A PDF or a count of exposed slide objects cannot establish that inheritance.

On a private copy, use suitable native Keynote authoring to repair the relevant shared layout, assign the correct existing layout or restore the affected inheritance where the actual application supports it. Reuse the authorized source asset with its intended placement, proportions and contrast. Keep foreground marks inside the symmetric work area; intentional full-canvas background watermarks retain their background role and coverage. Do not add per-slide duplicates, indiscriminately reveal all layout objects or replace unrelated brand variants. If no source asset or clear intended pattern exists, do not invent one. Layout editing, reassignment and display overrides are outside the bundled adapter; an unavailable native capability leaves the repair pending rather than authorizing conversion to PowerPoint.

Inspect every slide affected by a layout change for duplicate marks, clipping, obscured content or logos, and unintended background changes. Verify the native layout relationship and editability separately while preserving protected research objects. This route has not been tested on Mac in this development environment; record only the application actions and checks actually performed.

## Native adapter contract

[keynote_native.py](../scripts/keynote_native.py) validates plans and coordinates the fixed [JXA adapter](../scripts/keynote_native.js). It works through Keynote rather than editing IWA or converting to PPTX. This is a separate bounded contract from the [PPTX plan](transform-plan.md): selectors are native inventory positions and geometry uses points, not inches.

| Contract element | Requirement |
| :--- | :--- |
| Source identity | Bind the current source hash and the inspected inventory hash. A changed source needs fresh inspection and a new plan. |
| Selector | One-based `slide`, `object_kind` (`text_item` or `shape`) and one-based `object_index` within that inspected kind/order. These are not persistent object IDs across document revisions. |
| `geometry` | `bounds_points: [x, y, width, height]`. Text-item frames may move/resize; shapes may move without resizing custom diagrams. Keep the target inside the slide. |
| `text_style` | Uniform `font_size_pt` as a finite number from 1 to 512 points, including fractional sizes such as `10.5`; `font_family` or six-digit hex `color` without `#`, on supported native text only. Preserve meaningful emphasis, mathematics and scientific color encoding. |
| Design basis | Every operation needs `reason` and `rule_ids`; use an empty list for engineering or task-specific choices. |
| Source review | A hash-bound record of all source slides, actual target-safety review, reviewer and evidence is required before applying changes. It records performed judgments; it does not automate them. |
| Excluded operations | Document canvas changes, creating icons/tables/diagrams, text rewriting/translation, unit-label changes, anchoring or paragraph alignment, table-cell alignment or padding, grouped or locked targets, styling mixed or math-bearing text, image reconstruction, chart-internal edits, table resizing, build changes, adding logos or watermarks, and slide-layout edits or reassignment need appropriate native authoring and separate review. The adapter has no master/layout relationship or display-override operation. |
| Output policy | Use new paths. Existing outputs are refused. Source and unrelated open documents are not replacement targets; keep any retained scratch copy private for recovery. |

Build the plan from the actual inspection, not from example indices. Use the returned `inspection_sha256`, which is a digest of the canonical native inventory rather than the JSON file's bytes. The top-level fields are `schema_version`, `source_sha256`, `inspection_sha256`, `source_review` and `operations`; this native contract has no PPTX `context` field. Replace the illustrative hashes, selectors, bounds and slide coverage below with the actual source and performed review:

```json
{
  "schema_version": 1,
  "source_sha256": "FULL_CURRENT_SOURCE_SHA256",
  "inspection_sha256": "FULL_NATIVE_INVENTORY_SHA256",
  "source_review": {
    "source_sha256": "FULL_CURRENT_SOURCE_SHA256",
    "reviewed_slides": [1, 2],
    "target_safety_status": "passed",
    "reviewer": "Actual reviewer",
    "evidence": ["Actual source review and target-safety evidence"]
  },
  "operations": [
    {
      "slide": 1,
      "object_kind": "text_item",
      "object_index": 1,
      "action": "geometry",
      "bounds_points": [36, 32, 640, 64],
      "rule_ids": [],
      "reason": "Separate the existing title from its supporting evidence."
    }
  ]
}
```

Do not reuse a plan after native editing has changed the source or its inventory. A `passed` source review must describe actual Keynote inspection, not a status copied from this example.

Apply and independently check a fresh candidate:

```text
python scripts/keynote_native.py apply input.key --plan build/keynote-plan.json --output build/candidate.key --receipt build/keynote-apply.json --pdf build/keynote-candidate.pdf
python scripts/keynote_native.py validate input.key build/candidate.key --plan build/keynote-plan.json --receipt build/keynote-recheck.json
```

The candidate is saved natively as `.key`. Exposed text, notes, slide/object inventories and planned changes are compared, but a native save may re-encode the package. There is no byte-identical preservation guarantee and no claim that all chart data, formulas, equation semantics, fonts, build settings or media behavior are exposed by the scripting interface. Resolve these obligations through actual Keynote inspection. A successful command leaves the scientific, visual, editability and playback judgments to the reviewer.

For translation, slide decomposition or reconstruction, use available controlled native Keynote authoring and the [content ledger](scientific-fidelity.md#content-changingrebuilding-path). Verify that the actual tool can preserve the required objects before using it. If no suitable authoring path is available, explain the limitation and leave that change pending rather than flattening the deck or silently taking a PowerPoint detour.

## Review and deliver in Keynote

The shared quality gates remain independent of application and implementation:

| Review | Evidence required in Keynote |
| :--- | :--- |
| Content | Compare every slide with the original and any content ledger. Preserve numbers, units, labels, legends, categories, uncertainty, equations, conclusions, assumptions, caveats and references, including notes and skipped slides. Inspect chart data and native formulas where relevant. |
| Appearance | Export and inspect every final slide, comparing changed slides with the source. Check fonts, wraps, clipping, proportions, connectors, figure labels, spacing and scientific reading order. Re-export after repairs. |
| Editability and protected objects | Select native text, tables, charts, diagrams and equations in Keynote and test a separate editable copy where needed. Review dependencies and retained image regions explicitly. An unchanged image or PDF cannot prove native editability or chart data preservation. |
| Playback | Inspect transitions, builds, audio and video where present, including ordering, timing and staged evidence. If none are present, record that actual check. Static PDFs and inventory comparisons cannot prove playback. |

After the actual review, create a private record with `source_sha256`, `candidate_sha256`, `reviewed_slides`, `native_application: "Keynote"`, `reviewer`, nonempty `evidence` and an empty `remaining_issues` list. Coverage must include every source slide. The native finalizer requires `visual_status`, `scientific_status`, `editability_status`, `playback_status` and `protected_content_status` each to equal `"passed"`. Never manufacture these statuses from an adapter receipt or a successful PDF export.

```text
python scripts/keynote_native.py finalize input.key build/candidate.key --plan build/keynote-plan.json --review build/keynote-review.json --output outputs/refined.key --report outputs/transformation-report.md
```

Finalization rechecks the observable inventory and bound records, then produces a separate native delivery copy and report. A recorded pass remains a reviewer's assertion; the finalizer does not independently certify scientific equivalence or inaccessible native internals. If any required review is unavailable, retain a clearly labeled candidate and describe the remaining work instead of reporting completion.

## Optional cross-format delivery

Conversion is useful when the user needs a different application or explicitly chooses it as an alternative. It is not the default Keynote workflow. Establish the source baseline and separate conversion defects from later design changes.

| Requested route | Application work and review |
| :--- | :--- |
| Keynote source, PowerPoint delivery | In Keynote on Mac, export a new PowerPoint copy and a visual baseline. Compare protected content and native objects with the original before entering the [PowerPoint workflow](pptx-workflow.md). Final appearance and editability review belongs in PowerPoint. |
| PowerPoint source, Keynote delivery | Open a separate PPTX copy in Keynote, inspect conversion/font warnings, save a new `.key`, compare it with the source, then continue native Keynote work and final review. |
| No access to the needed native application | Explain the missing access. The owner may provide exports or perform specified application checks, or choose a different delivery format. Record what remains pending without treating the alternative as equivalent native validation. |

Apple documents exporting a separate PowerPoint copy and opening PowerPoint files in Keynote. Its compatibility matrix describes feature differences, so neither direction implies a lossless round trip. Check scientific typography, chart types and data, connectors, notes, hidden slides and build behavior at each conversion boundary. ([Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac), [Apple import guide](https://support.apple.com/guide/keynote/open-or-close-a-presentation-tan72232b56/mac), [Apple compatibility matrix](https://www.apple.com/keynote/compatibility/))

PDF is a visual reference, not an editable Keynote import adapter. Renaming a file cannot change its format. Keynote for iCloud is also a separate cloud workflow, not an automatic fallback; transferring research to an additional service requires explicit authorization.

## Verification status and report

| Component | Established here | Not established here |
| :--- | :--- | :--- |
| Container router | Bounded recognition, source-preserving routing and unavailable-runtime handling can be tested without a presentation application. | Native file validity, object fidelity, appearance or playback. |
| Python native adapter | Plan/output guards and simulated application-boundary tests exercise Python behavior. | JXA compilation/execution against a real Mac Keynote installation. |
| Native Keynote workflow | Application-specific implementation and review requirements are provided. | Live native inspection, edits, PDF export, native saving, finalization, editability or playback have not been tested on Mac in this environment. |

Identify source, candidate and delivery files in the final report, with meaningful design changes and separate content, appearance, editability and playback results. Record the application/version and checks actually performed. Mark unperformed native checks `not-run`, keep requested `.key` delivery pending where necessary, and distinguish conversion loss from redesign. Keep research-bearing files and detailed evidence outside version control.
