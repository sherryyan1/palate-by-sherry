# Keynote format handoff for palate

palate uses the same intake, design decisions and scientific fidelity rules for PowerPoint and Keynote. The executable adapter edits compatible PPTX objects. Keynote sources enter through a verified export, and native Keynote delivery requires an actual Keynote runtime. There is no native `.key` editor or transformer in this package.

## Inspect and choose a route

Run the read-only standard-library helper before choosing an authoring path:

```powershell
python scripts/presentation_route.py "input.key" --target keynote
python scripts/presentation_route.py "input.pptx" --target pptx
```

The helper reads containers, emits JSON to standard output and never changes sources, launches applications or uploads files. Keep its output and source-specific evidence private. Exit code 0 means a recognized route was emitted; it does not mean the requested presentation was produced. Exit code 2 means unsupported input.

| Input and requested delivery | State | Next action |
| --- | --- | --- |
| Compatible PPTX, PPTX delivery | `ready-pptx` | Enter the [shared PPTX workflow](pptx-workflow.md); all reviews remain pending. |
| Compatible PPTX, native Keynote delivery | `requires-keynote-runtime` | Polish the PPTX, then import, save and validate a new `.key` in Keynote. |
| Recognized Keynote ZIP or directory bundle | `requires-export` | Obtain new local PPTX and PDF exports from an available Keynote runtime. |
| PDF | `reference-only` | Review appearance; obtain an editable deck before transforming native objects. |
| Credential `.key`, unknown, malformed or unsupported container | `unsupported` | Select the actual presentation or obtain compatible exports. |

`can_transform_now` means the source may enter full PPTX inspection and the resolved shared workflow. It does not authorize bypassing intake, animations or fidelity guards. `can_deliver_target_now` is false until the downstream workflow has produced and reviewed the deliverable. This router does not certify a finished deck.

The router recognizes modern Keynote directory bundles and ZIPs using an IWA document plus slide/master-slide signature, including a bounded nested `Index.zip` variant. This is a conservative recognition rule, not an Apple file-format parser. It does not decode IWA, count native objects, validate media, prove that Keynote can open the file, or cover every historic/encrypted Keynote variant. An APXL marker gets a legacy export handoff without a native-validity claim. Missing or unfamiliar markers remain unsupported. The filename extension alone is insufficient: `.key` can also contain credentials, which are excluded without returning their text.

Compatible PPTX recognition checks the core transitional OOXML content type, presentation/slide roots and relationships. It does not replace `palate_pptx.py inspect` or full validation. Macro-enabled, strict OOXML, protected and malformed files need a compatible application export before using this adapter. ZIP inspection is bounded, never extracts members, and rejects duplicate, unsafe or linked members. File hashes bind sources; directory bundles use a deterministic sorted member-name/content-hash manifest.

## Keynote source to a reviewed PPTX candidate

1. Preserve the original `.key` and use a duplicate for application work. Retain its source hash and record the Keynote version and export settings locally. Keynote auto-saves, so use the duplicate for inspection or repairs that could change the source.
2. With available Keynote on Mac, export separate fresh copies with **File > Export To > PowerPoint** and **File > Export To > PDF**. Keynote's PowerPoint export produces `.pptx`. Apple documents export as a separate copy, leaving the original unaffected. Password protection can carry to exported copies; use the owner's authorized export settings and keep passwords out of reports. ([Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac))
3. Use the PDF as source appearance evidence. Include skipped slides and presenter notes where they contain required evidence, and export build stages separately when needed. Preserve slide/build correspondence rather than assuming one PDF page always equals one slide. These PDF settings are documented in the same [Apple export guide](https://support.apple.com/guide/keynote/export-to-powerpoint-or-another-file-format-tana0d19882a/mac).
4. Inspect the exported PPTX and compare it with the original in Keynote before changing design. Record any conversion loss separately from later design changes. Verify numerical values, units, categories, equations, citations, uncertainty and qualifications; check notes, skipped slides, charts and media. Stop on unresolved evidence loss and retain complex source figures when reconstruction cannot be verified.
5. Apply the [PPTX workflow](pptx-workflow.md) to a new candidate, using the shared design system and scientific fidelity rules. Preserve original, exported baseline and candidate as separate files. Review content, rendered appearance and editability independently. A PDF page or whole-slide screenshot does not establish native editability.

A `.key` directory bundle is a valid packaging form on Mac; it must be preserved as a directory, not treated as a text key or flattened. Apple also provides **File > Advanced > Change File Type > Single File** when an available Keynote runtime needs to change packaging on a duplicate. Packaging is not conversion to PowerPoint. ([Apple package guide](https://support.apple.com/guide/keynote/save-a-large-presentation-as-a-package-file-tanaa443947b/mac), [Apple single-file/package guidance](https://support.apple.com/119883))

## Reviewed PPTX candidate to native Keynote delivery

Apple documents opening and editing `.pptx` and `.ppt` in Keynote. In available Keynote on Mac, use **File > Open** on the reviewed PPTX and save the imported presentation as a fresh `.key` file. Inspect missing-font and conversion warnings; resolve substitutions with the original scientific typography in view. ([Apple import guide](https://support.apple.com/guide/keynote/open-or-close-a-presentation-tan72232b56/mac))

Before calling the `.key` complete, perform these separate reviews in Keynote:

- **Content:** Compare every slide with the reviewed PPTX and original research source. Check values, units, labels, legends, categories, equations, caveats, references, notes and skipped slides. Inspect chart data and table formulas where required; cached pictures are insufficient.
- **Appearance:** Export a fresh PDF from Keynote and inspect every final slide, including changed slides against both baselines. Check text wraps, clipping, fonts, aspect ratios, connectors, figure labels and scientific reading order. Re-export after repairs.
- **Editability:** Select and inspect text, tables, charts and diagrams in Keynote. Confirm that intended native objects can still be edited and that chart data remain available. Report retained image regions and limitations precisely. Imported PPTX structure and a static PDF do not certify Keynote editability.
- **Playback:** Rehearse in Keynote when the deck includes transitions, builds, audio or video. Review order, timing and staged evidence; a PDF export cannot prove playback.

Apple's compatibility matrix documents substitutions such as SmartArt becoming shapes, unsupported fonts being replaced, some chart types changing, and connectors attached to placeholders becoming straight lines. These are reasons to review specific objects, not permission to discard evidence. The matrix describes Office feature support; it does not guarantee a lossless Keynote-to-PowerPoint-to-Keynote round trip. ([Apple compatibility matrix](https://www.apple.com/keynote/compatibility/))

PDF serves as visual reference in this workflow. Exporting or placing PDF pages does not restore slide-native chart data, editable tables or animations; do not advertise PDF-to-Keynote as an editable import adapter.

## Windows delivery limits and validation status

On Windows, the installed PPTX workflow can inspect and polish a compatible local PowerPoint export. This helper provides local file detection and deterministic handoff instructions. It does not implement native `.key` editing or export, and no native Keynote import, export, rendering, editability or playback has been tested in this environment. Unit tests use synthetic container signatures; they establish detection and routing behavior only.

If an available local Keynote runtime cannot be used, obtain exports from the owner or deliver the independently reviewed PPTX with a clear native-Keynote validation limit. A requested `.key` remains pending until imported, saved and reviewed in Keynote. Preserve that state in the transformation report instead of treating a `.pptx` renamed `.key` as delivery.

Apple offers Keynote for iCloud in supported browsers on Windows. It is a cloud workflow that can synchronize presentation changes. This local route does not invoke it, create an account or upload research; it is not an automatic fallback. ([Apple Keynote for iCloud overview](https://support.apple.com/guide/keynote-icloud/intro-to-keynote-for-icloud-gilf2fb004e2/icloud))

Return a concise report stating the original/export/candidate mapping, meaningful design changes, separate content/appearance/editability results, conversion defects and actual application/version used. Include native Keynote results only when performed; otherwise state `not-run` and the remaining handoff. Keep research-bearing files and detailed review evidence outside version control.
