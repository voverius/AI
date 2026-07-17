---
name: pkm-book-prepare
description: Prepare a Harmony book memo from a Goodreads URL or a title and author. Use to create a spoiler-free, metadata-complete book record in Envoy/Memos before later promotion to Sources/Books.
---

# Harmony Book Preparation

Create the memo in `Envoy/Memos/`. Do not promote it. Work silently and use the result format below.

## Resolve the Book

Resolve the title from the provided Goodreads URL or title and author. Before doing further work, search filenames only in `Sources/Books/`, `Lounge/Books/`, and `Envoy/Memos/` for that title. A matching filename is a duplicate: stop and report it.

Use the exact Goodreads URL first. If Goodreads blocks direct access, use indexed Goodreads results and Goodreads edition pages. Prefer Goodreads-derived data; use another source only to confirm an otherwise unavailable ISBN, page count, or language.

Use any English edition with a valid ISBN. Prefer ISBN-13; otherwise use ISBN-10. If several English editions exist, select the most complete record. Ask only when the book identity is ambiguous, not to choose an edition.

Use the primary credited author. Treat clear Goodreads name variants as one person; ask only if multiple distinct authors make filename ownership unclear. Split `Title: Subtitle` at the first colon. Use `Title, Author.md` as the filename and use the title without subtitle for the H1, alias, title display, and cover filename. When no subtitle exists, leave the template's subtitle line unchanged.

## Apply the Template

Apply `Bins/Templates/Template - Book.md` by copying the file exactly into the target path. Do not read the template into model context, reconstruct it from memory, or duplicate its schema in this skill.

The template is the only structural source of truth. `## Personal` and everything after it are under a strict ban: do not read, modify, clear, replace, validate, or reason about any of that content. Edit only the content before the `## Personal` heading.

## Populate the Editable Sections

Populate every existing public book-information field above `## Personal` from Goodreads-derived data. Replace the template's Goodreads ID with the canonical numeric ID. Use `-` for unavailable data; price is normally `-`. Keep rating votes as an integer without separators.

Use only existing Harmony tags. Set `#progress/released`, exactly one established book-genre tag, and up to two established book-topic tags. Match Goodreads shelves to existing lower-camel-case tags. Never create a tag, and remove generic book tag placeholders. If no existing genre tag fits, stop and ask.

Write an original overview of at most two paragraphs. It gives an engaging distant view of the book: its shape, atmosphere, scope, and central terrain without revealing underlying information. Never mention the book title or author, copy Goodreads marketing text, add personal evaluation, or include spoilers.

For nonfiction, cover subject, scope, approach, and central questions. When a nonfiction book centres on one topic already present in `Notes/`, link that one topic in the overview. Do not add such a link for multi-topic books or fiction by default.

For fiction, cover premise, initial situation, central conflict, setting, and themes.

## Validate

Before reporting completion, verify the memo is only in `Envoy/Memos/`, its filename is `Title, Author.md`, and duplicate filenames were checked first. Verify the canonical Goodreads link, English ISBN when available, existing genre tag, and original spoiler-free overview without title or author.

Scan only the content before `## Personal` for unresolved template material: `{{`, `Quick summary`, `2026-xx-xx`, `★★★★★`, and standalone generic book tags. Do not inspect `## Personal` or anything after it.

## Result

Respond with exactly one line:

- `Created: Envoy/Memos/Title, Author.md`
- `Exists: <existing path>`
- `Blocked: <concise reason>`
