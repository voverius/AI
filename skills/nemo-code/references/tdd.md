# Test-driven development

Default for every observable behavior change: red → green → refactor.

## Seams

A **seam** is the public boundary you test at — observe behavior without reaching inside.

Confirm seams with the user only when the boundary is ambiguous. Otherwise pick the smallest public interface that expresses the behavior and proceed.

Prefer vertical slices: one failing test → minimal implementation → repeat. Do not write all tests first, then all code (horizontal slicing).

## Red

- Define expected behavior and the smallest test that proves it.
- Write or update the test before changing production code.
- Run it; confirm it fails for the expected reason.
- For a bug, reproduce with a regression test at a correct seam.
- If the new test passes before production changes, it is not exercising the missing behavior — revise it.

## Green

- Smallest production change that makes the failing test pass.
- Do not broaden beyond what the test proves.
- Re-run the focused test until green.

## Refactor

- Refactor while tests are green, within the requested scope.
- Keep public behavior unchanged; re-run focused tests after meaningful refactors.

## Test quality

- Assert externally observable behavior and stable interfaces, not incidental internals.
- Prefer real code and deterministic fakes; mock only genuine external boundaries when practical.
- Expected values come from an independent source of truth (spec, known literal), not a tautology that recomputes the implementation.
- Cover relevant errors, boundaries, and regressions without chasing arbitrary coverage.

## Narrow exceptions (only these)

Test-first is not required for: documentation-only edits, comment-only edits, generated artifacts, or purely mechanical changes with no runtime behavior.

If no suitable harness exists or a test is genuinely impractical, state the reason before implementing and define the strongest available alternative verification. Inconvenience or "small change" is not an exception.
