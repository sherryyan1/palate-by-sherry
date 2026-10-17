"""Crop explicitly reviewed panel boxes without resizing or reconstructing data.

CLI: --source IMAGE --plan PLAN.json --output-dir NEW_DIRECTORY
The strict version-1 plan contains source_sha256 and panels records with id,
source_panel and box [left, top, right, bottom]. Coordinates refer to raw decoded
pixels, use half-open bounds, and do not apply EXIF rotation. Static PNG, JPEG,
TIFF and WebP inputs are supported when their decoded mode is PNG-preservable.
Outputs are private PNG crops and an extraction manifest, not reviewed science
or native editable figure interiors. Review panel identity and shared context
before placing the crops in a slide. No automatic panel detection is performed.
"""

import argparse
from contextlib import contextmanager
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import warnings

from PIL import Image


MAX_SOURCE_BYTES = 256 * 1024 * 1024
MAX_PLAN_BYTES = 1024 * 1024
MAX_SOURCE_PIXELS = 64_000_000
MAX_TOTAL_CROP_PIXELS = 64_000_000
MAX_PANELS = 64
FORMATS = {"PNG", "JPEG", "TIFF", "WEBP"}
PNG_MODES = {"1", "L", "LA", "P", "RGB", "RGBA", "I;16"}
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    prefix + str(number) for prefix in ("COM", "LPT") for number in range(1, 10)
}
MANIFEST_NAME = "extraction-manifest.json"


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _absolute_path(value):
    path = Path(value).expanduser()
    if ".." in path.parts:
        raise ValueError("Paths must not contain parent-directory traversal components")
    return Path(os.path.abspath(path))


def _reject_links(path):
    """Reject existing symlinks and Windows reparse points in the whole path."""
    for part in reversed((path, *path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        ):
            raise ValueError("Symlink and reparse-point paths are not supported")


def _read_regular_file(path, limit):
    _reject_links(path)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("Inputs must be regular files without hard links")
        if info.st_size > limit:
            raise ValueError("Input exceeds the supported file size")
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Input exceeds the supported file size")
    return data


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON keys are not allowed")
        result[key] = value
    return result


def _validate_plan(data, source_hash, size):
    try:
        plan = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("The plan must be valid UTF-8 JSON") from error
    if not isinstance(plan, dict) or set(plan) != {"schema_version", "source_sha256", "panels"}:
        raise ValueError("Plan fields must be schema_version, source_sha256 and panels")
    if type(plan["schema_version"]) is not int or plan["schema_version"] != 1:
        raise ValueError("Only schema_version 1 is supported")
    checksum = plan["source_sha256"]
    if not isinstance(checksum, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", checksum):
        raise ValueError("source_sha256 must be a SHA-256 hexadecimal digest")
    if checksum.lower() != source_hash:
        raise ValueError("Source hash does not match the reviewed plan")
    panels = plan["panels"]
    if not isinstance(panels, list) or not 1 <= len(panels) <= MAX_PANELS:
        raise ValueError(f"The plan must contain between 1 and {MAX_PANELS} panels")
    identifiers = set()
    total_pixels = 0
    for panel in panels:
        if not isinstance(panel, dict) or set(panel) != {"id", "source_panel", "box"}:
            raise ValueError("Panel fields must be id, source_panel and box")
        identifier = panel["id"]
        if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier):
            raise ValueError("Panel IDs must be 1-64 filename-safe ASCII letters, digits, underscores or hyphens")
        if identifier.upper() in RESERVED_NAMES or identifier.casefold() in identifiers:
            raise ValueError("Panel IDs must be unique without case collisions or reserved device names")
        identifiers.add(identifier.casefold())
        identity = panel["source_panel"]
        if not isinstance(identity, str) or not identity.strip() or len(identity) > 200 or any(
            ord(character) < 32 or ord(character) == 127 for character in identity
        ):
            raise ValueError("source_panel must be a nonempty identity of at most 200 characters without controls")
        box = panel["box"]
        if not isinstance(box, list) or len(box) != 4 or any(type(value) is not int for value in box):
            raise ValueError("Each box must contain four integer pixel coordinates")
        left, top, right, bottom = box
        if not (0 <= left < right <= size[0] and 0 <= top < bottom <= size[1]):
            raise ValueError("Panel boxes must have positive area and stay within the source pixels")
        total_pixels += (right - left) * (bottom - top)
    if total_pixels > MAX_TOTAL_CROP_PIXELS:
        raise ValueError("The combined crop area exceeds the supported pixel budget")
    return panels


def _identity(path):
    info = path.lstat()
    return info.st_dev, info.st_ino


@contextmanager
def _directory_guard(path, expected_identity):
    """Hold the destination against replacement during file creation."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        create = kernel.CreateFileW
        create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        create.restype = wintypes.HANDLE
        close = kernel.CloseHandle
        close.argtypes = [wintypes.HANDLE]
        close.restype = wintypes.BOOL
        # READ_ATTRIBUTES, share read/write but not deletion, OPEN_EXISTING,
        # BACKUP_SEMANTICS | OPEN_REPARSE_POINT: this holds a directory handle
        # without following a substituted reparse point or allowing a rename.
        handle = create(str(path), 0x80, 0x3, None, 3, 0x02200000, None)
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            _reject_links(path)
            if _identity(path) != expected_identity:
                raise OSError("Output directory changed during extraction")
            yield None
        finally:
            close(handle)
    else:
        descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            info = os.fstat(descriptor)
            if (info.st_dev, info.st_ino) != expected_identity:
                raise OSError("Output directory changed during extraction")
            yield descriptor
        finally:
            os.close(descriptor)


def _write_new(path, data, owned, directory_fd=None):
    # Exclusive creation prevents a competing file from being overwritten.
    _reject_links(path.parent)
    if directory_fd is None:
        handle = path.open("xb")
    else:
        descriptor = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory_fd)
        handle = os.fdopen(descriptor, "wb")
    with handle:
        info = os.fstat(handle.fileno())
        owned.append((path, (info.st_dev, info.st_ino)))
        handle.write(data)


def extract(source, plan_path, output_dir):
    """Return the manifest after exporting reviewed boxes to a fresh directory.

    Validation and PNG encoding finish before output creation. An existing
    destination is never reused. Failed writes remove only this run's files
    whose identities still match, leaving competing files untouched.
    """
    source = _absolute_path(source)
    plan_path = _absolute_path(plan_path)
    output_dir = _absolute_path(output_dir)
    _reject_links(output_dir)
    if output_dir.exists():
        raise FileExistsError("Output directory must not already exist")
    if not output_dir.parent.is_dir():
        raise ValueError("The output parent directory must already exist")
    if source.is_relative_to(output_dir) or plan_path.is_relative_to(output_dir):
        raise ValueError("Inputs must not be inside the output directory")
    source_data = _read_regular_file(source, MAX_SOURCE_BYTES)
    plan_data = _read_regular_file(plan_path, MAX_PLAN_BYTES)
    source_hash = _sha256(source_data)
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(BytesIO(source_data)) as image:
            if image.format not in FORMATS:
                raise ValueError("Source format must be PNG, JPEG, TIFF or WebP")
            if getattr(image, "n_frames", 1) != 1 or getattr(image, "is_animated", False):
                raise ValueError("Animated and multipage images require an explicitly selected static source")
            if image.width * image.height > MAX_SOURCE_PIXELS:
                raise ValueError("Source exceeds the supported pixel budget")
            if image.mode not in PNG_MODES:
                raise ValueError(f"Decoded mode {image.mode!r} cannot be exported without color conversion")
            panels = _validate_plan(plan_data, source_hash, image.size)
            image.load()
            source_info = {
                "filename": source.name, "sha256": source_hash, "format": image.format,
                "width": image.width, "height": image.height, "mode": image.mode,
            }
            outputs = []
            entries = []
            for panel in panels:
                cropped = image.crop(tuple(panel["box"]))
                # Crops use raw coordinates; copied EXIF orientation would make
                # some slide applications rotate them a second time on import.
                cropped.info.clear()
                buffer = BytesIO()
                options = {key: image.info[key] for key in ("icc_profile", "transparency") if key in image.info}
                cropped.save(buffer, format="PNG", **options)
                png = buffer.getvalue()
                filename = panel["id"] + ".png"
                outputs.append((filename, png))
                entries.append({
                    **panel, "file": filename, "sha256": _sha256(png),
                    "semantic_crop_review": "pending",
                    "native_editability": "raster interior is not native editable",
                })
    manifest = {
        "schema_version": 1, "source": source_info,
        "coordinate_system": "half-open raw decoded pixel bounds; no EXIF rotation",
        "pixel_transform": "crop only; no resize, color conversion or data reconstruction",
        "semantic_review": "pending: verify panel identity, labels, axes, legends, shared context and source attribution",
        "panels": entries,
    }
    outputs.append((MANIFEST_NAME, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")))
    # Recheck immediately before the one directory mutation. mkdir also refuses
    # a directory created by another process after preflight validation.
    _reject_links(output_dir)
    output_dir.mkdir(mode=0o700)
    directory_identity = _identity(output_dir)
    owned = []
    try:
        with _directory_guard(output_dir, directory_identity) as directory_fd:
            try:
                for filename, data in outputs:
                    if _identity(output_dir) != directory_identity:
                        raise OSError("Output directory changed during extraction")
                    _write_new(output_dir / filename, data, owned, directory_fd)
            except BaseException:
                # Clean up while the directory handle still protects the path.
                _reject_links(output_dir)
                if _identity(output_dir) == directory_identity:
                    for path, identity in reversed(owned):
                        if path.exists() and _identity(path) == identity:
                            path.unlink()
                raise
    except BaseException:
        # Never recursively delete: a competing process may have added content.
        try:
            _reject_links(output_dir)
            if _identity(output_dir) == directory_identity:
                output_dir.rmdir()
        except (OSError, ValueError):
            pass
        raise
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = extract(args.source, args.plan, args.output_dir)
    except (OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        parser.error(str(error))
    print(json.dumps({"output_dir": str(args.output_dir), "panels": len(manifest["panels"]), "semantic_crop_review": "pending"}))


if __name__ == "__main__":
    main()
