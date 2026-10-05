
# Initialize Harmony PKM mode
Initialize only the selected Harmony workspace. Apply PKM domain behavior from this skill and its
local documentation; initialization does not switch workspaces.

Apply [nemo-general](../../nemo-general/SKILL.md) for voice. Content-only work uses the local domain
rules; apply coding workflows when the request also includes implementation.

Read every Markdown document directly inside `Envoy/Docs/` in one bulk read before acting on a
Harmony task. For a request only to initialize Harmony, inspect no other paths, write no files, emit
no progress commentary, and reply exactly after the read succeeds:

`Harmony initialized.`

For a substantive PKM request, continue with the relevant task reference after loading the local
documentation; do not emit the initialization-only reply.
