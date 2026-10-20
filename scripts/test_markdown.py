import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


CHECKER = Path(__file__).resolve().parents[1] / 'skills/nemo-general/scripts/check_markdown.py'


class MarkdownTests(unittest.TestCase):
    def check(self, text, fragment=False, frontmatter=False):
        spec = importlib.util.spec_from_file_location('markdown_checker', CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        options = {'fragment': fragment}
        if frontmatter:
            options['frontmatter'] = True
        return module.check(text, **options)

    def test_saved_heading_spacing_differs_from_chat_spacing(self):
        self.assertEqual(self.check('\n# Notes\nUseful text\n\n'), [])
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '\n# Notes\n\nUseful text\n\n')})

    def test_headings_following_prose_need_a_blank_line(self):
        self.assertEqual(self.check('\nFirst paragraph\n\n## Next\nText\n\n'), [])
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '\nFirst paragraph\n## Next\nText\n\n')})

    def test_frontmatter_and_fenced_examples_keep_their_syntax(self):
        text = ('---\nname: sample\ndescription: Example\n---\n\n'
                '# Guide\nText\n\n```markdown\n# Example\n\n- One\n\n- Two\n```\n\n')
        self.assertEqual(self.check(text), [])

    def test_exact_file_boundaries(self):
        self.assertEqual(self.check('\nText\n\n'), [])
        for text in ('Text\n\n', '\n\nText\n\n', '\nText\n', '\nText\n\n\n'):
            with self.subTest(text=text):
                self.assertIn('file_boundary', {e['rule'] for e in self.check(text)})

    def test_fragment_omits_only_file_boundary_checks(self):
        self.assertEqual(self.check('# Notes\nText\n', fragment=True), [])
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '# Notes\n\nText\n', fragment=True)})

    def test_crlf_and_nested_lists(self):
        self.assertEqual(self.check('\r\n# Notes\r\n- One\r\n  - Nested\r\n- Two\r\n\r\n'), [])
        self.assertIn('list_spacing', {e['rule'] for e in self.check(
            '\n# Notes\n- One\n\n- Two\n\n')})

    def test_indented_code_is_not_a_list_to_reformat(self):
        self.assertEqual(self.check('\nExample:\n\n    - One\n\n    - Two\n\n'), [])

    def test_wrapped_list_items_still_require_contiguous_spacing(self):
        self.assertIn('list_spacing', {e['rule'] for e in self.check(
            '\n- One\n  continuation\n\n- Two\n\n')})

    def test_thematic_break_is_not_another_list_item(self):
        self.assertEqual(self.check('\n- One\n\n* * *\n\n'), [])

    def test_backticks_in_fence_info_do_not_hide_layout_errors(self):
        self.assertIn('list_spacing', {e['rule'] for e in self.check(
            '\n```a``` b\n\n- One\n\n- Two\n\n')})

    def test_only_one_blank_line_before_a_heading_after_prose(self):
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '\nText\n\n\n# Next\nText\n\n')})

    def test_unicode_separator_is_not_a_markdown_line_break(self):
        self.assertEqual(self.check('\nText\u2028# literal\n\n'), [])

    def test_empty_list_markers_do_not_hide_spacing_errors(self):
        self.assertIn('list_spacing', {e['rule'] for e in self.check('\n-\n\n- Next\n\n')})

    def test_fragment_thematic_break_does_not_start_unclosed_frontmatter(self):
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '---\n# Guide\n\nText\n', fragment=True)})

    def test_fragment_boundaries_do_not_guess_frontmatter(self):
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '---\n# Guide\n\nText\n\n---\n', fragment=True)})
        self.assertEqual(self.check('---\nname: sample\n---\n# Guide\nText\n',
                                    fragment=True, frontmatter=True), [])

    def test_only_ascii_markers_and_heading_whitespace_are_syntax(self):
        self.assertEqual(self.check('\n#\u00a0literal\n\nText\n\n'), [])
        self.assertEqual(self.check('\n١. Literal\n\n٢. Literal\n\n'), [])
        self.assertEqual(self.check('\n1234567890. Literal\n\n1234567891. Literal\n\n'), [])

    def test_link_definition_is_not_a_paragraph_before_a_heading(self):
        self.assertEqual(self.check('\n[ref]: https://example.org\n# Guide\nText\n\n'), [])
        self.assertIn('heading_spacing', {e['rule'] for e in self.check(
            '\n[status]: this is explanatory prose\n# Guide\nText\n\n')})

    def test_setext_heading_is_not_a_paragraph_before_an_atx_heading(self):
        self.assertEqual(self.check('\nTitle\n=====\n# Guide\nText\n\n'), [])

    def test_unreadable_input_is_an_execution_error_with_json(self):
        result = subprocess.run([sys.executable, '-B', str(CHECKER),
                                 str(CHECKER / 'missing.md')], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('read_error', result.stdout)
        self.assertNotIn('Traceback', result.stderr)

    def test_errors_contain_locations_and_rules_without_document_content(self):
        errors = self.check('\n# Private title\n\nSecret text\n\n')
        self.assertTrue(errors)
        self.assertTrue(all(set(e) == {'line', 'rule'} for e in errors))

    def test_command_checks_stdin_and_returns_no_document_body(self):
        text = '# Sensitive title\n\nSensitive body\n'
        result = subprocess.run([sys.executable, '-B', str(CHECKER), '--fragment'],
                                input=text, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertFalse(data['ok'])
        self.assertEqual(data['results'][0]['errors'],
                         [{'line': 1, 'rule': 'heading_spacing'}])
        self.assertNotIn('Sensitive', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
