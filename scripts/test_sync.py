
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.repository = Path(__file__).resolve().parent.parent

    def sync(self, platform):
        environment = dict(os.environ, TASK_TEST_ROOT=str(self.root), TASK_PLATFORM=platform,
                           TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'))
        return subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_instructions_path() { printf '%s\\n' "$TASK_TEST_ROOT/rules/$1.mdc"; }
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            sync_tool "$TASK_PLATFORM"
            '''], env=environment, text=True, capture_output=True)

    def test_cursor_rule_applies_and_points_to_shared_source(self):
        result = self.sync('cursor')
        self.assertEqual(result.returncode, 0, result.stderr)
        content = (self.root / 'rules/cursor.mdc').read_text()
        self.assertTrue(content.startswith('---\nalwaysApply: true\n---\n'))
        self.assertIn(str(self.repository / 'AGENTS.md'), content)

    def test_cursor_replaces_only_its_legacy_link_without_editing_source(self):
        target = self.root / 'rules/cursor.mdc'
        target.parent.mkdir()
        source = self.repository / 'AGENTS.md'
        before = source.read_bytes()
        target.symlink_to(source)
        result = self.sync('cursor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(target.is_symlink())
        self.assertEqual(source.read_bytes(), before)
        first = target.stat().st_mtime_ns
        self.assertEqual(self.sync('cursor').returncode, 0)
        self.assertEqual(target.stat().st_mtime_ns, first)

    def test_cursor_preserves_foreign_links_and_user_files(self):
        for kind in ('file', 'link', 'directory'):
            with self.subTest(kind=kind):
                target = self.root / 'rules/cursor.mdc'
                target.parent.mkdir(exist_ok=True)
                if kind == 'file':
                    target.write_text('User instructions')
                elif kind == 'link':
                    target.symlink_to(self.root / 'missing-user-rules')
                else:
                    target.mkdir()
                result = self.sync('cursor')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Conflict:', result.stderr)
                if kind == 'file':
                    self.assertEqual(target.read_text(), 'User instructions')
                    target.unlink()
                elif kind == 'link':
                    self.assertEqual(target.readlink(), self.root / 'missing-user-rules')
                    target.unlink()
                else:
                    self.assertTrue(target.is_dir())
                    target.rmdir()

    def test_instruction_parent_conflict(self):
        (self.root / 'rules').write_text('Keep this file')
        self.assertNotEqual(self.sync('cursor').returncode, 0)
        self.assertEqual((self.root / 'rules').read_text(), 'Keep this file')

    def test_other_platforms_keep_links_and_all_skills_install(self):
        for platform in ('codex', 'claude', 'cursor'):
            with self.subTest(platform=platform):
                result = self.sync(platform)
                self.assertEqual(result.returncode, 0, result.stderr)
                if platform != 'cursor':
                    self.assertEqual((self.root / f'rules/{platform}.mdc').resolve(),
                                     self.repository / 'AGENTS.md')
                for skill in (self.repository / 'skills').glob('nemo-*'):
                    self.assertEqual((self.root / f'skills/{platform}' / skill.name).resolve(),
                                     skill)

    def test_managed_skill_symlink_is_repointed(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        stale = self.repository / 'skills' / f'.stale-{skill.name}'
        stale.mkdir(exist_ok=True)
        self.addCleanup(lambda: stale.rmdir() if stale.exists() else None)
        target.unlink()
        target.symlink_to(stale)
        result = self.sync('codex')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.readlink(), skill)

    def test_foreign_skill_symlink_is_preserved(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        foreign = self.root / 'foreign-skill'
        foreign.mkdir()
        target.unlink()
        target.symlink_to(foreign)
        result = self.sync('codex')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Conflict:', result.stderr)
        self.assertEqual(target.readlink(), foreign)

    def test_dangling_managed_skill_is_pruned_then_reinstalled(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        missing = self.repository / 'skills' / '.missing-skill-for-test'
        target.unlink()
        target.symlink_to(missing)
        self.assertFalse(target.exists())
        result = self.sync('codex')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.readlink(), skill)

    def test_remove_uninstalls_managed_skill(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        self.assertTrue(target.is_symlink())
        environment = dict(os.environ, TASK_TEST_ROOT=str(self.root),
                           TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'),
                           TASK_SKILL=skill.name)
        result = subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_available() { [[ "$1" == codex ]]; }
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            remove_managed_skill "$TASK_SKILL" codex
            '''], env=environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
