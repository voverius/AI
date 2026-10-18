---
name: nemo-code
description: >-
  Software development: implementation, TDD, debugging, verification, and code review. Use when
  coding, fixing bugs, writing tests, reviewing diffs/PRs, or initializing code mode. Not for
  critique of docs/plans (nemo-critique) or skill-package authoring/review (nemo-skill). Apply
  nemo-general for voice. Use nemo-project for saved project knowledge. Personal libraries use
  nemo-pkm.
---

# Code
Voice: nemo-general. This skill owns coding procedure only.

Commit and push only when the user asks, as the global agent rules require.

## References
- [workflow](references/workflow.md) - Workspace inspection, minimal edits, and verification
  Required read before implementation or debugging
- [tdd](references/tdd.md) - Test seams, red-green-refactor, test quality, and exceptions
  Required read before any production edit for implementation and debugging. The only skips are
  the exceptions listed in tdd.md
- [debug](references/debug.md) - Reproduction, hypothesis testing, regression, and cleanup
  Required read for a bug fix, before choosing the fix
- [review](references/review.md) - Separate standards and specification checks, with finding format
  Read for code reviews. Review alone does not authorize edits

Initialization-only: read the nemo-general init reference and reply with the code-mode string.
Do not load the references above.

