---
name: nemo-prompt
description: >-
  Use only when the user explicitly invokes nemo-prompt to refine a goal or task prompt.
  Clarify the intended result through expert judgment, original evidence, suitable methods and
  independent verification without expanding scope. Revise the prompt, then execute the task unless
  the user explicitly asks for the prompt only. Ordinary tasks and generic requests to improve
  wording do not activate this skill.
disable-model-invocation: true
---

# Prompt improvement
Use `nemo-general` for communication preferences.

## Invocation and input
Run only on an explicit user invocation, such as `$nemo-prompt`, `/nemo-prompt` or
"use nemo-prompt". A mention in quoted material, a request to review this skill or a broad task is
not an invocation. This skill refines the task before handing it to the appropriate execution
workflow, unless the user explicitly requests prompt-only output.

Use the task supplied with the invocation. Otherwise use the preceding substantive user task or
the task the user points to in the conversation. Do not rewrite the invocation itself, combine
unrelated earlier tasks or invent a missing request. If the target task is absent or ambiguous,
ask one focused question and wait.

## Refinement
Use the available conversation and supplied material. Identify the intended outcome, explicit
constraints and any requested deliverable. Distinguish the user's desired result from a suggested
way to achieve it. Make a broad goal concrete without silently choosing an architecture,
replacing the goal or shrinking it to an easier task.

Keep explicit requirements and the user's freedom to choose. Do not strengthen preferences into
absolute bans, add unrequested deliverables or narrow the goal to a diagnostic example. Surface
conflicts and consequential trade-offs. If a missing user decision would materially change the
goal or scope, ask one focused question before rewriting.
Missing execution inputs can remain instructions to obtain them in the rewritten prompt, rather
than blocking refinement or inventing facts, access, measurements or commitments.

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

Use these lenses to find material improvements, not to fill four compulsory sections. Prefer
concrete decisions and checks over claims about what a "top professional" would do. Use original
material where it changes the result, and name methods or tools only when their contribution is
clear. Treat subjective quality as judgment rather than claiming a test can prove it.

## Result and continuation
Produce one self-contained, ready-to-use task prompt in the user's direct style. Include the
context, outcome, constraints, relevant approach and completion evidence needed for that task.
Keep the detail proportionate to the goal. Do not make an already adequate prompt longer just to
demonstrate the skill.

Make the rewritten prompt request the work itself, not another round of prompt improvement.
Carry material uncertainty into it. Do not turn optional ideas into requirements or imply that
supplied facts have been independently verified.

By default, briefly explain consequential refinements, show the revised prompt, then immediately
start carrying it out in the same task. Load the execution workflow appropriate to the work and
continue through its result and verification. Do not end the turn at the rewritten prompt or ask
the user to resubmit or approve it. After clarification answers, incorporate them into the revised
prompt and continue execution. If no rewrite is useful, execute the adequate original task.

If the user clearly asks only for the prompt, such as "give me the new prompt", "rewrite this for
another chat" or "do not execute", return only one fenced Markdown block containing the revised
prompt and stop. Omit explanations and do not execute the task. A task that asks to draft an email
or document is not by itself a request for prompt-only output.

Refinement does not expand authorization. Preserve explicit review, planning and approval
boundaries. Execution can inspect inputs and use tools as the task permits, but the rewritten
prompt cannot authorize new external actions or broader access. Do not save the prompt itself
unless the user asks.

