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
describes. Reviewing this skill does not execute its project workflow. The result is a maintained,
linked wiki of generalized knowledge, not a saved research reply.

## Routes
Combine routes when needed. Load only the references named below. External implementation or
sending a result needs its own authorization. When consulting an external repository, follow its
instructions and link the authoritative files.

- [resolve](references/resolve.md) - Project root selection
  Required. Open this file before any file under the project root
- [retrieve](references/retrieve.md) - Questions, continuation, and investigation
  Required read before answering a question, resuming a continuation, or investigating
- [knowledge](references/knowledge.md) - Page standard, file roles, ownership, and evidence
  Read before changing a subject, its index, or a deliverable. When that file is Markdown, also
  read nemo-general markdown.md before saving
- [distill](references/distill.md) - Findings, merges, and intake
  Read with knowledge.md when saving a useful finding. An unchanged answer needs no record
- [capture](references/capture.md) - Handover contents and closure
  Read for a pause, a transfer, or unfinished work. On finish, read it only when continuation
  remains. Completion alone does not require a handover
- [check](references/check.md) - Navigation checker
  Read after a project write. Skip it on a read-only route
- [init](references/init.md) - Setup, audit, repair, and migration
  Read for structural work or a knowledge audit. Audits report defects. Repair needs authorization

Finish a task by distilling reusable findings, then applying the cleanup rules in knowledge.md.

Keep using the relevant guidance through the task. Do not reload every branch on every turn. After
context loss, recover the task from the project entry and saved state. Installation and discovery
belong to the host, not a project-local skill copy.

