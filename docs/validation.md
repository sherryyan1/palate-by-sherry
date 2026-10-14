# Validation

The workflow checks scientific content, native editability and rendered appearance separately.

| Check | Coverage |
| :--- | :--- |
| Automated regression | 16 synthetic OOXML and packaging tests |
| End-to-end transformation | Two-slide native chart, table, text and process fixture |
| Render review | Before/after PowerPoint exports, individually inspected |
| Editability | Reversible text, table-cell and chart-series edits in PowerPoint |
| Content conservation | Values, units, categories, qualifiers, media, notes and workbooks |

The integration fixture contains synthetic data only. Its authoring package, layout, chart, font and import checks passed. Transformation preserved all six chart values and the embedded workbook; the reviewed candidate was finalized with a mapping report.

## Run regression tests

```text
python -m unittest discover -s tests -v
python scripts/audit_repository.py
```

The test suite covers stale hashes, unsafe image geometry, native table placement, animation/math guards, unknown actions, overwrites, review coverage and installed local-edit preservation. Chart identity follows relationship targets rather than assumed package locations.

For integration, create a fixture with `tests/create_fixture.mjs` using the bundled presentation authoring workflow, then apply `tests/run_integration.py`. Render source and candidate with `scripts/render_pptx.ps1`, inspect every slide and exercise `tests/check_powerpoint_objects.ps1`. Record actual review evidence before finalization.

## Scope of a pass

Structural checks establish package/content conservation. Human or agent review establishes the visual and scientific judgment recorded for that output. Static exports do not verify animation playback. Raster interiors remain raster unless verified reconstruction is performed. A test pass is not a guarantee for arbitrary scientific content or unsupported imported objects.

Content rewriting, table resizing, chart-internal styling, grouped geometry and animation changes use the native authoring path and its content ledger. Every deliverable still receives the checks appropriate to its actual changes.
