
# Verification
- Narrowest relevant tests first
- Confirm the test imports or executes the changed workspace code, not an installed copy
- Widen (broader tests, lint, format, types, build) in proportion to risk
- An independent check needs a different input, expectation source or execution path than the suite
  being validated; re-running a covered assertion is not independent
- State related paths inspected and left unchanged, and why
- Diff-check: correctness, unintended edits, edges, errors, compatibility, user-facing behavior
- Continue until success criteria hold or a concrete blocker exists
- Never claim a check passed unless it was run
- Report: what changed, what was verified (and not widened), blockers / unresolved risk
