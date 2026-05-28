---
name: wordpress-to-astro
description: Migrate a WordPress site (especially Elementor + Gravity Forms) to a static Astro site on Cloudflare Pages, with MDX content collections, a contact form via Pages Functions + Resend, JSON-LD SEO, and a real Search-Console-driven content refinement loop. Triggers on requests like "migrate WordPress to Astro", "WP to static site", "convert this wp site to MDX", "scrape WordPress to Astro". Provides the proven recipe end-to-end.
---

# WordPress → Astro + MDX migration

## Default stack (use this unless there's a specific reason not to)

- **Astro 6** with `output: "static"`, `trailingSlash: "always"`, `build.format: "directory"`
- **Astro Content Collections** (the `glob` loader) for MDX content
- **MDX** via `@astrojs/mdx`
- **React** (only) for interactive components (`@astrojs/react`) — contact form, mobile nav
- **Tailwind v4** via `@tailwindcss/vite` with `@theme` CSS-first tokens; legacy `:root --foo` mirrors for back-compat
- **Cloudflare Pages** (static) + **Pages Functions** for the contact endpoint
- **Resend** for transactional email; call the HTTPS API directly from the Function (no SDK — keep the bundle small)
- **Zod** for validation
- **bun** for everything; `oxlint`, `oxfmt`
- **`@astrojs/sitemap`** for `sitemap-index.xml` + `sitemap-0.xml`
- **`@astrojs/check`** for typecheck

Why Astro over TanStack Start: for a content-heavy marketing site (44 pages + case studies + news), Astro's static output is dramatically simpler, faster, cheaper, and avoids the Cloudflare-Worker-runtime gotchas that show up immediately in TanStack Start (no fs at runtime, content must be inlined via `import.meta.glob`, etc.). Use TanStack Start only if the site needs SSR for personalisation, auth, or cart.

## Directory layout

```
src/
├─ pages/                         # file routes, .astro + .mdx
│  ├─ index.astro
│  ├─ about.astro
│  ├─ contact.astro
│  ├─ criminal-law/
│  │  ├─ index.astro
│  │  └─ [slug].astro
│  ├─ news/
│  │  ├─ index.astro
│  │  ├─ category/[cat].astro
│  │  ├─ media_article/[slug].astro
│  │  └─ [year]/[month]/[day]/[slug].astro      # preserves WP YYYY/MM/DD permalink
│  └─ locations/[slug].astro
├─ content/
│  ├─ pages/  criminal-law/  traffic-offences/
│  ├─ case-studies/  media/  news/  team/  locations/
├─ content.config.ts              # Zod schemas, glob() loaders
├─ components/
│  ├─ ui/   (Button, Icon, Kicker, GoogleRating, PublicationLogo, SectionHeader)
│  ├─ sections/ (ServiceCard, HighlightCard, TestimonialCard, TeamCard, NewsCard)
│  ├─ Header.astro Footer.astro CtaBanner.astro PageHero.astro
├─ layouts/Base.astro             # html shell, meta, JSON-LD slot
├─ lib/  (utils.ts, publications.ts)
├─ styles/globals.css             # Tailwind v4 + @theme tokens
├─ config/site.ts                 # offices, phone, email, social, defaultOgImage
└─ emails/ContactEnquiry.tsx      # React Email template
functions/                        # Cloudflare Pages Functions (auto-loaded by CF)
└─ api/contact.ts                 # POST /api/contact -> Resend
public/
├─ _headers _redirects robots.txt
├─ favicon.ico  favicon.png
├─ images/                        # all scraped images (preserve WP paths)
└─ images/og/legalaccess-og.jpg   # 1200x630 OG card
scripts/
├─ scrape-site.ts                 # live -> MDX + images (bun run)
└─ extract-xml.ts                 # WP export -> news fallback
astro.config.mjs  wrangler.jsonc  squirrel.toml  package.json
.env.local                        # gitignored: RESEND_*, PUBLIC_GOOGLE_MAPS_EMBED_KEY
```

## Content collections schema (Astro)

```ts
// src/content.config.ts
import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const baseSeo = z.object({
  title: z.string(),
  excerpt: z.string().optional(),
  metaTitle: z.string().optional(),
  metaDescription: z.string().optional(),
  metaImage: z.string().optional(),
  heroImage: z.string().optional(),
});

const criminalLaw = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/criminal-law" }),
  schema: baseSeo.extend({ order: z.number().optional() }),
});

const team = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/team" }),
  schema: baseSeo.extend({
    role: z.string(),
    portrait: z.string(),
    locations: z.array(z.string()).optional(),   // multi-office support
    admittedYear: z.number().optional(),
    order: z.number().optional(),
  }),
});

const locations = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/locations" }),
  schema: baseSeo.extend({
    office: z.string(),                          // links to site.offices[].name
    lead: z.string().optional(),
    courts: z.array(z.string()).optional(),
    serviceAreas: z.array(z.string()).optional(),
  }),
});

export const collections = { /* ...all collections... */ };
```

`getCollection(name)` in `getStaticPaths()` for `[slug].astro` pages. Use `render(entry)` for the MDX `<Content/>`.

## Content migration recipe

1. **Get sitemaps first** — every WP site exposes `/sitemap_index.xml`. Enumerate every child sitemap (`page-sitemap`, `post-sitemap`, custom post types, `category-sitemap`). This is the source of truth for URLs to migrate.
2. **Don't trust the WP XML export for content** — usually stale and Elementor stores page bodies as serialized JSON in `<wp:postmeta>`. Use it only for: author/byline data, the rare native post body, and to fill in the dates on a date-permalinked post that the live HTML doesn't expose.
3. **Scrape live HTML** with cheerio. Selectors that usually contain real content: `.entry-content` → `main article` → `main` → fall back to the longest `div[data-elementor-type="wp-page"]` by text length. Most Elementor sites don't have `.entry-content`.
4. **Strip Elementor wrappers** before turndown: remove `script`, `style`, `noscript`, `.elementor-widget-icon`, `.elementor-widget-spacer`, `.elementor-widget-divider`. Unwrap `.elementor-widget-container`, `.elementor-widget-wrap`, `.elementor-column`, `.elementor-row`.
5. **Convert HTML→MD** with `turndown` (heading rule `atx`, code block `fenced`). Custom rules for `<figure>+<figcaption>`, `<blockquote>`, accordion/tab widgets.
6. **Rewrite image URLs** during turndown: `https://<site>/wp-content/uploads/PATH` → `/images/PATH`. Download each to `public/images/PATH` preserving the original path (so CDN paths stay stable). Stream with `fetch` + `Bun.write`. Skip already-downloaded files.
7. **Frontmatter from `<head>`**: title from `og:title` or `<title>` (strip the site-name prefix); description from `meta[name=description]` or `og:description`; OG image from `og:image`. Maintain a `SITE_NAME_PATTERNS` regex list.
8. **Strip filler images**: maintain a `DECORATIVE_IMG_PATTERNS` list (`dark_logo`, `white_logo`, `quotation`, `placeholder`, favicons). Drop them at scrape time.
9. **Strip embedded nav menus**: count internal-link ratio inside `<ul>` elements — if >60% of href values match top-level routes, it's the navigation, drop it.
10. **Strip Cloudflare email obfuscation links** — `/cdn-cgi/l/email-protection#...` — at scrape time AND turn off Scrape Shield → Email Obfuscation on the destination zone after deploy.
11. **Idempotent re-runs** — scrape script should never duplicate files; only re-download missing images.

## Permalink preservation (Astro static)

| WP pattern | Astro route |
|---|---|
| `/<slug>/` | `src/pages/<slug>.astro` |
| `/<cat>/<slug>/` | `src/pages/<cat>/[slug].astro` |
| `/<YYYY>/<MM>/<DD>/<slug>/` | `src/pages/<cat>/[year]/[month]/[day]/[slug].astro` |
| `/category/<cat>/` | `src/pages/<cat>/category/[cat].astro` |
| Custom post type `/<cpt>/<slug>/` | `src/pages/<cpt>/[slug].astro` |

Set `trailingSlash: "always"` + `build.format: "directory"` in `astro.config`. Cloudflare Pages serves `/foo/index.html` on `/foo/` requests; `/foo` (no slash) does a 308 → `/foo/` automatically.

For internal links — always emit with the trailing slash, or you get a 308 hop on every nav click that shows up as `links/redirect-chains` warnings in squirrelscan.

## SEO — Base.astro & JSON-LD

`Base.astro` should:
- Compose `title` as `${title} | ${site.name}` only when total length ≤ 60; otherwise use raw title alone
- Default `og:image` to `site.defaultOgImage` (a generated 1200×630 brand card; generate once with `magick -size 1200x630 xc:NAVY -fill GOLD ... legalaccess-og.jpg`)
- Always emit `og:image:width=1200`, `og:image:height=630`
- Emit `<meta name="author">` on `ogType="article"` pages
- Google Fonts via `<link rel="preconnect">` + `<link rel="preload" as="style">` + `<link rel="stylesheet">` — **never** `@import url("https://fonts.googleapis...")` in CSS (creates a critical request chain)

JSON-LD on every law-firm site:
- Home: `LegalService` with `address` (primary office), `location[]` of `Place` (all offices), `aggregateRating`, `sameAs`, `areaServed`
- Per location page: `LegalService` keyed to that single office's address + `BreadcrumbList`
- News article pages: `Article` with `author`, `datePublished`, `image`
- Squirrelscan's `schema/local-business` rule wants a **single** `address` object — pass an array as `location[]` instead

## Pages Functions for the contact form

Drop the file `functions/api/contact.ts` at repo root. CF Pages auto-loads `functions/**` and routes them. The Astro static output is in `dist/`; CF serves Functions alongside static assets — no extra config.

```ts
// functions/api/contact.ts
import { z } from "zod";
import { render } from "@react-email/render";
import { ContactEnquiry } from "../../src/emails/ContactEnquiry";

const ContactSchema = z.object({
  name: z.string().min(1).max(120),
  email: z.string().email(),
  phone: z.string().max(40).optional().or(z.literal("")),
  message: z.string().min(10).max(8000),
  _hp: z.string().optional(),       // honeypot
});

type Env = { RESEND_API_KEY: string; CONTACT_FROM_EMAIL?: string; CONTACT_TO_EMAIL?: string; };

export const onRequestPost: PagesFunction<Env> = async (ctx) => {
  const body = await ctx.request.json().catch(() => null);
  const parsed = ContactSchema.safeParse(body);
  if (!parsed.success) return Response.json({ error: parsed.error.issues[0].message }, { status: 400 });
  if (parsed.data._hp) return Response.json({ ok: true });          // bot, fake success
  const html = await render(ContactEnquiry({ ...parsed.data }));
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${ctx.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: ctx.env.CONTACT_FROM_EMAIL!,
      to: ctx.env.CONTACT_TO_EMAIL!,
      subject: `New enquiry from ${parsed.data.name}`,
      html,
      reply_to: parsed.data.email,
    }),
  });
  if (!res.ok) return Response.json({ error: "Could not send" }, { status: 500 });
  return Response.json({ ok: true });
};
```

**Honeypot the right way**: a real off-screen `<label>` containing a real `<input>` with `tabIndex={-1}` and `autoComplete="off"`. **Never** use `aria-hidden` on a focusable input — squirrelscan flags it as `a11y/aria-hidden-focus`.

## Cloudflare Pages deployment

### wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "legalaccess",
  "pages_build_output_dir": "./dist",
  "compatibility_date": "2025-09-02",
  "compatibility_flags": ["nodejs_compat"],
  "vars": {
    "CONTACT_TO_EMAIL":   "sam@example.com",
    "CONTACT_FROM_EMAIL": "Firm Name <noreply@mail.example.com>",
    "RESEND_SEND_DOMAIN": "mail.example.com"
  }
}
```

**Critical lesson**: `wrangler pages deploy` only auto-binds **secrets** to deployments. Plain env vars set via the dashboard or `PATCH /pages/projects/{name}` deployment_configs API **do not** flow into deployments triggered by wrangler. Put non-secret vars in `wrangler.jsonc` `"vars"` so they're config-as-code and bind to every deploy. Secrets (API keys) stay set via:

```bash
wrangler pages secret put RESEND_API_KEY --project-name=<name>
```

or via API with `"type": "secret_text"`.

### public/_headers

```
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob:; frame-src https://www.google.com https://maps.google.com; connect-src 'self'; base-uri 'self'; form-action 'self';

/_astro/*       Cache-Control: public, max-age=31536000, immutable
/images/*       Cache-Control: public, max-age=31536000, immutable
/*.webp         Cache-Control: public, max-age=31536000, immutable
/*.png          Cache-Control: public, max-age=31536000, immutable
/*.css          Cache-Control: public, max-age=31536000, immutable
/*.js           Cache-Control: public, max-age=31536000, immutable
```

### public/_redirects

```
# Block legacy WP paths
/wp-admin/* /404 410
/wp-login.php /404 410
/wp-content/* /404 410
/xmlrpc.php /404 410

# Legacy WP feed -> news
/feed/  /news/  301
/feed/* /news/  301

# Sitemap aliases — squirrelscan probes these
/sitemap.xml       /sitemap-index.xml  301
/sitemap_index.xml /sitemap-index.xml  301
/sitemaps.xml      /sitemap-index.xml  301
/post-sitemap.xml  /sitemap-0.xml      301
```

### Custom domain wiring (via API, when wrangler OAuth lacks DNS scope)

```bash
TOKEN=<bearer>; ACCT=<account-id>
# Register both apex + www on the Pages project
for D in example.com www.example.com; do
  curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCT/pages/projects/<proj>/domains" \
    -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    --data "{\"name\":\"$D\"}"
done
```

Then in the CF dashboard DNS panel:
- `@` (apex): **CNAME** → `<project>.pages.dev`, **proxied**. CF flattens CNAME at apex automatically.
- `www`: **CNAME** → `<project>.pages.dev`, **proxied** (or remove the Pages binding if you prefer a CF redirect rule to apex)
- Delete any existing A/AAAA records pointing at the old WP origin.

If the apex returns **HTTP 522** after the change, an A record pointing at a dead WP origin is still in place — find it and delete it.

If the dashboard shows "CNAME record not set" for the Pages domain, the CNAME isn't propagated yet or there's a competing record. Verify with `dig CNAME example.com @1.1.1.1`.

### CF settings to flip after launch

- **Scrape Shield → Email Address Obfuscation: OFF** — otherwise CF rewrites every `mailto:` into `/cdn-cgi/l/email-protection#...`, which (a) shows `[email protected]` in audits and SERPs and (b) is flagged as 50+ "broken links" by squirrelscan.
- (Optional) Speed → Brotli; Caching → Browser TTL.

## Map embeds — show the place card, not just the address

`?q=address&output=embed` returns a plain map. To get the **place card with rating + reviews** in-iframe (which is what clients want), use the **Maps Embed API** with each office's place_id:

```html
<iframe src="https://www.google.com/maps/embed/v1/place?key=KEY&q=place_id:ChIJ...&zoom=15" />
```

The Maps Embed API is **free, no quota** (unlike other Maps APIs). Steps:

1. Get each office's `place_id` from the client (open Google Maps → click the business → URL contains `!1s0x...ChIJ...` — or just ask them for the ChIJ string).
2. Create an API key in https://console.cloud.google.com/apis/credentials. Enable only "Maps Embed API". Restrict to HTTP referrers (`https://example.com/*`, `https://*.pages.dev/*`, `http://localhost:3000/*`).
3. Store as `PUBLIC_GOOGLE_MAPS_EMBED_KEY` (PUBLIC_ prefix → exposed at Astro build time). Add to `.env.local` for build, and as a plain var on Pages for future git-builds.
4. Save `placeId` per office in `src/config/site.ts`.

## Analytics — GA4 + auto-tracked conversions

Drop a small `<Analytics>` component into `Base.astro <head>` that emits both the gtag loader and a single delegated click listener. No per-link `onclick` attributes anywhere.

```astro
<!-- src/components/Analytics.astro -->
{gaId && (
  <>
    <script async src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}></script>
    <script is:inline define:vars={{ gaId }}>
      window.dataLayer = window.dataLayer || [];
      function gtag(){ dataLayer.push(arguments); }
      window.gtag = gtag;
      gtag("js", new Date());
      gtag("config", gaId, { send_page_view: true });
      // Delegated listener: covers every <a> click site-wide, even mobile-nav links
      document.addEventListener("click", function (e) {
        let el = e.target;
        while (el && el !== document.body && el.tagName !== "A") el = el.parentNode;
        if (!el || el.tagName !== "A") return;
        const href = el.getAttribute("href") || "";
        const section = el.closest("header") ? "header" : el.closest("footer") ? "footer" : "body";
        const label = (el.textContent || "").trim().slice(0, 80);
        if (href.startsWith("tel:"))      gtag("event", "phone_click",    { phone_number: href.slice(4), link_text: label, section });
        else if (href.startsWith("mailto:")) gtag("event", "email_click", { email_address: href.slice(7), link_text: label, section });
        else if (/\/contact(\/|$|#)/.test(href)) gtag("event", "cta_click", { cta_type: "free_consultation", link_text: label, section, link_url: href });
        else if (/^https?:\/\//.test(href)) {
          try { const u = new URL(href); if (u.hostname !== location.hostname)
            gtag("event", "outbound_click", { outbound_url: href, outbound_domain: u.hostname, link_text: label, section });
          } catch {}
        }
      }, true);
    </script>
  </>
)}
```

Contact form fires `contact_form_submit` from the React component's success branch:
```ts
(window as any).gtag?.("event", "contact_form_submit", { form_id: "contact", page_path: location.pathname });
```

CSP additions:
- `script-src` + `https://www.googletagmanager.com`
- `connect-src` + `https://www.google-analytics.com https://*.analytics.google.com`
- `img-src` + the same

**Tell the client** to mark each event as a Key Event in GA4 (Admin → Events → Mark as key event) **after** the event fires the first time. The toggle isn't available until then.

## Live data on a static site (KV + Pages Function + client refresher)

When the client needs numbers that update without redeploys (Google reviews, inventory counts, status indicators), use stale-while-revalidate via a single Pages Function. **No separate Worker, no cron job, no scheduled handler.**

1. **KV namespace** — `wrangler kv namespace create REVIEWS_CACHE`; bind in `wrangler.jsonc`:
   ```jsonc
   "kv_namespaces": [{ "binding": "REVIEWS_CACHE", "id": "..." }]
   ```
2. **Function** at `functions/api/reviews.ts` (note: no `.json` extension — see [Pages Function naming gotcha](./LESSONS.md)):
   - GET handler reads `env.REVIEWS_CACHE.get("v1")`
   - Parses `fetched_at`; if `Date.now() - parsed > TTL_MS` (e.g. 1 hour), call `ctx.waitUntil(refresh())` and return the cached payload immediately
   - On cache miss with no value, refresh synchronously so the first request gets real data
   - Set response cache headers: `cache-control: public, max-age=300, stale-while-revalidate=3600`
3. **Upstream call** — fetch the source-of-truth API (Google Places API New for reviews) using a secret env var:
   ```bash
   echo -n "AIza..." | wrangler pages secret put GOOGLE_PLACES_API_KEY --project-name=<proj>
   ```
4. **Client refresher** — a tiny inline `<script is:inline>` in Base layout that fetches `/api/reviews` on every page load and updates `[data-place-id]` and `[data-review-badge="total"]` elements via `setText` helpers. Server-side initial paint uses placeholder values from `site.ts` so the page is correct from byte 1, and updates if the API has newer data.

Cost analysis (Google Places API New as example): at 1h TTL × 2 places × 24h × 30 days = 1,440 calls/month. Free tier is 5,000/month for Place Details. Effectively free.

## Custom 404

Create `src/pages/404.astro` reusing the `Base` layout + Kicker/Button. Astro emits `dist/404.html` and Cloudflare Pages auto-serves it with HTTP 404 status for unmatched routes. **Without this file**, CF Pages falls through to `index.html` and returns HTTP 200 with the homepage for unknown URLs — bad for SEO and confusing for users.

Add a card grid linking to the major sections so users can self-recover.

## Brand kit — use the real assets from day one

Don't ad-hoc invent logo marks. Ask the client for the brand kit (usually a folder with `Logomark/`, `Full Logo/`, `01 Colour/`, `02 Black and White/` subdirs containing SVG, PNG, EPS variants). Standard set you'll need in `public/images/brand/`:

```
karnib-logomark-navy.svg     # small mark, light bg
karnib-logomark-white.svg    # small mark, dark bg
karnib-logomark-cream.svg    # small mark, off-white/cream variant
karnib-fulllogo-navy-horizontal.svg
karnib-fulllogo-white-horizontal.svg
```

If the project doesn't have a brand kit yet, isolate the placeholder mark in **one** `<BrandMark>` component used everywhere — then the eventual swap is a single-file edit.

### Favicon set (full modern)

Generate from a single 512×512 transparent-bg PNG of the logomark:

```bash
SRC=assets/favicon-512.png
magick "$SRC" -define icon:auto-resize=16,32,48 public/favicon.ico
magick "$SRC" -resize 32x32   public/favicon-32.png
magick "$SRC" -resize 96x96   public/favicon-96.png
magick "$SRC" -resize 180x180 public/apple-touch-icon.png
magick "$SRC" -resize 192x192 public/icon-192.png
magick "$SRC" -resize 512x512 public/icon-512.png
cp brand-kit/Logomark.svg public/favicon.svg
```

Then in `Base.astro` `<head>`:

```html
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
```

Plus a minimal `public/site.webmanifest`:
```json
{
  "name": "...", "short_name": "...",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#...", "background_color": "#...", "display": "browser"
}
```

**Tell the client to hard-refresh** (Cmd-Shift-R) after deploying — favicons are aggressively cached.

## Google Maps API keys — two, not one

Provision two keys, not one:

| Key | Use | Restriction | Stored as |
|---|---|---|---|
| `<project>-embed` | Map embeds in browser HTML | HTTP referrers (`site.com/*`, `*.pages.dev/*`, `localhost/*`); API restrictions: Maps Embed API only | `PUBLIC_GOOGLE_MAPS_EMBED_KEY` env var (visible in HTML — safe because referrer-locked) |
| `<project>-server` | Places API / Geocoding from Pages Functions | None (or strict IP if available); API restrictions: only the APIs you actually call (Places API New) | Pages **secret** via `wrangler pages secret put` |

CF Workers don't carry a referrer header, so a referrer-restricted key fails or fails-open from a Worker. Different products, different keys.

## OG card via headless Chrome

Build the OG card as an HTML page in `scripts/og-card.html`, then screenshot via headless Chrome (no Playwright needed):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --hide-scrollbars --disable-gpu \
  --window-size=1200,630 --force-device-scale-factor=2 \
  --screenshot=/tmp/og.png \
  --virtual-time-budget=4000 \
  "http://localhost:3000/og-card.html"
magick /tmp/og.png -resize 1200x630 -quality 88 public/images/og/<site>-og.jpg
```

`--force-device-scale-factor=2` captures at 2400×1260 for sharp text at the final 1200×630. The HTML lives in version control so you can iterate on the design like any other component.

## Schema migrations across MDX content

When renaming or restructuring a content collection schema field (e.g. `location: string` → `locations: string[]`), the consumers won't fail the build — they'll just render `undefined`. Always:

1. **Grep first**: `grep -rn "data\.<oldFieldName>\b" src/`
2. Update the schema + every MDX file + every consumer in a single commit.
3. `bun run build` — schema validation will flag any MDX file you missed.

## SEO refinement loop (after launch)

This is half the job — the audit + GSC + Maps profile loop is where rankings actually come from.

### 1. Run squirrelscan deep audit

```bash
squirrel audit https://example.com/ --coverage full --refresh --format llm --output /tmp/audit.llm.txt
```

Triage findings into:
- **True positives** — fix immediately (missing alt, heading skips, redundant alt, broken internal links, content gaps, thin meta descriptions, missing schema, slow LCP)
- **Dev-mode false positives** (only relevant if auditing localhost) — `/@vite/client` "leaked secret", unminified, no compression, missing sitemap
- **CF settings** — CSP `unsafe-inline`, missing CAPTCHA on form, HTTP→HTTPS redirects (acceptable, but warn)
- **Heuristic noise** — `alt=""` flagged as "missing" (semantically correct for decorative), tel-href mismatches (intentional)

Score target: **Grade B+ (≥85)** on prod after first pass.

### 2. Submit to Google Search Console

- Add the site as a **Domain property** (covers all subdomains + http/https)
- Submit `https://example.com/sitemap-index.xml`
- Wait ~24-72 hours for first indexing pass

### 3. Pull GSC data → find gaps

```bash
google_search_console performance --site sc-domain:example.com --days 90 -n 500 -f json
```

Bucket queries by position:
- **Pos 1–10** (page 1) — protect. Especially brand queries.
- **Pos 8–15** (edge of page 1) — promote with a small content nudge. Add the exact query phrase as an H2 on the target page.
- **Pos 11–30** (page 2-3, high impressions) — biggest ROI. Expand content with NSW-specific terms, FAQ section, schema.
- **Pos 30+** (buried, high impressions) — content gap. Either expand existing page substantially, or write a dedicated landing.

Common buckets in legal niches:
- **"<offence> nsw"** + **"<offence> defence"** — already have pages, need expansion with statute refs
- **"can i get a section 10 for X"** — long-tail FAQ targets, write a Q&A blog post
- **"<service> <city>"** — needs dedicated `/locations/<city>-<service>/` page with `LegalService` JSON-LD and the office's address

### 4. Submit indexing requests via API

The google-indexing skill submits up to 200 URLs/day. Run after each meaningful content push:

```bash
google_indexing submit --file urls.txt -f table
```

Note: technically the API requires Owner-level access in GSC, but it accepts submissions for Restricted users on verified domain properties in practice.

### 5. Repeat. Track week-over-week position changes for the priority cluster.

## Content depth — for legal sites especially

For a legal site, every claim must be grounded. The audit isn't enough — **the content has to be legally accurate** because the firm's reputation rides on it.

Approach:
1. For each priority page, identify the **NSW Act + section** that creates the offence.
2. Use **Judicial Commission of NSW Local Court Bench Book** as the authoritative source for penalty tables — it accepts WebFetch where AustLII and legislation.nsw.gov.au usually 403.
3. **Quote actual statutory text** as a blockquote where possible. Italicise Act names (e.g. _Crimes Act 1900_).
4. **Don't invent case law**. If you cite a case (e.g. _R v Whyte_ for s 52A dangerous driving), web-search to confirm citation + relevance before committing.
5. Have subagents flag any figures they couldn't verify — and verify them yourself before deploying.
6. Add an **FAQ section** at the bottom of each offence page — these are the long-tail queries from GSC ("can I get a section 10 for mid range pca", "common assault dv t2") that win ranking on page 2.
7. Cross-link related pages (`/criminal-law/common-assault/` → `/criminal-law/breach-of-an-apprehended-domestic-violence-order/`) and case studies (`/case-studies/<matching-outcome>/`).

## Useful selectors / quirks

- **Gravity Forms** uses `input_<id>` names. Either rewrite to friendly names or preserve them if external integrations depend on them.
- **Rank Math SEO** writes meta tags directly; OG fields are reliable.
- **Elementor headers** often have duplicate nav (desktop + mobile). Dedupe by href when scraping.
- **WP XML serialised data** uses PHP serialize (`a:5:{s:5:"width";i:512;...}`). Skip unless you really need it.
- **NSW penalty unit** = $110 (as of 2024). Don't confuse "20 penalty units" with "$20" — multiply by 110.
- **Astro 6 content collection IDs** drop the `.mdx` and any `index` suffix. `entry.id` is the slug.
- **`bun run build`** produces `dist/`. Deploy with `wrangler pages deploy dist --project-name=<name> --branch=main --commit-dirty=true`.

## When NOT to use this skill

- Headless WP staying with WP — different problem
- WooCommerce — needs a real e-commerce layer (Shopify, Medusa, etc.); Astro static won't cover it
- Sites with thousands of posts where scraping is too slow — use a Postgres dump + custom parser instead
- Sites needing SSR for personalisation, auth, or per-user content — use TanStack Start or Astro with SSR adapter
