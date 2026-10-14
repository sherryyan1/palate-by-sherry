# Usage

## Requirements

| Task | Required |
| :--- | :--- |
| Inspect and preserve PPTX objects | Python 3.11+, lxml |
| Raster-resolution diagnostics | Pillow |
| Included Windows rendering | Microsoft PowerPoint |
| New or rebuilt native slides | Available native presentation authoring workflow |

Use existing bundled runtimes when available. The conservative helper requires no Node SDK. The installed presentations workflow provides JavaScript authoring through `@oai/artifact-tool`.

## Install

From the repository root:

```powershell
python -m pip install -r requirements.txt
python scripts/package_skill.py --output dist/palate-by-sherry.zip --install "$env:USERPROFILE\.codex\skills\palate-by-sherry"
```

On other systems, install to the configured Codex skills directory under `palate-by-sherry`. Use a fresh package filename for updates. The installer verifies its manifest, preserves local edits and retains a recoverable previous snapshot.

## Give the brief

Attach a research PPTX and specify audience, time, technical depth and purpose. For example:

```text
Use $palate-by-sherry to redesign this deck for a 30-minute expert project briefing.
Keep enough method detail for live discussion. Foreground the findings,
preserve all data, uncertainty and references, and return an editable PPTX
with a concise transformation report.
```

Named [contexts](../references/presentation-contexts.md) supply defaults. The current request overrides them. Single-page monthly updates are outside this skill's scope.

## Workflow

1. Inspect the source, resolve the brief and review rendered slides.
2. Choose the composition and document source-to-output changes.
3. Preserve existing objects or use native authoring for larger changes.
4. Check content, editability and visual appearance; finalize a new deck and report.

| Preservation helper | Native authoring path |
| :--- | :--- |
| Place existing objects and resize chart frames | Rebuild slides or diagrams |
| Style text, shapes, lines and backgrounds | Summarize or split content with a ledger |
| Retain source text, media, charts and workbooks | Edit chart internals or table dimensions |
| Reject unsafe geometry and animation edits | Review grouped geometry and animation states |

See the [plan contract](../references/transform-plan.md) for CLI commands and the [scientific fidelity guide](../references/scientific-fidelity.md) for content-changing work. Structural checks complement visual and scientific review; they do not replace them.

Research files and task artifacts remain local unless their upload is explicitly authorized. Packages include runtime instructions and code only. Git, packages and installed copies are synchronized explicitly.
