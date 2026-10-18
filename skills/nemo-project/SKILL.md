---
name: nemo-project
description: >-
  Maintain project knowledge across chats. Use for project setup, saved-context questions,
  investigations, deliverables, source intake, knowledge audits or repairs, and handovers. Supports
  planning and knowledge for external code repositories. Code implementation and work inside a
  selected personal knowledge library use their own workflows.
---

# Project knowledge
Use `nemo-general` for voice. This skill manages project information, not the external systems it
describes. Reviewing this skill does not execute its project workflow. It maintains a linked wiki
and continuation state so a later agent can find relevant knowledge, understand evidence limits and
resume unfinished work. A read-only answer or audit can finish without changing project files.

## Routes
Combine routes when needed. Load only the references named below. External implementation or
sending a result needs its own authorization. When consulting an external repository, follow its
instructions and link the authoritative files.
Before authoring project Markdown, read nemo-general's Markdown reference.

- [resolve](references/resolve.md) - Project root selection
  Required. Resolve the root from the request and operating contract before reading subjects or
  making project changes
- [retrieve](references/retrieve.md) - Questions, continuation, and investigation
  Required read before answering a question, resuming a continuation, or investigating
- [knowledge](references/knowledge.md) - Page standard, file roles, ownership, and evidence
  Read before a knowledge audit or any project change, including handovers and task cleanup
- [distill](references/distill.md) - Findings, merges, and intake
  Read with knowledge.md when saving a useful finding. An unchanged answer needs no record
- [capture](references/capture.md) - Handover contents and closure
  Read for a pause, a transfer, unfinished work, or closure of an existing matching handover.
  Completion alone does not require a new handover
- [check](references/check.md) - Navigation checker
  Read after a project write. Skip it on a read-only route
- [init](references/init.md) - Setup, audit, repair, and migration
  Read for structural work or a knowledge audit. Audits report defects. Repair needs authorization

For authorized maintenance, distill new useful findings and apply the cleanup rules in knowledge.md.
Read-only questions and audits finish with the answer or findings, without project writes or cleanup.

Keep using the relevant guidance through the task. Do not reload every branch on every turn. After
context loss, recover the task from the project entry and saved state. Installation and discovery
belong to the host, not a project-local skill copy.

