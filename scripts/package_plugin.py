"""Generate a portable, skills-only plugin from the canonical Skill allowlist.

The ZIP has plugin.json at its root and one skill at skills/palate/. An optional
fresh directory receives the same bytes for local testing. This does not install
or publish a plugin, extract an archive, or replace any existing output.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import stat
import zipfile


# Load the sibling by filename so both direct CLI use and external imports work.
SPEC = importlib.util.spec_from_file_location("palate_package_skill", Path(__file__).with_name("package_skill.py"))
package_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package_skill)
ROOT = package_skill.ROOT
PLUGIN_MANIFEST = "packaging/plugin.json"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SKILL_PREFIX = "skills/" + package_skill.NAME + "/"


def linked(path):
    """Include broken symlinks and Windows junctions without following them."""
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        return True
    try:
        return getattr(path.lstat(), "st_reparse_tag", None) == getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", 0xA0000003)
    except FileNotFoundError:
        return False


def fresh_path(path):
    """Check the requested path and every ancestor before resolving links."""
    requested = Path(path).absolute()
    for member in (requested, *requested.parents):
        if linked(member):
            raise ValueError("Output path and its ancestors must not be linked")
        if member != requested and member.exists() and not member.is_dir():
            raise ValueError("Output parent must be a directory")
    if requested.exists():
        raise ValueError("Output exists; choose a fresh package filename or directory")
    return requested.resolve()


def source_bytes(name):
    """Read only an explicit relative runtime path inside the source repository."""
    if (not isinstance(name, str) or not name or "\\" in name or ":" in name or
            any(part in {"", ".", ".."} for part in name.split("/")) or Path(name).is_absolute()):
        raise ValueError("Unsafe source allowlist path")
    source = ROOT / name
    for member in (source, *source.parents):
        if linked(member):
            raise ValueError("Linked source paths are unsupported")
        if member == ROOT:
            break
    if not source.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Source path escapes the repository")
    return source.read_bytes()


def plugin_manifest_bytes():
    """Keep this package limited to portable metadata and OpenAI presentation."""
    data = source_bytes(PLUGIN_MANIFEST)
    metadata = json.loads(data)
    allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "extensions"}
    if (not isinstance(metadata, dict) or set(metadata) - allowed or
            metadata.get("$schema") != PLUGIN_SCHEMA or metadata.get("name") != package_skill.NAME):
        raise ValueError("Expected the skills-only portable plugin manifest")
    for field in ("version", "description", "homepage", "repository"):
        if field in metadata and not isinstance(metadata[field], str):
            raise ValueError("Plugin metadata fields must be strings")
    author = metadata.get("author", {})
    if not isinstance(author, dict) or set(author) - {"name"} or any(not isinstance(value, str) for value in author.values()):
        raise ValueError("Expected author name metadata only")
    extensions = metadata.get("extensions", {})
    if not isinstance(extensions, dict) or set(extensions) - {"com.openai"}:
        raise ValueError("Unsupported plugin extension")
    openai = extensions.get("com.openai", {})
    if not isinstance(openai, dict) or set(openai) - {"interface"}:
        raise ValueError("Only OpenAI interface metadata is supported")
    interface = openai.get("interface", {})
    interface_fields = {"displayName", "shortDescription", "developerName", "defaultPrompt"}
    if not isinstance(interface, dict) or set(interface) - interface_fields:
        raise ValueError("Unsupported plugin interface metadata")
    for field, value in interface.items():
        if field == "defaultPrompt":
            if not isinstance(value, list) or not all(isinstance(prompt, str) for prompt in value):
                raise ValueError("Default prompts must be strings")
        elif not isinstance(value, str):
            raise ValueError("Interface metadata fields must be strings")
    return data


def payload():
    """Use the same runtime bytes, hashes and manifest encoding as package_skill."""
    files = list(package_skill.FILES)
    if len(files) != len(set(files)):
        raise ValueError("Duplicate runtime allowlist paths")
    runtime = {name: source_bytes(name) for name in files}
    manifest = {"name": package_skill.NAME, "schema_version": 1,
                "files": {name: package_skill.digest(data) for name, data in runtime.items()}}
    members = {"plugin.json": plugin_manifest_bytes()}
    members.update({SKILL_PREFIX + name: data for name, data in runtime.items()})
    members[SKILL_PREFIX + "package-manifest.json"] = json.dumps(manifest, indent=2).encode("utf-8")
    return members, manifest


def build(output, directory=None):
    """Create new outputs only; the optional folder is generated from source bytes."""
    output = fresh_path(output)
    directory = fresh_path(directory) if directory is not None else None
    if directory is not None and (output == directory or output.is_relative_to(directory) or directory.is_relative_to(output)):
        raise ValueError("Package and directory outputs must be separate paths")
    members, manifest = payload()
    output.parent.mkdir(parents=True, exist_ok=True)
    fresh_path(output)
    with output.open("xb") as stream, zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    if directory is not None:
        fresh_path(directory)
        directory.mkdir(parents=True, exist_ok=False)
        for name, data in members.items():
            target = directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            fresh_path(target)
            with target.open("xb") as stream:
                stream.write(data)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Fresh portable plugin ZIP filename")
    parser.add_argument("--directory", help="Also generate a fresh plugin folder for local testing")
    args = parser.parse_args()
    try:
        manifest = build(args.output, args.directory)
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps({"package": str(Path(args.output).resolve()), "file_count": len(manifest["files"]),
                      "bytes": Path(args.output).stat().st_size,
                      "directory": str(Path(args.directory).resolve()) if args.directory else None}))


if __name__ == "__main__":
    main()
