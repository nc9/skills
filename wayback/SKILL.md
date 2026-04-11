---
name: wayback
description: Query the Wayback Machine / Internet Archive — search snapshots, check availability, fetch archived page content. Use when user needs historical web pages, archived content, or wants to check if a URL was previously captured.
allowed-tools: Bash, Read
---

# Wayback Machine

Query the Internet Archive's Wayback Machine for archived web pages.

## When to Use

- User wants to see an old/archived version of a web page
- Checking if a URL/domain was previously active
- Retrieving historical page content
- Searching for all snapshots of a URL
- Comparing page content over time

## Requirements

No API key required — Wayback Machine is free and public.

## Commands

### search — Find snapshots

```bash
./scripts/wayback_search search "https://example.com" [-n 25] [--from 20200101] [--to 20231231]
```

### check — Quick availability check

```bash
./scripts/wayback_search check "https://example.com"
```

### latest — Fetch latest snapshot content

```bash
./scripts/wayback_search latest "https://example.com" [-f json]
```

### get — Fetch snapshot at specific timestamp

```bash
./scripts/wayback_search get "https://example.com" -t 20200101120000
```

## Options

| Option | Description |
|--------|-------------|
| `-n, --limit` | Max results for search (default: 25) |
| `--from` | Start date YYYYMMDD |
| `--to` | End date YYYYMMDD |
| `-s, --status` | Filter by HTTP status (e.g. 200) |
| `--collapse` | Dedupe by field (e.g. `digest`, `timestamp:6`) |
| `-m, --match` | URL match: `exact`, `prefix`, `host`, `domain` |
| `-t, --timestamp` | Snapshot timestamp for get/check |
| `--raw` | Return raw HTML instead of extracted text |
| `-c, --max-chars` | Max content chars (default: 10000) |
| `-f, --format` | Output: `json` (default) or `table` |

## Output Format

**search** — list of snapshots:
```json
[
  {"timestamp": "20200101120000", "original": "https://example.com/", "statuscode": "200", "mimetype": "text/html", "digest": "ABC123"}
]
```

**latest/get** — extracted content:
```json
{
  "url": "https://example.com",
  "timestamp": "20231215120000",
  "archiveUrl": "https://web.archive.org/web/20231215120000/https://example.com",
  "title": "Example Domain",
  "content": "Extracted page text..."
}
```

## Examples

Search with date range:
```bash
./scripts/wayback_search search "https://example.com" --from 20200101 --to 20201231
```

Search all subpages of a domain:
```bash
./scripts/wayback_search search "example.com" --match domain --status 200 -n 50
```

Deduplicate by content:
```bash
./scripts/wayback_search search "https://example.com" --collapse digest
```

Get page as it appeared on a specific date:
```bash
./scripts/wayback_search get "https://example.com" -t 20200615
```
