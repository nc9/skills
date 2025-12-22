---
name: keyword-research
description: Performs SEO keyword research using DataForSEO API. Use when user asks about keyword ideas, search volume, CPC, competition data, or needs keywords for blog posts, landing pages, or content strategy.
allowed-tools: Bash, Read
---

# Keyword Research

Research keywords for SEO, content planning, and paid search using the DataForSEO API.

## When to Use

- User asks for keyword ideas or suggestions
- User needs search volume, CPC, or competition data
- User is planning blog posts, articles, or landing pages
- User wants to analyze keyword opportunities
- User mentions SEO keyword research

## Requirements

Environment variables must be set:
- `DATAFORSEO_USERNAME` - DataForSEO login email
- `DATAFORSEO_PASSWORD` - DataForSEO API password

## Commands

### Get Keyword Suggestions

Returns keywords containing the seed term with metrics:

```bash
./scripts/keyword_research.py suggestions "seed keyword" -n 20
```

### Get Related Keywords

Returns semantically related keywords:

```bash
./scripts/keyword_research.py related "seed keyword" -n 20
```

## Options

| Option | Description |
|--------|-------------|
| `-n, --limit` | Max results per seed (default: 50) |
| `-f, --format` | Output format: `json` (default) or `table` |

## Output Format

Default JSON output for easy parsing:

```json
[
  {
    "seed": "ai seo",
    "keywords": [
      {
        "keyword": "ai seo tools",
        "search_volume": 2900,
        "cpc": 25.48,
        "competition": 0.09,
        "competition_level": "LOW"
      }
    ]
  }
]
```

## Examples

Research keywords for a blog post:
```bash
./scripts/keyword_research.py suggestions "python tutorial" -n 30
```

Compare multiple seed keywords:
```bash
./scripts/keyword_research.py suggestions "react hooks" "vue composition api" -n 20
```

Get table output for human review:
```bash
./scripts/keyword_research.py suggestions "ai tools" -f table
```

## Interpreting Results

| Field | Meaning |
|-------|---------|
| `search_volume` | Monthly searches (Google US) |
| `cpc` | Cost per click in USD |
| `competition` | 0-1 scale (higher = more competitive) |
| `competition_level` | LOW, MEDIUM, or HIGH |
