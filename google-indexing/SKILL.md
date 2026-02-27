---
name: google-indexing
description: Submit, remove, or check indexing status of URLs via Google's Indexing API. Use when user wants to notify Google about new/updated/deleted pages, check indexing status, or speed up crawling.
allowed-tools: Bash, Read
---

# Google Indexing

Notify Google when pages are added, updated, or removed using the Web Search Indexing API.

## When to Use

- User wants to submit URLs to Google for indexing
- User wants to notify Google about removed pages
- User asks about indexing status of URLs
- User mentions Google indexing, crawling, or re-indexing
- User wants to speed up Google discovering page changes

## Requirements

- `GOOGLE_INDEXING_KEY_FILE` - Path to Google Cloud service account JSON key file
- Service account must be added as Owner in Google Search Console

## Commands

### Submit URLs (new/updated)

```bash
./scripts/google_indexing.py submit "https://example.com/page1" "https://example.com/page2"
```

### Remove URLs (deleted)

```bash
./scripts/google_indexing.py remove "https://example.com/old-page"
```

### Check Indexing Status

```bash
./scripts/google_indexing.py status "https://example.com/page1"
```

### View API Quotas

```bash
./scripts/google_indexing.py quota
```

## URL Input

All URL commands accept multiple input methods:

```bash
# Positional args
./scripts/google_indexing.py submit "https://a.com" "https://b.com"

# From file
./scripts/google_indexing.py submit --file urls.txt

# From stdin
cat urls.txt | ./scripts/google_indexing.py submit
```

## Options

| Option | Description |
|--------|-------------|
| `-k, --key-file` | Service account JSON key path (overrides env) |
| `-f, --format` | Output format: `json` (default) or `table` |
| `--file` | File with URLs, one per line |
| `-b, --batch-size` | Batch size for publish requests (max 100) |

## Output Format

### submit/remove

```json
{
  "command": "submit",
  "total": 3,
  "succeeded": 2,
  "failed": 1,
  "results": [
    {
      "url": "https://example.com/page",
      "success": true,
      "type": "URL_UPDATED",
      "notify_time": "2024-01-15T10:30:00Z",
      "error": null
    }
  ]
}
```

### status

```json
{
  "results": [
    {
      "url": "https://example.com/page",
      "latest_update": {
        "type": "URL_UPDATED",
        "notify_time": "2024-01-15T10:30:00Z"
      },
      "latest_remove": null,
      "error": null
    }
  ]
}
```

## API Quotas (free)

| Quota | Limit |
|-------|-------|
| Publish requests | 200/day (resets midnight PT) |
| Metadata reads | 600/min |
| Batch size | 100 URLs/request |

## Examples

Submit a single URL:
```bash
./scripts/google_indexing.py submit "https://example.com/new-post"
```

Bulk submit from file:
```bash
./scripts/google_indexing.py submit --file sitemap-urls.txt -f table
```

Check status with table output:
```bash
./scripts/google_indexing.py status "https://example.com/page" -f table
```
