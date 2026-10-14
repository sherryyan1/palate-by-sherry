"""Check tracked text, links and package content before sharing or committing."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
SECRETS = [re.compile(pattern) for pattern in (
    r"gh[pousr]_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"AKIA[A-Z0-9]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")]
PRIVATE_PREFIXES = ("assets/", "analysis/", "local/", "interviews/", "dist/", "docs/local/")
RESEARCH_SUFFIXES = {".pptx", ".ppt", ".key", ".pdf", ".xlsx", ".csv", ".tsv", ".parquet", ".png", ".zip"}
PRIVATE_FIELDS = {"confirmation", "revision_history", "name_zh", "render_path"}


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
        if (name.startswith(PRIVATE_PREFIXES) or path.suffix.lower() in RESEARCH_SUFFIXES
                or any(part.lower().endswith(".key") for part in Path(name).parts)):
            findings.append({"file": name, "issue": "private_or_generated_material"})
        data = git("show", ":" + name) if staged else path.read_bytes()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            findings.append({"file": name, "issue": "unexpected_binary"})
            continue
        checked += 1
        if CJK.search(text):
            findings.append({"file": name, "issue": "non_English_script"})
        if any(pattern.search(text) for pattern in SECRETS):
            findings.append({"file": name, "issue": "credential_pattern"})
        if path.suffix == ".json" and PRIVATE_FIELDS.intersection(keys(json.loads(text))):
            findings.append({"file": name, "issue": "private_provenance_fields"})
        if path.suffix == ".md":
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
            links += re.findall(r'(?:src|srcset)="([^"]+)"', text)
            for target in links:
                target = target.strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z]+:", target):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.is_relative_to(ROOT) or resolved.relative_to(ROOT).as_posix() not in available:
                    findings.append({"file": name, "issue": "untracked_or_missing_link", "target": target})
    return {"status": "passed" if not findings else "failed", "files_checked": checked, "findings": findings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="Read the exact Git index rather than working files")
    args = parser.parse_args()
    result = audit(args.staged)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)
