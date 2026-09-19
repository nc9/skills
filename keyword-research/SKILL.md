---
name: keyword-research
description: SEO keyword research via DataForSEO — search volume, CPC, and competition for keyword suggestions and semantically related terms. Use when asked for keyword ideas, search volume, or keywords for a blog post, landing page, or content plan.
allowed-tools: Bash, Read
---

# Keyword Research

DataForSEO Labs wrapper returning volume, CPC and competition per keyword.

## Requirements

- `DATAFORSEO_USERNAME` — DataForSEO login email
- `DATAFORSEO_PASSWORD` — DataForSEO API password

## Commands

```bash
./scripts/keyword_research suggestions "seed" ["seed2" ...] [options]   # keywords containing the seed
./scripts/keyword_research related "seed" ["seed2" ...] [options]       # semantically related keywords
```

## Options

| Option | Description |
|--------|-------------|
| `-n, --limit` | Max results per seed (default 50) |
| `-f, --format` | `json` (default) or `table` |

## Output

JSON array, one object per seed: `{seed, keywords: [{keyword, search_volume, cpc, competition, competition_level}]}`. `competition` is 0-1, `competition_level` is `LOW`/`MEDIUM`/`HIGH`, `cpc` is USD.

## Gotchas

- Locale is hardcoded to US (location code 2840) and English, with no CLI override. Edit `DEFAULT_LOCATION_CODE`/`DEFAULT_LANGUAGE_CODE` in the script for other markets.
- Each seed is a separate billed API call, so `-n` caps results but not cost.
- A seed that errors is logged to stderr and dropped from the output array while the exit code stays 0. Compare array length against seeds passed.

## Examples

```bash
./scripts/keyword_research suggestions "python tutorial" -n 30
./scripts/keyword_research related "react hooks" "vue composition api" -n 20
./scripts/keyword_research suggestions "ai tools" -f table
```
