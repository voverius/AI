
import json
from pathlib import Path
import subprocess
import sys
import unittest


class ReplyTests(unittest.TestCase):
    checker = (Path(__file__).resolve().parents[1] /
               'skills/nemo-general/scripts/check_reply.py')

    def check_reply(self, text, mode='reply', **options):
        return subprocess.run([sys.executable, str(self.checker)],
                              input=json.dumps({'mode': mode, 'text': text, **options}),
                              text=True, capture_output=True)

    def test_rejects_extra_sentence(self):
        result = self.check_reply('Updated the parser. Checked the result. One path is untested. '
                                  'Let me know if you need anything else.')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)['ok'])

    def test_rejects_long_sentences_and_forbidden_prose_punctuation(self):
        for text in (' '.join(['word'] * 36) + '.', 'Updated it; checked it.',
                     'Updated it\u2014checked it.', 'Updated it\u2013checked it.'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertFalse(json.loads(result.stdout)['ok'])

    def test_preserves_valid_reply_with_code_links_and_abbreviations(self):
        text = ('Dr. Reed updated [the parser](https://example.com/parse.py?a=1;b=2). '
                'The token is `x;y`. One path is untested.')
        result = self.check_reply(text)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_preserves_requested_detail(self):
        text = 'First finding. Second finding. Third finding.\n\nFourth finding.'
        result = self.check_reply(text, 'detail')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_preserves_paragraph_breaks_in_short_ordinary_replies(self):
        for text in (
                'The saved decision is unchanged.\n\n'
                'The authoritative source remains available.\n\n'
                'The next step is already recorded.',
                'The configuration controls the current retry limit.\n \n'
                'The retained report records its earlier observation.'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_rejects_excess_items_and_unrequested_code_blocks(self):
        for text in ('- Changed parser\n- Checked syntax\n- Skipped integration\n- Ready for review',
                     '```python\nprint("hello")\n```'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 1, result.stderr)

    def test_paragraph_breaks_do_not_relax_the_sentence_budget(self):
        text = 'One finding.\n\nAnother finding.\n\nA third finding.\n\nA fourth finding.'
        self.assertEqual(self.check_reply(text).returncode, 1)

    def test_preserves_selected_review_layout_with_context_and_source_excerpt(self):
        text = ('**Should we change when the handover guidance is read?**\n\n'
                'The current instruction says:\n\n'
                '> On finish, read it only when continuation remains.\n\n'
                'That excludes the guidance needed to close an existing handover. '
                '\n\n**Suggestion:** Include completion and cancellation as reasons to read it.\n\n'
                'The test closed its handover correctly, so '
                '**a closure failure has not been reproduced**.')
        result = self.check_reply(text, 'review')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_review_distinguishes_quoted_questions_from_questions_to_the_user(self):
        text = ('**Which source should control retry settings?**\n\n'
                'The old note asks:\n\n> Should retries stay at 3?\n\n'
                '**Suggestion:** Use the service configuration because it controls execution.')
        result = self.check_reply(text, 'review')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)
        for draft in ('Which source should control retry settings?',
                      text + '\n\nShould I change the export format too?',
                      '**Which source? Which format?**'):
            with self.subTest(draft=draft):
                self.assertEqual(self.check_reply(draft, 'review').returncode, 1)

    def test_review_requires_a_bold_suggestion_label(self):
        question = '**Which source should control retries?**\n\n'
        for suggestion in ('Use the service configuration.',
                           'Suggestion: Use the service configuration.',
                           '> **Suggestion:** Use the old note.',
                           '`**Suggestion:** Use the old note.`'):
            with self.subTest(suggestion=suggestion):
                self.assertEqual(self.check_reply(question + suggestion, 'review').returncode, 1)
        self.assertEqual(self.check_reply(question + '**Suggestion**: Use the configuration.',
                                         'review').returncode, 0)

    def test_review_accepts_inline_quoted_source_questions(self):
        for quote in ('"Should retries stay at 3?"', '\u201cShould retries stay at 3?\u201d',
                      "'Should retries stay at 3?'"):
            text = ('**Which source should control retries?**\n\nThe old note asks ' + quote +
                    '\n\n**Suggestion:** Use the service configuration.')
            with self.subTest(quote=quote):
                self.assertEqual(self.check_reply(text, 'review').returncode, 0)
                self.assertEqual(self.check_reply(text + '\n\nShould I edit it?',
                                                 'review').returncode, 1)

    def test_accepts_three_short_list_items_and_word_limit(self):
        for text in ('1. Changed parser\n2. Checked syntax\n3. Integration untested',
                     ' '.join(['word'] * 35) + '.'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 0, result.stdout)

    def test_ordinary_lists_are_not_completion_reports(self):
        for text in ('- Check the scope\n- Run the focused test',
                     '- Check the scope\n- Run the focused test\n- Read the result',
                     'Inspect the requested change.\n\n- Check its scope\n- Run its focused test'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_ordinary_list_opener_still_uses_the_ordinary_budget(self):
        text = 'Inspect the requested change.\n\n- Check its scope\n- Run its test\n- Read the result'
        self.assertEqual(self.check_reply(text).returncode, 1)

    def test_ordinary_soft_wrapping_does_not_add_sentences(self):
        text = 'The result remains\nuncertain. A direct source is\nunavailable.'
        result = self.check_reply(text)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)
        for text in ('- Check the scope\n- Run the test\n- Read the result\n- Record failures',
                     'First fact.\nSecond fact.\nThird fact.\nFourth fact.'):
            with self.subTest(text=text):
                self.assertEqual(self.check_reply(text).returncode, 1)

    def test_invalid_input_is_rejected_without_traceback(self):
        for raw in ('{', '{}', '[]', '{"text": 12}', '{"text": ""}',
                    '{"text": "OK", "mode": "skip"}',
                    '{"text": "OK", "mode": "artifact"}'):
            with self.subTest(raw=raw):
                result = subprocess.run([sys.executable, str(self.checker)], input=raw,
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 1)
                self.assertFalse(json.loads(result.stdout)['ok'])
                self.assertEqual(result.stderr, '')

    def test_markdown_and_quotes_do_not_hide_sentences(self):
        for text in ('**Done.** Checked. Verified. Finished.',
                     '"Done." Checked. Verified. Finished.',
                     '(Done.) Checked. Verified. Finished.'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_preserves_approved_completion_report(self):
        text = ('CSV exports now preserve accented names.\n\n'
                '- **Change:** export encoding switched to UTF-8\n'
                '- **Validation:** focused regression test passed, but the full suite was not run\n'
                '- **Impact:** no production data was changed')
        result = self.check_reply(text, 'report')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_rejects_report_without_plain_sentence_and_bold_first_words(self):
        for text in ('**The update is ready.**\n\n- **Validation:** focused test passed',
                     'The update is ready. Tests passed.\n\n- **Impact:** data unchanged',
                     'The update is ready.\n\n- Validation: focused test passed',
                     'The update is ready.\n\n- **Focused test:** passed'):
            with self.subTest(text=text):
                result = self.check_reply(text, 'report')
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_rejects_report_with_four_bullets(self):
        text = ('The update is ready.\n\n- **Change:** parser updated\n'
                '- **Validation:** test passed\n- **Impact:** data unchanged\n'
                '- **Next:** more work')
        self.assertEqual(self.check_reply(text, 'report').returncode, 1)

    def test_report_accepts_colon_inside_or_outside_bold_label(self):
        for label in ('**Validation:**', '**Validation**:'):
            text = 'Search preserves accented queries.\n\n- ' + label + ' focused test passed'
            with self.subTest(label=label):
                self.assertEqual(self.check_reply(text, 'report').returncode, 0)

    def test_report_rejects_missing_colon_and_additional_emphasis(self):
        for bullet in ('**Validation** focused test passed',
                       '**Validation:** focused test **passed**',
                       '**Validation:** focused test __passed__'):
            with self.subTest(bullet=bullet):
                self.assertEqual(self.check_reply('Search preserves accented queries.\n\n- '
                                                 + bullet, 'report').returncode, 1)

    def test_preserves_tabular_answer_without_counting_rows_as_sentences(self):
        text = ('2 projects need attention.\n\n'
                '| Project | Owner | Status | Next action |\n'
                '| --- | --- | --- | --- |\n'
                '| Website | Maya | On track | Publish FAQ |\n'
                '| Mobile | Leo | Blocked | Obtain access |\n'
                '| Billing | Sam | At risk | Resolve mismatch |\n'
                '| Search | Noor | Complete | Monitor |')
        result = self.check_reply(text)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_table_does_not_hide_excessive_prose(self):
        text = ('One. Two. Three. Four.\n\n'
                '| Project | Status |\n| --- | --- |\n| Search | Complete |')
        self.assertEqual(self.check_reply(text).returncode, 1)

    def test_report_requires_gap_and_labels_even_if_shape_is_wrong(self):
        text = 'The parser is ready.\n- Changed parser\n- Tests passed'
        self.assertEqual(self.check_reply(text, 'report').returncode, 1)

    def test_report_accepts_outer_whitespace_and_wrapped_bullets(self):
        text = ('\nThe parser is ready.\n\n'
                '- **Validation:** focused test passed,\n  full suite not run\n')
        result = self.check_reply(text, 'report')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)

    def test_multiple_valid_tables_and_inconsistent_columns(self):
        text = ('| Project | Status |\n| --- | --- |\n| Atlas | Ready |\n\n'
                '| Project | Status |\n| --- | --- |\n| Beacon | Blocked |')
        self.assertEqual(self.check_reply(text).returncode, 0)
        for table in ('| Project |\n| --- | --- |\n| Atlas | Ready |',
                      '| Project | Status |\n| --- | --- |\n| Atlas |'):
            with self.subTest(table=table):
                self.assertEqual(self.check_reply(table).returncode, 1)

    def test_fact_requires_one_sentence_without_changing_text(self):
        text = 'A reference is supporting material read when needed.'
        result = self.check_reply(text, 'fact')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)
        self.assertEqual(self.check_reply(text + ' It keeps the entry short.', 'fact').returncode, 1)

    def test_comparison_checks_requested_count_not_ordinary_reply_budget(self):
        alternatives = ['The deadline moves by 2 days.',
                        'The required review is unfinished. Delivery moves by 2 days.',
                        'Delivery is delayed by 2 days because the review is unfinished.']
        text = '\n\n---\n\n'.join(alternatives)
        result = self.check_reply(text, 'comparison', count=3)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)
        self.assertEqual(self.check_reply(text + '\n\n---\n\nAn extra example.',
                                         'comparison', count=3).returncode, 1)
        for count in (None, True, 0, -1, '3'):
            with self.subTest(count=count):
                self.assertEqual(self.check_reply(text, 'comparison', count=count).returncode, 1)

    def test_json_argument_matches_stdin_without_needing_a_shell_heredoc(self):
        text = "A reference supplies guidance when it's needed."
        payload = json.dumps({'mode': 'fact', 'text': text})
        result = subprocess.run([sys.executable, '-I', str(self.checker), payload],
                                input='', text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout, self.check_reply(text, 'fact').stdout)
        for args in (['{'], [payload, payload]):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(self.checker), *args],
                                        input='', text=True, capture_output=True)
                self.assertEqual(result.returncode, 1)
                self.assertFalse(json.loads(result.stdout)['ok'])

    def test_routine_progress_is_a_compact_paragraph_without_first_person_opening(self):
        text = 'Reviewed 3 of 8 adapters. Each has a retry conflict. Checking the remaining.'
        self.assertEqual(self.check_reply(text, 'progress').returncode, 0)
        for draft in ("I'm reviewing the remaining adapters.",
                      'I have reviewed 3 of 8 adapters. Checking the remaining.',
                      'Reviewed 3 of 8 adapters.\n\n- **Next:** check the remaining'):
            with self.subTest(draft=draft):
                self.assertEqual(self.check_reply(draft, 'progress').returncode, 1)
        self.assertEqual(self.check_reply('Checking I/O latency.', 'progress').returncode, 0)

    def test_progress_preserves_a_soft_wrapped_paragraph_and_does_not_require_counts(self):
        text = ('Reviewed 3 of 8 adapters. Each has\n'
                'a retry conflict. Checking the\nremaining adapters.')
        result = self.check_reply(text, 'progress')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['text'], text)
        self.assertEqual(self.check_reply('The source is unreachable. Checking its mirror.',
                                         'progress').returncode, 0)

    def test_report_mode_requires_the_completion_layout(self):
        text = ('Search preserves accented queries.\n\n'
                '- **Validation:** focused test passed, full suite not run')
        self.assertEqual(self.check_reply(text, 'report').returncode, 0)
        self.assertEqual(self.check_reply('Search preserves accented queries. '
                                         'The focused test passed.', 'report').returncode, 1)

    def test_report_budget_counts_bullets_not_sentences_inside_bullets(self):
        text = ('Search preserves accented queries.\n\n'
                '- **Change:** normalization updated\n'
                '- **Validation:** focused test passed. The full suite was not run\n'
                '- **Data:** no production data changed')
        self.assertEqual(self.check_reply(text, 'report').returncode, 0)
        long_item = 'Search is updated.\n\n- **Validation:** ' + ' '.join(['word'] * 36)
        self.assertEqual(self.check_reply(long_item, 'report').returncode, 1)

    def test_comparison_ignores_separator_text_inside_code(self):
        for fence, closing in (('```', '```'), ('~~~', '~~~'), ('~~~~', '~~~~~')):
            text = (f'{fence}yaml\n---\nname: first\n{closing}\n\n---\n\n'
                    f'{fence}yaml\n---\nname: second\n{closing}')
            with self.subTest(fence=fence):
                self.assertEqual(self.check_reply(text, 'comparison', count=2).returncode, 0)


if __name__ == '__main__':
    unittest.main()

