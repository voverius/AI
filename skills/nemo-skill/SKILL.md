---
name: nemo-skill
description: Write, extract, review, refactor, or test agent skills and their references. Use when
             turning a proven workflow into a skill or judging an existing skill setup. This is not
             for executing the task described by the skill under review.
---

# Skill creation and review
Use `nemo-general` for communication preferences.
Inspect the requested source, applicable instructions and existing changes. Establish the
intended users, trigger, inputs, result and authorization boundary from available evidence. Ask
only about consequential gaps. Reviewing a skill does not activate its target workflow or
authorize edits.

- [design](references/design.md) - Task coverage, dependencies, ownership and concise instructions
  Read when writing, refactoring or reviewing. Extract reusable decisions from real work, including
  corrections and failures. Preserve unrelated work. Reviews report concrete defects, consequences
  and smallest useful corrections, distinguishing observed failures from untested concerns
- [format](references/format.md) - Package structure, metadata, links and installation boundaries
  Read before delivery or installation
- [testing](references/testing.md) - Branch tests, version checks and completion evidence
  Read for new workflows, changed triggers or branches, and claimed reliability improvements
  Minor wording changes need proportionate checks

Done means the requested artifact or review exists, relevant checks were inspected, and remaining
limitations are stated. Installation is distinct from source editing; use the existing installer
when authorized. Report what changed and what tests actually demonstrated.
