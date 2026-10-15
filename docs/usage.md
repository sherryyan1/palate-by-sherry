# Usage

## Requirements

| Task | Required |
| :--- | :--- |
| Identify source format and route the workflow | Python 3.11+ |
| Inspect and preserve PowerPoint objects | Python 3.11+, lxml |
| Raster-resolution diagnostics | Pillow |
| Included Windows rendering | Microsoft PowerPoint |
| New or rebuilt native slides | Available native presentation authoring workflow |
| Native Keynote delivery and review | Keynote on Mac |

Use existing bundled runtimes when available. The conservative helper requires no Node SDK. The installed presentations workflow provides JavaScript authoring through `@oai/artifact-tool`.

## Install

From the repository root:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate.zip --install "$env:USERPROFILE\.codex\skills\palate"
```

On other systems, install to the configured Codex skills directory under `palate`. Use a fresh package filename for updates. The installer verifies the package, refuses to overwrite local edits and keeps a recoverable previous snapshot.

To migrate an earlier installation, name it explicitly:

```powershell
python scripts/package_skill.py --output dist/palate-update.zip --install "$env:USERPROFILE\.codex\skills\palate" --migrate-legacy "$env:USERPROFILE\.codex\skills\palate-by-sherry"
```

The installer verifies the complete managed installation before archiving it outside the skills directory. Local edits stop migration; the previous files remain intact.

## Start with one sentence

Attach your research slides and ask:

```text
Use palate to polish my slides.
```

palate obtains missing context through [guided choices](../references/guided-intake.md):

| Selection | Options |
| :--- | :--- |
| Setting | Internal tutorial, internal research, external |
| External audience | Experts, C-suite/executives, general audience |
| Duration | Common times or custom minutes |
| Depth | Let palate choose, key takeaways, full technical detail |

The external-audience question appears only on that branch. Duration and depth can share a short question card. Native choice cards depend on the host's available tools; concise numbered questions provide the fallback. The user can enter a custom answer or provide a detailed brief upfront. Supplied fields are not asked again.

Named [contexts](../references/presentation-contexts.md) suggest duration defaults; the current request overrides them. The brief guides reading order, pacing and visible detail rather than selecting a fixed template. Single-page monthly updates are outside this skill's scope.

## Workflow

1. Identify the source format, resolve the brief and review rendered slides.
2. Choose the composition and document source-to-output changes.
3. Preserve existing objects or use native authoring for larger changes.
4. Check content, editability and visual appearance; finalize a new deck and report.

**Preserve existing objects.** The conservative helper changes placement, chart frames, text styling, shapes, lines and backgrounds while retaining source content and embedded workbooks. It rejects unsafe geometry and animation edits.

**Rebuild or change content.** Use native authoring for new slides or diagrams, summaries, slide splits, chart internals and table dimensions. Maintain a content ledger and review any changes to grouped objects or animation states.

See the [plan contract](../references/transform-plan.md) for CLI commands and the [scientific fidelity guide](../references/scientific-fidelity.md) for content-changing work. Structural checks complement visual and scientific review; they do not replace them.

## PowerPoint and Keynote

The design brief, decision rules and scientific checks are shared. File handling follows the source format. The read-only router reports the next step without converting, launching applications or uploading files:

```text
python scripts/presentation_route.py "source.pptx" --target pptx
python scripts/presentation_route.py "source.key" --target keynote
```

For a Keynote source, preserve the original and export a PowerPoint copy plus a PDF visual reference. Compare the export with the source before design. After polishing, open the result in Keynote, save a new native deck and check every slide, native objects and playback. Follow the [Keynote workflow](../references/keynote-workflow.md) for export settings and conversion review.

Windows can prepare the interchange deck. Native Keynote delivery requires Keynote on Mac; when it is unavailable, record that review as pending. A PDF is a visual reference, and renaming a file does not convert its format.

Research files and task artifacts remain local unless their upload is explicitly authorized. Packages include runtime instructions and code only. Git, packages and installed copies are synchronized explicitly.
