# Skills

- [nemo-general](nemo-general/SKILL.md) - Default voice for every chat; dialogue +
  actionable shape; init, `rethink`, and `TLDR`
- [nemo-code](nemo-code/SKILL.md) - Code mode: orientation, TDD, implement, debug,
  verify, review; uses nemo-general for voice
- [nemo-pkm](nemo-pkm/SKILL.md) - Harmony PKM mode + book memos; uses nemo-general for
  voice
- [nemo-project](nemo-project/SKILL.md) - Project setup, context selection, knowledge
  distillation, and handovers

From the repository root, run the command for the platform you need. Each command
links all four `nemo-*` skills and the repository's global instructions; it leaves
matching links alone and stops at conflicting files.

Codex:
```bash
./scripts/sync.sh codex
```

All detected platforms:
```bash
./scripts/sync.sh all
```
