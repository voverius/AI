---
name: nemo-code
description: >-
  Software development: implementation, TDD, debugging, verification, and code review. Use when
  coding, fixing bugs, writing tests, reviewing diffs/PRs, or initializing code mode. Not for
  critique of docs/plans/skills (nemo-critique) or skill-package authoring (nemo-skill). Apply
  nemo-general for voice. Use nemo-project for saved project knowledge; Harmony uses nemo-pkm.
---

# Code
Voice: [nemo-general](../nemo-general/SKILL.md). This skill owns coding procedure only.

## References
- [init](references/init.md) - Initialization-only response and boundaries. Read for code-mode setup
- [orientation](references/orientation.md) - Workspace inspection, scope and implementation choices
  Read before implementation or debugging
- [tdd](references/tdd.md) - Test seams, red-green-refactor, test quality and exceptions. Read for
  behaviour changes. During debugging, apply after reproduction identifies a regression seam
- [implement](references/implement.md) - Minimal changes and edit boundaries. Read when implementing
- [debug](references/debug.md) - Reproduction, hypothesis testing, regression and cleanup. Read for
  debugging before choosing a fix
- [verify](references/verify.md) - Verification scope and completion evidence. Read before
  completing implementation or debugging
- [review](references/review.md) - Separate standards and specification checks, with finding format
  Read for code reviews. Review alone does not authorize edits

No commit/push unless the user asks.
