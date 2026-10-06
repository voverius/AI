
# Initialize Harmony PKM mode
Initialize only the selected Harmony workspace. Apply PKM domain behavior from this skill and its
local documentation; initialization does not switch workspaces.

Apply [nemo-general](../../nemo-general/SKILL.md) for voice. Content-only work uses the local domain
rules; apply coding workflows when the request also includes implementation.

## Resolve the Harmony root
Before any Harmony read or write, resolve one root that contains `Envoy/Docs/` as a directory.
Prefer the active workspace when it qualifies. If the user named a root, use that after the same
check. If none qualifies or several fit, stop and ask; do not invent a root or write relative paths
against an unresolved location. Absolute paths under that root for every subsequent read and write.

Read every Markdown document directly inside `<root>/Envoy/Docs/` in one bulk read before acting on
a Harmony task. For a request only to initialize Harmony, inspect no other paths, write no files,
emit no progress commentary, and reply exactly after the read succeeds:

`Harmony initialized.`

For a substantive PKM request, continue with the relevant task reference after loading the local
documentation; do not emit the initialization-only reply.
