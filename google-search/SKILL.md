---
name: google-search
description: Search Google via Serper API — web, news, images, videos, places, maps, shopping, scholar, patents, autocomplete, reviews. Use when user needs Google search results, local business info, academic papers, news, shopping comparisons, or search suggestions.
allowed-tools: Bash, Read
---

# Google Search

Google search across 11 search types using Serper API.

## When to Use

- User needs Google search results
- Looking up local businesses or places
- Searching for news, images, videos
- Academic/scholarly research
- Shopping/price comparisons
- Patent searches
- Getting autocomplete suggestions

## Requirements

- `SERPER_API_KEY` - [Get one at serper.dev](https://serper.dev/)

## Commands

```bash
./scripts/google_search web "query" [-n 10] [--gl us] [--hl en] [-t d] [-l "location"] [-f json]
./scripts/google_search news "query" [-n 10] [-t w]
./scripts/google_search images "query" [-n 10]
./scripts/google_search videos "query" [-n 10]
./scripts/google_search places "query" [-l "San Francisco"]
./scripts/google_search maps "query" [-l "New York"]
./scripts/google_search shopping "query" [-n 10]
./scripts/google_search scholar "query" [-n 10]
./scripts/google_search patents "query" [-n 10]
./scripts/google_search autocomplete "query"
./scripts/google_search reviews --data-id "cid_from_places"
```

## Common Options

| Option | Description |
|--------|-------------|
| `-n, --num` | Number of results (default: 10) |
| `--gl, --country` | Country code (default: us) |
| `--hl, --lang` | Language code (default: en) |
| `-p, --page` | Page number (default: 1) |
| `-t, --time` | Time filter: h, d, w, m, y |
| `-l, --location` | Location string |
| `-f, --format` | Output: `json` (default) or `table` |

## Output Format

Default JSON for LLM parsing:

```json
{
  "answerBox": {"title": "...", "answer": "..."},
  "knowledgeGraph": {"title": "...", "type": "...", "description": "..."},
  "results": [
    {"position": 1, "title": "...", "link": "...", "snippet": "..."}
  ]
}
```

## Examples

Web search with time filter:
```bash
./scripts/google_search web "AI regulation news" --time w
```

Local places:
```bash
./scripts/google_search places "coffee shops" --location "San Francisco"
```

Then get reviews using cid from places result:
```bash
./scripts/google_search reviews --data-id "0x808f7e..."
```

Academic search:
```bash
./scripts/google_search scholar "transformer architecture" -n 5
```

Autocomplete suggestions:
```bash
./scripts/google_search autocomplete "how to"
```

Table output:
```bash
./scripts/google_search web "python asyncio" -f table
```
