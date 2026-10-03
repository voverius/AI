# Project workflow glue

Project knowledge and working context. Voice: `nemo-general`.

Access already ran at skill entry. Load by task:

- Init / repair → [lifecycle](lifecycle.md) + [init](init.md)
- Operate / continue → [operate](operate.md) (load [lifecycle](lifecycle.md) before
  changing files or filing)
- Distill / wiki ingest → [lifecycle](lifecycle.md) + [distill](distill.md)
  ([wiki](wiki.md) via lifecycle)
- Capture → [lifecycle](lifecycle.md) + [capture](capture.md)
- Read-only retrieval → [operate](operate.md) step 1 only; skip filing sections of
  lifecycle

Always:

- Project holds domain facts; this skill holds reusable procedure
- External systems stay authoritative for their own state
- Never invent a next task just because one finished
