---
name: google-search-console
description: Query Google Search Console — URL indexing status, search performance (clicks, impressions, CTR, position by query/page/country/device/date), submitted sitemaps, and verified properties. Use for indexing checks, rankings, or search traffic.
allowed-tools: Bash, Read
---

# Google Search Console

Read-only Search Console API wrapper: inspect, performance, sitemaps, sites.

## Requirements

- `GOOGLE_INDEXING_KEY_FILE` — service account JSON key path (shared with the google-indexing skill)
- Service account added as a user on the property; Search Console API enabled in the Cloud project

## Commands

```bash
./scripts/google_search_console inspect [URLS...] -s sc-domain:example.com [--file urls.txt]
./scripts/google_search_console performance -s sc-domain:example.com [options]
./scripts/google_search_console sitemaps -s sc-domain:example.com
./scripts/google_search_console sites
```

## Options

| Option | Description | Commands |
|--------|-------------|----------|
| `-s, --site` | Property, e.g. `sc-domain:example.com` | all but `sites` |
| `-k, --key-file` | Key path, overrides env | all |
| `-f, --format` | `json` (default) or `table` | all |
| `--file` | File of URLs, one per line, `#` comments skipped | `inspect` |
| `-d, --dimension` | `query` (default), `page`, `country`, `device`, `date` | `performance` |
| `--days` | Days back from today (default 28) | `performance` |
| `--start-date` | `YYYY-MM-DD`, overrides `--days` | `performance` |
| `--end-date` | `YYYY-MM-DD` (default today) | `performance` |
| `-q, --query` | Filter: query contains | `performance` |
| `-p, --page` | Filter: page URL contains | `performance` |
| `-n, --limit` | Max rows, default 1000, clamped to 25000 | `performance` |

## Output

JSON. `inspect`: `{site, results[]}` per URL with `verdict`, `coverage_state`, `last_crawl_time`, `page_fetch_state`, `robots_txt_state`, `indexing_state`, `google_canonical`, `user_canonical`, `crawled_as`, `error`. `performance`: `{site, start_date, end_date, dimension, rows[]}`, rows carrying `keys`, `clicks`, `impressions`, `ctr`, `position`. `sitemaps`: path, submit/download times, warning and error counts. `sites`: `site_url` + `permission_level`.

## Gotchas

- `-p` on `performance` is a page **filter**, not pagination. There is no paging; raise `-n`. One `-d` dimension per call, so no query x page breakdowns.
- Search Console data lags 2-3 days, so the tail of a `--days` range is usually empty.
- `inspect` reads URLs from stdin when none are given as args or via `--file`; a per-URL failure lands in that row's `error` and the run still exits 0, so check `error` before trusting a null `verdict`.
- Omitting `-s` prints the available properties to stderr before exiting — quickest way to find the property string.

## API Quotas

| Quota | Limit |
|-------|-------|
| URL Inspection | 2,000/day per property, 600/min |
| Search Analytics | 1,200 queries/min |
| Sitemaps / Sites | Standard quota |

## Examples

```bash
./scripts/google_search_console inspect "https://example.com/page" -s sc-domain:example.com
./scripts/google_search_console performance -s sc-domain:example.com -d page -n 20 -f table
cat urls.txt | ./scripts/google_search_console inspect -s sc-domain:example.com
```
