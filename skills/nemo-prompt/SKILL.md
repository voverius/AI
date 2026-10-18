---
name: nemo-prompt
description: >-
  Deepen a task prompt without expanding its scope. Use when asked to improve a prompt through
  expert judgment, original evidence, suitable methods and independent verification. Produce a
  rewritten prompt before execution. Skill creation and review use nemo-skill.
---

# Prompt improvement

Use `nemo-general` for communication preferences.

Before rewriting the user's task prompt, identify how to make the work deeper without expanding
its scope. Keep the intended outcome, constraints and deliverable fixed.

Examine:

1. **Expert judgment:** What consequential decision, assumption or failure would an experienced
   practitioner address that the prompt overlooks? Explain why it matters here
2. **Source material:** What original evidence or direct observation would they start from?
   Explain what supplied summaries might conceal, and whether returning to the source would
   materially improve this task
3. **Method:** What specific methods and tools would help resolve those issues? Explain what each
   contributes. Do not add tools merely to make the process look rigorous
4. **Verification:** What observable evidence, test or independent standard could support or
   contradict the result? Distinguish what can be checked from what remains a judgment call

Recommend only changes that materially improve this task. If something is already adequate, say
so. Do not invent missing facts or assume access to unavailable evidence.

Then rewrite the prompt to incorporate those changes as concrete instructions. Preserve its scope,
flag consequential missing inputs, and stop before executing the rewritten prompt.

