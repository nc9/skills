---
name: parallel
description: Web search and deep research via Parallel AI — domain-filtered cited excerpts from the Search API, and externally-run multi-source research reports from the Task API. Use when results must carry source URLs or come only from named domains.
allowed-tools: Bash, Read
---

# Parallel AI

Two scripts over the Parallel AI API. Prefer the built-in `WebSearch` tool for ordinary
lookups, and the built-in deep-research skill for ordinary research — reach for these when
you need domain-filtered cited excerpts, or a long report run outside this session.

## Requirements

- `PARALLEL_API_KEY` — https://platform.parallel.ai

## Search — cited excerpts

```bash
./scripts/parallel_search search -o "objective" [-q "keyword query"] [-d example.com] [-n 5]
```

| Option | Default | Description |
|--------|---------|-------------|
| `-o, --objective` | required | Self-contained description of the goal |
| `-q, --query` | objective | Keyword query, 3-6 words, repeatable; 2-3 gives best results |
| `-m, --mode` | `fast` | `turbo`/`fast` ($1/1k), `basic`/`advanced` ($5/1k, deeper retrieval) |
| `-n, --limit` | 10 | Max results, 1-20 (sent server-side; >10 bills extra) |
| `-c, --max-chars` | 500 | Cap on excerpt chars **per result**, not per request |
| `-d, --domain` | – | Restrict to these domains, repeatable (`source_policy.include_domains`) |
| `-f, --format` | `json` | `json` or `table` |

JSON out: `{objective, queries, mode, results:[{title, url, excerpt, publish_date}]}`.
Excerpts are markdown joined per URL; `publish_date` is often null.

## Research — full reports

```bash
./scripts/parallel_research research "query" [-p core] [-t 1800] [-f markdown]
```

| Option | Default | Description |
|--------|---------|-------------|
| `-p, --processor` | `pro` | `lite base core core2x pro ultra ultra2x ultra4x ultra8x` |
| `-t, --timeout` | 600 | Max wait, seconds |
| `-f, --format` | `json` | `json` or `markdown` |

Processor cost per 1k runs: lite $5, base $10, core $25, core2x $50, pro $100, ultra $300,
doubling to ultra8x $2400. Use `core` for routine multi-source questions and `ultra` only
for genuinely hard ones. JSON out: `{query, processor, run_id, content, basis}`, where
`basis` maps each output field to its source excerpts.

## Gotchas

- `search_queries` is required by the API; omitting `-q` sends the whole objective as one
  query, which is worse than 2-3 tight keyword queries.
- Research runs 1-45 minutes and blocks until done — raise `-t` past the default 600s for
  `ultra*`, or the call times out while the run keeps billing.
- Query must be under 15,000 chars. Progress goes to stderr, results to stdout.
- The legacy `-fast` processor names (`pro-fast`, `ultra-fast`) still resolve but are not
  recommended for new work and cost the same as their standard counterparts.
