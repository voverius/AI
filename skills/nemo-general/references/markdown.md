
# Saved Markdown
Apply the entry skill's voice, list punctuation, and final check. These rules add the file
layout. Explicit target-format requirements take precedence where they conflict.

- Put text, a list, or the next heading immediately after a heading, with no blank line between
  them, and use one blank line before a heading that follows a paragraph or a list
- No empty lines between list items
- A file without frontmatter starts with one empty line (`\n` for LF). End each file with one
  empty line after its last content line (`\n\n` for LF). Required frontmatter remains first
- Wrap authored prose at 100 characters. Preserve intact links, tables, code, and required syntax
- Tables only for data that is truly tabular with short uniform cells, at most one per section.
  Rendered tables take their width from their content, so neighbouring tables differ in size and
  the larger one reads as more important. Key and value pairs go in headed prose or a list, not a
  table

After saving authored Markdown, run [check_markdown.py](../scripts/check_markdown.py) with the
changed file paths. It checks file boundaries, ATX heading spacing and simple list spacing without
rewriting files or printing their contents. Check wrapping, table judgment and other layout
manually. A successful spacing check does not validate content or every Markdown construct.

Check only authorized authored content, never retained source snapshots or protected sections.
For a permitted excerpt, pass that view on stdin with `--fragment`, which omits file-boundary
checks. If the excerpt starts at the file's frontmatter, also use `--frontmatter`. Excerpts do not
infer frontmatter from thematic breaks. Obtain the view within the workflow's read boundary before
output. Do not expose a full protected file to prepare the check. If execution is unavailable,
inspect these rules manually.

