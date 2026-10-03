---
name: nemo-code
description: >-
  Software development mode: implementation, TDD, debugging, verification, and code review in the
  user's repositories. Use when coding, fixing bugs, writing tests, reviewing diffs/PRs, or when
  asked to initialize code mode. Apply nemo-general for voice. Excludes Harmony PKM and project
  lifecycle workflows (use nemo-pkm or nemo-project).
---

# Code

Apply [nemo-general](../nemo-general/SKILL.md) for voice (dialogue + shape). This skill owns coding procedure only.

- For code-mode initialization, read [workflow](references/workflow.md) and [init](references/init.md); follow the init contract.
- For implementation, read [workflow](references/workflow.md), then [orientation](references/orientation.md), [tdd](references/tdd.md), [implement](references/implement.md), and [verify](references/verify.md).
- For debugging, read [workflow](references/workflow.md), then [orientation](references/orientation.md) and [debug](references/debug.md); use [tdd](references/tdd.md) for the regression test once a seam exists.
- For a requested code review, read [review](references/review.md); load [workflow](references/workflow.md) only if edits are also requested.

Keep code mode separate from PKM. Do not commit or push unless the user explicitly asks.
