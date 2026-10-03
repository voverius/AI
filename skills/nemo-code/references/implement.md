# Surgical implementation

## Simplicity

- Write the minimum code that correctly solves the requested problem.
- No unrequested features, flexibility, configurability, or speculative abstractions.
- No handling for scenarios that cannot occur under established constraints.
- Prefer existing patterns, dependencies, and helpers.
- Add an abstraction only when it removes current complexity or matches an established pattern.
- If the solution is substantially larger than necessary, simplify before presenting it.

## Surgical edits

- Touch only what the request requires; every changed line traces to the outcome.
- Do not improve adjacent code, comments, naming, formatting, or architecture.
- Do not refactor working code without a task-specific reason (TDD green-loop refactors inside scope are allowed).
- Match existing style even when another style would be preferable.
- Mention unrelated dead code or defects; do not change them.
- Remove only imports, variables, functions, or files made obsolete by the current change.
- Prefer structured APIs or parsers over ad hoc text manipulation.
- Add concise comments only where the code is not self-explanatory.
- Do not modify generated files unless the task requires it.
