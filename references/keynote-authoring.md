# Native Keynote authoring

Use `scripts/keynote_author.py` for declarative native creation/editing on a Mac with live Keynote access. It creates `.key` directly. Its tested operations and remaining gaps are recorded in [capability status](native-capabilities.json). Controlled Keynote editing remains the path for operations absent from the scripting dictionary. Do not extend fixture evidence to untested features or versions.

Supply JSON fields `schema_version: 1`, `mode` (`create` or `edit`), `source_sha256` (null for create, exact source hash for edit), nonempty `content_ledger`, and `operations`. Selectors are one-based, referring to the state after preceding operations. Requests are data, never executable code.

```text
python scripts/keynote_author.py --spec private/spec.json --output private/candidate.key --receipt private/author.json --pdf private/preview.pdf
python scripts/keynote_author.py --spec private/edit.json --source input.key --output private/edited.key --receipt private/edited.json --pdf private/edited.pdf
```

| Action | Fields beyond action | Behavior |
| --- | --- | --- |
| add_slide | optional layout, notes, skipped | Append slide; layout must exist in this document. |
| set_slide | slide; optional layout, notes, skipped | Update native metadata/layout assignment. |
| delete_slide / duplicate_slide | slide | Delete/duplicate on an owned copy; last slide protected. |
| move_slide | slide, before | Move before the given current slide. |
| set_canvas | width, height | Native points; reflow remains the author's responsibility. |
| add_text / add_shape | slide, text, bounds; optional font, size, color | Native editable objects; detailed shape design requires UI. |
| set_text | slide, kind (text_item or shape), index, text; optional font, size, color | Explicit content-changing text edit. |
| add_table | slide, rectangular cells, bounds | Native literal-value table. |
| set_cell | slide, index, row, column, value | Edit literal cell; formulas need separate native review. |
| add_chart | slide, rows, columns, data, chart_type, bounds | Native chart with rectangular numeric data. |
| add_image | slide, absolute path, sha256, bounds | Verified PNG/JPEG asset, never a flattened slide. |

`bounds` is `[x,y,width,height]` in points. For `add_text`, `height_mode` defaults to `fixed`: an exact height mismatch blocks the operation. Use explicit `height_mode: fit` when the design allows Keynote to shrink the text container within the requested height; position and width must still match, and overflow is rejected. Use native UI for fixed text frames the scripting interface cannot produce; `color` is RGB hex. Chart types: `vertical_bar_2d`, `stacked_vertical_bar_2d`, `horizontal_bar_2d`, `line_2d`, `pie_2d`. Preserve image aspect ratios and scientific context. Inspect chart data in Keynote: exposed inventory counts cannot prove chart fidelity.

The orchestrator stages owned copies, verifies asset hashes, exports all slides, compares exposed inventory after independent save/reopen, and preserves sources. Failed work retains scratch evidence. Outputs remain candidates until the [shared delivery gate](native-delivery.md) and actual native review pass. The preservation finalizer cannot validate content-changing authoring. After actual review, use `python scripts/keynote_author.py --finalize private/candidate.key --review private/review.json --output outputs/final.key --receipt outputs/final-review.json`; this reopens the candidate and applies the shared gate before copying final bytes.
