---
name: google-search-console
description: Query Google Search Console data — check indexing status, view search performance (keywords, clicks, impressions, CTR, position), list sitemaps and properties. Use when user asks about page indexing, search analytics, Google rankings, search traffic, or wants to check which pages are indexed.
allowed-tools: Bash, Read
---

# Google Search Console

Query Search Console data: indexing status, search performance, sitemaps, and properties.

## When to Use

- User wants to check if a URL is indexed by Google
- User asks about search performance, rankings, or traffic
- User wants to see top keywords/queries for a site
- User asks about clicks, impressions, CTR, or position data
- User wants to list sitemaps or Search Console properties
- User mentions Google Search Console, search analytics, or crawl status

## Requirements

- `GOOGLE_INDEXING_KEY_FILE` - Path to Google Cloud service account JSON key file (same as google-indexing skill)
- Service account must have read access in Google Search Console
- Search Console API enabled in Google Cloud Console

## Commands

### Inspect URL Indexing Status

```bash
./scripts/google_search_console.py inspect "https://example.com/page" --site sc-domain:example.com
./scripts/google_search_console.py inspect --file urls.txt --site sc-domain:example.com
```

### Search Performance (Analytics)

```bash
# Top queries (last 28 days)
./scripts/google_search_console.py performance --site sc-domain:example.com

# Top pages
./scripts/google_search_console.py performance --site sc-domain:example.com --dimension page

# Filter by query
./scripts/google_search_console.py performance --site sc-domain:example.com --query "seo"

# Custom date range
./scripts/google_search_console.py performance --site sc-domain:example.com --start-date 2024-01-01 --end-date 2024-01-31

# Limit rows with table output
./scripts/google_search_console.py performance --site sc-domain:example.com -n 20 -f table
```

### List Sitemaps

```bash
./scripts/google_search_console.py sitemaps --site sc-domain:example.com
```

### List Properties

```bash
./scripts/google_search_console.py sites
```

## Options

| Option | Description |
|--------|-------------|
| `-k, --key-file` | Service account JSON key path (overrides env) |
| `-f, --format` | Output format: `json` (default) or `table` |
| `-s, --site` | Search Console property (e.g. `sc-domain:example.com`) |
| `--file` | File with URLs, one per line (inspect only) |
| `-d, --dimension` | Dimension: `query`, `page`, `country`, `device`, `date` |
| `--days` | Days back from today (default: 28) |
| `--start-date` | Start date YYYY-MM-DD (overrides --days) |
| `--end-date` | End date YYYY-MM-DD |
| `-q, --query` | Filter by search query (contains) |
| `-p, --page` | Filter by page URL (contains) |
| `-n, --limit` | Max rows (default: 1000, max: 25000) |

## Output Format

### inspect

```json
{
  "site": "sc-domain:example.com",
  "results": [
    {
      "url": "https://example.com/page",
      "verdict": "PASS",
      "coverage_state": "Submitted and indexed",
      "last_crawl_time": "2024-01-15T10:30:00Z",
      "page_fetch_state": "SUCCESSFUL",
      "robots_txt_state": "ALLOWED",
      "indexing_state": "INDEXING_ALLOWED",
      "google_canonical": "https://example.com/page",
      "user_canonical": "https://example.com/page",
      "crawled_as": "MOBILE",
      "referring_urls": [],
      "sitemaps": [],
      "error": null
    }
  ]
}
```

### performance

```json
{
  "site": "sc-domain:example.com",
  "start_date": "2024-01-01",
  "end_date": "2024-01-28",
  "dimension": "query",
  "rows": [
    {
      "keys": ["example keyword"],
      "clicks": 150,
      "impressions": 3200,
      "ctr": 0.047,
      "position": 8.3
    }
  ]
}
```

### sites

```json
{
  "sites": [
    {
      "site_url": "sc-domain:example.com",
      "permission_level": "siteOwner"
    }
  ]
}
```

## API Quotas

| Quota | Limit |
|-------|-------|
| URL Inspection | 2,000/day per property, 600/min |
| Search Analytics | 1,200 queries/min |
| Sitemaps/Sites | Standard quota |

## Examples

Check if a page is indexed:
```bash
./scripts/google_search_console.py inspect "https://example.com/page" --site sc-domain:example.com
```

Top 10 queries with table output:
```bash
./scripts/google_search_console.py performance --site sc-domain:example.com -n 10 -f table
```

List all verified properties:
```bash
./scripts/google_search_console.py sites -f table
```
