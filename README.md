# Personal AI Control Plane

This repository is the version-controlled source of truth for personal AI rules, skills, and tool
setup. Clone it on a new machine, sync it into supported AI tools, and keep behavioral changes here
instead of editing tool-managed copies.

It supports three isolated modes and one project workflow:

- `nemo-general` - default voice for every chat; concise general reasoning and discussion
- `nemo-code` - software development and code review; its init reference activates code mode
- `nemo-pkm` - Harmony PKM mode and book preparation; voice from `nemo-general`
- `nemo-project` - project setup, operation, knowledge distillation, and handover

Only one mode should be active at a time. Universal concision, truthfulness, authorization, and
safety rules always apply; domain-specific workflows must stay inside their mode.

Each `nemo-*` skill is a discoverable entry point with focused references. Earlier comparison
skills (`init-code`, `project-workflow/`) may remain in the repository; sync installs only
`nemo-*` skills. `init-general` / `init-pkm` / `pkm-book-prepare` are retired in favor of the
matching `nemo-*` skills.

## Repository Map

- `AGENTS.md` - universal rules shared across tools and repositories
- `skills/` - canonical session modes and reusable task skills
- `scripts/` - setup and synchronization commands
- `manifests/` - recorded tools, plugins, skills, sources, and ownership
- `docs/` - architecture and rollout plans for coding and PKM workflows
- `hooks/` - deterministic safety enforcement
- `templates/` - reusable repository-level context and documentation templates

Repository-local `AGENTS.md` files may add project context and commands, but must not weaken global
safety rules. PKM content remains outside this repository; this repository owns only its operating
rules and skills. Never store credentials, sessions, caches, or machine-local state here.

## Scripts

`sync.sh` symlinks canonical instructions and repository skills into the selected AI tool:

```bash
./scripts/sync.sh codex
```

Supported targets are `codex`, `cursor`, `claude`, and `all`:

```bash
./scripts/sync.sh all
```

`all` syncs only detected tools. The script creates missing configuration directories, leaves
matching links unchanged, and refuses to overwrite existing files or conflicting links.
