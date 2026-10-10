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
describes. Reviewing this skill does not execute its project workflow.

The result is a maintained, linked wiki of generalized knowledge, not a saved research reply.
Subject pages must follow the page standard and link boundaries in knowledge.md, including on a
cold start. Preserve the useful explanation locally and keep authoritative source references brief.

## Resolve the project
Create new projects at `~/Projects/<project>/`. Existing projects elsewhere are valid legacy work.
Use their established root without requiring migration. Select the project from the user's request
and its local contract. Implementation repositories remain external to that knowledge root,
regardless of the tool's working directory. A repository's AGENTS.md governs repository work, not
the knowledge project's identity.
If several projects fit, ask which one before reading subjects or writing. If the named
root is missing, report it. Create it only for an authorized bootstrap request.

Resolve symbolic links before treating two paths as separate projects. Keep one knowledge root.
Do not create a parallel tree or move existing work unless migration is requested.

Once when selecting a root: resolve its real path, confirm it is a readable directory, check
writability for requested writes, and orient from README or AGENTS. Recheck only when the root,
access or requested operation changes. On failure, report the path and failed check. Do not use
another directory silently. For explicitly requested creation, verify the destination's existing
parent is writable, create the authorized directory, then check the resulting root. Empty roots need
explicit setup intent.

Use absolute project paths or an explicit project working directory for every write. The tool's
default directory may still be an external repository. Earlier commands do not change that default.

## Select the work
Orient from README and the relevant index or task state for every route. Load knowledge before
content or structure changes, including deliverables and handovers, and when auditing those rules.
Combine routes when the request needs them. Load only their required references.

- **Question or continuation:** read README, the knowledge index when present, and only relevant
  subjects or the handover matching the requested task. Search index cues, then likely branches
  Broaden only if necessary. Include a source-subject link in factual answers. Follow its provenance
  to verify living-source claims when the answer or next step needs current state, including in a
  fresh chat. On access failure, state what remains unverified. Saved state is not a fallback truth
  Ordinary questions, reviews and audits are read-only unless changes are authorized
- **Investigate or plan:** use relevant saved knowledge and necessary sources. Separate supported
  findings, proposals and unresolved questions. Save new reusable findings through distill and
  capture unfinished work when needed. Discussion alone does not require a deliverable
- **Produce a requested deliverable:** write the artifact in outputs/ or its mapped equivalent,
  unless the user specifies another destination or a chat-only answer. Check its contents against
  the request and supporting evidence, verify the saved file exists, and return its link. Link the
  populated directory from README using its existing role cue, without listing individual files
  An output may summarize knowledge without becoming another owner of reusable claims

External implementation or sending a result requires its own authorization and appropriate workflow.
When consulting external repositories, follow their local instructions and link authoritative files.
- [init](references/init.md) - Project setup, contract template, audit, repair and migration
  Read for structural work or knowledge audits. Audits report defects. Repair requires authorization
- [knowledge](references/knowledge.md) - Page structure, density, link boundaries, ownership and
  evidence
  Read before changing content or structure
- [distill](references/distill.md) - Extracting findings, merging knowledge and processing inputs
  Read with knowledge when saving useful findings from authorized work at a substantive boundary
  Unchanged answers need no record
- [capture](references/capture.md) - Handover contents, continuation checks and closure
  Read for pauses, transfers or unfinished work. Preserve durable findings first when applicable
  Completion alone does not require a handover

After project writes, run [check_navigation](scripts/check_navigation.py) with an absolute script
path from the installed skill (resolve the `nemo-project` symlink), for example:
`python3 ~/.cursor/skills/nemo-project/scripts/check_navigation.py <project-root>`.
Do not run `scripts/check_navigation.py` relative to the project root. Repair reported defects
within scope. The checker reads files only: it checks core files, standard role links, README
scope, subject reachability and common Markdown link paths in docs, outputs and handovers. It does
not verify anchors, claim quality, ownership or safety of recommendations. If Python is unavailable,
perform those checks manually. Mapped optional roles still need review.

Before delivery, read changed subjects as standalone knowledge against knowledge.md. Fail delivery
if a format, interface or method is described without a representative example a reader can apply;
if a new lesson sits beside overlapping guidance instead of updating it; if pending actions, pause
instructions or run chronology appear as subject facts; or if navigation alone is the quality
evidence.

Continue using relevant guidance throughout the task. Do not reload every branch on every turn.
After context loss, recover the task from the project entry and relevant saved state. Installation
and discovery belong to the host, not project-local skill copies.

