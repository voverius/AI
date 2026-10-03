---
name: nemo-project
description: >-
  Maintain project knowledge across chats. Use for project setup, saved-context questions,
  investigations, source intake, knowledge audits or repairs, and handovers. Supports planning and
  knowledge for external code repositories. Code implementation and personal knowledge management
  use their own workflows.
---

# Project knowledge
Use `nemo-general` for voice. This skill manages project information, not the external systems it
describes. Reviewing this skill does not execute its project workflow.

## Resolve the project
Use the user's explicit project location. Otherwise use the current project's entry files, including
an enclosing project when working in a subdirectory. A name alone does not authorize inventing a
path. If the location is ambiguous, ask before writing. Never relocate an existing project or create
a second tree to match a naming convention.

Once when selecting a root: resolve its real path, confirm it is a readable directory, check
writability for requested writes, and orient from README or AGENTS. Recheck only when the root,
access or requested operation changes. On failure, report the path and failed check. Do not use
another directory silently. For explicitly requested creation, verify the destination's existing
parent is writable, create the authorized directory, then check the resulting root. Empty roots need
explicit setup intent.

## Select the work
- **Question or continuation:** read README, the knowledge index when present, and only relevant
  subjects or the handover matching the requested task. Search index cues, then likely branches
  Broaden only if necessary. Cite saved knowledge and verify changing external facts before action
  Ordinary questions, reviews and audits are read-only unless changes are authorized
- [init](references/init.md) - Project setup, contract template, audit, repair and migration
  Read for structural work or knowledge audits. Audits report defects. Repair requires authorization
- [knowledge](references/knowledge.md) - File roles, subject ownership, evidence and navigation
  Read before changing content or structure
- [distill](references/distill.md) - Extracting findings, merging knowledge and processing inputs
  Read with knowledge when saving useful findings from authorized work at a substantive boundary
  Unchanged answers need no record
- [capture](references/capture.md) - Handover contents, continuation checks and closure
  Read for pauses, transfers or unfinished work. Preserve durable findings first when applicable
  Completion alone does not require a handover

Continue using relevant guidance throughout the task. Do not reload every branch on every turn.
After context loss, recover the task from the project entry and relevant saved state. Installation
and discovery belong to the host, not project-local skill copies.

