---
name: nemo-skill
description: Write, extract, review, refactor, or test agent skills and their references. Use when
             turning a proven workflow into a skill or judging an existing skill setup. This is not 
             for executing the task described by the skill under review.
---

# Skill creation and review
Inspect the requested source, applicable instructions and existing changes. Establish the 
intended users, trigger, inputs, result and authorization boundary from available evidence. Ask 
only about consequential gaps. Reviewing a skill does not activate its target workflow or 
authorize edits.

- **Write or refactor:** read [design](references/design.md). Extract the reusable decisions from real work, 
  including corrections and failures; separate domain-specific examples from general procedure. 
  Edit the maintained source, preserving unrelated work.
- **Review:** apply [design](references/design.md) to actual files and loading routes. Report concrete defects with
  location, consequence and smallest useful correction; distinguish observed failures from 
  untested concerns. Review requests produce findings, not automatic rewrites.
- **Validate packaging:** use [format](references/format.md) before delivery or installation.
- **Test behaviour:** use [testing](references/testing.md) for new workflows, changed triggers or branches, and
  claimed reliability improvements. Minor wording changes need proportionate checks, not a 
  mandatory agent fleet.

Done means the requested artifact or review exists, relevant checks were inspected, and remaining 
limitations are stated. Installation is distinct from source editing; use the existing installer 
when authorized. Report what changed and what tests actually demonstrated.
