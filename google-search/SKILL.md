---
name: google-search
description: Search Google via Serper API — web, news, images, videos, places, maps, shopping, scholar, patents, autocomplete, reviews. Use for Google results, local business info, academic papers, news, price comparisons, or search suggestions.
allowed-tools: Bash, Read
---

# Google Search

Serper API wrapper over 11 Google verticals.

## Requirements

- `SERPER_API_KEY` — [serper.dev](https://serper.dev/)

## Command

```bash
./scripts/google_search <vertical> "query" [options]
# verticals: web news images videos places maps shopping scholar patents autocomplete reviews
```

## Options

| Option | Description | Verticals |
|--------|-------------|-----------|
| `-n, --num` | Results (default 10) | all but autocomplete, reviews |
| `--gl, --country` | Country code (default us) | all |
| `--hl, --lang` | Language code (default en) | all |
| `-p, --page` | Page number (default 1) | all but autocomplete, reviews |
| `-t, --time` | Recency: `h` `d` `w` `m` `y` | web, news, images, videos |
| `-l, --location` | Location string | web, news, images, videos, places, maps, shopping |
| `-d, --data-id` | Place cid, required | reviews |
| `-f, --format` | `json` (default) or `table` | all |

## Output

JSON. `web` returns `{answerBox?, knowledgeGraph?, results[]}`, `autocomplete` a string array, every other vertical a bare result array.

## Gotchas

- `reviews` takes no query argument — only `-d`, sourced from the `cid` field of a `places`/`maps` row.
- Options are per-vertical: `-t` on `scholar` or `-l` on `patents` exits 2 with "no such option", it is not ignored.

## Examples

```bash
./scripts/google_search web "AI regulation" -t w -l "San Francisco"
./scripts/google_search places "coffee shops" -l "San Francisco"   # yields cid
./scripts/google_search reviews -d "0x808f7e..."
```
