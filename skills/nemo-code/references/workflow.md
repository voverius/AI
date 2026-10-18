
# Workflow
## Boundary
- Software development, repo maintenance, debugging, and code review
- Use `nemo-project` for relevant saved context and authorized knowledge updates in a selected
  project. Keep implementation in its repository. Do not create a knowledge project automatically
- Voice from `nemo-general`. Read tdd.md before a production edit, and debug.md for a bug fix

## Before editing
- Before a behavior-changing production edit, run a test that fails for the intended reason, as
  tdd.md directs. For a behavior-preserving refactor, establish a passing relevant baseline and
  preserve its expectations. Other skips are limited to the exceptions in tdd.md
- Read global and repo-local instructions that apply
- Inspect relevant code, tests, config, and docs
- Check repo status. Preserve user changes
- Smallest ownership boundary for the request
- One focused question only when missing information would change the implementation

## Think before coding
- State assumptions that affect the implementation
- Surface materially different interpretations. Do not silently pick one
- Surface real architectural or behavioral trade-offs
- Simplest viable approach. Push back on needless complexity
- Non-trivial work: a short plan with success criteria
- Stop when ambiguity blocks a correct implementation

## Simplicity
- Minimum code that correctly solves the request
- No unrequested features, flexibility, or speculative abstractions
- No handling for scenarios that cannot occur under known constraints
- Prefer existing patterns, dependencies, and helpers
- Abstract only to remove current complexity or match an established pattern
- If the change is substantially oversized, simplify it before presenting

## Surgical edits
- Touch only what the request requires
- No drive-by cleanup of adjacent code, naming, formatting, or architecture
- No refactor of working code without a task reason. Green-loop refactors in scope are fine
- Match existing style
- Mention unrelated defects. Do not fix them
- Remove only what this change makes obsolete
- Prefer structured APIs and parsers over ad hoc text edits
- Comments only where the code is not self-explanatory
- No edits to generated files unless required

## Verification
- Apply nemo-general's action response rules and final check to the reply
- Narrowest relevant tests first
- Confirm the test imports or executes the changed workspace code, not an installed copy
- Widen to broader tests, lint, format, types, or build in proportion to risk
- An independent check needs a different input, expectation source, or execution path than the
  suite being validated. Re-running a covered assertion is not independent
- State related paths inspected and left unchanged, and why
- Diff-check correctness, unintended edits, edges, errors, compatibility, and user-facing behavior
- Continue until the success criteria hold or a concrete blocker exists
- Never claim a check passed unless it was run
- Report what changed, what was verified and what was not widened, plus blockers or unresolved risk

