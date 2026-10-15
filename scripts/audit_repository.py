"""Check tracked text, links and package content before sharing or committing."""
import argparse
import json
from pathlib import Path
import posixpath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
HTML_LINK = re.compile(r'''(?<![\w:-])(?:href|src|srcset)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.IGNORECASE)
SECRETS = [re.compile(pattern) for pattern in (
    r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[A-Z0-9]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
PRIVATE_PREFIXES = ("assets/", "analysis/", "local/", "interviews/", "dist/", "docs/local/")
REVIEWED_README_ICON_ASSETS = frozenset({
    "assets/icons/LICENSE",
    "assets/icons/arrow-down.svg",
    "assets/icons/book-open.svg",
    "assets/icons/chart-no-axes-combined.svg",
    "assets/icons/compass.svg",
    "assets/icons/files.svg",
    "assets/icons/languages.svg",
    "assets/icons/package-check.svg",
    "assets/icons/shield-check.svg",
    "assets/icons/square-terminal.svg",
    "assets/icons/users-round.svg",
})
RESEARCH_SUFFIXES = {".pptx", ".ppt", ".key", ".pdf", ".xlsx", ".csv", ".tsv", ".parquet", ".png", ".zip"}
PRIVATE_FIELDS = {"confirmation", "revision_history", "name_zh", "render_path"}
LOCALIZED_READMES = frozenset({"README.zh-CN.md", "README.ja.md", "README.ko.md"})
README_LANGUAGE_NAMES = "**English, \u7b80\u4f53\u4e2d\u6587, \u65e5\u672c\u8a9e, and \ud55c\uad6d\uc5b4**"
LANGUAGE_NAVIGATION = (
    "<!-- language-navigation -->\n"
    '<p align="center">\n'
    '  <a href="README.md" lang="en">English</a> &nbsp;\u00b7&nbsp;\n'
    '  <a href="README.zh-CN.md" lang="zh-CN">\u7b80\u4f53\u4e2d\u6587</a> &nbsp;\u00b7&nbsp;\n'
    '  <a href="README.ja.md" lang="ja">\u65e5\u672c\u8a9e</a> &nbsp;\u00b7&nbsp;\n'
    '  <a href="README.ko.md" lang="ko">\ud55c\uad6d\uc5b4</a>\n'
    "</p>\n"
    "<!-- /language-navigation -->"
)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from keys(child)


def audit(staged=False):
    args = ["ls-files", "-z", "--cached"]
    if not staged:
        args += ["--others", "--exclude-standard"]
    names = sorted(set(n for n in git(*args).decode().split("\x00") if n))
    available = set(names)
    findings = []
    checked = 0
    for name in names:
        path = ROOT / name
        if ((name.startswith(PRIVATE_PREFIXES) and name not in REVIEWED_README_ICON_ASSETS)
                or path.suffix.lower() in RESEARCH_SUFFIXES
                or any(part.lower().endswith(".key") for part in Path(name).parts)):
            findings.append({"file": name, "issue": "private_or_generated_material"})
        data = git("show", ":" + name) if staged else path.read_bytes()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            findings.append({"file": name, "issue": "unexpected_binary"})
            continue
        checked += 1
        language_text = text
        if name == "README.md":
            # Permit only the exact navigation and one approved language-name list.
            language_text = text.replace("\r\n", "\n").replace(LANGUAGE_NAVIGATION, "", 1).replace(README_LANGUAGE_NAMES, "", 1)
        if name not in LOCALIZED_READMES and CJK.search(language_text):
            findings.append({"file": name, "issue": "non_English_script"})
        if any(pattern.search(text) for pattern in SECRETS):
            findings.append({"file": name, "issue": "credential_pattern"})
        if path.suffix == ".json" and PRIVATE_FIELDS.intersection(keys(json.loads(text))):
            findings.append({"file": name, "issue": "private_provenance_fields"})
        if path.suffix == ".md":
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
            links += [next((value for value in match if value), "") for match in HTML_LINK.findall(text)]
            for target in links:
                target = target.strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z]+:", target):
                    continue
                if staged:
                    # Resolve index paths without consulting working-tree files or links.
                    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                    missing = target.startswith("/") or resolved == ".." or resolved.startswith("../") or resolved not in available
                else:
                    resolved = (path.parent / target).resolve()
                    missing = not resolved.is_relative_to(ROOT) or resolved.relative_to(ROOT).as_posix() not in available
                if missing:
                    findings.append({"file": name, "issue": "untracked_or_missing_link", "target": target})
    return {"status": "passed" if not findings else "failed", "files_checked": checked, "findings": findings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="Read the exact Git index rather than working files")
    args = parser.parse_args()
    result = audit(args.staged)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)
