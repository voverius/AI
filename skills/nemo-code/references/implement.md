
# Surgical implementation

## Simplicity
- Minimum code that correctly solves the request
- No unrequested features, flexibility, or speculative abstractions
- No handling for scenarios that cannot occur under known constraints
- Prefer existing patterns, dependencies, helpers
- Abstract only to remove current complexity or match an established pattern
- If substantially oversized: simplify before presenting

## Surgical edits
- Touch only what the request requires
- No drive-by cleanup of adjacent code, naming, formatting, or architecture
- No refactor of working code without a task reason (green-loop refactors in scope are fine)
- Match existing style
- Mention unrelated defects; do not fix them
- Remove only what this change makes obsolete
- Prefer structured APIs/parsers over ad hoc text edits
- Comments only where code is not self-explanatory
- No edits to generated files unless required

