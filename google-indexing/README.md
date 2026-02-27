# Google Indexing

Notify Google when pages are added, updated, or removed using the [Web Search Indexing API](https://developers.google.com/search/apis/indexing-api/v3/quickstart). Bypasses waiting for normal crawling.

## Setup

### 1. Create a Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select existing)
3. Enable the **Web Search Indexing API**: [direct link](https://console.cloud.google.com/apis/library/indexing.googleapis.com)
4. Go to **IAM & Admin** > **Service Accounts** > **Create Service Account**
5. Name it (e.g. `indexing-api`), click **Create and Continue**, skip optional steps
6. Click the service account > **Keys** > **Add Key** > **Create new key** > **JSON**
7. Save the downloaded JSON key file somewhere safe

### 2. Add Service Account to Search Console

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property
3. **Settings** > **Users and permissions** > **Add user**
4. Enter the service account email (from the JSON key, e.g. `indexing-api@project.iam.gserviceaccount.com`)
5. Set permission to **Owner** (required — lower permissions won't work)

### 3. Configure Environment

Set the path to your JSON key file:

```bash
export GOOGLE_INDEXING_KEY_FILE=/path/to/service-account-key.json
```

Or add to `.env` in your project root:

```bash
GOOGLE_INDEXING_KEY_FILE=/path/to/service-account-key.json
```

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/google-indexing

# Install for user (all projects)
npx claude-plugins install @nc9/skills/google-indexing --user
```

## Usage

### Submit URLs (new/updated)

```bash
./scripts/google_indexing.py submit "https://example.com/new-page"
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

### Bulk URL Input

```bash
# From file (one URL per line, # comments supported)
./scripts/google_indexing.py submit --file urls.txt

# From stdin
cat urls.txt | ./scripts/google_indexing.py submit

# Table output for human review
./scripts/google_indexing.py submit --file urls.txt -f table
```

## Options

| Option | Description |
|--------|-------------|
| `-k, --key-file` | Service account JSON key path (overrides env) |
| `-f, --format` | Output: `json` (default) or `table` |
| `--file` | File with URLs, one per line |
| `-b, --batch-size` | Batch size for publish requests (max 100) |

## Output

JSON by default:

```json
{
  "command": "submit",
  "total": 2,
  "succeeded": 2,
  "failed": 0,
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

## API Quotas

All free, no billing required:

| Quota | Limit |
|-------|-------|
| Publish requests | 200/day (resets midnight PT) |
| Metadata reads | 600/min |
| Batch size | 100 URLs/request |

## Key File Resolution

Searches in order:
1. `--key-file` CLI flag
2. `GOOGLE_INDEXING_KEY_FILE` env var
3. `.env` in current directory
4. `.env` in home directory
