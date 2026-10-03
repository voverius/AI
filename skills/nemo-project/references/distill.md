# Distill

Read [lifecycle](lifecycle.md), [wiki](wiki.md), [ownership](ownership.md), and
[retention](retention.md) if not already loaded.

Distill is wiki **ingest** (and filing durable query answers into `docs/`).
`outputs/` and handovers are out of scope except for stripping task status / staleness.

1. **Select.** Identify the processed set: relevant inputs, findings, conversation material
   Choose owning wiki subjects via ownership rules: reusable entity/domain facts vs
   tool-specific procedures. Read existing `docs/` owners and needed raw context. No owner
   for a reusable finding → create a wiki page. A deliverable alone is not distillation.
   Leave unrelated or incompletely read inputs untouched
2. **Merge.** Compile into owning `docs/` pages (update before create). Keep evidence and
   decision rationale. Provenance with claims (source identity or user decision/observation,
   plus supporting detail); keep that when discarding an input. Keep useful proposals and
   rejected approaches with status. Decision = intent; claim execution only with execution
   evidence. Contradictions: assess evidence and scope; supersede only when justified,
   else retain the conflict and what would resolve it. Recency alone is not truth. After
   wiki changes: read back README, `docs/index.md`, affected outputs and handovers. Strip
   task status from navigation; refresh editable results or mark stale; keep retained
   originals immutable under `sources/`
3. **Index, log, clean.** Update owning index branch and incoming links when subjects or
   cues change; create `docs/index.md` with the first maintained page. Append `docs/log.md`
   for this ingest or filed answer. Every wiki topic reachable; README stays a role map.
   Before cleanup: check retained claims against cited sources; separate inference from
   source content. Confirm useful findings survive without duplication, uncertainty stays
   visible. Move explicitly retained processed originals to `sources/` and repair links.
   Delete eligible inputs/intermediates only under retention rules; surviving knowledge
   must keep source identity and support for deleted originals

Clean resolved detail from handovers after preservation. Report unresolved processing or
conflicts briefly. Re-running with no new information should not change files.
Done: relevant wiki knowledge is retrievable and supported (not: inbox empty).
