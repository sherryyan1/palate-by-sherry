"""Verify portable plugin boundaries and parity with the canonical Codex package."""
import importlib.util
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP = ROOT / "analysis/local-only/test-temp"
SPEC = importlib.util.spec_from_file_location("package_plugin", ROOT / "scripts/package_plugin.py")
plugin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plugin)
SKILL_PREFIX = "skills/palate/"


class PackagePluginTests(unittest.TestCase):
    def setUp(self):
        TEST_TEMP.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="palate-plugin-test-", dir=TEST_TEMP)
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)

    def archive_members(self, path):
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), len(set(names)), "Duplicate ZIP members")
            return {name: archive.read(name) for name in names}

    def expected_names(self):
        return {"plugin.json", SKILL_PREFIX + "package-manifest.json"} | {
            SKILL_PREFIX + name for name in plugin.package_skill.FILES}

    def source_fixture(self):
        source = self.folder / "source"
        for name in [*plugin.package_skill.FILES, plugin.PLUGIN_MANIFEST]:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        return source

    def directory_link(self, link, target):
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as error:
            if os.name != "nt":
                self.skipTest(f"Directory links unavailable: {error}")
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)],
                                    capture_output=True, text=True)
            if result.returncode:
                self.skipTest("Neither directory symlinks nor Windows junctions are available")
        self.addCleanup(lambda: link.unlink() if link.is_symlink() else link.rmdir())

    def test_runtime_bytes_hashes_and_manifest_match_the_codex_package(self):
        codex_path = self.folder / "codex.zip"
        plugin_path = self.folder / "plugin.zip"
        codex_manifest = plugin.package_skill.build(codex_path)
        plugin_manifest = plugin.build(plugin_path)
        self.assertEqual(plugin_manifest, codex_manifest)
        codex_members = self.archive_members(codex_path)
        plugin_members = self.archive_members(plugin_path)
        self.assertEqual(set(plugin_members), self.expected_names())
        for name in [*plugin.package_skill.FILES, "package-manifest.json"]:
            with self.subTest(name=name):
                self.assertEqual(plugin_members[SKILL_PREFIX + name], codex_members["palate/" + name])
        for name, checksum in plugin_manifest["files"].items():
            self.assertEqual(plugin.package_skill.digest(plugin_members[SKILL_PREFIX + name]), checksum)

    def test_manifest_is_portable_with_one_skill_and_no_servers_or_hooks(self):
        output = self.folder / "plugin.zip"
        plugin.build(output)
        members = self.archive_members(output)
        self.assertEqual(members["plugin.json"], (ROOT / plugin.PLUGIN_MANIFEST).read_bytes())
        manifest = json.loads(members["plugin.json"])
        self.assertEqual(manifest["$schema"], plugin.PLUGIN_SCHEMA)
        self.assertEqual(manifest["name"], "palate")
        self.assertEqual(manifest["version"], "0.1.0-alpha.1")
        self.assertEqual(manifest["author"], {"name": "Sherry"})
        self.assertEqual(manifest["repository"], "https://github.com/sherryyan1/palate-by-sherry")
        self.assertEqual(manifest["homepage"], manifest["repository"])
        self.assertEqual(set(manifest), {"$schema", "name", "version", "description", "author", "homepage", "repository", "extensions"})
        self.assertIn("PowerPoint", manifest["description"])
        self.assertIn("Keynote", manifest["description"])
        self.assertEqual(manifest["extensions"], {"com.openai": {"interface": {
            "displayName": "palate by Sherry",
            "shortDescription": "Research presentations from slides, notes or papers.",
            "developerName": "Sherry",
            "defaultPrompt": ["Use palate to prepare my research presentation."],
        }}})
        self.assertEqual({name.split("/")[1] for name in members if name.startswith("skills/")}, {"palate"})
        self.assertEqual({name for name in members if name.endswith("/SKILL.md")}, {SKILL_PREFIX + "SKILL.md"})
        self.assertTrue(all(name == "plugin.json" or name.startswith(SKILL_PREFIX) for name in members))

    def test_every_relative_runtime_document_link_resolves_inside_the_skill(self):
        output = self.folder / "plugin.zip"
        plugin.build(output)
        members = self.archive_members(output)
        checked = 0
        html_links = re.compile(r'''(?:href|src|srcset)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.IGNORECASE)
        for name, data in members.items():
            if not name.endswith(".md"):
                continue
            text = data.decode("utf-8-sig")
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
            links += [next(value for value in match if value) for match in html_links.findall(text)]
            for target in links:
                parsed = urlsplit(target.strip("<>"))
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                checked += 1
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path)))
                with self.subTest(document=name, link=target):
                    self.assertTrue(resolved.startswith(SKILL_PREFIX), "Link escapes the packaged skill")
                    self.assertIn(resolved, members)
        self.assertGreater(checked, 20, "The runtime link check did not inspect the reference graph")

    def test_private_and_development_neighbors_are_never_copied(self):
        source = self.source_fixture()
        excluded = ["analysis/private-notes.md", "docs/local/private.md", "docs/installation.md",
                    "tests/development.py", "scripts/package_plugin.py", "README.md", ".env",
                    ".git/config", ".agents/plugins/marketplace.json", "assets/research.txt"]
        for name in excluded:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Synthetic development neighbor.\n", encoding="utf-8")
        output = self.folder / "plugin.zip"
        with patch.object(plugin, "ROOT", source):
            plugin.build(output)
        members = self.archive_members(output)
        self.assertEqual(set(members), self.expected_names())
        self.assertTrue(all(SKILL_PREFIX + name not in members for name in excluded))
        self.assertNotIn("packaging/plugin.json", members)

    def test_new_allowlisted_runtime_file_is_used_without_a_second_allowlist(self):
        source = self.source_fixture()
        additional = "references/synthetic-new-runtime.md"
        data = b"Synthetic runtime addition.\n"
        (source / additional).write_bytes(data)
        output = self.folder / "plugin.zip"
        with patch.object(plugin, "ROOT", source), patch.object(plugin.package_skill, "FILES", [*plugin.package_skill.FILES, additional]):
            manifest = plugin.build(output)
        members = self.archive_members(output)
        self.assertEqual(members[SKILL_PREFIX + additional], data)
        self.assertEqual(manifest["files"][additional], plugin.package_skill.digest(data))

    def test_cli_generates_a_fresh_folder_with_the_same_bytes_as_the_zip(self):
        output = self.folder / "nested/plugin.zip"
        directory = self.folder / "generated/plugin"
        result = subprocess.run([sys.executable, str(ROOT / "scripts/package_plugin.py"),
                                 "--output", str(output), "--directory", str(directory)],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["package"], str(output.resolve()))
        self.assertEqual(summary["directory"], str(directory.resolve()))
        self.assertNotIn("installed", summary)
        generated = {path.relative_to(directory).as_posix(): path.read_bytes()
                     for path in directory.rglob("*") if path.is_file()}
        self.assertEqual(generated, self.archive_members(output))

    def test_existing_zip_is_preserved(self):
        output = self.folder / "plugin.zip"
        output.write_bytes(b"existing package")
        with self.assertRaises(ValueError):
            plugin.build(output)
        self.assertEqual(output.read_bytes(), b"existing package")

    def test_existing_directory_is_preserved_before_any_zip_is_created(self):
        directory = self.folder / "plugin"
        directory.mkdir()
        marker = directory / "private.txt"
        marker.write_bytes(b"local edits")
        output = self.folder / "plugin.zip"
        with self.assertRaises(ValueError):
            plugin.build(output, directory)
        self.assertFalse(output.exists())
        self.assertEqual(marker.read_bytes(), b"local edits")
        self.assertEqual(list(directory.iterdir()), [marker])

    def test_overlapping_outputs_are_rejected_before_any_creation(self):
        directory = self.folder / "plugin"
        for output in (directory, directory / "plugin.zip"):
            with self.subTest(output=output), self.assertRaises(ValueError):
                plugin.build(output, directory)
        self.assertFalse(directory.exists())

    def test_linked_output_file_is_never_followed(self):
        target = self.folder / "existing.zip"
        target.write_bytes(b"existing package")
        link = self.folder / "linked.zip"
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest(f"File symlinks unavailable: {error}")
        with self.assertRaises(ValueError):
            plugin.build(link)
        self.assertTrue(link.is_symlink())
        self.assertEqual(target.read_bytes(), b"existing package")

    def test_link_guards_reject_each_output_and_nested_ancestor_before_writing(self):
        # Native link creation requires unavailable privileges in some Windows
        # sandboxes; exercise the filesystem link predicate deterministically too.
        original_is_symlink = Path.is_symlink
        for location in ("archive", "archive-parent", "directory", "directory-parent"):
            case = self.folder / location
            case.mkdir()
            output = case / "nested/plugin.zip"
            directory = case / "generated/plugin"
            linked_path = {"archive": output, "archive-parent": output.parent,
                           "directory": directory, "directory-parent": directory.parent}[location]

            def is_symlink(path):
                return path == linked_path or original_is_symlink(path)

            with self.subTest(location=location), patch.object(Path, "is_symlink", is_symlink):
                with self.assertRaises(ValueError):
                    plugin.build(output, directory)
            self.assertEqual(list(case.iterdir()), [])

    def test_linked_parent_is_rejected_for_both_outputs(self):
        target = self.folder / "target"
        target.mkdir()
        link = self.folder / "linked"
        self.directory_link(link, target)
        self.assertTrue(plugin.linked(link))
        with self.assertRaises(ValueError):
            plugin.build(link / "nested/plugin.zip")
        output = self.folder / "plugin.zip"
        with self.assertRaises(ValueError):
            plugin.build(output, link / "nested/plugin")
        self.assertFalse(output.exists())
        self.assertEqual(list(target.iterdir()), [])

    def test_dangling_output_link_is_rejected(self):
        link = self.folder / "dangling.zip"
        target = self.folder / "missing.zip"
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest(f"File symlinks unavailable: {error}")
        with self.assertRaises(ValueError):
            plugin.build(link)
        self.assertTrue(link.is_symlink())
        self.assertFalse(target.exists())

    def test_non_skill_components_in_manifest_are_rejected_without_outputs(self):
        source = self.source_fixture()
        manifest_path = source / plugin.PLUGIN_MANIFEST
        original = json.loads(manifest_path.read_bytes())
        changes = [dict(original, skills="./skills/"), dict(original, mcpServers={}),
                   dict(original, extensions={"com.openai": {"hooks": "./hooks/hooks.json"}}),
                   dict(original, extensions={"com.openai": {"apps": "./.app.json"}})]
        for index, metadata in enumerate(changes):
            manifest_path.write_text(json.dumps(metadata), encoding="utf-8")
            output = self.folder / f"rejected-{index}.zip"
            with self.subTest(manifest=metadata), patch.object(plugin, "ROOT", source):
                with self.assertRaises(ValueError):
                    plugin.build(output)
                self.assertFalse(output.exists())

    def test_unsafe_allowlist_paths_cannot_include_an_outside_file(self):
        for name in ("../outside.txt", "/outside.txt", "references/../outside.txt", "C:/outside.txt", "references\\outside.txt"):
            output = self.folder / "rejected.zip"
            with self.subTest(name=name), patch.object(plugin.package_skill, "FILES", [name]):
                with self.assertRaises(ValueError):
                    plugin.build(output)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
