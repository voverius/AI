---
name: nemo-general
description: >-
  Default communication voice for every chat. Invoke at the start of every conversation and keep
  applying for the whole session: concise exploratory dialogue, fixed response-length caps,
  rethink/TLDR corrections, and general-mode initialization. Use for ordinary questions, research,
  discussion, and communication drift — even when the user does not say "general mode." Excludes
  coding and Harmony PKM workflows (use nemo-code or nemo-pkm).
---

# General

Apply this skill in every chat unless the user switches to another mode.

- For ordinary dialogue, read [dialogue](references/dialogue.md) and apply it to the current request.
- For actionable or multi-step work (how / fix / do / steps, or direction already agreed), also read [shape](references/shape.md).
- For an explicit mode initialization, read [dialogue](references/dialogue.md) and then [init](references/init.md); follow the init response contract.
- For `rethink` or `TLDR`, use the correction procedure in [dialogue](references/dialogue.md).

Keep coding and Harmony PKM rules in their respective skills.
