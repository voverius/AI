---
name: nemo-project
description: Maintain project knowledge across chats. Use for project setup, saved-context questions, investigations, source intake, knowledge audits or repairs, and handovers. Supports planning and knowledge for external code repositories; code implementation and personal knowledge management use their own workflows.
---

# Project knowledge

Use `nemo-general` for voice. This skill manages project information, not the external systems it describes. Reviewing this skill does not execute its project workflow.

## Resolve the project

Use the user's explicit project location; otherwise use the current project's entry files, including an enclosing project when working in a subdirectory. A name alone does not authorize inventing a path. If the location is ambiguous, ask before writing. Never relocate an existing project or create a second tree to match a naming convention.

Once when selecting a root: resolve its real path, confirm it is a readable directory, check writability for requested writes, and orient from README or AGENTS. Recheck only when the root, access or requested operation changes. On failure, report the path and failed check; do not use another directory silently. For explicitly requested creation, verify the destination's existing parent is writable, create the authorized directory, then check the resulting root. Empty roots need explicit setup intent.

## Select the work

- **Question or continuation:** read README, the knowledge index when present, and only relevant subjects or the handover matching the requested task. Search index cues, then likely branches; broaden only if necessary. Cite saved knowledge and verify changing external facts before action. Ordinary questions, reviews and audits are read-only unless changes are authorized.
- **Setup, structural repair or knowledge audit:** read [init](references/init.md). An audit reports defects; repair requires authorization.
- **Save findings or process inputs:** read [distill](references/distill.md) and [knowledge](references/knowledge.md) before changing content. Save new useful findings from authorized project work at its substantive boundary; an unchanged answer needs no new record.
- **Pause, transfer or unfinished work:** read [capture](references/capture.md). Preserve durable findings first when applicable. Completion alone does not require a handover.

Continue using relevant guidance throughout the task; do not reload every branch on every turn. After context loss, recover the task from the project entry and relevant saved state. Installation and discovery belong to the host, not project-local skill copies.
