
# Harmony Book Preparation
Voice from `nemo-general`. This task is actionable: follow
[shape](../../nemo-general/references/shape.md) while working, but the only user-facing reply is the
Result line below (no progress chatter, no soft closers).

## Operating Rules
- Create notes only in `Envoy/Books/`
- Do not promote a memo
- Work silently until the Result line
- Use the result format below once each book is complete
- For multiple books or links, finish one complete workflow before starting the next

## Resolve
- Accept a Goodreads URL or a title and author
- Use only Goodreads data
- Try the exact Goodreads URL first
- If it is blocked, use indexed Goodreads results and Goodreads edition pages
- Do not use another source

### Duplicate Check
Before resolving any other data, search filenames only for the title in:

- `Sources/Books/`
- `Envoy/Books/`

A matching filename is a duplicate. Stop and report it.

### Edition and Identity
- Use any English edition with a valid ISBN
- Prefer ISBN-13; otherwise use ISBN-10
- If several English editions qualify, use the most complete Goodreads record
- Ask only when the book identity is ambiguous
- Do not ask the user to choose an edition
- Use the primary credited author
- Treat clear Goodreads name variants as one person
- Ask only when multiple distinct authors make filename ownership unclear

### File Identity
- Split `Title: Subtitle` at the first colon
- Derive the target filename as `Title, Author.md`
- Avoid any extra `.` or other punctuation in the Title or the Author

## Apply the Template
- Copy `Bins/Templates/Template - Book.md` exactly to `Envoy/Books/Title, Author.md`
- Do not read the template into model context
- Do not reconstruct the template from memory
- Do not duplicate its schema in this skill
- Treat the template as the only structural source of truth

`## Personal` and everything after it are prohibited:

- Do not read it
- Do not modify, clear, replace, validate, or reason about it
- Edit only content before the `## Personal` heading

## Populate
Populate existing public book-information fields before `## Personal` from Goodreads data.
Rule of thumb - FOLLOW THE TEMPLATE, DO NOT INVENT WHAT DOES NOT EXIST.

- Set the H1, alias, title display, and cover filename from the title without subtitle
- The title field MUST be a wikilink with a pseudo `[[filename | Title]]`
- Put only the subtitle in the Subtitle field
- When no subtitle exists, leave the template's Subtitle line unchanged
- Set the Author field as `[[Author Name]]`
- Use note names only in wikilinks; never include a directory path
- Set Goodreads exactly as `[Goodreads](https://www.goodreads.com/book/show/<numeric-id>)`
- Keep only the numeric Goodreads ID; remove title slugs, query strings, and fragments
- Use `-` for unavailable Goodreads values
- Price is normally `-` unless Goodreads provides it
- Keep Votes as an integer without separators
- Record every unavailable Goodreads field for the result

### Tags
- Reuse existing Harmony tags only
- Set `#progress/released`
- Set exactly one existing `#book/genre/...` tag
- Set zero to two existing `#book/topic/...` tags
- Normalize Goodreads shelves to existing lower-camel-case tags
- Remove generic book tag placeholders
- Never invent a tag
- Stop and ask if no existing genre tag fits

### Overview
- Write an original overview of at most two paragraphs
- Give an engaging distant view: shape, atmosphere, scope, and central terrain
- Do not reveal underlying information, add spoilers, marketing copy, personal evaluation, title, or
 author

For nonfiction:

- Cover the subject, scope, approach, and central questions
- Link one existing `Notes/` topic only when the book centres on that one topic

For fiction:

- Cover the premise, initial situation, central conflict, setting, and themes

Do not add a topic link for fiction or multi-topic books by default.

## Validate
- Confirm the memo exists only in `Envoy/Books/`
- Confirm the filename is `Title, Author.md`
- Confirm the duplicate check happened first
- Confirm the canonical numeric Goodreads link
- Confirm an English ISBN when Goodreads provides one
- Confirm one existing genre tag and no generic tag placeholders
- Confirm an original, spoiler-free overview without title or author
- Scan only content before `## Personal` for `{{`, `Quick summary`, `2026-xx-xx`, `★★★★★`, and
 generic book tags

## Result
Respond with exactly one line per book:

- `Created: Envoy/Books/Title, Author.md`
- `Created: Envoy/Books/Title, Author.md (Goodreads missing: ISBN, Length)`
- `Exists: <existing path>`
- `Blocked: <title> (Goodreads unavailable)`

