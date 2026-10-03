# Places

In-tree layout under the project root from [access](access.md).
Create folders when content needs them. Bootstrap may create an empty `inbox/`.
Use stable descriptive names. Group by topic or task only when a flat folder is hard to scan.

## Ownership

- `AGENTS.md` - local operating contract; routes to shared skills
- `README.md` - purpose, external locations, role navigation only (no findings or task state)
- `inbox/` - arrivals awaiting processing
- `work/` - temporary extracts, drafts, experiments
- `docs/` - LLM wiki: compounding facts, decisions, entities, concepts (see [wiki](wiki.md))
- `outputs/` - deliverables and artifacts kept for use (not wiki)
- `handovers/<task>.md` - continuation state for one workstream (not wiki)
- `sources/` - retained raw originals (immutable; wiki cites, does not rewrite)

## Rules

- Keep native code and established external repos in place (paths noted in README)
- In an existing project, resolve equivalent in-tree paths from README and keep them
- Relocate maintained content only for an explicitly requested reorganization
- Avoid parallel filing systems
