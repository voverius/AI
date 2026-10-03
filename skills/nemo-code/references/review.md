# Review code changes

Review alone does not authorize edits.

## Scope

Pin what to review: PR, branch, commit, or working tree. Fixed point: `git diff <point>...HEAD`.
If the base is missing, inspect what exists; ask only when the base choice would change the review.
Confirm the ref resolves and the diff is non-empty before deep review.

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
