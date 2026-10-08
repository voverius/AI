
# Book preparation in a PKM library
Voice from `nemo-general`. This task is actionable: follow
[shape](../../nemo-general/references/shape.md) while working, but the only user-facing reply is the
Result line below (no progress chatter, no soft closers).

## Operating Rules
- Resolve the selected library through [the entry skill](../SKILL.md)
- From its local rules and existing notes, identify the book draft location, existing book-record
  locations, and any book template or tag vocabulary. Ask if the destination or format is unclear
- Create a note only in the mapped book draft location
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

- the library's existing book-record locations
- the mapped book draft location

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
- Derive the target filename as `Title, Author.md` unless local rules require another format
- Avoid any extra `.` or other punctuation in the Title or the Author

## Apply the Template
- If a book template exists, copy it exactly to the mapped book draft location; do not read it into
  model context or reconstruct it from memory
- If no template exists, use the library's documented book format or consistent existing pattern
- Do not duplicate either schema in this skill

If the template has a `## Personal` section, that section and everything after it are prohibited:

- Do not read it
- Do not modify, clear, replace, validate, or reason about it
- Edit only content before the `## Personal` heading

## Populate
Populate existing public book-information fields from Goodreads data without crossing a protected
personal section.
Rule of thumb - FOLLOW THE TEMPLATE, DO NOT INVENT WHAT DOES NOT EXIST.

- Fill title, subtitle, author, alias and cover fields only where the template defines them
- Use the local format for links and fields; wikilinks, when required, contain note names rather
  than directory paths
- When no subtitle exists, leave any template subtitle placeholder unchanged
- Set Goodreads exactly as `[Goodreads](https://www.goodreads.com/book/show/<numeric-id>)`
- Keep only the numeric Goodreads ID; remove title slugs, query strings, and fragments
- Use the template's missing-value convention for unavailable Goodreads values
- Keep numeric vote counts as integers if that field exists
- Record every unavailable Goodreads field for the result

### Tags
- Reuse the selected library's existing tags only
- Apply its required progress tag and exactly one existing genre tag when its schema defines them
- Apply at most two existing topic tags when its schema defines them
- Map Goodreads shelves to the library's existing tag vocabulary and spelling
- Remove generic book tag placeholders
- Never invent a tag
- Stop and ask if a required genre tag has no existing match

### Overview
- Write an original overview of at most two paragraphs
- Give an engaging distant view: shape, atmosphere, scope, and central terrain
- Do not reveal underlying information, add spoilers, marketing copy, personal evaluation, title, or
 author

For nonfiction:

- Cover the subject, scope, approach, and central questions
- Link one existing topic note only when the book centres on that one topic

For fiction:

- Cover the premise, initial situation, central conflict, setting, and themes

Do not add a topic link for fiction or multi-topic books by default.

## Validate
- Confirm the memo exists only in the mapped book draft location
- Confirm the filename follows the selected library's rule
- Confirm the duplicate check happened first
- Confirm the canonical numeric Goodreads link
- Confirm an English ISBN when Goodreads provides one
- Confirm required existing tags and no generic tag placeholders
- Confirm an original, spoiler-free overview without title or author
- Scan only the editable section for `{{`, `Quick summary`, `2026-xx-xx`, `★★★★★`, and generic
  book tags

## Result
Respond with exactly one line per book:

- `Created: <relative path to book draft>`
- `Created: <relative path to book draft> (Goodreads missing: ISBN, Length)`
- `Exists: <existing path>`
- `Blocked: <title> (Goodreads unavailable)`
