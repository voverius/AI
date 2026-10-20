import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


HELPER = Path(__file__).resolve().parents[1] / 'skills/nemo-pkm/scripts/public_section.py'


class PublicSectionTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def call(self, *arguments):
        return subprocess.run([sys.executable, '-B', str(HELPER), *map(str, arguments)],
                              capture_output=True, text=True, check=False)

    def assert_error(self, result, code):
        self.assertEqual(result.returncode, 1)
        self.assertTrue(result.stderr == '')
        self.assertTrue(json.loads(result.stdout) == {'status': 'error', 'error': code})

    def replace(self, target, source, expected=b'Public\n', heading='## Personal'):
        return self.call('replace', '--root', self.root, '--heading', heading,
                         '--public-file', source, '--expected-public-sha256',
                         hashlib.sha256(expected).hexdigest(), target)

    def test_view_exposes_only_public_prefix(self):
        target = self.root / 'entry.md'
        public = b'# Public\nUseful text\n\n'
        protected = b'## Personal\nfixture-confidential\xff\xfe\n'
        target.write_bytes(public + protected)
        before = hashlib.sha256(target.read_bytes()).hexdigest()

        result = self.call('view', '--root', self.root, '--heading', '## Personal', target)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, '')
        self.assertTrue(json.loads(result.stdout) == {
            'public_text': public.decode(), 'boundary_found': True,
            'public_sha256': hashlib.sha256(public).hexdigest(),
        })
        self.assertFalse('fixture-confidential' in result.stdout + result.stderr)
        self.assertTrue(hashlib.sha256(target.read_bytes()).hexdigest() == before)

    def test_cr_only_view_does_not_emit_the_protected_suffix(self):
        target = self.root / 'entry.md'
        public = b'Open\r'
        protected = b'## Personal\rfixture-private-marker\n'
        target.write_bytes(public + protected)
        before = hashlib.sha256(target.read_bytes()).digest()
        result = self.call('view', '--root', self.root, '--heading', '## Personal', target)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stderr == '')
        self.assertFalse('fixture-private-marker' in result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout) == {
            'public_text': public.decode(), 'boundary_found': True,
            'public_sha256': hashlib.sha256(public).hexdigest(),
        })
        self.assertTrue(hashlib.sha256(target.read_bytes()).digest() == before)

    def test_paths_stay_inside_the_resolved_library(self):
        library = self.root / 'library'
        library.mkdir()
        target = library / 'entry.md'
        target.write_bytes(b'Public\n## Personal\nopaque\xff\n')
        outside = self.root / 'outside.md'
        outside.write_bytes(b'outside-confidential\n')
        (library / 'escape.md').symlink_to(outside)
        for path in (outside, '../outside.md', 'escape.md'):
            with self.subTest(path=str(path)):
                self.assert_error(self.call('view', '--root', library, '--heading',
                                            '## Personal', path), 'outside_root')
        result = self.call('view', '--root', library, '--heading', '## Personal', 'entry.md')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout)['public_text'] == 'Public\n')

    def test_errors_are_content_free(self):
        target = self.root / 'entry.md'
        target.write_bytes(b'nonutf8-public\xff\n## Personal\nopaque\xfe')
        self.assert_error(self.call('view', '--root', self.root, '--heading',
                                    '## Personal', target), 'invalid_public_utf8')
        for heading in ('Personal', '####### Personal', '## Personal\nother'):
            with self.subTest(heading=heading):
                self.assert_error(self.call('view', '--root', self.root, '--heading',
                                            heading, target), 'invalid_heading')
        self.assert_error(self.call('view', '--root', self.root, '--heading', '## Personal',
                                    'missing.md'), 'io_error')
        self.assert_error(self.call('view', '--root', target, '--heading', '## Personal',
                                    target), 'invalid_root')
        self.assert_error(self.call('view'), 'invalid_arguments')

    def test_literal_atx_heading_variants_and_no_boundary(self):
        target = self.root / 'entry.md'
        public = b'# Public\r\n## Personal detail\r\n'
        for heading, boundary in [
            ('## Personal', b'   ## Personal ###  \r\n'),
            ('# Private', b'# Private\n'),
            ('###### My notes', b' ###### My notes ##\n'),
            ('### A.* [private]', b'  ### A.* [private]\r\n'),
            ('##', b' ## ###\n'),
            ('## Personal ###', b'## Personal\n'),
        ]:
            with self.subTest(heading=heading):
                target.write_bytes(public + boundary + b'opaque\xff\n')
                result = self.call('view', '--root', self.root, '--heading', heading, target)
                self.assertEqual(result.returncode, 0)
                self.assertTrue(json.loads(result.stdout) == {
                    'public_text': public.decode(), 'boundary_found': True,
                    'public_sha256': hashlib.sha256(public).hexdigest(),
                })
        public = b'Public\n    ## Personal\n### Personal\n## Personal#\n'
        target.write_bytes(public)
        result = self.call('view', '--root', self.root, '--heading', '## Personal', target)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout) == {
            'public_text': public.decode(), 'boundary_found': False,
            'public_sha256': hashlib.sha256(public).hexdigest(),
        })

    def test_replace_returns_only_status_and_preserves_opaque_suffix_and_mode(self):
        target = self.root / 'entry.md'
        protected = b'   ## Personal ###\r\nfixture-confidential\xff\xfe\x00\n'
        target.write_bytes(b'Public\n' + protected)
        target.chmod(0o640)
        source = self.root / 'public.md'
        replacement = b'# New public\r\nUseful correction\r\n\r\n'
        source.write_bytes(replacement)
        source_before = source.stat().st_mtime_ns

        result = self.replace(target, source)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stderr == '')
        self.assertTrue(json.loads(result.stdout) == {
            'status': 'replaced', 'public_sha256': hashlib.sha256(replacement).hexdigest(),
        })
        actual = target.read_bytes()
        self.assertTrue(actual[:len(replacement)] == replacement)
        self.assertTrue(hashlib.sha256(actual[len(replacement):]).digest() ==
                        hashlib.sha256(protected).digest())
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o640)
        self.assertTrue(source.read_bytes() == replacement)
        self.assertEqual(source.stat().st_mtime_ns, source_before)
        self.assertTrue(set(self.root.iterdir()) == {source, target})
        viewed = self.call('view', '--root', self.root, '--heading', '## Personal', target)
        self.assertEqual(viewed.returncode, 0)
        self.assertTrue(json.loads(viewed.stdout)['public_text'] == replacement.decode())

    def test_replacement_keeps_protected_heading_at_line_start(self):
        target = self.root / 'entry.md'
        protected = b'## Personal\nopaque\xff'
        original = b'Public\n' + protected
        target.write_bytes(original)
        source = self.root / 'public.md'
        for replacement in (b'joined', b'joined\x0b'):
            with self.subTest(ending=replacement[-1:]):
                source.write_bytes(replacement)
                before = target.stat().st_mtime_ns
                self.assert_error(self.replace(target, source), 'replacement_needs_newline')
                self.assertTrue(hashlib.sha256(target.read_bytes()).digest() ==
                                hashlib.sha256(original).digest())
                self.assertEqual(target.stat().st_mtime_ns, before)
                self.assertTrue(source.read_bytes() == replacement)

        source.write_bytes(b'')
        result = self.replace(target, source)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(hashlib.sha256(target.read_bytes()).digest() ==
                        hashlib.sha256(protected).digest())
        viewed = self.call('view', '--root', self.root, '--heading', '## Personal', target)
        self.assertTrue(json.loads(viewed.stdout)['public_text'] == '')

    def test_replace_rejects_invalid_utf8_public_content(self):
        target = self.root / 'entry.md'
        source = self.root / 'public.md'
        for public, replacement in ((b'Public\n', b'invalid\xff\n'),
                                    (b'invalid\xfe\n', b'New public\n')):
            with self.subTest(invalid_replacement=b'\xff' in replacement):
                original = public + b'## Personal\nopaque\xff'
                target.write_bytes(original)
                source.write_bytes(replacement)
                before = target.stat().st_mtime_ns
                self.assert_error(self.replace(target, source, expected=public),
                                  'invalid_public_utf8')
                self.assertTrue(hashlib.sha256(target.read_bytes()).digest() ==
                                hashlib.sha256(original).digest())
                self.assertEqual(target.stat().st_mtime_ns, before)

    def test_cr_replacement_preserves_exact_suffix_offsets_and_noop(self):
        target = self.root / 'entry.md'
        source = self.root / 'public.md'
        for public, boundary in ((b'Open\r', b'## Personal\r'),
                                 (b'One\nTwo\r\nThree\r', b'   ## Personal ###\r\n')):
            with self.subTest(mixed=b'\n' in public):
                protected = boundary + b'opaque\xff\x00\r\n'
                target.write_bytes(public + protected)
                replacement = b'Changed\r'
                source.write_bytes(replacement)
                result = self.replace(target, source, expected=public)
                self.assertEqual(result.returncode, 0)
                self.assertTrue(json.loads(result.stdout) == {
                    'status': 'replaced',
                    'public_sha256': hashlib.sha256(replacement).hexdigest(),
                })
                actual = target.read_bytes()
                self.assertTrue(actual[:len(replacement)] == replacement)
                self.assertTrue(hashlib.sha256(actual[len(replacement):]).digest() ==
                                hashlib.sha256(protected).digest())
                before = target.stat().st_mtime_ns
                result = self.replace(target, source, expected=replacement)
                self.assertTrue(json.loads(result.stdout)['status'] == 'unchanged')
                self.assertEqual(target.stat().st_mtime_ns, before)

    def test_stale_public_hash_rejects_without_changing_either_file(self):
        target = self.root / 'entry.md'
        target.write_bytes(b'Changed public\n## Personal\nopaque\xff')
        source = self.root / 'public.md'
        source.write_bytes(b'New public\n')
        before = {path: (hashlib.sha256(path.read_bytes()).digest(), path.stat().st_mtime_ns)
                  for path in (target, source)}
        self.assert_error(self.replace(target, source), 'stale_public_hash')
        for path, (digest, mtime) in before.items():
            self.assertTrue(hashlib.sha256(path.read_bytes()).digest() == digest)
            self.assertEqual(path.stat().st_mtime_ns, mtime)

    def test_noop_preserves_bytes_mtime_and_inode(self):
        target = self.root / 'entry.md'
        target.write_bytes(b'Public\n## Personal\nopaque\xff')
        source = self.root / 'public.md'
        source.write_bytes(b'Public\n')
        before = target.stat()
        digest = hashlib.sha256(target.read_bytes()).digest()
        result = self.replace(target, source)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(json.loads(result.stdout) == {
            'status': 'unchanged', 'public_sha256': hashlib.sha256(b'Public\n').hexdigest(),
        })
        self.assertTrue(hashlib.sha256(target.read_bytes()).digest() == digest)
        self.assertEqual(target.stat().st_mtime_ns, before.st_mtime_ns)
        self.assertEqual(target.stat().st_ino, before.st_ino)
        self.assertTrue(set(self.root.iterdir()) == {source, target})

    def test_replace_requires_a_protected_boundary(self):
        target = self.root / 'entry.md'
        target.write_bytes(b'Public\n')
        source = self.root / 'public.md'
        source.write_bytes(b'New public\n')
        before = target.stat().st_mtime_ns
        self.assert_error(self.replace(target, source), 'boundary_missing')
        self.assertTrue(target.read_bytes() == b'Public\n')
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_public_replacement_cannot_introduce_the_protected_heading(self):
        target = self.root / 'entry.md'
        original = b'Public\n### My secrets\nopaque\xff'
        source = self.root / 'public.md'
        for replacement in (b'New\n### My secrets\n', b'   ### My secrets ###\r\n',
                            b'New\n### My secrets\nopaque\xff\n',
                            b'New\r### My secrets\ropaque\xff\r'):
            with self.subTest(closing_hashes=b'###\r\n' in replacement):
                target.write_bytes(original)
                source.write_bytes(replacement)
                before = target.stat().st_mtime_ns
                self.assert_error(self.replace(target, source, heading='### My secrets'),
                                  'replacement_boundary')
                self.assertTrue(hashlib.sha256(target.read_bytes()).digest() ==
                                hashlib.sha256(original).digest())
                self.assertEqual(target.stat().st_mtime_ns, before)
                self.assertTrue(source.read_bytes() == replacement)

    def test_replacement_source_must_be_distinct_and_root_bounded(self):
        library = self.root / 'library'
        library.mkdir()
        target = library / 'entry.md'
        target.write_bytes(b'Public\n## Personal\nopaque\xff')
        alias = library / 'hardlink.md'
        os.link(target, alias)
        symlink = library / 'symlink.md'
        symlink.symlink_to(target)
        outside = self.root / 'outside.md'
        outside.write_bytes(b'Outside\n')
        escape = library / 'escape.md'
        escape.symlink_to(outside)
        before = hashlib.sha256(target.read_bytes()).digest()
        mtime = target.stat().st_mtime_ns
        for source, error in ((target, 'same_file'), (alias, 'same_file'),
                              (symlink, 'same_file'), (outside, 'outside_root'),
                              (escape, 'outside_root')):
            with self.subTest(error=error, source=source.name):
                result = self.call('replace', '--root', library, '--heading', '## Personal',
                                   '--public-file', source, '--expected-public-sha256',
                                   hashlib.sha256(b'Public\n').hexdigest(), target)
                self.assert_error(result, error)
                self.assertTrue(hashlib.sha256(target.read_bytes()).digest() == before)
                self.assertEqual(target.stat().st_mtime_ns, mtime)

    def test_atomic_replace_failure_preserves_original_and_cleans_temp(self):
        spec = importlib.util.spec_from_file_location('public_section', HELPER)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        target = self.root / 'entry.md'
        target.write_bytes(b'Public\n## Personal\nopaque\xff')
        source = self.root / 'public.md'
        source.write_bytes(b'New public\n')
        before = {path: (hashlib.sha256(path.read_bytes()).digest(), path.stat().st_mtime_ns)
                  for path in (target, source)}
        stdout, stderr = io.StringIO(), io.StringIO()
        arguments = ['replace', '--root', str(self.root), '--heading', '## Personal',
                     '--public-file', str(source), '--expected-public-sha256',
                     hashlib.sha256(b'Public\n').hexdigest(), str(target)]
        with mock.patch('os.replace', side_effect=OSError('fixture-confidential OS message')):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = helper.main(arguments)
        result = subprocess.CompletedProcess(arguments, code, stdout.getvalue(), stderr.getvalue())
        self.assert_error(result, 'io_error')
        for path, (digest, mtime) in before.items():
            self.assertTrue(hashlib.sha256(path.read_bytes()).digest() == digest)
            self.assertEqual(path.stat().st_mtime_ns, mtime)
        self.assertTrue(set(self.root.iterdir()) == {source, target})


if __name__ == '__main__':
    unittest.main()
