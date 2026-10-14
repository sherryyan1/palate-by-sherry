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

## Start with one sentence

Attach a research PPTX and ask:

```text
Use palate-by-sherry to polish my PPT.
```

Palate obtains missing context through [guided choices](../references/guided-intake.md):

| Selection | Options |
| :--- | :--- |
| Setting | Internal tutorial, internal research, external |
| External audience | Experts, C-suite/executives, general audience |
| Duration | Common times or custom minutes |
| Depth | Palate decides, key takeaways, full technical detail |

The external-audience question appears only on that branch. Duration and depth can share a short question card. Native choice cards depend on the host's available tools; concise numbered questions provide the fallback. The user can enter a custom answer or provide a detailed brief upfront. Supplied fields are not asked again.

Named [contexts](../references/presentation-contexts.md) suggest duration defaults; the current request overrides them. The brief guides reading order, pacing and visible detail rather than selecting a fixed template. Single-page monthly updates are outside this skill's scope.

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
