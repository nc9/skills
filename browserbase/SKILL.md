---
name: browserbase
description: Fetch web pages via Browserbase headless browsers with proxy and automatic captcha solving. Use when a page is behind Cloudflare, bot protection or geo-restriction, or needs JavaScript rendered before its content is readable.
allowed-tools: Bash, Read
---

# Browserbase Fetch

Remote headless Chromium via Browserbase, with proxy, captcha solving and ad blocking.

## Requirements

- `BROWSERBASE_API_KEY` — [browserbase.com](https://browserbase.com/)
- `BROWSERBASE_PROJECT_ID` — from the Browserbase dashboard

## Commands

```bash
./scripts/browserbase_fetch fetch "https://example.com" [options]
./scripts/browserbase_fetch fetch-many "https://a.com" "https://b.com" [options]
```

## Options

| Option | Description |
|--------|-------------|
| `-f, --format` | `text` \| `html` \| `json` (default `text` for `fetch`, `json` for `fetch-many`) |
| `--proxy / --no-proxy` | Proxy, default on |
| `--captcha / --no-captcha` | Captcha solving, default on |
| `--block-ads / --no-block-ads` | Ad blocking, default on |
| `-t, --timeout` | Page load timeout, seconds (default 30) |
| `-w, --wait` | Extra wait after load, ms (default 0) |

## Output

`text` is `document.body.innerText`, `html` the rendered DOM, `json` is `{url, title, content}`. `fetch-many` emits an array of those objects, substituting `{url, error}` for any page that failed.

## Gotchas

- `fetch-many` ignores `-f` and always prints JSON. Use `fetch` per URL for text or html.
- Each `fetch` opens and releases its own billed session; `fetch-many` reuses one, so batch when you can. `--no-proxy` is cheaper and faster where geo and IP reputation do not matter.
- Load waits for `networkidle`, so pages that poll never settle — cap with `-t` and lean on `-w`.

## Examples

```bash
./scripts/browserbase_fetch fetch "https://example.com" -f json
./scripts/browserbase_fetch fetch "https://spa.example.com" -w 3000 -t 15
./scripts/browserbase_fetch fetch-many "https://a.com" "https://b.com" --no-proxy
```
