# WordPress → Astro

Migrate a WordPress site (Elementor + Gravity Forms + Rank Math SEO is the common Australian small-business stack) to a static **Astro 6 + MDX** site on **Cloudflare Pages**, with a contact form via **Pages Functions + Resend**, **JSON-LD** for Local SEO, and a real **Search Console + squirrelscan** refinement loop after launch.

## What this skill gives you

- A vetted stack — Astro 6, Tailwind v4, Content Collections (`glob` loader), Pages Functions, Resend
- Directory layout that maps cleanly from WP routes to Astro file routes (including dated post permalinks)
- A scrape recipe (live HTML → MDX + downloaded images) that handles Elementor's wrapper soup, embedded nav menus, decorative images, and the `cdn-cgi/l/email-protection` Cloudflare obfuscation
- A working Pages Functions contact endpoint with Zod validation, honeypot, and Resend HTTPS call (no SDK bundled)
- Cloudflare Pages config — `wrangler.jsonc` `vars`, `_headers`, `_redirects`, custom domain wiring via API
- The Google Maps **Embed v1 place_id** pattern that makes business listings (rating + reviews) render inside the map
- JSON-LD schema patterns — `LegalService` + `BreadcrumbList` per location page, single primary `address` + `location[]` for multi-office
- A Search Console + squirrelscan loop for refining content after the site is indexed
- A `LESSONS.md` running journal of non-obvious gotchas (one per dated entry)

## When to use

Trigger this skill whenever a user wants to:

- "Migrate this WordPress site to Astro"
- "Replace this WP site with a static one on Cloudflare"
- "Convert this WP site to MDX"
- "Scrape this WP site and rebuild it"

Especially if the source is Elementor + Gravity Forms + Rank Math — that combo is the well-trodden path.

## When NOT to use

- The user is keeping WordPress (headless WP, custom theme) — different problem
- WooCommerce — static won't cover it
- Sites with thousands of posts where scraping is too slow — use a Postgres dump
- Sites that need SSR for personalisation, auth, or per-user content — use TanStack Start or Astro with an SSR adapter

## Prerequisites

| Tool / service | Why |
|---|---|
| `bun` | Run scripts, install deps |
| Cloudflare account | Pages hosting, DNS (recommended on same account as the zone) |
| `wrangler` CLI | Deploy + secrets |
| Resend account | Transactional email for the contact form |
| Google Cloud project | Maps Embed API key (free, no quota) |
| Google Search Console | Verify the new domain, drive content refinement |
| `squirrel` CLI ([squirrelscan.com](https://squirrelscan.com)) | Post-launch SEO + a11y + perf audit |

## Files in this skill

- `SKILL.md` — the full recipe (directory layout, content collections schema, scrape steps, Pages Functions config, deploy gotchas, SEO refinement loop, content depth guidance for legal/regulated niches)
- `LESSONS.md` — running journal of non-obvious things we learned, newest at top. **Append to this every time something surprises you.**

## How to use

1. The skill auto-triggers when the user mentions WP→Astro migration. Open `SKILL.md` and follow the recipe top-to-bottom.
2. Before deploying anything, run the scrape script and review the output MDX files. Almost every page needs at least one content cleanup pass before the firm's people approve it.
3. Deploy to Cloudflare Pages preview (`<hash>.pages.dev`), then wire the real domain after the user confirms the preview matches.
4. Run `squirrel audit https://<live-domain>/ --coverage full` after launch and triage findings (the SKILL has the full triage rubric).
5. Add the GSC service account, wait 1-2 days, then use the GSC performance data to drive content expansion on real-demand pages.
6. **Append a new entry to `LESSONS.md`** any time the migration surprises you in a way that the next migration will benefit from knowing.

## Related skills

- [audit-website](../audit-website/) — squirrelscan deep audit
- [google-search-console](../google-search-console/) — pull performance + indexing data
- [google-indexing](../google-indexing/) — submit URLs after each content push
- [keyword-research](../keyword-research/) — supplement GSC data with volume/CPC where DataForSEO has regional coverage
- [optimize-image-web](../optimize-image-web/) — convert scraped JPGs to WebP, generate the 1200×630 OG card
- [humanizer](../humanizer/) — pass over scraped or expanded copy so it doesn't read as AI-generated
