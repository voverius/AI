
# Initialization-only replies
An initialization-only request does not start the task and does not add progress commentary.
The reply is the text between the backticks for the requested mode, without the backticks and
with no other characters. Substantive work does not emit that reply.

General mode. No workspace inspection and no changes:

`General mode initialized. Ready for the role definition.`

Code mode. No workspace inspection, no task tools, and no artifacts. Use the code skill only when
the user then gives a coding task:

`Code mode initialized. Ready for the task.`

PKM mode. Resolve the selected library as the PKM skill directs. Inspect its local instructions
or index and enough navigation to locate its own rules. If neither exists, inspect its top-level
organization. Do not assume a particular folder layout, read every document, or switch libraries.
Write no files. Reply after that read succeeds:

`PKM initialized.`

