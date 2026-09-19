---
name: google-indexing
description: Submit, remove, or check indexing status of URLs via Google's Indexing API and Bing's Webmaster URL Submission API. Use to notify Google or Bing about new, updated, or deleted pages, or to speed up crawling of a site.
allowed-tools: Bash, Read
---

# Search Engine Indexing (Google + Bing)

Tell Google and Bing that pages were added, updated, or removed, and read back what was
last notified.

## Requirements

- `GOOGLE_INDEXING_KEY_FILE` — path to a Google Cloud service account JSON key. The
  service account email must be added as an **Owner** of the property in Search Console.
- `BING_WEBMASTER_API_KEY` — account-level key from Bing Webmaster Tools → Settings → API
  access. It covers every site verified under that account; unverified sites return
  `NotAuthorized`.

## Google

```bash
./scripts/google_indexing submit "https://example.com/new-post"
./scripts/google_indexing remove "https://example.com/old-page"
./scripts/google_indexing status "https://example.com/page" -f table
./scripts/google_indexing quota
```

All URL commands take positional URLs, `--file urls.txt`, or stdin. Options:
`-k/--key-file`, `-f/--format json|table`, `--file`, `-b/--batch-size` (max 100).

## Bing

```bash
./scripts/bing_submit sitemap example.com                       # every URL in sitemap.xml
./scripts/bing_submit submit https://example.com https://example.com/new-post
./scripts/bing_submit submit https://example.com --file urls.txt
./scripts/bing_submit quota https://example.com
```

`submit` takes the site URL first — it must match the Bing Webmaster Tools property
exactly. URLs come from positional args, `--file`, or stdin. `-f/--format json|table`.

## Quotas

| Quota | Limit |
|-------|-------|
| Google publish requests | 200/day, resets midnight PT |
| Google metadata reads | 600/min |
| Google batch size | 100 URLs/request |
| Bing submissions | ~100/day, ~1600/month per site (grows with site age and trust) |
| Bing batch size | 500 URLs/call (auto-chunked) |

## Gotchas

- Bing rejects a batch **wholesale** when it exceeds the remaining quota, so `bing_submit`
  pre-checks quota and reports the overflow as `"deferred": N` — re-run the next day to
  send the rest.
- Google's Indexing API is officially supported only for `JobPosting` and
  `BroadcastEvent` pages; other URLs are accepted but Google may ignore the hint.
- The Bing Webmaster API does **not** fan out to IndexNow partners (Yandex, Naver, Seznam,
  Yep). That needs a real IndexNow ping plus a `/{key}.txt` file served at the domain root.
- Submitting is a hint, not indexing. Use `status` (Google) to confirm what was notified,
  and Search Console / Bing Webmaster Tools to confirm what was actually indexed.
