"""Build a small, explicit-allowlist Skill package; optionally install/update its snapshot.

No research assets, analysis outputs, credentials or machine-specific source state included.
Existing installations are updated only when their complete managed manifest still matches.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "SKILL.md", "agents/openai.yaml", "requirements.txt",
    "scripts/palate_pptx.py", "scripts/render_pptx.ps1",
    "scripts/guided_intake.py", "references/guided-intake.md", "references/guided-intake.json",
    "references/design-system.md", "references/design-decision-library.json",
    "references/presentation-contexts.json", "references/presentation-contexts.md",
    "references/redesign-intake.md", "references/transform-plan.md",
    "references/pptx-workflow.md", "references/scientific-fidelity.md",
    "references/style-adaptation.md",
]
NAME = "palate-by-sherry"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(output):
    output = Path(output)
    if output.exists():
        raise ValueError("Package exists; choose a new revision filename")
    payload = {n: (ROOT / n).read_bytes() for n in FILES}
    manifest = {"name": NAME, "schema_version": 1, "files": {n: digest(d) for n, d in payload.items()}}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream, zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in payload.items():
            z.writestr(NAME + "/" + name, data)
        z.writestr(NAME + "/package-manifest.json", json.dumps(manifest, indent=2))
    return manifest


def install(package, destination):
    destination = Path(destination).resolve()
    if destination.name != NAME or destination == ROOT.resolve() or destination in ROOT.resolve().parents:
        raise ValueError("Install to a separate skills/palate-by-sherry directory")
    with zipfile.ZipFile(package) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate package paths")
        manifest = json.loads(z.read(NAME + "/package-manifest.json"))
        if manifest.get("name") != NAME or manifest.get("schema_version") != 1 or set(manifest["files"]) != set(FILES):
            raise ValueError("Unexpected package manifest")
        expected = {NAME + "/" + n for n in FILES} | {NAME + "/package-manifest.json"}
        if set(names) != expected:
            raise ValueError("Package contains non-allowlisted paths")
        payload = {n: z.read(NAME + "/" + n) for n in FILES}
        if any(digest(data) != manifest["files"][n] for n, data in payload.items()):
            raise ValueError("Package hash mismatch")
    if destination.exists():
        marker = destination / "package-manifest.json"
        if not marker.exists():
            raise ValueError("Existing Skill is unmanaged; preserve it and choose another resolution")
        old = json.loads(marker.read_text(encoding="utf-8"))
        existing = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
        old_files = set(old.get("files", {}))
        safe_paths = all(not Path(n).is_absolute() and ".." not in Path(n).parts and
                         (destination / n).resolve().is_relative_to(destination) for n in old_files)
        if old.get("name") != NAME or old.get("schema_version") != 1 or not safe_paths or existing != old_files | {"package-manifest.json"}:
            raise ValueError("Installation has extra/changed managed files; preserve them")
        if any(not (destination / n).exists() or digest((destination / n).read_bytes()) != h for n, h in old["files"].items()):
            raise ValueError("Installation contains local edits; refusing to overwrite")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Stage and verify before replacing only this managed directory. No recursive delete.
    with tempfile.TemporaryDirectory(prefix="palate-stage-", dir=destination.parent) as temp:
        stage = Path(temp) / NAME
        stage.mkdir()
        for name, data in payload.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (stage / "package-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        if destination.exists():
            # Keep the prior installation as a recoverable sibling snapshot.
            old_id = digest(marker.read_bytes())[:12]
            backup = destination.parent / ".palate-backups" / old_id / NAME
            if backup.exists():
                raise ValueError("Previous snapshot exists; preserve it before the next update")
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
            try:
                stage.rename(destination)
            except Exception:
                backup.rename(destination)
                raise
        else:
            stage.rename(destination)
    return str(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--install")
    args = parser.parse_args()
    manifest = build(args.output)
    installed = install(args.output, args.install) if args.install else None
    print(json.dumps({"package": str(Path(args.output).resolve()), "file_count": len(manifest["files"]),
                      "bytes": Path(args.output).stat().st_size, "installed": installed}))


if __name__ == "__main__":
    main()
