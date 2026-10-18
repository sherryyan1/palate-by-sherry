"""Build a small, explicit-allowlist Skill package; optionally install/update its snapshot.

No research assets, analysis outputs, credentials or machine-specific source state included.
Existing installations are updated only when their complete managed manifest still matches.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "SKILL.md", "agents/openai.yaml", "requirements.txt",
    "scripts/palate_pptx.py", "scripts/render_pptx.ps1",
    "scripts/guided_intake.py", "references/guided-intake.md", "references/guided-intake.json",
    "scripts/presentation_route.py", "references/keynote-workflow.md",
    "scripts/keynote_native.py", "scripts/keynote_native.js",
    "references/design-system.md", "references/design-decision-library.json",
    "references/read-the-room.md", "references/find-the-thread.md",
    "references/distill-the-message.md", "references/refine-the-visuals.md",
    "references/storytelling-examples.md", "scripts/review_title_sequence.py",
    "references/editorial-judgment.md", "references/editorial-techniques.md",
    "references/editorial-source-notes.md",
    "references/presentation-contexts.json", "references/presentation-contexts.md",
    "references/redesign-intake.md", "references/transform-plan.md",
    "references/pptx-workflow.md", "references/scientific-fidelity.md",
    "references/style-adaptation.md",
    "references/writing-style.md",
    "references/communication-design.md",
    "references/spacing-and-hierarchy.md",
    "references/host-workflows.md",
    "references/source-to-slides.md",
    "references/visual-storytelling.md",
    "references/comparison-patterns.md",
    "references/cover-art-direction.md",
    "references/asset-sourcing.md", "references/figure-panels.md",
    "scripts/extract_figure_panels.py",
    "assets/slide-icons/LICENSE", "assets/slide-icons/NOTICE.md",
    "assets/slide-icons/sun.svg", "assets/slide-icons/solar-panel.svg",
    "assets/slide-icons/battery-charging.svg", "assets/slide-icons/house.svg",
    "assets/slide-icons/factory.svg", "assets/slide-icons/network.svg",
    "assets/slide-icons/boxes.svg", "assets/slide-icons/cpu.svg",
    "assets/slide-icons/cloud-rain.svg", "assets/slide-icons/wheat.svg",
    "assets/slide-icons/coins.svg", "assets/slide-icons/sliders-horizontal.svg",
    "assets/slide-icons/dna.svg", "assets/slide-icons/microscope.svg",
]
NAME = "palate"
LEGACY_NAME = "palate-by-sherry"


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


def linked(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def managed_snapshot(directory, expected_name):
    """Verify the complete managed tree before moving or replacing it."""
    marker = directory / "package-manifest.json"
    if not directory.is_dir() or linked(directory) or not marker.is_file() or linked(marker):
        raise ValueError("Existing Skill is unmanaged or linked; preserve it and choose another resolution")
    marker_bytes = marker.read_bytes()
    try:
        manifest = json.loads(marker_bytes)
        files = manifest["files"]
        if manifest.get("name") != expected_name or manifest.get("schema_version") != 1 or not isinstance(files, dict) or not files:
            raise ValueError("Unexpected installation manifest")
        for name, checksum in files.items():
            if (not isinstance(name, str) or not name or "\\" in name or ":" in name or
                    Path(name).is_absolute() or any(part in {"", ".", ".."} for part in name.split("/")) or
                    not (directory / name).resolve().is_relative_to(directory.resolve()) or
                    not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum)):
                raise ValueError("Unsafe installation manifest")
        members = list(directory.rglob("*"))
        if any(linked(member) for member in members):
            raise ValueError("Linked installation members are unsupported")
        existing = {member.relative_to(directory).as_posix() for member in members if member.is_file()}
        if existing != set(files) | {"package-manifest.json"}:
            raise ValueError("Installation has extra/changed managed files; preserve them")
        if any(digest((directory / name).read_bytes()) != checksum for name, checksum in files.items()):
            raise ValueError("Installation contains local edits; refusing to overwrite or migrate")
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError("Invalid installation manifest; preserve the existing Skill") from error
    return marker_bytes


def snapshot_path(directory, marker_bytes):
    # The archive is a sibling of the skills directory, outside skill discovery.
    return directory.parent.parent / ".palate-backups" / digest(marker_bytes)[:12] / directory.name


def prepare_archive(backup, discovery_root):
    archive_root = discovery_root.parent / ".palate-backups"
    if linked(archive_root) or linked(backup.parent) or linked(backup):
        raise ValueError("Linked backup locations are unsupported")
    if not backup.resolve().is_relative_to(archive_root.resolve()) or backup.resolve().is_relative_to(discovery_root.resolve()):
        raise ValueError("Backup must remain outside the skills discovery directory")
    if backup.exists():
        raise ValueError("Previous snapshot exists; preserve it before the next update")


def install(package, destination, migrate_legacy=None):
    requested = Path(destination).absolute()
    if linked(requested):
        raise ValueError("Install destination must not be linked")
    destination = requested.resolve()
    if destination.name != NAME or destination == ROOT.resolve() or destination in ROOT.resolve().parents:
        raise ValueError("Install to a separate skills/palate directory")
    legacy = destination.parent / LEGACY_NAME
    if migrate_legacy is not None:
        supplied = Path(migrate_legacy).absolute()
        if supplied != legacy or linked(supplied):
            raise ValueError("Legacy migration must name the exact sibling skills/palate-by-sherry directory")
    elif legacy.exists():
        raise ValueError("Legacy Skill exists; explicitly use --migrate-legacy to archive it outside discovery")
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
    snapshots = []
    if destination.exists():
        marker_bytes = managed_snapshot(destination, NAME)
        snapshots.append((destination, snapshot_path(destination, marker_bytes), marker_bytes, NAME))
    if migrate_legacy is not None:
        marker_bytes = managed_snapshot(legacy, LEGACY_NAME)
        snapshots.append((legacy, snapshot_path(legacy, marker_bytes), marker_bytes, LEGACY_NAME))
    for _, backup, _, _ in snapshots:
        prepare_archive(backup, destination.parent)
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
        managed_snapshot(stage, NAME)
        moved = []
        try:
            for original, backup, marker_bytes, expected_name in snapshots:
                if managed_snapshot(original, expected_name) != marker_bytes:
                    raise ValueError("Installation changed while staging; preserve it")
                prepare_archive(backup, destination.parent)
                backup.parent.mkdir(parents=True, exist_ok=True)
                original.rename(backup)
                moved.append((original, backup))
            stage.rename(destination)
        except Exception:
            for original, backup in reversed(moved):
                backup.rename(original)
            raise
    return str(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--install")
    parser.add_argument("--migrate-legacy", help="Explicitly archive the unchanged managed sibling skills/palate-by-sherry outside discovery")
    args = parser.parse_args()
    if args.migrate_legacy and not args.install:
        parser.error("--migrate-legacy requires --install")
    manifest = build(args.output)
    legacy_backup = None
    if args.migrate_legacy:
        legacy = Path(args.migrate_legacy).resolve()
        legacy_backup = snapshot_path(legacy, managed_snapshot(legacy, LEGACY_NAME))
    installed = install(args.output, args.install, migrate_legacy=args.migrate_legacy) if args.install else None
    print(json.dumps({"package": str(Path(args.output).resolve()), "file_count": len(manifest["files"]),
                      "bytes": Path(args.output).stat().st_size, "installed": installed,
                      "legacy_archived": str(legacy_backup) if legacy_backup else None}))


if __name__ == "__main__":
    main()
