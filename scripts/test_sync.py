
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

    def sync(self, platform, answer=''):
        environment = dict(os.environ, TASK_TEST_ROOT=str(self.root), TASK_PLATFORM=platform,
                           TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'))
        return subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_instructions_path() { printf '%s\\n' "$TASK_TEST_ROOT/rules/$1.mdc"; }
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            sync_tool "$TASK_PLATFORM"
            '''], env=environment, input=answer, text=True, capture_output=True)

    def test_all_detects_codex_desktop_without_cli(self):
        for marker in ('.codex', 'Applications/Codex.app'):
            with self.subTest(marker=marker):
                directory = self.root / marker
                directory.mkdir(parents=True)
                environment = dict(os.environ, TASK_TEST_ROOT=str(self.root),
                                   TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'))
                result = subprocess.run(['bash', '-c', '''
                    source "$TASK_SYNC_SCRIPT" help >/dev/null
                    # Redirect home-directory probes without changing the real HOME.
                    definition="$(declare -f tool_available)"
                    eval "${definition//\\$HOME/\\$TASK_TEST_ROOT}"
                    command() { [[ "$1" != -v ]] && builtin command "$@"; }
                    tool_instructions_path() { printf '%s\\n' "$TASK_TEST_ROOT/rules/$1.mdc"; }
                    tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
                    main all
                    '''], env=environment, input='', text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((self.root / 'rules/codex.mdc').resolve(),
                                 self.repository / 'AGENTS.md')
                for skill in (self.repository / 'skills').glob('nemo-*'):
                    self.assertEqual((self.root / 'skills/codex' / skill.name).resolve(), skill)
                directory.rmdir()

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

    def test_instruction_replacement_requires_confirmation(self):
        for platform in ('claude', 'codex', 'cursor'):
            for answer in ('n\n', '', 'y\n', '\n'):
                with self.subTest(platform=platform, answer=answer):
                    target = self.root / f'rules/{platform}.mdc'
                    target.parent.mkdir(exist_ok=True)
                    target.write_text('Existing instructions')
                    result = self.sync(platform, answer)
                    self.assertIn('[Y/n]', result.stderr)
                    if answer in ('n\n', ''):
                        self.assertNotEqual(result.returncode, 0)
                        self.assertEqual(target.read_text(), 'Existing instructions')
                    else:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        if platform == 'cursor':
                            self.assertIn('alwaysApply: true', target.read_text())
                        else:
                            self.assertEqual(target.readlink(), self.repository / 'AGENTS.md')
                    target.unlink()

    def test_confirmed_foreign_instruction_link_preserves_source(self):
        original = self.root / 'original-instructions'
        original.write_text('Keep the original source')
        for platform in ('claude', 'codex', 'cursor'):
            with self.subTest(platform=platform):
                target = self.root / f'rules/{platform}.mdc'
                target.parent.mkdir(exist_ok=True)
                target.symlink_to(original)
                result = self.sync(platform, 'Y\n')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(original.read_text(), 'Keep the original source')
                if platform == 'cursor':
                    self.assertFalse(target.is_symlink())
                else:
                    self.assertEqual(target.readlink(), self.repository / 'AGENTS.md')

    def test_confirmed_foreign_skill_link_is_replaced(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        foreign = self.root / 'foreign-skill'
        foreign.mkdir()
        target.unlink()
        target.symlink_to(foreign)
        result = self.sync('codex', 'y\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(target.readlink(), skill)
        self.assertTrue(foreign.is_dir())

    def test_all_continues_after_declined_replacement(self):
        for platform in ('claude', 'codex', 'cursor'):
            target = self.root / f'rules/{platform}.mdc'
            target.parent.mkdir(exist_ok=True)
            target.write_text('Existing instructions')
        environment = dict(os.environ, TASK_TEST_ROOT=str(self.root),
                           TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'))
        result = subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_available() { return 0; }
            tool_instructions_path() { printf '%s\\n' "$TASK_TEST_ROOT/rules/$1.mdc"; }
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            main all
            '''], env=environment, input='y\nn\ny\n', text=True, capture_output=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual((self.root / 'rules/claude.mdc').readlink(),
                         self.repository / 'AGENTS.md')
        self.assertEqual((self.root / 'rules/codex.mdc').read_text(), 'Existing instructions')
        self.assertIn('alwaysApply: true', (self.root / 'rules/cursor.mdc').read_text())
        for platform in ('claude', 'codex', 'cursor'):
            for skill in (self.repository / 'skills').glob('nemo-*'):
                self.assertEqual((self.root / 'skills' / platform / skill.name).resolve(), skill)

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
        stale = next(p for p in (self.repository / 'skills').glob('nemo-*') if p != skill)
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

    def test_equivalent_link_representations_leave_every_entry_unchanged(self):
        for platform in ('claude', 'codex', 'cursor'):
            with self.subTest(platform=platform):
                self.assertEqual(self.sync(platform).returncode, 0)
                targets = list((self.root / 'skills' / platform).iterdir())
                if platform != 'cursor':
                    targets.append(self.root / 'rules' / f'{platform}.mdc')
                alias = self.root / f'{platform}-repo-alias'
                alias.symlink_to(self.repository, target_is_directory=True)
                for target in targets:
                    source = target.resolve()
                    target.unlink()
                    target.symlink_to(os.path.relpath(alias / source.relative_to(self.repository),
                                                     target.parent))
                before = {p: (p.readlink(), p.lstat().st_ino, p.lstat().st_mtime_ns)
                          for p in targets}
                result = self.sync(platform)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, '')
                self.assertEqual(result.stderr, '')
                self.assertEqual(before, {p: (p.readlink(), p.lstat().st_ino,
                                              p.lstat().st_mtime_ns) for p in targets})

    def test_equal_instruction_copy_explains_propagation_difference(self):
        target = self.root / 'rules/codex.mdc'
        target.parent.mkdir()
        target.write_bytes((self.repository / 'AGENTS.md').read_bytes())
        result = self.sync('codex')
        self.assertEqual(result.returncode, 1)
        self.assertIn('content matches', result.stderr)
        self.assertIn('follow future', result.stderr)
        self.assertFalse(target.is_symlink())
        self.assertEqual(self.sync('codex', 'y\n').returncode, 0)
        before = target.lstat()
        result = self.sync('codex')
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '', ''))
        self.assertEqual(target.lstat().st_mtime_ns, before.st_mtime_ns)

    def test_cursor_legacy_relative_link_and_equivalent_wrapper(self):
        target = self.root / 'rules/cursor.mdc'
        target.parent.mkdir()
        target.symlink_to(os.path.relpath(self.repository / 'AGENTS.md', target.parent))
        result = self.sync('cursor')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        alias = self.root / 'rules-alias.md'
        alias.symlink_to(self.repository / 'AGENTS.md')
        target.write_text('---\nalwaysApply: true\n---\n\n'
                          f'Read and follow [the global agent rules](<{alias}>) before working.\n\n')
        before = target.stat().st_mtime_ns
        result = self.sync('cursor')
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '', ''))
        self.assertEqual(target.stat().st_mtime_ns, before)

    def test_foreign_equal_file_link_requires_propagation_choice(self):
        target = self.root / 'rules/claude.mdc'
        target.parent.mkdir()
        foreign = self.root / 'foreign.md'
        foreign.write_bytes((self.repository / 'AGENTS.md').read_bytes())
        target.symlink_to(foreign)
        result = self.sync('claude')
        self.assertEqual(result.returncode, 1)
        self.assertIn('follow future', result.stderr)
        self.assertEqual(target.readlink(), foreign)

    def test_parent_failure_never_prompts_for_replacement(self):
        (self.root / 'rules').write_text('not a directory')
        for platform in ('claude', 'codex', 'cursor'):
            result = self.sync(platform, 'y\n')
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('[Y/n]', result.stderr)
            self.assertEqual((self.root / 'rules').read_text(), 'not a directory')

    def test_link_to_a_hardlinked_copy_needs_a_propagation_choice(self):
        foreign = self.root / 'hardlinked-rules.md'
        foreign.hardlink_to(self.repository / 'AGENTS.md')
        target = self.root / 'rules/codex.mdc'
        target.parent.mkdir()
        target.symlink_to(foreign)
        result = self.sync('codex')
        self.assertEqual(result.returncode, 1)
        self.assertIn('follow future', result.stderr)
        self.assertEqual(target.readlink(), foreign)

    def test_cursor_extra_instruction_is_a_real_choice(self):
        self.assertEqual(self.sync('cursor').returncode, 0)
        target = self.root / 'rules/cursor.mdc'
        content = target.read_text() + '\nKeep this local policy.\n'
        target.write_text(content)
        result = self.sync('cursor', 'n\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('[Y/n]', result.stderr)
        self.assertEqual(target.read_text(), content)

    def test_directory_link_with_dot_or_trailing_slash_is_unchanged(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        for suffix in ('/.', '/'):
            with self.subTest(suffix=suffix):
                target.unlink()
                target.symlink_to(str(skill) + suffix)
                before = target.lstat().st_mtime_ns
                result = self.sync('codex')
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '', ''))
                self.assertEqual(target.lstat().st_mtime_ns, before)

    def test_relative_managed_repoint_and_remove(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skills = list((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skills[0].name
        target.unlink()
        target.symlink_to(os.path.relpath(skills[1], target.parent))
        result = self.sync('codex')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Relink:', result.stdout)
        target.unlink()
        target.symlink_to(os.path.relpath(skills[0], target.parent))
        environment = dict(os.environ, TASK_TEST_ROOT=str(self.root),
                           TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'),
                           TASK_SKILL=skills[0].name)
        result = subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            remove_managed_skill "$TASK_SKILL" codex
            remove_managed_skill "$TASK_SKILL" codex
            '''], env=environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('Remove:'), 1)
        self.assertFalse(target.is_symlink())

    def test_prefix_with_parent_escape_is_foreign_and_loops_are_preserved(self):
        self.assertEqual(self.sync('codex').returncode, 0)
        skill = next((self.repository / 'skills').glob('nemo-*'))
        target = self.root / 'skills/codex' / skill.name
        target.unlink()
        foreign_path = str(self.repository / 'skills') + '/../../foreign-skill'
        target.symlink_to(foreign_path)
        result = self.sync('codex')
        self.assertEqual(result.returncode, 1)
        self.assertIn('[Y/n]', result.stderr)
        self.assertEqual(str(target.readlink()), foreign_path)
        target.unlink()
        target.symlink_to(target.name)
        result = self.sync('codex')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(str(target.readlink()), target.name)

    def test_remove_rejects_names_that_escape_the_skill_directory(self):
        environment = dict(os.environ, TASK_SYNC_SCRIPT=str(self.repository / 'scripts/sync.sh'),
                           TASK_TEST_ROOT=str(self.root))
        result = subprocess.run(['bash', '-c', '''
            source "$TASK_SYNC_SCRIPT" help >/dev/null
            tool_skills_path() { printf '%s\\n' "$TASK_TEST_ROOT/skills/$1"; }
            remove_managed_skill 'nemo-x/../../elsewhere' codex
            '''], env=environment, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('skill names', result.stderr)

    def test_cursor_equivalent_markdown_link_and_line_endings_are_unchanged(self):
        self.assertEqual(self.sync('cursor').returncode, 0)
        target = self.root / 'rules/cursor.mdc'
        for newline in ('\n', '\r\n'):
            with self.subTest(newline=newline):
                content = ('---\nalwaysApply: true\n---\n\nRead and follow '
                           f'[the global agent rules]({self.repository}/AGENTS.md) before working.\n\n')
                target.write_bytes(content.replace('\n', newline).encode())
                before = target.stat().st_mtime_ns
                result = self.sync('cursor')
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, '', ''))
                self.assertEqual(target.stat().st_mtime_ns, before)


if __name__ == '__main__':
    unittest.main()
