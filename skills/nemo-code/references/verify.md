# Verification

- Run the narrowest relevant tests first.
- Widen to broader tests, lint, format, typecheck, or builds in proportion to risk.
- Inspect the final diff for correctness, unintended changes, edge cases, error paths, compatibility, and user-facing behavior.
- Continue until success criteria are verified or a concrete blocker is identified.
- Never claim a check passed unless it was run successfully.
- Report what changed, what was verified, and any blocker or unresolved risk.
