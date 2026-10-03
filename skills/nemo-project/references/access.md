# Project root and access

Single owner for where projects live and how to open them. Other refs only link here.

## Location

Every project knowledge space lives at:

`~/Projects/<project>/`

`<project>` is the directory name the user gives or that already exists under `~/Projects/`.
Do not invent a sibling root. Do not keep a parallel knowledge tree elsewhere for the same
project.

Code repos and other external systems may live outside this path; README records those
locations. The knowledge space itself always uses the path above.

## Access check (once per skill activation)

Run from the skill entry, before any branch. Not again on every reference load.
Fail closed: do not pretend the project is loaded if any check fails.

1. Resolve the path (expand `~` to the real home)
2. Confirm the path exists and is a directory
3. Confirm it is readable (list or read `README.md` / `AGENTS.md` when present)
4. If the task will write: confirm it is writable
5. Confirm enough entry info to orient: at least one of `README.md`, `AGENTS.md`, or (for
   brand-new bootstrap only) explicit user intent to create the project

## Bootstrap create

Only when the user asked to create that project:

1. Confirm `~/Projects/` exists and is writable (create `~/Projects/` only if missing and
   authorized)
2. Create `~/Projects/<project>/` if missing
3. Re-run the access check, then continue [init](init.md)

## On failure

Stop. Report which check failed and the path tried. Ask only what is needed:

- Missing directory: bootstrap create, or correct the project name?
- Not readable / not writable: fix permissions or pick another project?
- Empty of entry files and not a bootstrap request: add README/AGENTS, or wrong path?

Do not invent project contents from memory of other chats or machines.

## Workspace note

If the current editor workspace is not the project root, still use the path above for
project knowledge once access succeeds. Say when the workspace root and the project root
differ.
