---
name: nemo-pkm
description: >-
  Harmony personal knowledge management: initialize PKM mode, follow Harmony local docs, and run
  PKM tasks such as Goodreads book memo preparation. Use at the start of Harmony work or when the
  user asks for PKM, books, or memos. Apply nemo-general for voice. Excludes coding and project
  lifecycle workflows (use nemo-code or nemo-project).
---

# PKM

Apply [nemo-general](../nemo-general/SKILL.md) for voice (dialogue + shape). This skill owns Harmony
PKM procedure only. Harmony's local documentation is authoritative for domain rules.

- For Harmony mode initialization, read [workflow](references/workflow.md) and
  [init](references/init.md); follow the init contract
- For a substantive PKM task, read [workflow](references/workflow.md) and
  [init](references/init.md) (load local docs), then only the task reference needed
- For book memo preparation, read [book-prepare](references/book-prepare.md)

Keep PKM separate from code mode. The active mode lasts until the user switches it.
