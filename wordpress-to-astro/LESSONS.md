# WordPress → Astro migration — lessons log

Running journal. Append a new entry every time something surprises us during a WP→Astro migration. Newest at top.

Format: **YYYY-MM-DD — Short title**
- **What happened:**
- **Why:**
- **How to apply next time:**

---

## 2026-05-28 — Pivot: Astro 6 beats TanStack Start for marketing sites

- **What happened:** We initially planned TanStack Start + Cloudflare Pages. Hit the worker-runtime-no-fs problem immediately, then the wrangler-OAuth-DNS-permission problem, then the CSS-in-CF problem. Pivoted to Astro 6 static + Cloudflare Pages + Pages Functions and the entire migration finished in a day.
- **Why:** A law-firm marketing site (44 pages + case studies + news, contact form, sitemap, JSON-LD) is a textbook static use case. TanStack Start is built for SSR/personalisation, which we don't need. Astro's Content Collections + `glob` loader + MDX is dramatically less ceremony than wiring `import.meta.glob` + gray-matter + unified by hand.
- **How to apply next time:** Default to **Astro 6** unless the brief explicitly requires per-user SSR, auth, or cart. The whole `app/` directory + `lib/content.ts` + TanStack Router scaffolding disappears.

## 2026-05-28 — Pages env vars only bind if config-as-code (wrangler.jsonc)

- **What happened:** Set `CONTACT_TO_EMAIL=sam@...` via the Cloudflare API `PATCH /pages/projects/<name>` deployment_configs endpoint. Verified it saved. Redeployed via `wrangler pages deploy`. The Function still used the default fallback. Emails kept landing in the wrong inbox.
- **Why:** `wrangler pages deploy` only auto-binds **secrets** (`secret_text` type) to the deployment it creates. Plain env vars set via the dashboard or the deployment_configs API are only applied to deployments triggered by **the dashboard's build pipeline** (i.e. git-connected builds). Wrangler-triggered direct uploads ignore them.
- **How to apply next time:**
  1. Put **non-secret** env vars in `wrangler.jsonc` under `"vars": { ... }` so they're config-as-code and ride along with every `wrangler pages deploy`.
  2. Put **secrets** (API keys) via `wrangler pages secret put NAME --project-name=<proj>` or via API with `"type": "secret_text"` — these *do* auto-bind.
  3. After changing env vars, **redeploy** — env changes don't apply retroactively to existing deployments.
  4. Verify what actually shipped: `curl -H "Authorization: Bearer $TOKEN" https://api.cloudflare.com/client/v4/accounts/$ACCT/pages/projects/<proj>/deployments?env=production&per_page=1` and check the `env_vars` block.

## 2026-05-28 — Maps Embed v1 + place_id for in-iframe rating

- **What happened:** Client wanted the Google Maps place card with "5.0 ★★★★★ (85 reviews)" visible inside the map iframe — not as separate UI we layered outside. Standard `maps.google.com/maps?q=ADDRESS&output=embed` only shows a map pin, no place card. Tried `q=place_id:ChIJ...&output=embed` — also no card, just a centered map.
- **Why:** The "no-key" embed URL doesn't resolve to the business listing. The **Maps Embed API** (`embed/v1/place`) is the only no-effort way to render the place card with rating. It requires an API key but has **zero quota cost** — Google explicitly states the Embed API is free with no usage limits, even though other Maps APIs are paid.
- **How to apply next time:**
  1. Ask the client for the place ID (the `ChIJ...` string from the Google Maps URL of their business).
  2. Create a Google Cloud API key, enable only "Maps Embed API", restrict to HTTP referrers (`https://example.com/*`, `https://*.pages.dev/*`, `http://localhost:3000/*`).
  3. Store as `PUBLIC_GOOGLE_MAPS_EMBED_KEY` (Astro `PUBLIC_` prefix → baked into the build).
  4. Iframe: `https://www.google.com/maps/embed/v1/place?key=${KEY}&q=place_id:${PLACE_ID}&zoom=15`.
  5. The key is visible in HTML — that's expected and safe **only** if you've set HTTP referrer restrictions in Cloud Console.

## 2026-05-28 — Custom domain wiring needs DNS write permission

- **What happened:** Wrangler OAuth token has `pages:write` + `zone:read` but NOT `dns_records:edit`. Could `POST /pages/projects/<name>/domains` to register the domain against the Pages project — Cloudflare accepted, marked it "pending validation: CNAME record not set". But couldn't update the DNS records to actually point at `<project>.pages.dev` via API.
- **Why:** Wrangler's OAuth flow doesn't request DNS edit. The dashboard does it implicitly when you add a custom domain via the UI. Direct API calls need either a token with `dns_records:edit` scope or the user updating DNS themselves.
- **How to apply next time:**
  1. Register the domain via API (`POST /domains` on the Pages project). This is the easy part.
  2. Tell the user to update DNS in the dashboard: `@` (apex) and `www` both `CNAME` → `<project>.pages.dev`, **proxied**.
  3. Delete any leftover A/AAAA records pointing at the old WP origin — these cause **HTTP 522** at the apex (CF can't reach the dead origin).
  4. Verify with `dig CNAME example.com @1.1.1.1`. The Pages domain status moves from "CNAME record not set" → "active" within seconds once the record is correct.
  5. If the user wants a server-side option, ask them to create a scoped API token with `Zone:DNS:Edit` for that one zone and paste it.

## 2026-05-28 — Cloudflare Email Obfuscation breaks audits

- **What happened:** Squirrelscan deep audit reported **94 broken internal links** on the new prod site — all pointing at `/cdn-cgi/l/email-protection#...`. Initially scoped 4-6 hours of "fix broken links" work into the audit response. It was actually zero work — Cloudflare Email Obfuscation (Scrape Shield) rewrites every `mailto:` link in HTML on the fly.
- **Why:** When Email Obfuscation is on, CF replaces `<a href="mailto:sam@firm.com">sam@firm.com</a>` with `<a href="/cdn-cgi/l/email-protection#HEXENCODED" class="__cf_email__">[email protected]</a>` and includes a client-side script to decode and reveal it. Crawlers (squirrelscan, Googlebot) see `[email protected]` as the link text — that's why "email protected" sometimes shows up in Google search results.
- **How to apply next time:**
  1. After deploying, turn off **Scrape Shield → Email Address Obfuscation** for the zone.
  2. If you can't (client policy etc.), accept the audit noise — those 94 "broken links" are working in browsers.
  3. Either way, also strip `cdn-cgi/l/email-protection` patterns at scrape time when ingesting the old WP site, since CF may have obfuscated outbound links inside scraped content too.

## 2026-05-28 — Squirrelscan dev-server noise is everywhere

- **What happened:** First squirrel audit ran against `http://localhost:3000` and returned a **35/F** grade with claims like "leaked DigitalOcean Spaces key in @vite/client", "JS file > 250 KB", "no compression", "render-blocking resources", "no sitemap", "35 broken links". Felt like the site was in worse shape than it was.
- **Why:** Astro dev injects `/@vite/client` (which contains literal example strings that match secret-detection regex), serves unminified CSS/JS, doesn't gzip, and Astro builds the sitemap at production build time. Also, the dev server compiles routes on demand — a fast crawler hits 404 on a route mid-compile, audit logs it as broken even though it returns 200 a moment later.
- **How to apply next time:**
  1. Run an initial squirrel audit on localhost to find **real content issues** (alt text, meta descriptions, heading order, image dimensions) — these *are* real.
  2. Disregard the Performance, Security, and Crawlability category scores entirely on localhost — they're dominated by dev-mode artifacts.
  3. **After deploying to prod, re-audit on the live URL**. The numbers change dramatically (we went 35/F → 72/C on the same site within an hour just by deploying).
  4. Set sensible `_headers` (HSTS, CSP, immutable cache on `/_astro/*`, `/images/*`) and `_redirects` (sitemap aliases, WP-block) before launch — closes the second-tier of "real on prod too" warnings.

## 2026-05-28 — JSON-LD `LocalBusiness` wants a single primary address

- **What happened:** Set up `LegalService` schema for a multi-office firm with `address` as an **array** of `PostalAddress`. Squirrelscan flagged `schema/local-business: Address incomplete`. Looked correct — the Schema.org docs allow it. Google didn't care for it.
- **Why:** Schema.org technically allows arrays, but `LocalBusiness`/`LegalService` consumers (Google Rich Results, validators) treat the schema as describing **one** local business per page. The home page is the "main" business; sub-locations should be separate pages with their own `LegalService` schema (one office each).
- **How to apply next time:**
  1. Home page: single primary `address` of the head office. Add `location[]` of `Place` for sub-offices if you want to list them.
  2. Each `/locations/<slug>/` page: full `LegalService` schema with that one office's address + its own `aggregateRating`.
  3. Also emit `BreadcrumbList` schema on every non-home page — separate `<script type="application/ld+json">` block.

## 2026-05-28 — Content groundedness is the actual moat

- **What happened:** GSC analysis after launch showed the firm ranks page 2-3 for "criminal lawyer Liverpool" (1,661 imp), "common assault" (271 imp), "high range pca" (235 imp). The pages existed but were 19-65 lines of generic copy. Expanded them with verified NSW statute references — section numbers, exact max penalties, sentencing options, defences, FAQ for long-tail queries. That work, more than any technical SEO, is what moves rankings.
- **Why:** Legal queries reward authoritative content. Google's helpful-content + E-E-A-T systems privilege pages that quote statute, cite real case law, and answer the specific FAQ that the long-tail query expressed.
- **How to apply next time:**
  1. The Judicial Commission of NSW Local Court Bench Book is the **authoritative penalty source** for NSW criminal & traffic offences — and unlike AustLII / legislation.nsw.gov.au, WebFetch can read it.
  2. AustLII and legislation.nsw.gov.au sit behind Cloudflare 403/anti-bot; expect to use 2nd-tier sources (gotocourt, armstronglegal, sydneycriminallawyers, Judicial Commission). Cross-reference numbers across 2+ sources before committing.
  3. NSW penalty unit = $110 (2024). Don't display "30 pu" without the dollar equivalent.
  4. **Never invent case law.** When citing a guideline judgment (e.g. *R v Whyte* for s 52A), web-search to confirm citation + year + relevance before writing. Spot-check sub-agents' citations specifically.
  5. The exact phrases people search for are gold. "Can I get a section 10 for mid range pca" had 297 combined impressions across variations — write a dedicated H2 with that exact phrase in it.
  6. Have the firm's lawyer review the expanded pages before marketing them — even with grounded research, legal-content review is essential.

## 2026-05-28 — GSC service account permission threshold

- **What happened:** Docs say the Google Indexing API requires **Owner** access in Search Console. Tried submitting URLs with the service account added as **Restricted** (the default safest setting). Expected 403 across the board. Actually got **34/34 OK**.
- **Why:** Behaviour appears more permissive than documented for verified **domain-property** accounts (vs URL-prefix). The API accepted submissions even at Restricted. Indexing isn't actually triggered by the API alone — Google still has to decide to crawl — so the API's tolerance for permissions may be why.
- **How to apply next time:**
  1. Start by adding the service account at **Restricted** (read). It's enough for `performance` queries and *often* enough for `submit`.
  2. If submissions 403, bump to **Owner**.
  3. After each meaningful content push, submit the changed URLs via the Indexing API. Quota is 200/day.

---

## 2026-05-27 — TanStack Start dev runs in Cloudflare Worker — no fs

- **What happened:** Wrote `src/lib/content.ts` using `node:fs/promises` to read MDX from `content/` at request time. Every route that called the loader threw `about.mdx not found` (or similar). At first looked like a path issue, but the real cause is that the `@cloudflare/vite-plugin` runs the SSR worker in the Workers runtime even in `vite dev` — there is no Node fs and `process.cwd()` is `/`. The same code would also fail when deployed.
- **Why:** Cloudflare Workers don't expose a filesystem. Reading files needs to happen at build time, not at runtime, or files must be served via the `ASSETS` binding (which is heavier).
- **How to apply next time:**
  1. Default content loader for TanStack Start + Cloudflare = `import.meta.glob('/content/**/*.mdx', { query: '?raw', import: 'default', eager: true })`. Files get inlined as strings into the worker bundle.
  2. Parse frontmatter from the inlined strings with `gray-matter`; render to HTML with unified at request time (cheap).
  3. Build an in-memory index keyed by `{dir, slug}` once at module load.
  4. Same applies to any data file (json, txt, yaml). Use `import.meta.glob` or direct `import` — never `readFile`.
  5. Also a more-general lesson: when a TanStack Start error message names a *file path* and you're sure the file exists, suspect runtime env (worker vs node) before path/typo issues.

- **Side observation:** `createServerFileRoute` is gone in v1.168 of `@tanstack/react-start`. The new pattern is `createFileRoute('/path')({ server: { handlers: { GET, POST } } })`. Always check the installed version's `.d.ts` first if a function name doesn't resolve.

## 2026-05-27 — Scraper title and image cleanup

- **What happened:** First scrape pulled every page title with a "Karnib & Co. Criminal Defence Lawyers - " site-name prefix because that's how the site sets `<title>` and `og:title`. Many pages also had repeated decorative images (`dark_logo`, `white_logo`, `quotation`) that Elementor injects as section ornaments, plus the whole header navigation embedded inside `main` content because Elementor builds the *entire page* including header/footer as one big elementor-section tree.
- **Why:** Most Elementor sites don't use a separate theme `<header>` — header/menu/footer are all `.elementor-section` elements inside the WP-page. `.entry-content` often doesn't exist; `main` includes the whole layout.
- **How to apply next time:**
  1. Always strip site-name prefix/suffix from `og:title` before saving. Maintain a `SITE_NAME_PATTERNS` regex list.
  2. Maintain a `DECORATIVE_IMG_PATTERNS` list (logos, favicons, "quotation" graphics, etc.) and drop them.
  3. Detect & remove the embedded nav `<ul>` by counting how many of its links match the site's known top-level routes — if >60% are internal nav links, the `<ul>` is the menu, drop it.
  4. Strip Cloudflare email-protection links (`/cdn-cgi/l/email-protection#...`).
  5. Strip "Skip to content" anchors.
  6. Fall back from `.entry-content` to picking the longest `div[data-elementor-type="wp-page"]` element by text length.
  7. Orphan kicker labels (e.g. "Criminal Law", "Case overview") survive turndown as bare paragraphs — accept this and surface them in the page template as visual section labels, or strip them via a post-process regex if not wanted.

## 2026-05-27 — Initial setup

First migration: legalaccess.com.au (Karnib & Co. Lawyers).

- WP XML export had only 5 pages / 1 post / 6 media articles even though the live site has 44 pages + 13 case studies. The WP export was 2 years stale. **Always check the live sitemap first** to estimate true content size, then decide if XML is useful.
- Site uses Elementor + Gravity Forms + Rank Math SEO — the common Australian small-business WP stack. Scrape live HTML, not XML.
- Live URLs use trailing slashes consistently. Permalink format `/<YYYY>/<MM>/<DD>/<slug>/` for date-based posts; custom post type `media_article` at `/news/media_article/<slug>/`.
- Brand colours found via `getComputedStyle` on `.elementor-button` — gold `#bf9752` was clear; font stack `Work Sans` + `Figtree`.
