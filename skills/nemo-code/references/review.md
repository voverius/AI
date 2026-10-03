# Review code changes

A review request alone does not authorize editing the code.

## Scope

Identify what to review: supplied PR, branch, commit, or working-tree diff. Pin a fixed point (`git diff <point>...HEAD`). If the reference is missing, inspect the available change and ask only when choosing a base would materially alter the review. Confirm the ref resolves and the diff is non-empty before deep review.

## Two axes (two passes)

Review **Standards** and **Spec** as separate passes so one cannot mask the other.

| Axis | Question |
| --- | --- |
| **Standards** | Does the diff follow this repo's documented coding standards and avoid clear design smells? |
| **Spec** | Does the diff implement what was asked (issue/spec/user request) without missing requirements or scope creep? |

Prefer two parallel sub-agents when the harness supports it (one prompt per axis). Otherwise run two sequential passes in one agent. Always report under separate `## Standards` and `## Spec` headings; do not merge or cross-rank findings into one winner.

### Standards pass

- Read repo standards (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, etc.). Repo docs override heuristics.
- Flag hard violations of documented rules with file/line cites.
- Optionally note judgement-call smells (e.g. duplication, speculative generality, shotgun surgery, feature envy) — never as hard blockers when tooling already enforces the concern.
- Skip anything automated checks already cover unless the diff clearly bypasses them.

### Spec pass

Resolve the spec in order: commit/PR issue refs → path the user gave → `docs/` / `specs/` match → ask. If none exists and the user confirms none, report "no spec available" for this axis.

Report: missing/partial requirements; behavior not asked for; implementations that look wrong vs the spec. Quote the requirement for each finding.

## Output

- Prioritize actionable defects: wrong behavior, missing requirements, regressions, security/data-loss risks, tests that fail to cover those risks.
- Cite precise files and lines; separate observed defects from judgment.
- End with counts per axis and the worst issue within each axis.
- If no actionable findings remain, say so plainly.
