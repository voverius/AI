"""Public navigation-checker regressions using disposable local projects."""
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / 'skills/nemo-project/scripts/check_navigation.py'
LINK_PATHS = runpy.run_path(str(CHECKER))['link_paths']


class LinkPathsTests(unittest.TestCase):
    def test_first_reference_definition_wins(self):
        text = '[Guide][ref]\n\n[REF]: guide.md\n[ref]: missing.md\n'
        self.assertEqual(set(LINK_PATHS(text)), {'guide.md'})

    def test_empty_reference_destination_still_wins(self):
        text = '[Guide][ref]\n\n[ref]: <>\n[ref]: missing.md\n'
        self.assertEqual(LINK_PATHS(text), [])

    def test_escaped_opening_brackets_are_literal_text(self):
        for literal in (r'\[Example](missing.md)', r'\[Example]\[ref]', r'\[ref]'):
            text = literal + '\n[ref]: missing.md\n[Real](real.md)'
            with self.subTest(literal=literal):
                self.assertEqual(LINK_PATHS(text), ['real.md'])
        self.assertEqual(LINK_PATHS(r'\\[Real](real.md)'), ['real.md'])
        # Escaping the first opener leaves an independent shortcut reference.
        text = r'\[Example][ref]' + '\n[ref]: real.md\n'
        self.assertEqual(set(LINK_PATHS(text)), {'real.md'})

    def test_destinations_can_start_on_the_next_line(self):
        for text in ('[Guide](\nguide.md)', '[Guide](\n <guide.md>)',
                     '[Guide][ref]\n\n[ref]:\n guide.md\n',
                     '[Guide][ref]\n\n[ref]:\n <guide.md>\n'):
            with self.subTest(text=text):
                self.assertEqual(set(LINK_PATHS(text)), {'guide.md'})

    def test_balanced_and_escaped_destinations(self):
        for text, expected in (
                ('[Guide](guide_(current).md)', 'guide_(current).md'),
                ('[Guide](guide_(part_(two)).md)', 'guide_(part_(two)).md'),
                (r'[Guide](guide_\(current\).md)', 'guide_(current).md'),
                ('[Guide](<guide_(current).md>)', 'guide_(current).md'),
                ('[Guide](guide_(current).md "Read this guide")', 'guide_(current).md')):
            with self.subTest(text=text):
                self.assertEqual(LINK_PATHS(text), [expected])

    def test_reference_destinations_and_normalized_labels(self):
        for destination in ('guide_(current).md', r'guide_\(current\).md',
                            '<guide_(current).md>'):
            text = f'[Guide][ USER guide ]\n\n[user GUIDE]: {destination}\n'
            with self.subTest(destination=destination):
                paths = LINK_PATHS(text)
                self.assertTrue(paths)
                self.assertEqual(set(paths), {'guide_(current).md'})

    def test_both_fence_characters_exclude_examples(self):
        for fence in ('```', '~~~', '````', '~~~~'):
            text = f'{fence}markdown\n[Example](not-a-file.md)\n{fence}\n[Real](real.md)'
            with self.subTest(fence=fence):
                self.assertEqual(LINK_PATHS(text), ['real.md'])

    def test_shorter_or_other_fences_do_not_close_a_block(self):
        for text in ('````markdown\n```\n[Example](not-a-file.md)\n````\n',
                     '~~~~markdown\n~~~\n[Example](not-a-file.md)\n~~~~\n',
                     '```markdown\n~~~\n[Example](not-a-file.md)\n```\n'):
            with self.subTest(text=text):
                self.assertEqual(LINK_PATHS(text + '[Real](real.md)'), ['real.md'])

    def test_indented_and_unclosed_fences_exclude_examples(self):
        for text in ('   ~~~markdown\n[Example](not-a-file.md)\n   ~~~\n',
                     '~~~markdown\n[Example](not-a-file.md)\n'):
            with self.subTest(text=text):
                self.assertEqual(LINK_PATHS(text), [])

    def test_reference_definitions_inside_code_do_not_supply_real_links(self):
        text = '~~~markdown\n[sample]: missing.md\n~~~\n[sample]\n[Real](real.md)'
        self.assertEqual(LINK_PATHS(text), ['real.md'])

    def test_inline_code_does_not_supply_links(self):
        text = '`[Example](missing.md)` and [Real](real.md)'
        self.assertEqual(LINK_PATHS(text), ['real.md'])


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='nemo-navigation-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'docs').mkdir()
        (self.root / 'inbox').mkdir()
        (self.root / 'AGENTS.md').write_text('\n# Project\n\n')
        (self.root / 'README.md').write_text(
            '\n# Project\n[Contract](AGENTS.md)\n[Knowledge](docs/index.md)\n'
            '[Inbox](inbox/)\n\n')

    def run_checker(self, index, filename='guide.md'):
        (self.root / 'docs/index.md').write_text('\n# Knowledge\n' + index + '\n\n')
        (self.root / 'docs' / filename).write_text('\n# Guide\nUseful content.\n\n')
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, str(CHECKER), str(self.root)],
                                capture_output=True, text=True)
        after = {p: (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after, 'The checker must not modify project state')
        return result

    def test_valid_parentheses_pass_without_changing_the_project(self):
        text = ('[Bare](guide_(current).md)\n'
                r'[Escaped](guide_\(current\).md)' + '\n'
                '[Angled](<guide_(current).md>)')
        result = self.run_checker(text, 'guide_(current).md')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.strip(), 'Navigation checks passed')

    def test_fenced_examples_are_not_missing_files(self):
        text = '~~~markdown\n[Example](missing.md)\n~~~\n[Guide](guide.md)'
        result = self.run_checker(text)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_literals_and_shadowed_definitions_do_not_add_targets(self):
        # CommonMark 0.31.2: backslash escapes and reference-link example 544.
        text = (r'\[Literal](not-a-file.md)' + '\n\n[Guide][ref]\n\n'
                '[ref]: guide.md\n[REF]: shadowed.md\n\n[Void][empty]\n\n'
                '[empty]: <>\n[empty]: also-shadowed.md')
        result = self.run_checker(text)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_real_broken_links_still_fail(self):
        result = self.run_checker('[Guide](guide.md)\n[Missing](missing.md)')
        self.assertEqual(result.returncode, 1)
        self.assertIn('missing link target missing.md', result.stdout)

    def test_unreachable_subjects_still_fail(self):
        result = self.run_checker('No subject route.')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Unreachable subject: docs/guide.md', result.stdout)


if __name__ == '__main__':
    unittest.main()
