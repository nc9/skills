# Installable, offline and local-first (detail)

Distilled from a production dashboard PWA and its client data layer (reference implementation, private). SKILL.md has the summary and the checklist; this file has the specs. Everything here is optional per product, but the order matters: local-first data first, then installable, then service worker, then offline actions, then push.

## 1. Local-first data layer

Goal: after one load, every navigation, range change and switch paints from the browser's copy in under 100ms and revalidates behind it.

**Query cache (every read)**
- One cache library (TanStack Query shape). Every server read is a `queryOptions` with a stable key `[tenant, child, dataset, range, filters]`. No fetch in `useEffect` anywhere in the app (add a lint rule or a test that greps for it).
- Route loaders call `ensureQueryData` with cached data; components read with suspense queries. **A loader must never block the route commit**: the target route's skeleton (or cached data) paints within 100ms of the click. A navigation that waits seconds for a loader before the URL changes looks ignored.
- **Freshness per dataset** (stale-while-revalidate: cached data shows instantly, a refetch happens only when stale):

  | Data | staleTime |
  |---|---|
  | daily external data (search consoles) and closed past days | 6 h |
  | aggregates that include today | 5 min |
  | tenant context, members, features | 5 min, plus invalidate on mutation |
  | live lists and unread counts | live (socket), 60s poll only as fallback |

- `refetchOnWindowFocus` only for live-ish data. Every range includes "today so far", labelled "to today", with the comparison window shifted to match; closed days stay cached.
- Fill dashboard cards in parallel, not one at a time.
- **Persist the cache per user to IndexedDB** (idb persister, 24h max age, `buster` = deploy version + schema version). The storage key includes the user id. Wipe on sign-out and on any 401/403. Never persist tokens or invite links. The client cache is display only; the server re-checks authorisation on every fetch.
- **Bootstrap on first load:** a cold load (no persisted cache for this user) shows ONE full-screen branded loader with a progress line while a single batched `getBootstrap` call loads the init set (me, tenants, children, features and roles, the default-range overview cards, the current child's main pages, unread counts, the live lists) and seeds the cache with `setQueryData` under the SAME keys the pages use. The per-section authz checks are unchanged. After that nothing blocks: anything uncached shows its section skeleton inline. A warm reload (persisted cache present) skips the loader entirely.
- **Prefetch on intent:** router `defaultPreload: "intent"`, loaders write into the cache, so hover or focus on a nav link warms it.
- Stale data revalidates in the background and swaps in progressively: no layout jump, at most a subtle "Updating" indicator.

**Live collections (lists that change every few minutes)**
- Keep the hot entities (inbox items, leads, notifications) in client collections (TanStack DB shape), not in per-page state. The list, the unread badge, the sidebar count, the bell and the dashboard card are all **live queries over the same collection**, so every view agrees instantly.
- **Sync:** initial load through the query collection, then deltas pushed over the app's live channel (WebSocket): `created`, `updated` (status, notes, read), `deleted`. Apply them as sync writes. Fall back to a 60s poll while the socket is down. Target: a new item shows in an open list in under 5s (under 1s is achievable).
- **Authorisation:** collections hold only what the server already lets this user read. Deltas are scoped server-side to the user's tenants and children; a delta for a tenant the user cannot read is dropped on the server, never sent (test it).
- **Optimistic mutations** go through collection transactions, call the existing server function, and roll back visibly on failure (mark read, status, notes, spam, clear, prefs). Replaces ad-hoc local state plus `router.invalidate()`.
- Collections are keyed per user id and wiped on sign-out and 401/403, never shared across users.
- **Socket health:** reconnect with exponential backoff and jitter (cap 60s), reconnect on `online` and `visibilitychange`, heartbeat, and on every reconnect a **resync** (refetch counts and lists once). Two tabs stay in step through the socket.
- **Long-open tabs** (users keep dashboards open all day): renew the session silently before it expires; on a real 401 go to sign-in with `next=<current url>`, never a broken screen, and ask to "Sign in again" in place without losing page state; cap notification lists; clean up every interval and listener on unmount; test that mounting and unmounting the shell N times returns listener and interval counts to baseline.
- **Server cache** (the other half): cache external and closed-range aggregate reads per tenant in the edge cache or KV (6h closed, 2 to 5 min today). Authorisation runs BEFORE the cache lookup; keys contain tenant and query shape, never the user; never cache user-specific content. A test proves a non-member gets 403 with a warm cache.

**Evidence is the gate.** Claims of "instant" need a Performance trace of a click-through of every sidebar item and back, plus range changes (click-to-commit ms, any page-level skeleton, count of navigation-blocking requests). Targets: zero blocking requests, paint under 100ms warm. Add realistic dev-only server latency (300 to 800ms per section) so blocking would show. Do one never-aborted warm-up request first (cold-start trap).

## 2. Installable app

**Manifest** (served only on the app's routes, e.g. `/app/manifest.webmanifest`; the marketing site keeps its own and its icon paths must exist):
- identity: `id`, `start_url`, `scope` (the app prefix with trailing slash), `name`, `short_name`;
- `display: "standalone"`, `display_override: ["window-controls-overlay", "standalone"]`, theme and background colours from the tokens;
- icons: 192, 512, a 512 **maskable** with a safe zone, a 180 apple-touch icon, and a 96 **monochrome badge** (white on transparent) for Android notifications, all generated from one SVG;
- `shortcuts`: the two or three places used most (inbox, all sites), for the user's landing tenant (or a generic path that redirects);
- `launch_handler: { client_mode: ["navigate-existing", "auto"] }` so a click on a notification or shortcut reuses the open window;
- two `screenshots` (wide and narrow) for the richer install sheet.
- Bump a `?v=N` on icon links when changing them. Verify with Lighthouse or DevTools "installable".

**Install UI**
- "Install app" entry in the bottom-left account menu (the user menu).
- One dismissible in-context card where the value is obvious (the live inbox: "Keep it open for new leads: install it as an app"). Dismissal is remembered per user and device (localStorage); do not nag.
- Chromium: capture `beforeinstallprompt`, call `prompt()` from the click. iOS Safari: a short sheet "Share, then Add to Home Screen", and say that web push on iOS only works once installed (iOS 16.4+).
- Hide ALL install UI when `display-mode: standalone`.

**Unread everywhere**
- `navigator.setAppBadge(unread)` / `clearAppBadge()` kept in step with the unread count; `document.title` prefix `(3) Inbox · App`; a dot on the favicon while unread > 0 for tab users. Feature-detect each.

## 3. Service worker

Scope the worker to the app prefix. Keep push handlers working through every change.
- **Precache** the built app shell (hashed JS, CSS, fonts from the build manifest). Static assets and fonts **cache-first**. Navigations **network-first**, falling back to a static offline shell page.
- **Never cache data responses or server functions in the worker.** Offline data comes from the per-user IndexedDB cache (section 1), so nothing is shared between users.
- **Offline UI:** a slim banner "You're offline. Showing what you had at 10:42." Server-only actions (invite, billing, settings) are disabled with a tooltip. Back online: revalidate and drop the banner. A `useOnline` hook feeds it.
- **Update flow:** when a new worker is waiting, show the "A new version is ready. Reload" toast (the same prompt as the auto-refresh pattern in SKILL.md) and call `skipWaiting` only on that click, plus a forced-update path for security fixes. Retain the previous hashed assets for 24h on the host.
- **Sign-out wipes:** worker caches, the IndexedDB data, and the push subscription (unsubscribe in the browser and delete it server-side). Wipe with a fail-closed pending marker so a crash mid-wipe is finished on next start. Never delete the whole database in a way that can block; IndexedDB calls have short timeouts (a few hundred ms) and never block rendering.
- **Offline mutation queue:** lead-style mutations (mark read, status, notes) made offline are queued per user in IndexedDB, applied optimistically in the collections, and replayed in order on reconnect or by Background Sync (`sync` event with a tag) through the normal server functions (auth and CSRF as usual). A replay that gets 401/403 drops the queue and wipes. Conflicts are last-write-wins with a visible "Updated elsewhere" note.
- **Periodic Background Sync** (Chromium, installed app only) refreshes the unread badge every ~12h; feature-detect and no-op elsewhere.

## 4. Browser notifications

Ask in two stages; never fire the native prompt cold.
1. **Soft ask in the app.** A quiet card or banner at a moment of value: "Get notified when a new lead arrives" with Enable and "Not now". "Not now" is respected: store it per user and re-ask rarely (weeks, and only after a relevant event). Show the current state in settings with a toggle, and explain how to re-enable when the browser has blocked it.
2. **Only after a yes**, call `Notification.requestPermission()` and subscribe to web push; store the subscription server-side against the user and device. On iOS require installation first and say so in the ask.

Delivery:
- Send push for important events only (new lead, failed run, approval needed). Group by `tag` per entity with `renotify`; include the monochrome `badge`.
- **Actions** on the notification: Open and Mark read. The worker posts Mark read to an authenticated same-origin endpoint with the session cookie, CSRF-safe; if that is not possible from the worker, Open the record instead and say so.
- **Click-through** focuses the existing app window (via `launch_handler` and `clients.matchAll`) and opens the record's permalink; it never opens a second window.
- Keep the badge, the title prefix and the in-app bell in step with the same unread source.
- Never email or notify existing members as a side effect of testing; use test tenants and example domains.
