
# Test-driven development
Every observable behavior change: red → green → refactor.

## Seams
A **seam** is the public boundary you test at (observe behavior without reaching inside).

Confirm seams with the user only when the boundary is ambiguous. Otherwise pick the smallest public
interface that expresses the behavior.

Vertical slices only: one failing test → minimal implementation → repeat.
No horizontal slicing (all tests, then all code).

## Red
- Define expected behavior and the smallest test that proves it
- Write or update the test before production code
- Run it; confirm fail for the expected reason
- Bugs: regression test at a correct seam
- If it passes before production changes: it is not testing the gap; revise it

## Green
- Smallest production change that passes the failing test
- Keep each change minimal; repeat the cycle until the full requested behavior and its stated
  variants are covered. A focused test does not narrow the user's request
- Re-run the focused test until green

## Refactor
- Refactor while green, inside requested scope
- Public behavior unchanged; re-run focused tests after meaningful refactors

## Test quality
- Observable behavior and stable interfaces, not incidental internals
- Real code and deterministic fakes; mock only real external boundaries when needed
- Expected values from an independent source (spec, known literal), not a tautology
- Relevant errors, boundaries, regressions; no coverage theater

## Narrow exceptions (only these)
Skip test-first for: docs-only, comments-only, generated artifacts, mechanical edits with no runtime
behavior.

If no harness exists or a test is genuinely impractical: state why, then the strongest alternative
verification. "Inconvenient" or "small" is not an exception.
