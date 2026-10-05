
# Review code changes
Review alone does not authorize edits.

## Scope
Identify the requested comparison: working changes, staged changes, a branch, a PR, or named files.
Use the matching diff; a branch comparison does not include uncommitted work. Include relevant
untracked files when they are part of the requested change. Confirm available refs before using
them. If Git metadata or a baseline is absent, inspect the named files and state that comparison
limit. Ask only when the missing baseline would change the review.

## Two axes (two passes)
Keep **Standards** and **Spec** separate so one cannot mask the other.

- **Standards**: repo coding standards and clear design smells
- **Spec**: implements what was asked (issue/spec/request); no missing pieces or scope creep

Prefer two parallel sub-agents (one prompt per axis). Else two sequential passes in one agent.
Report under `## Standards` and `## Spec`. Do not merge or cross-rank into one winner.

### Standards
- Read repo standards (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, …). Repo wins
- Hard violations: cite file/line and the rule
- Optional judgement-call smells (duplication, speculative generality, shotgun surgery, feature
  envy): never hard blockers when tooling already covers them
- Skip what automation already enforces unless the diff clearly bypasses it

### Spec
Resolve spec: commit/PR issue refs → user path → `docs/` / `specs/` match → ask.
None and user confirms none: "no spec available" for this axis.

Report: missing/partial requirements; unasked behavior; wrong-looking implementation. Quote the
requirement per finding.

## Output
- Prioritize actionable defects: wrong behavior, missing requirements, regressions,
  security/data-loss, weak tests for those risks
- Cite file/line; separate observation from judgment
- Counts per axis + worst issue within each axis
- No findings: say so plainly

