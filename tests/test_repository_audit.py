"""Exercise repository language, privacy and link checks without a real Git index."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("repository_audit", ROOT / "scripts/audit_repository.py")
repository_audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(repository_audit)


class RepositoryAuditTests(unittest.TestCase):
    def fixture(self, working_files, *, index_files=None, staged=False):
        """Supply separate working files and index bytes through mocked Git calls."""
        index_files = working_files if index_files is None else index_files
        calls = []

        def encoded(content):
            return content.encode("utf-8") if isinstance(content, str) else content

        def fake_git(*args):
            calls.append(args)
            if args == ("ls-files", "-z", "--cached"):
                names = set(index_files)
            elif args == ("ls-files", "-z", "--cached", "--others", "--exclude-standard"):
                names = set(index_files) | set(working_files)
            elif len(args) == 2 and args[0] == "show" and args[1].startswith(":"):
                return encoded(index_files[args[1][1:]])
            else:
                raise AssertionError(f"Unexpected Git call: {args}")
            return ("\x00".join(sorted(names)) + "\x00").encode("utf-8")

        with tempfile.TemporaryDirectory(prefix="palate-repository-audit-") as temporary:
            root = Path(temporary).resolve()
            for name, content in working_files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(encoded(content))
            with patch.object(repository_audit, "ROOT", root), patch.object(repository_audit, "git", side_effect=fake_git):
                result = repository_audit.audit(staged=staged)
        return result, calls

    def readmes(self):
        nav = repository_audit.LANGUAGE_NAVIGATION
        return {
            "README.md": nav + "\n\nEnglish project documentation.\n",
            "README.zh-CN.md": nav + "\n\n# \u7b80\u4f53\u4e2d\u6587\n",
            "README.ja.md": nav + "\n\n# \u65e5\u672c\u8a9e\n",
            "README.ko.md": nav + "\n\n# \ud55c\uad6d\uc5b4\n",
        }

    def issues(self, result, name):
        return {finding["issue"] for finding in result["findings"] if finding["file"] == name}

    def test_all_root_locales_and_canonical_navigation_are_allowed(self):
        result, calls = self.fixture(self.readmes())
        self.assertEqual(result["status"], "passed", result)
        self.assertEqual(result["files_checked"], 4)
        self.assertEqual(calls, [("ls-files", "-z", "--cached", "--others", "--exclude-standard")])

    def test_canonical_navigation_accepts_windows_line_endings(self):
        files = self.readmes()
        files["README.md"] = files["README.md"].replace("\n", "\r\n")
        result, _ = self.fixture(files)
        self.assertEqual(result["status"], "passed", result)

    def test_approved_language_names_are_allowed_in_the_english_readme(self):
        for staged in (False, True):
            for newline in ("\n", "\r\n"):
                with self.subTest(staged=staged, newline=newline):
                    files = self.readmes()
                    files["README.md"] += "\nThis README is available in " + repository_audit.README_LANGUAGE_NAMES + ".\n"
                    files["README.md"] = files["README.md"].replace("\n", newline)
                    result, _ = self.fixture(files, staged=staged)
                    self.assertEqual(result["status"], "passed", result)

    def test_language_name_exception_rejects_extra_text_duplicates_and_other_paths(self):
        names = repository_audit.README_LANGUAGE_NAMES
        for text in (names + " \u79d1\u7814\u7b14\u8bb0", names + "\n" + names, names.replace("English", "English edition")):
            with self.subTest(text=text):
                result, _ = self.fixture({"README.md": text})
                self.assertIn("non_English_script", self.issues(result, "README.md"))
        for path in ("SKILL.md", "references/guide.md", "docs/README.md"):
            with self.subTest(path=path):
                result, _ = self.fixture({path: names})
                self.assertIn("non_English_script", self.issues(result, path))

    def test_language_name_exception_keeps_credentials_and_links_checked(self):
        text = repository_audit.README_LANGUAGE_NAMES + "\n" + "ghp_" + "x" * 24 + '\n<a href="missing.md">Guide</a>\n'
        result, _ = self.fixture({"README.md": text})
        self.assertEqual(self.issues(result, "README.md"), {"credential_pattern", "untracked_or_missing_link"})

    def test_cjk_outside_canonical_navigation_is_rejected(self):
        files = self.readmes()
        files["README.md"] += "\n\u4e2d\u6587 outside the navigation.\n"
        result, _ = self.fixture(files)
        self.assertIn("non_English_script", self.issues(result, "README.md"))

    def test_modified_navigation_is_not_an_exception(self):
        nav = repository_audit.LANGUAGE_NAVIGATION
        variations = (
            nav.replace('lang="zh-CN"', 'lang="zh"'),
            nav.replace("</p>", "  <span>\u4e2d\u6587</span>\n</p>"),
            nav.replace("English</a>", "English edition</a>"),
        )
        for changed in variations:
            with self.subTest(navigation=changed):
                files = self.readmes()
                files["README.md"] = changed
                result, _ = self.fixture(files)
                self.assertIn("non_English_script", self.issues(result, "README.md"))

    def test_canonical_navigation_is_exempted_only_once(self):
        files = self.readmes()
        files["README.md"] += "\n" + repository_audit.LANGUAGE_NAVIGATION
        result, _ = self.fixture(files)
        self.assertIn("non_English_script", self.issues(result, "README.md"))

    def test_other_paths_cannot_claim_the_language_exception(self):
        for name in ("docs/README.ko.md", "README.zh-TW.md", "README.ZH-CN.md", "SKILL.md", "scripts/example.py"):
            with self.subTest(path=name):
                result, _ = self.fixture({name: "# \u4e2d\u6587\n"})
                self.assertIn("non_English_script", self.issues(result, name))

    def test_credentials_are_rejected_in_every_localized_readme(self):
        for name in sorted(repository_audit.LOCALIZED_READMES):
            with self.subTest(path=name):
                token = "ghp_" + "x" * 24
                result, _ = self.fixture({name: "# \u4e2d\u6587\n" + token})
                self.assertEqual(self.issues(result, name), {"credential_pattern"})

    def test_localized_readmes_still_check_links_and_private_material(self):
        files = {
            "README.ko.md": '# \ud55c\uad6d\uc5b4\n<a href="missing.md">Guide</a>\n[Notes](analysis/notes.md)\n',
            "analysis/notes.md": "Synthetic private task notes.\n",
        }
        result, _ = self.fixture(files)
        self.assertEqual(self.issues(result, "README.ko.md"), {"untracked_or_missing_link"})
        self.assertEqual(self.issues(result, "analysis/notes.md"), {"private_or_generated_material"})

    def test_localized_readmes_still_reject_unexpected_binary(self):
        result, _ = self.fixture({"README.ja.md": b"\xff\xfe\x00"})
        self.assertEqual(self.issues(result, "README.ja.md"), {"unexpected_binary"})

    def test_exact_reviewed_readme_icon_assets_are_allowed(self):
        files = {
            "assets/icons/LICENSE": "Synthetic English license.\n",
            "assets/icons/align-left.svg": "<svg/>\n",
            "assets/icons/arrow-down.svg": "<svg/>\n",
            "assets/icons/book-open.svg": "<svg/>\n",
            "assets/icons/compass.svg": "<svg/>\n",
            "assets/icons/files.svg": "<svg/>\n",
            "assets/icons/git-branch.svg": "<svg/>\n",
            "assets/icons/languages.svg": "<svg/>\n",
            "assets/icons/palette.svg": "<svg/>\n",
            "assets/icons/square-terminal.svg": "<svg/>\n",
            "assets/icons/users-round.svg": "<svg/>\n",
        }
        self.assertIsInstance(repository_audit.REVIEWED_README_ICON_ASSETS, frozenset)
        self.assertEqual(repository_audit.REVIEWED_README_ICON_ASSETS, frozenset(files))
        files["README.md"] = "\n".join(f'<img src="{name}">' for name in files)
        for staged in (False, True):
            with self.subTest(staged=staged):
                result, _ = self.fixture(files, staged=staged)
                self.assertEqual(result["status"], "passed", result)
                self.assertEqual(result["files_checked"], 12)

    def test_unreviewed_icon_siblings_and_research_assets_are_rejected(self):
        files = {name: "Synthetic unreviewed material.\n" for name in (
            "assets/icons/unreviewed.svg",
            "assets/icons/arrow-down.svg.bak",
            "assets/icons/ARROW-DOWN.svg",
            "assets/icons/nested/arrow-down.svg",
            "assets/research.svg",
            "assets/icons/research.pdf",
            "assets/icons/research.png",
            "assets/icons/deck.key/notes.svg",
            "assets/slide-icons/unreviewed.svg",
            "assets/slide-icons/sun.svg.bak",
            "assets/slide-icons/SUN.svg",
            "assets/slide-icons/nested/sun.svg",
            "assets/slide-icons/research.pdf",
            "assets/slide-icons/research.png",
            "assets/slide-icons/deck.key/notes.svg",
            "docs/research.pdf",
            "docs/deck.key/notes.svg",
        )}
        for staged in (False, True):
            result, _ = self.fixture(files, staged=staged)
            for name in files:
                with self.subTest(path=name, staged=staged):
                    self.assertEqual(self.issues(result, name), {"private_or_generated_material"})

    def test_exact_reviewed_slide_icons_and_notices_are_allowed(self):
        filenames = {
            "LICENSE", "NOTICE.md", "sun.svg", "solar-panel.svg",
            "battery-charging.svg", "house.svg", "factory.svg", "network.svg",
            "boxes.svg", "cpu.svg", "cloud-rain.svg", "wheat.svg",
            "coins.svg", "sliders-horizontal.svg", "dna.svg", "microscope.svg",
        }
        reviewed = frozenset("assets/slide-icons/" + name for name in filenames)
        self.assertIsInstance(repository_audit.REVIEWED_SLIDE_ICON_ASSETS, frozenset)
        self.assertEqual(repository_audit.REVIEWED_SLIDE_ICON_ASSETS, reviewed)
        self.assertTrue(reviewed.isdisjoint(repository_audit.REVIEWED_README_ICON_ASSETS))
        files = {name: "Synthetic English asset.\n" for name in reviewed}
        for staged in (False, True):
            with self.subTest(staged=staged):
                result, _ = self.fixture(files, staged=staged)
                self.assertEqual(result["status"], "passed", result)
                self.assertEqual(result["files_checked"], 16)

    def test_reviewed_asset_exception_keeps_research_suffix_and_key_directory_checks(self):
        files = {
            "assets/icons/research.pdf": "Synthetic research material.\n",
            "assets/icons/deck.key/notes.svg": "<svg/>\n",
        }
        reviewed = repository_audit.REVIEWED_README_ICON_ASSETS | frozenset(files)
        with patch.object(repository_audit, "REVIEWED_README_ICON_ASSETS", reviewed):
            result, _ = self.fixture(files)
        for name in files:
            with self.subTest(path=name):
                self.assertEqual(self.issues(result, name), {"private_or_generated_material"})

    def test_reviewed_icon_assets_still_reject_credentials_binary_and_non_english_text(self):
        cases = (
            ("ghp_" + "x" * 24, "credential_pattern"),
            (b"\xff\xfe\x00", "unexpected_binary"),
            ("<svg><title>\u4e2d\u6587</title></svg>\n", "non_English_script"),
        )
        for name in sorted(repository_audit.REVIEWED_README_ICON_ASSETS | repository_audit.REVIEWED_SLIDE_ICON_ASSETS):
            for content, issue in cases:
                with self.subTest(path=name, issue=issue):
                    result, _ = self.fixture({name: content})
                    self.assertEqual(self.issues(result, name), {issue})

    def test_markdown_href_src_and_srcset_links_are_preserved(self):
        files = {
            "README.md": '[Guide](docs/guide.md#details)\n<a href="docs/guide.md">Guide</a>\n<a href=docs/guide.md>Guide</a>\n<img src=\'docs/media/light.svg\'>\n<SOURCE SRCSET = "docs/media/dark.svg">\n',
            "docs/guide.md": "# Guide\n[Home](../README.md)\n",
            "docs/media/light.svg": "<svg/>\n",
            "docs/media/dark.svg": "<svg/>\n",
        }
        result, _ = self.fixture(files)
        self.assertEqual(result["status"], "passed", result)

    def test_canonical_navigation_reports_missing_html_target(self):
        files = self.readmes()
        del files["README.ja.md"]
        result, _ = self.fixture(files)
        self.assertIn({"file": "README.md", "issue": "untracked_or_missing_link", "target": "README.ja.md"}, result["findings"])
        self.assertNotIn("non_English_script", self.issues(result, "README.md"))

    def test_unquoted_html_href_is_checked(self):
        result, _ = self.fixture({"README.md": "<a href=missing.md>Guide</a>\n"})
        self.assertIn({"file": "README.md", "issue": "untracked_or_missing_link", "target": "missing.md"}, result["findings"])

    def test_links_outside_the_repository_are_rejected(self):
        for target in ("../outside.md", "/outside.md"):
            with self.subTest(target=target):
                result, _ = self.fixture({"README.md": f'<a href="{target}">Outside</a>\n'})
                self.assertEqual(self.issues(result, "README.md"), {"untracked_or_missing_link"})

    def test_working_tree_links_keep_physical_containment_checks(self):
        files = {"README.md": '<a href="docs/guide.md">Guide</a>\n', "docs/guide.md": "Synthetic guide.\n"}
        original_resolve = Path.resolve

        def resolve(path, *args, **kwargs):
            if path.name == "guide.md":
                return path.parents[2] / "outside-guide.md"
            return original_resolve(path, *args, **kwargs)

        with patch.object(Path, "resolve", resolve):
            result, _ = self.fixture(files)
        self.assertEqual(self.issues(result, "README.md"), {"untracked_or_missing_link"})

    def test_staged_audit_uses_index_bytes_and_ignores_untracked_files(self):
        index = self.readmes()
        working = dict(index)
        working["README.md"] += "\n\u4e2d\u6587 working-tree-only addition.\n"
        working["untracked.md"] = "\u4e2d\u6587\n"
        result, calls = self.fixture(working, index_files=index, staged=True)
        self.assertEqual(result["status"], "passed", result)
        self.assertEqual(result["files_checked"], 4)
        self.assertEqual(calls[0], ("ls-files", "-z", "--cached"))
        self.assertEqual(set(calls[1:]), {("show", ":" + name) for name in index})

    def test_staged_audit_rejects_index_content_even_when_working_copy_is_clean(self):
        index = {"README.md": "\u4e2d\u6587 index-only text.\n"}
        result, _ = self.fixture({"README.md": "English working-tree text.\n"}, index_files=index, staged=True)
        self.assertEqual(self.issues(result, "README.md"), {"non_English_script"})

    def test_reviewed_closing_backgrounds_pass_in_working_and_staged_audits(self):
        files = {name: (ROOT / name).read_bytes()
                 for name in repository_audit.REVIEWED_CLOSING_BACKGROUNDS}
        files["assets/closing-backgrounds/NOTICE.md"] = "Approved generated backgrounds.\n"
        for staged in (False, True):
            with self.subTest(staged=staged):
                result, _ = self.fixture(files, staged=staged)
                self.assertEqual(result["status"], "passed", result)

    def test_changed_background_bytes_need_a_new_review(self):
        name = "assets/closing-backgrounds/coastal-panorama.png"
        original = (ROOT / name).read_bytes()
        result, _ = self.fixture({name: original + b"unreviewed"})
        self.assertIn("unreviewed_closing_background_bytes", self.issues(result, name))
        result, _ = self.fixture({name: original}, index_files={name: b"different-index-image"}, staged=True)
        self.assertIn("unreviewed_closing_background_bytes", self.issues(result, name))

    def test_closing_asset_exception_does_not_allow_other_images_or_reference_decks(self):
        image = (ROOT / "assets/closing-backgrounds/coastal-panorama.png").read_bytes()
        files = {"assets/closing-backgrounds/unreviewed.png": image,
                 "assets/closure_slide/reference.pptx": b"private reference"}
        result, _ = self.fixture(files)
        for name in files:
            self.assertIn("private_or_generated_material", self.issues(result, name))

    def test_staged_links_are_resolved_against_index_names_only(self):
        index = {"README.md": '<a href="working-only.md">Guide</a>\n'}
        working = dict(index, **{"working-only.md": "Untracked guide.\n"})
        result, _ = self.fixture(working, index_files=index, staged=True)
        self.assertIn({"file": "README.md", "issue": "untracked_or_missing_link", "target": "working-only.md"}, result["findings"])

    def test_staged_links_do_not_consult_working_tree_resolution(self):
        index = {"README.md": '<a href="docs/guide.md">Guide</a>\n', "docs/guide.md": "Index-only guide.\n"}
        with patch.object(Path, "resolve", side_effect=AssertionError("Working-tree resolution is not index evidence")):
            with tempfile.TemporaryDirectory(prefix="palate-repository-audit-") as temporary:
                root = Path(temporary)

                def fake_git(*args):
                    if args == ("ls-files", "-z", "--cached"):
                        return ("\x00".join(index) + "\x00").encode()
                    if len(args) == 2 and args[0] == "show":
                        return index[args[1][1:]].encode()
                    raise AssertionError(f"Unexpected Git call: {args}")

                with patch.object(repository_audit, "ROOT", root), patch.object(repository_audit, "git", side_effect=fake_git):
                    result = repository_audit.audit(staged=True)
        self.assertEqual(result["status"], "passed", result)


if __name__ == "__main__":
    unittest.main()
