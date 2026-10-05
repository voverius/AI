
# Verification
- Narrowest relevant tests first
- Confirm the test imports or executes the changed workspace code, not an installed copy
- Widen (broader tests, lint, format, types, build) in proportion to risk
- Diff-check: correctness, unintended edits, edges, errors, compatibility, user-facing behavior
- Continue until success criteria hold or a concrete blocker exists
- Never claim a check passed unless it was run
- Report: what changed, what was verified, blockers / unresolved risk
