---
name: init-pkm
description: >-
  Activate the isolated Harmony PKM mode and silently load its local documentation. Use at the start
  of a Harmony chat or before any PKM task.
---

# Harmony PKM Mode

Apply this mode for the remainder of the session unless the user explicitly switches modes.

## Boundary

- Apply PKM domain behavior only from `pkm-*` skills. Neutral tooling skills may still be used when
  the task requires them.
- Do not apply coding workflows, TDD, repository implementation rules, or coding review conventions.
- Do not apply exploratory general-dialogue rules unless the user explicitly requests them.
- Continue to follow universal safety, concision, and truthfulness rules.
- Treat Harmony as the active workspace and follow its local documentation as authoritative PKM
  context.

## Initialization

Read every Markdown document directly inside `Envoy/Docs/` in one bulk read.

Do not inspect other paths, write files, or emit progress updates. After reading succeeds, reply
exactly: `Harmony initialized.`
