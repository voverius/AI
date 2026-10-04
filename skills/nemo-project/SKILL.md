---
name: nemo-project
description: >-
  Maintain project knowledge across chats. Use for project setup, saved-context questions,
  investigations, deliverables, source intake, knowledge audits or repairs, and handovers. Supports
  planning and knowledge for external code repositories. Code implementation and personal knowledge
  management use their own workflows.
---

# Project knowledge
Use `nemo-general` for voice. This skill manages project information, not the external systems it
describes. Reviewing this skill does not execute its project workflow.

## Resolve the project
Project knowledge lives at `~/Projects/<project>/`. Select that root from the user's project name or
accessible project directories. With `~/Projects/AI` and `~/Repos/ai` available, the former is the
knowledge project and the latter is an external repository, regardless of the tool's working
directory. A repository's AGENTS.md governs repository work, not the knowledge project's identity.
If several canonical projects fit, ask which one before reading subjects or writing. If the named
root is missing, report it. Create it only for an authorized bootstrap request.

Resolve symbolic links before treating two paths as separate projects. Existing knowledge outside
`~/Projects/` requires an explicit migration decision: identify it and report the mismatch without
creating a parallel tree, silently moving files or adopting the old location as the new default.

Once when selecting a root: resolve its real path, confirm it is a readable directory, check
writability for requested writes, and orient from README or AGENTS. Recheck only when the root,
access or requested operation changes. On failure, report the path and failed check. Do not use
another directory silently. For explicitly requested creation, verify the destination's existing
parent is writable, create the authorized directory, then check the resulting root. Empty roots need
explicit setup intent.

## Select the work
Orient from README and the relevant index or task state for every route. Load knowledge before
content or structure changes, including deliverables and handovers, and when auditing those rules.
Combine routes when the request needs them. Load only their required references.

- **Question or continuation:** read README, the knowledge index when present, and only relevant
  subjects or the handover matching the requested task. Search index cues, then likely branches
  Broaden only if necessary. Include a source-subject link in factual answers and verify changing
  external facts before action
  Ordinary questions, reviews and audits are read-only unless changes are authorized
- **Investigate, plan or produce a deliverable:** use relevant saved knowledge and necessary sources
  Separate supported findings, proposals and unresolved questions. Create a deliverable only when
  requested, using outputs/ or its mapped equivalent unless the user specifies another destination
  or a chat-only answer. Check the result against its purpose and supporting evidence. For a
  saved project output, verify a working README link to its directory before completion. Update an
  existing role cue rather than adding a duplicate. A plain directory name is not a link. Save new
  reusable findings through distill and capture unfinished work when needed. Do not create duplicate
  knowledge for an output that only restates existing material. External implementation or sending
  the result requires its own authorization and appropriate workflow. When consulting external
  repositories, follow their local instructions and retain links to authoritative files
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

After project writes, run [check_navigation](scripts/check_navigation.py) from the installed skill:
`python3 scripts/check_navigation.py <project-root>`. Repair reported defects within scope. The
checker reads files only: it checks core files, standard role links, README scope and subject
reachability. If Python is unavailable, perform those checks manually. Mapped optional roles and
knowledge quality still need review.

Continue using relevant guidance throughout the task. Do not reload every branch on every turn.
After context loss, recover the task from the project entry and relevant saved state. Installation
and discovery belong to the host, not project-local skill copies.
