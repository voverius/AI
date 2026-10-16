
import json
from pathlib import Path
import subprocess
import sys
import unittest


class ReplyTests(unittest.TestCase):
    checker = (Path(__file__).resolve().parents[1] /
               'skills/nemo-general/scripts/check_reply.py')

    def check_reply(self, text, mode='reply'):
        return subprocess.run([sys.executable, str(self.checker)],
                              input=json.dumps({'mode': mode, 'text': text}),
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

    def test_rejects_ordinary_reports_and_fragment_lists(self):
        for text in ('Updated the parser.\n\nTests passed.',
                     'Updated the parser.\n \nTests passed.',
                     '- Changed parser\n- Checked syntax\n- Skipped integration\n- Ready for review',
                     '```python\nprint("hello")\n```'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 1, result.stderr)

    def test_accepts_three_short_list_items_and_word_limit(self):
        for text in ('1. Changed parser\n2. Checked syntax\n3. Integration untested',
                     ' '.join(['word'] * 35) + '.'):
            with self.subTest(text=text):
                result = self.check_reply(text)
                self.assertEqual(result.returncode, 0, result.stdout)

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


if __name__ == '__main__':
    unittest.main()

