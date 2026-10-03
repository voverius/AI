
# Initialize Harmony PKM mode
Treat Harmony as the active workspace. Apply PKM domain behavior from this skill and Harmony's local
documentation; neutral tooling may still apply.

Apply [nemo-general](../../nemo-general/SKILL.md) for voice. Do not apply coding workflows, TDD, or
repository implementation rules.

Read every Markdown document directly inside `Envoy/Docs/` in one bulk read before acting on a
Harmony task. For a request only to initialize Harmony, inspect no other paths, write no files, emit
no progress commentary, and reply exactly after the read succeeds:

`Harmony initialized.`

For a substantive PKM request, continue with the relevant task reference after loading the local
documentation; do not emit the initialization-only reply.

