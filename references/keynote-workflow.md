# Keynote format handoff for palate

PowerPoint and Keynote presentations need the same design judgment: the audience must be able to follow the argument and read the evidence without losing its qualifications. **palate** therefore shares intake, design decisions and scientific fidelity rules across both applications.

This reference guides the agent through the file handoff when the source or requested deliverable is a Keynote presentation. The executable preservation adapter edits compatible PPTX objects, so a Keynote source first needs a verified export and a native Keynote deliverable needs an actual Keynote runtime. This package contains no native `.key` editor or transformer.

Begin by [identifying the route](#inspect-and-choose-a-route). A Keynote source then needs an [export baseline](#keynote-source-to-a-reviewed-pptx-candidate); native Keynote delivery needs a separate [import and review](#reviewed-pptx-candidate-to-native-keynote-delivery). If that application work is unavailable, use the [delivery limits](#windows-delivery-limits-and-validation-status) to explain what remains pending.

## Inspect and choose a route

Resolve the delivery application before choosing an authoring path. Preserve the source application by default unless the user requests another format, then pass that target explicitly to the read-only standard-library helper:

```powershell
python scripts/presentation_route.py "input.key" --target keynote
python scripts/presentation_route.py "input.pptx" --target pptx
```

The helper reads the container and emits JSON to standard output; it never changes a source, launches an application or uploads a file. Keep its output and source-specific evidence private. The result identifies the next available step, with all delivery review still to come:

| Input and requested delivery | State | Next action |
| --- | --- | --- |
| Compatible PPTX, PPTX delivery | `ready-pptx` | Enter the [shared PPTX workflow](pptx-workflow.md); all reviews remain pending. |
| Compatible PPTX, native Keynote delivery | `requires-keynote-runtime` | Polish the PPTX, then import, save and validate a new `.key` in Keynote. |
| Recognized Keynote ZIP or directory bundle | `requires-export` | Obtain new local PPTX and PDF exports from an available Keynote runtime. |
| PDF | `reference-only` | Review appearance; obtain an editable deck before transforming native objects. |
| Credential `.key`, unknown, malformed or unsupported container | `unsupported` | Select the actual presentation or obtain compatible exports. |

Interpret the status and capability fields as routing information:

| Signal | Meaning |
| --- | --- |
| Exit code 0 | A recognized route was emitted. The requested presentation has not been produced by the router. |
| Exit code 2 | The input is unsupported. |
| `can_transform_now` | The source may enter full PPTX inspection and the resolved shared workflow. Intake, animation and fidelity guards still apply. |
| `can_deliver_target_now` | False in router output. The downstream workflow must produce and review the deliverable before delivery can be certified. |

Recognition is deliberately narrower than application validation. The container supplies enough evidence to choose a handoff, but only the application can establish how its objects open and behave:

| Container evidence | Recognition and limit |
| --- | --- |
| Modern Keynote directory bundle or ZIP | An IWA document plus slide/master-slide signature, including a bounded nested `Index.zip` variant. This conservative rule is not an Apple file-format parser: it does not decode IWA, count native objects, validate media, prove the file opens in Keynote or cover every historic/encrypted variant. |
| APXL marker | A legacy export handoff, without a native-validity claim. Missing or unfamiliar markers remain unsupported. |
| Compatible PPTX | Core transitional OOXML content type, presentation/slide roots and relationships. Full `palate_pptx.py inspect` and validation are still required. Macro-enabled, strict OOXML, protected and malformed files need a compatible application export. |
| Credential `.key` | Excluded without returning its text. An extension alone cannot establish that a file is a presentation. |

ZIP inspection is bounded, never extracts members and rejects duplicate, unsafe or linked members. Source hashes then bind the later work to the inspected baseline. Files use their content hash; directory bundles use a deterministic manifest of sorted member names and content hashes.

## Keynote source to a reviewed PPTX candidate

The export becomes the working baseline for design, so its fidelity must be understood before any redesign makes the source harder to compare.

1. Preserve the original `.key`, retain its source hash and use a duplicate for application work. Keynote auto-saves; a duplicate keeps inspection or repairs from changing the original. Record the Keynote version and export settings locally so later comparisons refer to a known conversion.
2. In available Keynote on Mac, export fresh copies with **File > Export To > PowerPoint** and **File > Export To > PDF**. The first supplies an editable `.pptx`, while the second records appearance. Apple documents these as separate copies that leave the original unaffected. Password protection can carry into exported copies, so use the owner's authorized export settings and keep passwords out of reports. ([Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac))
3. Set the PDF export to retain the evidence needed for comparison. Include skipped slides and presenter notes where they contain required material, and export build stages separately when needed. Preserve the correspondence between slides and builds: one PDF page does not always mean one slide. The available settings are described in the [Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac).
4. Inspect the PPTX and compare it with the original in Keynote before changing design. Check numerical values, units, categories, equations, citations, uncertainty and qualifications, along with notes, skipped slides, charts and media. Record conversion loss separately from later design changes. Stop if evidence loss remains unresolved, and retain complex source figures when reconstruction cannot be verified.
5. Apply the [PPTX workflow](pptx-workflow.md) to a new candidate with the shared design system and scientific fidelity rules. Keep the original, exported baseline and candidate as separate files. Review content, rendered appearance and editability independently; a PDF page or whole-slide screenshot provides appearance evidence, not proof of native editability.

A `.key` directory bundle is a valid packaging form on Mac and must remain intact as a directory. Do not flatten it or treat it as a text key. If packaging needs to change, available Keynote on Mac offers **File > Advanced > Change File Type > Single File**; perform that change on a duplicate. It changes the packaging while leaving conversion to PowerPoint as a separate export step. ([Apple package guide](https://support.apple.com/guide/keynote/save-a-large-presentation-as-a-package-file-tanaa443947b/mac), [Apple single-file/package guidance](https://support.apple.com/119883))

## Reviewed PPTX candidate to native Keynote delivery

Once the PPTX candidate has passed review, import creates another conversion boundary. Apple documents opening and editing `.pptx` and `.ppt` in Keynote. In available Keynote on Mac, use **File > Open** on the reviewed PPTX, inspect missing-font and conversion warnings, and save the imported presentation as a fresh `.key`. Resolve font substitutions with the original scientific typography in view so a changed symbol or wrap does not alter the evidence. ([Apple import guide](https://support.apple.com/guide/keynote/open-or-close-a-presentation-tan72232b56/mac))

Before calling the `.key` complete, gather separate evidence for each review dimension in Keynote:

| Review | Required evidence |
| --- | --- |
| Content | Compare every slide with the reviewed PPTX and original research source. Check values, units, labels, legends, categories, equations, caveats, references, notes and skipped slides. Inspect chart data and table formulas where required; cached pictures are insufficient. |
| Appearance | Export a fresh PDF from Keynote and inspect every final slide, comparing changed slides with both baselines. Check text wraps, clipping, fonts, aspect ratios, connectors, figure labels and scientific reading order. Re-export after repairs. |
| Editability | Select and inspect text, tables, charts and diagrams in Keynote. Confirm that the intended native objects remain editable and chart data remain available. Report retained image regions and their limits precisely; imported PPTX structure or a static PDF cannot certify Keynote editability. |
| Playback | When transitions, builds, audio or video are present, rehearse in Keynote and review order, timing and staged evidence. PDF export cannot prove playback. |

These checks matter because conversion can retain a familiar appearance while changing an object's behavior or representation. Apple's compatibility matrix documents SmartArt becoming shapes, substitutions for unsupported fonts, changes to some chart types, and straight lines replacing connectors attached to placeholders. Review the affected objects and preserve their evidence; the matrix describes Office feature support and gives no guarantee of a lossless Keynote-to-PowerPoint-to-Keynote round trip. ([Apple compatibility matrix](https://www.apple.com/keynote/compatibility/))

PDF remains a visual reference throughout this workflow. Exporting or placing its pages cannot restore slide-native chart data, editable tables or animations, so PDF-to-Keynote must not be advertised as an editable import adapter.

## Windows delivery limits and validation status

On Windows, the installed PPTX workflow can inspect and polish a compatible local PowerPoint export, and the router can identify a local container and provide deterministic handoff instructions. Neither provides native `.key` editing or export. Native Keynote import, export, rendering, editability and playback have not been tested in this environment; the unit tests use synthetic signatures and establish detection and routing behavior only.

When a local Keynote runtime cannot be used, obtain exports from the owner or deliver the independently reviewed PPTX with a clear native-Keynote validation limit. A requested `.key` remains pending until it has been imported, saved and reviewed in Keynote. Carry that remaining handoff into the report; renaming a `.pptx` to `.key` never completes it.

Apple also offers Keynote for iCloud through supported browsers on Windows. That cloud workflow can synchronize presentation changes, which makes it a separate file-handling decision from the local route described here. The local route does not invoke iCloud, create an account or upload research, and iCloud is not an automatic fallback. ([Apple Keynote for iCloud overview](https://support.apple.com/guide/keynote-icloud/intro-to-keynote-for-icloud-gilf2fb004e2/icloud))

## Report the handoff

The final report should let the owner distinguish the design work from conversion effects and unfinished application checks. Identify the original, export and candidate; explain meaningful design changes; and record separate content, appearance and editability results, conversion defects, and the application/version actually used. Include native Keynote results only when those checks were performed. Otherwise record `not-run` and the remaining handoff. Keep research-bearing files and detailed review evidence outside version control.
