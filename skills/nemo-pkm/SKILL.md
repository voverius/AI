---
name: nemo-pkm
description: >-
  Work in an explicitly selected personal knowledge library using its own structure and rules.
  Use for PKM initialization, note work, and book preparation in that library. Use nemo-project
  for project knowledge. Questions about PKM as a concept do not select a library.
---

# PKM
Apply nemo-general for voice.

Select the library named by the user or established by the active workspace. Verify its root and
resolve symbolic links before treating alternative paths as separate libraries. Then inspect its
local instructions and index. Apply their protection rules before searching or displaying note or
template content: obtain a permitted view locally, never a full-file read followed by filtering in
model context. Load the applicable reference before those content operations. If several libraries
fit or none is established, ask which one. Do not infer a root from a familiar folder name. Use
absolute paths within a filesystem library. Its local documentation owns the schema, note
locations, templates, vocabulary, and promotion rules. If no local rules exist, follow the existing
organization and ask only when a write destination or format is unclear. Do not impose one
library's layout on another or switch libraries silently.

## Protected content
For a suffix protected by an ATX heading, use [public_section.py](scripts/public_section.py).
Supply the resolved library root and the actual heading from its rules. Run it with Python 3.9 or
newer using these argument forms, replacing the uppercase placeholders:

```text
view --root LIBRARY --heading '## Personal' FILE
replace --root LIBRARY --heading '## Personal' --public-file PUBLIC_FILE --expected-public-sha256 HASH TARGET
```

`view` returns JSON with only `public_text`, `boundary_found` and `public_sha256`. Search that public
text, including for filename-only matches. Never give a protected file directly to a generic read,
search, edit or formatting tool. Even public-only edit arguments can cause a tool to return the
whole file or a diff containing protected bytes.
The helper stops at the first literal matching heading line, including one inside a fenced example.
It can therefore hide more than a full Markdown parser would, without exposing the suffix.

For an update, write only the intended public prefix to a new task-owned scratch file inside the
library, ending it with a line break so the protected heading remains on its own line. Validate that
public file, then use `replace` with the hash from the target's public view.
It checks the expected public state and preserves the protected suffix as opaque bytes. Confirm
the saved public view matches the checked replacement. Remove the public scratch file you created
when it is no longer needed, preserving user inputs. The helper cleans its internal atomic-write
temporary file itself.

If the helper cannot run, stop the protected-content operation. Do not fall back to a raw file
tool or approximate line ranges. For a different protection scheme, use a permitted local method
whose complete results enforce that scheme. This helper does not grant access or restrict other
tools, and it cannot enforce an actor's choice to use it.

## References
- [workflow](references/workflow.md) - Retrieval, note drafting, and library write boundaries
  Read for substantive note work
- [book-prepare](references/book-prepare.md) - Goodreads lookup, the library's book template, and
  validation. Read before preparing a book memo, after resolving the library and its book rules.
  Also read nemo-general shape.md before the result reply and markdown.md before saving the memo

Initialization-only: read the nemo-general init reference and reply with the PKM string. Do not
load the references above for that request.

The selected library's rules apply only there. Project knowledge remains under `nemo-project`.

