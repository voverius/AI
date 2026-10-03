# Docs as LLM wiki

`docs/` is the project's persistent, compounding wiki (Karpathy LLM-wiki pattern).
Conversation and source material are compiled into interlinked markdown here once, then
kept current. Answers come from the wiki, not by re-deriving from raw dumps each time.

Source idea:
[llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
Adapt shape to the project; skip unused tooling.

## Layers

- **Raw** → `inbox/` arrivals; retained originals in `sources/`
  Immutable. Read only. Never rewrite
- **Wiki** → `docs/`
  Agent owns write/maintain. Human reads and directs
- **Schema** → `AGENTS.md` + this skill
  Structure, conventions, workflows

`outputs/`, `handovers/`, and `work/` are outside the wiki. Distill knowledge into `docs/`;
leave deliverables and continuation where they belong.

## Operations

**Ingest** (via [distill](distill.md)). Read a source or conversation finding. Extract what
improves future work. Update or create entity/concept/summary pages. Note contradictions.
Update [index](#index) and append [log](#log). One source may touch many pages.

**Query** (via [operate](operate.md)). Read `docs/index.md` first, then relevant pages.
Cite wiki pages. File durable answers, comparisons, and discovered connections back into
`docs/` so exploration compounds (same merge rules as distill).

**Lint** (on request or when navigation feels stale). Check contradictions, superseded
claims, orphans, missing concept pages, broken links, and gaps worth a source search.
Fix what you can; report the rest briefly.

## Index

`docs/index.md` is the content catalog: link, one-line summary, optional cues (date,
source count). Group by subject. Update on every wiki change that adds, splits, merges,
or removes a page. Query starts here.

## Log

`docs/log.md` is append-only chronology of wiki work. Prefer a parseable prefix, e.g.
`## [YYYY-MM-DD] ingest | Title`. Record ingest, filed queries, and lint passes.
Create the log with the first wiki write that needs a timeline.

## Agent vs human

- Human: choose sources, ask questions, judge meaning, approve emphasis
- Agent: summarize, cross-link, file, update index/log, keep pages consistent

Prefer updating existing pages over spawning stubs. Rarely hand-author wiki pages.
