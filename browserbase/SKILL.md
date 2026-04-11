---
name: browserbase
description: Fetch web pages via Browserbase with proxy and captcha solving. Use when you need to scrape pages behind captchas, bot protection, or geo-restrictions.
allowed-tools: Bash, Read
---

# Browserbase Fetch

Fetch web pages using Browserbase headless browser with proxy and automatic captcha solving.

## When to Use

- Need to fetch a page behind Cloudflare/captcha protection
- Need to scrape content that blocks bots
- Need geo-located browsing via proxy
- Need rendered JavaScript content (not just raw HTML)

## Requirements

- `BROWSERBASE_API_KEY` - [Get at browserbase.com](https://browserbase.com/)
- `BROWSERBASE_PROJECT_ID` - from your Browserbase dashboard

## Commands

### fetch — Single URL

```bash
./scripts/browserbase_fetch fetch "https://example.com" [-f text] [--no-proxy]
```

### fetch-many — Multiple URLs (one session)

```bash
./scripts/browserbase_fetch fetch-many "https://a.com" "https://b.com" [-f json]
```

## Options

| Option | Description |
|--------|-------------|
| `-f, --format` | Output: `text` (default), `html`, `json` |
| `--proxy/--no-proxy` | Enable Browserbase proxy (default: on) |
| `--captcha/--no-captcha` | Enable captcha solving (default: on) |
| `--block-ads/--no-block-ads` | Block ads (default: on) |
| `-t, --timeout` | Page load timeout in seconds (default: 30) |
| `-w, --wait` | Extra wait after load in ms (default: 0) |

## Output Format

**text** (default) — page body text, ideal for LLM consumption

**html** — full rendered HTML

**json** — structured output:
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "Page body text..."
}
```

## Examples

Fetch with proxy + captcha (defaults):
```bash
./scripts/browserbase_fetch fetch "https://example.com"
```

Fetch as HTML:
```bash
./scripts/browserbase_fetch fetch "https://example.com" -f html
```

Without proxy (faster, cheaper):
```bash
./scripts/browserbase_fetch fetch "https://example.com" --no-proxy
```

Wait for dynamic content:
```bash
./scripts/browserbase_fetch fetch "https://example.com" -w 3000
```

Multiple pages:
```bash
./scripts/browserbase_fetch fetch-many "https://a.com" "https://b.com" "https://c.com"
```
