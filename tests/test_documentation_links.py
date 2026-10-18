"""Check published Markdown destinations, fragment anchors and runtime package closure.

This scanner handles this repository's ATX headings, inline/reference Markdown
links, HTML ids and asset attributes. It does not claim general Markdown parsing
or browser rendering.
"""

import html
from html.parser import HTMLParser
from pathlib import Path
import re
import tempfile
import unittest
import unicodedata
from urllib.parse import unquote, urlsplit

from scripts import package_skill


ROOT = Path(__file__).resolve().parents[1]
READMES = ('README.md', 'README.zh-CN.md', 'README.ja.md', 'README.ko.md')
# These exact anchors were published before the capability reorganization.
LEGACY_ANCHORS = {
    "references/design-system.md": [
        "01--establish-what-the-audience-needs",
        "02--give-the-evidence-a-readable-structure",
        "03--use-space-and-typography-to-show-relationships",
        "04--give-color-a-consistent-purpose",
        "05--check-the-result-against-the-research",
        "a-visual-ending",
        "choosing-a-text-box-treatment",
        "cover-composition",
        "design-system",
        "grouped-figure-panels-and-country-identifiers",
        "illustration-language-for-introduction-and-methodology",
        "recurring-logos-and-watermarks",
        "research-question-page",
        "table-color-options",
        "text-boxes-and-tables",
        "visual-treatment-for-every-slide",
        "visual-treatment-for-text-heavy-slides"
    ],
    "references/writing-style.md": [
        "develop-the-explanation",
        "localized-entry-points",
        "match-the-form-to-the-information",
        "preserve-the-substance",
        "research-slide-wording",
        "slide-citations-and-references",
        "write-readmes-for-researchers",
        "writing-style"
    ],
    "references/visual-storytelling.md": [
        "build-around-objects-and-relationships",
        "choose-the-illustration-language",
        "choose-what-the-visual-needs-to-explain",
        "close-with-visual-key-takeaways",
        "connect-the-intended-objects",
        "distinguish-a-symbol-from-a-scientific-schematic",
        "frame-a-research-question",
        "give-the-explanation-enough-space",
        "keep-icons-in-a-supporting-role",
        "outline-then-storyboard-then-build",
        "retain-the-substance-of-the-explanation",
        "review-every-slide-as-a-complete-composition",
        "review-the-contribution-then-the-rendering",
        "select-and-construct-assets-deliberately",
        "visual-storytelling"
    ]
}


def prose_only(text):
    """Ignore fenced code and HTML comments, which do not create prose links."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    lines, fence, length = [], None, 0
    for line in text.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            run, rest = marker.groups()
            if fence is None:
                fence, length = run[0], len(run)
                continue
            if run[0] == fence and len(run) >= length and not rest.strip():
                fence = None
                continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.targets = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for attribute in ('href', 'src'):
            if attrs.get(attribute):
                self.targets.append(attrs[attribute])
        if attrs.get('srcset'):
            for item in attrs['srcset'].split(','):
                if item.strip():
                    self.targets.append(item.strip().split()[0])

    handle_startendtag = handle_starttag


def heading_slug(heading):
    # HTML does not contribute its attribute values to a GitHub heading anchor.
    text = re.sub(r'<[^>]*>', '', heading)
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = html.unescape(text).lower()
    # Preserve Unicode letters/numbers/marks, literal spaces, hyphens and underscores.
    # In particular, a nonbreaking space is removed rather than becoming a hyphen.
    text = ''.join(c for c in text if c in ' -_' or unicodedata.category(c)[0] in 'LMN')
    return text.replace(' ', '-')


def anchors(text):
    prose = prose_only(text)
    tags = Tags()
    tags.feed(prose)
    result, seen = set(tags.ids), set()
    for line in prose.splitlines():
        match = re.match(r'^ {0,3}#{1,6}[ \t]+(.+?)(?:[ \t]+#+[ \t]*)?$', line)
        if not match:
            continue
        base = heading_slug(match.group(1))
        slug, counter = base, 0
        while slug in seen:
            counter += 1
            slug = f'{base}-{counter}'
        seen.add(slug)
        result.add(slug)
    return result


def targets(text):
    prose = prose_only(text)
    prose = re.sub(r'(`+).*?\1', '', prose, flags=re.S)
    tags = Tags()
    tags.feed(prose)
    result = list(tags.targets)
    # Destinations here use simple paths or angle brackets; optional titles are ignored.
    inline = r'!?\[(?:[^\[\]\n]|\[[^\]\n]*\])*\]\(\s*(<[^>\n]+>|[^\s)]+)'
    definition = r'^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)'
    result.extend(re.findall(inline, prose))
    result.extend(re.findall(definition, prose, flags=re.M))
    return [html.unescape(target.strip('<>')) for target in result]


def local_destination(source, target, root):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    resolved = (root / path.lstrip('/') if path.startswith('/') else source.parent / path).resolve() if path else source
    if not resolved.is_relative_to(root):
        raise ValueError('Local link escapes the documentation root')
    return resolved, unquote(parsed.fragment)


def inspect_links(source, root=ROOT, allowed=None):
    issues = []
    for target in targets(source.read_text(encoding='utf-8-sig')):
        try:
            local = local_destination(source, target, root)
        except ValueError:
            issues.append((source.relative_to(root).as_posix(), target, 'unsafe_path'))
            continue
        if local is None:
            continue
        path, fragment = local
        issue = None
        if not path.is_file():
            issue = 'missing_file'
        elif allowed is not None and path.relative_to(root).as_posix() not in allowed:
            issue = 'outside_runtime_package'
        elif fragment and path.suffix.lower() == '.md' and fragment not in anchors(path.read_text(encoding='utf-8-sig')):
            issue = 'missing_fragment'
        if issue:
            issues.append((source.relative_to(root).as_posix(), target, issue))
    return issues


class MarkdownScannerTests(unittest.TestCase):
    def test_heading_punctuation_inline_formatting_and_duplicates(self):
        result = anchors('# Title\n## Title\n## Title-1\n## Title\n## 01 | **Use** `x/y`\n')
        self.assertEqual(result, {'title', 'title-1', 'title-1-1', 'title-2', '01--use-xy'})

    def test_html_icon_entities_explicit_ids_and_unicode(self):
        text = ('## <img src="icon.svg" alt="decoration">&nbsp; Sherry\'s Picks\n'
                '<a id="stable-contract"></a>\n## \u7814\u7a76\u95ee\u9898\n')
        self.assertEqual(anchors(text), {'-sherrys-picks', 'stable-contract', '\u7814\u7a76\u95ee\u9898'})

    def test_code_fences_inline_code_and_comments_are_not_links(self):
        text = ('```md\n## False heading\n[ignored](missing.md)\n```\n'
                '~~~\n<a href="also-missing.md">x</a>\n~~~\n'
                '<!-- [comment](no.md) -->\n`[literal](no.md)`\n[real](real.md#part)')
        self.assertEqual(targets(text), ['real.md#part'])
        self.assertNotIn('false-heading', anchors(text))

    def test_html_and_markdown_assets_and_reference_targets(self):
        text = ('[one](guide.md?view=1#part) ![two](<assets/image name.svg>)\n'
                '[reference]: next.md#section "Label"\n'
                '<a href="#same">same</a><img src="image.svg">'
                '<source srcset="light.svg 1x, heavy.svg 2x">')
        self.assertEqual(set(targets(text)), {'guide.md?view=1#part', 'assets/image name.svg',
                         'next.md#section', '#same', 'image.svg', 'light.svg', 'heavy.svg'})

    def test_url_resolution_and_same_file_fragments(self):
        source = ROOT / 'references' / 'find-the-thread.md'
        self.assertIsNone(local_destination(source, 'https://example.org/missing#x', ROOT))
        self.assertIsNone(local_destination(source, '//example.org/missing#x', ROOT))
        self.assertEqual(local_destination(source, '#a%20b', ROOT), (source, 'a b'))
        self.assertEqual(local_destination(source, '../SKILL.md?view=1#runtime', ROOT), (ROOT / 'SKILL.md', 'runtime'))
        with self.assertRaises(ValueError):
            local_destination(source, '../../outside.md', ROOT)

    def test_missing_fragment_file_and_unpacked_target_are_distinct_failures(self):
        temporary_root = ROOT / 'analysis' / 'local-only' / 'test-temp'
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='markdown-links-', dir=temporary_root) as directory:
            root = Path(directory)
            source, other = root / 'source.md', root / 'other.md'
            source.write_text('# Source\n[own](#missing) [file](absent.md) '
                              '[other](other.md#present) [external](https://example.org/absent)', encoding='utf-8')
            other.write_text('# Present\n', encoding='utf-8')
            self.assertEqual(set(inspect_links(source, root)), {
                ('source.md', '#missing', 'missing_fragment'),
                ('source.md', 'absent.md', 'missing_file'),
            })
            self.assertIn(('source.md', 'other.md#present', 'outside_runtime_package'),
                          inspect_links(source, root, allowed={'source.md'}))


class DocumentationLinkTests(unittest.TestCase):
    def test_runtime_markdown_links_and_fragments_are_package_closed(self):
        allowed = set(package_skill.FILES)
        issues = []
        for name in sorted(allowed):
            if name.endswith('.md'):
                issues.extend(inspect_links(ROOT / name, allowed=allowed))
        self.assertEqual(issues, [], '\n'.join(map(str, issues)))

    def test_documentation_links_and_fragments_resolve(self):
        issues = []
        for path in sorted((ROOT / 'docs').rglob('*.md')):
            if not path.is_relative_to(ROOT / 'docs' / 'local'):
                issues.extend(inspect_links(path))
        self.assertEqual(issues, [], '\n'.join(map(str, issues)))

    def test_readme_paths_and_fragments_resolve(self):
        issues = [issue for name in READMES for issue in inspect_links(ROOT / name)]
        self.assertEqual(issues, [], '\n'.join(map(str, issues)))

    def test_legacy_design_entry_anchors_remain_available(self):
        for name, expected in LEGACY_ANCHORS.items():
            with self.subTest(path=name):
                current = anchors((ROOT / name).read_text(encoding='utf-8-sig'))
                self.assertEqual(set(expected) - current, set())


if __name__ == '__main__':
    unittest.main()
