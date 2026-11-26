---
name: app-ui
description: Build or redesign an admin, dashboard, internal tool, CRM, back office, data app or app shell as a keyboard-first, Linear/Attio-style application. Covers the sidebar shell, views as sidebar children, full record pages (no drawers), Gmail-style threads, EventFeed, dashboard stat tiles and cards, funnels, forms, structured data in UI, instant feedback on every action, density and a global semantic label system, local-first data, an installable PWA with notifications, a Gmail-plus-vim keymap, a porting procedure and a review checklist. Use on "admin redesign", "dashboard", "internal tool", "CRM", "app shell", "Linear style", "Attio style", "keyboard-first", or when porting an old tabbed dashboard.
---

Distilled from a real redesign of a data-heavy admin (reference implementation, private). Product-neutral: apply it to any CRUD, CRM, ops or analytics app. These are rules, not suggestions; deviate only when the user says so.

Scope split: this skill is the **app model** (shell, navigation, records, lists, dashboards, keys). Component and motion craft (focus, forms, transitions, accessibility details) is in `web-ui`. Chart colour and marks are in `dataviz`. Design tokens, focus rings and the visual floor are in `hallmark`. Do not restate those here; load them when you reach that layer.

References: `references/keymap.md` (full keymap), `references/semantic-labels.md` (tone, icon and label vocabulary), `references/pwa-local-first.md` (local-first data, install, service worker, notifications).

## Principles

1. **One screen, one idea.** Detail is a page, not a layer on top of a list. Nothing is stacked, expanded or slid in.
2. **Keyboard first.** Every action has a key and a visible hint. Mouse still works, but nothing is mouse-only.
3. **The URL is the state.** View, filters, sort, range, tab, page, and where you came from all live in the URL. Back, reload and a copied link restore the exact screen.
4. **Full pages, never drawers.** No sheets, peeks, side panels or inline row expansion to show more info. Dialogs are for short actions only.
5. **Structured data over free text.** Facts are typed fields that drive filters. Free text is only commentary.
6. **Quiet chrome, dense data.** Hairlines, no shadows except on overlays, small type, mono tabular numbers, token colours only.
7. **Never one more title.** The header breadcrumb is the page title. No in-page H1, no duplicate headings.
8. **Reversible by default.** Delete means Trash. Send means undo window. Every mutation has Undo.
9. **Never invent a number.** No source means a dash or a "Sample" chip, never a plausible fake.
10. **Instant.** Every click answers in the same frame; after one load the app runs from a local copy.

## Design concepts

These two decide whether the app feels like a professional tool. Apply them before any screen.

**Information density.** A dashboard is a working surface, not a landing page.
- Compact rows (32 to 40px), a small type scale (12 / 13 / 14 / 16 / 20, UI text 13px, meta 12px), mono tabular numbers, hairline panels, 4px spacing grid, no decorative whitespace, no hero areas, no illustrations in working views. Controls are 28 or 32px.
- Show more per screen before adding scroll or pagination: facts rows in headers, inline metadata in list rows (snippet, count, chips), sparklines in tiles.
- **Density is a user setting:** comfortable and compact (`data-density` on `<html>`), set in the user menu and settings, applied before first paint. Row height, view-bar height, UI text size, rail row height and card padding are CSS variables; components read the variables and never fixed pixel sizes.
- Density is not clutter: one idea per screen, aligned columns, quiet colour, and every number right-aligned and tabular so columns scan.

**Global semantic labels, colours and icons.** One vocabulary for status, stage, type, plan, grade and source, defined once.
- **A semantic value has exactly one tone and one icon everywhere:** lists, records, dashboard cards, sidebar counts, badges, charts, command menu. Users identify things by colour at a glance, so the same word must never be green on one page and amber on another.
- Define it as ONE token map (`STATUS_TONE[value] -> { tone, icon, label }`) over a fixed tone set (green, blue, violet, amber, red, grey; soft background plus readable foreground tokens, light and dark, contrast-checked). Never an ad-hoc colour per page; a test fails when a value in data has no entry.
- The text still says the value (colour is for scanning, never alone). Good, bad, waiting and neutral map to green, red, amber and grey consistently across every vocabulary; deltas follow the same rule.
- **Same entity type, same icon everywhere** (sidebar, command menu, header, rows, timeline); a real identity (favicon, avatar) beats the generic icon.
- Full spec and how to apply it to an existing app: `references/semantic-labels.md`.

## App shell

Inverted-L layout: a left sidebar plus a slim header; the content pane scrolls on its own, sidebar and header are fixed.

```
sidebar 232px (rail 52px) | header 44px: breadcrumb ......... [⌘K] [?]
                          | view bar (lists only): search + tokens ..... Filter Sort Display  [+ New]
                          | content: one gutter, one max width
```

**Sidebar**
- Top, unlabelled **global section**: the few things you open all day (Dashboard first, then Inbox, Tasks, Trash). Same set in every workspace.
- A **Pinned** section under it: user-pinned items or views. Hover/focus shows a pin icon, `p` toggles on the focused row, ⌘K has "Pin/Unpin/Move up/Move down". A pin is a shortcut, never a move. Hidden when empty. Stored per user (prefs), per-workspace pins whose target is missing are hidden, not deleted.
- Then **labelled groups** (12px muted, sentence case, never tracked caps), ordered by how often you act in them. Groups collapse; state is persisted. Rarely used groups start collapsed.
- **Items:** 28px, 16px icon, label, right-aligned **CountBadge**. Optional **sub-sections** (a collapsible heading inside a group) for a second tier such as "Outbound" within "Pipeline".
- **Children = views.** A list's views (statuses, cohorts, categories, saved views) are collapsible tree children of the item: chevron at the hover position, children indented 20px, 13px, quieter, active item's children auto-expand, expand state persisted. Each child is a URL: parent route plus a query param (`/inbox?view=tickets`). Children are hidden in rail mode. ⌘K lists them as `Inbox › Tickets`.
- **CountBadge:** an 18px tall, fully rounded pill, 11px tabular figures, `99+` cap, nothing at 0 or while loading. Tone: unread and attention counts are filled with the primary colour; every other count is a grey tinted pill. Never bare grey digits. In rail mode the pill sits on the icon corner. The parent shows the total, each child its own count. Counts come from a `CountSource` the shell reads, so the shell never imports a feature's internals.
- **Rail mode:** `⌘B` toggles 232px and 52px. Also a menu below ~960px. Check `⌘\` is never used (password managers own it).
- **Search lives only in ⌘K** (header trigger). No search box in the sidebar.
- **Footer:** resources, version and the user menu (full spec in "Sidebar footer"). The user menu is avatar plus name; menu holds theme (system/light/dark), density (comfortable/compact), timezone (a short list plus "More"), Settings, Keyboard shortcuts, Sign out. User-level settings live in one scrolling page, no tabs.
- **Switchers** live at the top: see "Context switching". For a workspace-only app the switcher is the sidebar header: initials, check on the active one, `g w`. Routes carry the workspace (`/w/<ws>/...`); in-app code uses canonical paths and a thin link/navigate wrapper translates at the edge.

**Header breadcrumb is the page title**
- Format: `workspace › section › view`. Earlier segments are muted links, the last is foreground weight 500. Always shown, also when the sidebar is collapsed. The view segment comes from the sidebar tree.
- Record pages: the breadcrumb stops at the list it came from. The record header keeps avatar and name, which is the entity's identity, not a second title.
- Empty and coming-soon pages are an EmptyState with nothing above it.

**One gutter, one width.** Every page uses the same horizontal padding and the same max width (or full width for tables). No page invents its own container.

**Tokens and density.** Radius 4/6/8, hairline borders, warm or neutral surfaces, one primary (brand) colour for primary action, selection and focus; everything else neutral. Chip tints are a small fixed set mapped from status in one place. Row height, view-bar height and UI text size come from CSS variables driven by a `data-density` attribute (comfortable 40px rows, compact 32px). Components read the variables, never fixed pixel sizes. Dark theme is a token swap on `:root[data-theme=dark]`; verify 4.5:1 for text and chips with a script, not by eye. Prefs (theme, density, clock, hint delay) sit in one typed store behind an interface so a server table can replace localStorage, applied before first paint.

## Context switching (org -> project/site)

For a topology of tenant -> child entity (organisation -> projects, websites, workspaces), the switchers are the **top of the shell**, one per level, and each filters everything below it.

- **One switcher per level, in the header, left to right:** brand mark (links home), tenant switcher, child switcher. Separate controls, never one merged dropdown. Each shows the current name (with favicon or avatar), a caret, and truncates long names with a tooltip.
- **Each level scopes the levels below it.** Switching the tenant reloads the child list, the sidebar tree, counts and every page; switching the child scopes the sidebar and pages to that child. Page content never shows data from outside the current scope.
- **The child switcher only appears when a child is in scope** (inside a child's pages). On tenant-level pages there is only the tenant switcher. Hide the child switcher on narrow screens, and fold both into the sidebar header.
- **Selection persists and lives in the URL.** The tenant (and child id) are path segments (`/<tenant>/child/<id>/...`), so reload, Back and a copied link restore scope. The last-used tenant is also stored (server-side preference or `localStorage`) so `/` lands in it. An unknown or forbidden slug redirects to the last valid one, never shows another tenant's data. Switching lands on the current section's list, never on a record id from the old scope.
- **Switching a tenant invalidates every cached query that is tenant-scoped** (children, usage, counts, saved views, pins), then navigates. Do not leave the previous tenant's rows on screen while loading.
- **Menu content:** the current item checked; a **Recent** group first (children sorted by last activity, capped at ~10) and **Pinned** items above it; a search field once the list is longer than ~8; a score or status chip per row where one exists; footer actions "Create <tenant>" / "Add <child>" and "All <children>" back to the full list. Cap the list, never render hundreds.
- **Keyboard:** each switcher opens with a key (for example `g w` for the tenant, `g s` for the child, or a numbered `⌘1`..`⌘9` for pinned items), arrows move, Enter selects, Esc closes, typing filters. Also expose "Switch to <name>" in ⌘K. Register them in the app registry like any other binding and show the hint on the trigger while ⌘ is held.
- **Pin and recent** are user prefs (ids, per tenant); a pin to an item that no longer exists is hidden, not an error.
- **Admin variant:** an operator app has no child level. It has only a workspace or tenant switcher at the top of the sidebar (initials, a check on the active one, rail shows the initial, `g w`). Which modules a workspace shows is configuration; a workspace without a data source runs on sample data and says "Sample". The ids and slugs are reserved so a section name can never be a slug.
- Reference implementation note: the customer dashboard ships tenant and child popovers with recents and an "all" link; the keyboard opening, pins and the search field above are required additions, not yet built there.

## Sidebar footer: profile, docs, support, version, auto-refresh

Bottom of the sidebar, top to bottom:

1. **Resources block** (small, hairline above): permanent entry points that exist whatever the onboarding state.
   - Setup (opens the setup flow; a quiet sparkle or dot while the user still has not connected what the product needs, with an `sr-only` explanation)
   - Take the tour (re-opens the tour at any time)
   - Docs (external link, new tab, `rel="noopener noreferrer"`, external-link icon)
   - Support (help or contact page inside the app)
   Use real links and buttons with visible focus, a key and hint like every other action. Operator apps can drop Setup and Tour but keep Docs and Support.
2. **Meta line:** system status pill (when the product has one), the **version label**, and small links (Changelog, Privacy, Terms).
3. **Profile and user menu** at the very bottom-left: avatar plus name (avatar only in rail mode), opening the menu described under App shell. The profile is always the last thing so it never moves.

**Version label.** Shows the human version (`1.4.2`, or `1.4.2-dev7` in development) with the exact build sha in the tooltip and a `data-build-sha` attribute so support and error reports can quote it. It links to the changelog. It turns the destructive colour and its tooltip says "A newer version is live: refresh to load it" when the tab is stale. Never derive staleness by parsing the version string (`dev10` sorts before `dev2`); compare build ids.

**App auto-refresh is required for every SPA dashboard.** A tab left open across a deploy keeps running old code, and its lazy chunks no longer exist, so a route dies with a "failed to fetch dynamically imported module" error. Build all of this:

1. **Build id.** Every build learns the commit sha it was built from. The client bundle must not contain it as a constant (that would change every chunk hash on every commit); put it in a `<meta name="build-sha">` in `index.html` (or the SSR root head) and read it from there. Server environments may use a build-time define.
2. **`/version.json`.** The client build writes `{ "sha": "..." }` beside its assets, served `Cache-Control: no-store` (a `_headers` rule on static hosts). A missing file, a non-JSON answer or an SPA fallback page counts as "unknown", never as "new version".
3. **Watch.** One page-wide watch, shared by every component that shows the version, started once in a browser and only for a real build (not dev). It checks on mount, on window focus and visibility return, and every 5 minutes while visible. At most one request at a time, at most one per ~10s for focus bursts, 10s fetch timeout, `cache: "no-store"`. An unreadable answer changes nothing (a blip must not flip the badge). `stale = deployed !== current`.
4. **Prompt.** A small non-blocking toast at the root, `role="status"`, `aria-live="polite"`: "A new version is available. Refresh" plus a dismiss. Never auto-reload while the user might be typing or mid-flow; refresh is the user's click. The version label in the sidebar also turns red. Position it clear of the sidebar and any bottom composer.
5. **Stale-chunk recovery.** A chunk or module that fails to load (match each browser's message: Chrome "Failed to fetch dynamically imported module", Firefox "error loading dynamically imported module", Safari "Importing a module script failed", Vite's CSS preload, `ChunkLoadError`) asks the version watch to check immediately, and the route error boundary reloads once onto the live build. Cap it: at most one automatic reload per ~30s per tab (store the timestamp in `sessionStorage`) so a chunk missing from the new build too can never loop; past the cap show the error screen with a Reload button. Do not reload if the router already did for the same failure.
6. **Deploy side.** Keep the previous deploy's hashed assets available for 24h (copy them from the live site into the new build before upload) so old tabs can still load their chunks while they wait to refresh.
7. **Tests:** a unit test of the watch with a fake host (focus, visibility, interval, gap, in-flight dedupe), of the stale-chunk matcher and reload cap, and of the version file writer.

## Views and navigation

- **No horizontal tab strips on lists. No filter-chip rows.** Every status, category or filter that would be a tab or chip becomes a sidebar child with a URL param. This is the most common regression when porting: audit for it.
- **Tabs only on rich records**, the single exception: a record with several distinct data types that cannot share one scroll (a user or an organisation with emails, audits, tokens, billing). Then tabs sit in the main column under a fixed header and rail, live in the URL (`?tab=`), and number keys switch them. If you think a tab is required elsewhere, say so explicitly instead of adding it quietly.
- **ViewBar** (lists only), no title. Left: search and active filter tokens. Right: Range, Sort, Display popovers, then the single filled primary action ("New x"). Height from `--viewbar-h`. Range (24h/7d/30d/90d) sits here and is shared by every chart on the page.
- **Saved views** become sidebar children and are pinnable.
- **Filters write URL params**, not component state. The filter builder is registry-driven (see Structured data).
- **Permalinks:** every record has one canonical URL. `y` copies it; a Copy link button does the same.
- **Return URLs:** a record opened from a list carries `?list=<encoded list URL>`. Accept only same-origin app paths (starts with the app prefix, rejects `//host`, schemes, backslashes). Browser Back and `u` return to the exact list URL with the row focused. Order and focus ride in router state.
- **Split view** (Attio style: list left, record right) is allowed only if the right pane is the real routed record page: no overlay, slide-in or close X, back works, and below ~1100px it falls back to a full page.
- Old URLs keep working through redirects, declared once and covered by a test table.

## Lists

- **DataTable:** 32px head with a type icon per column; first column sticky (name with favicon or avatar); rows `--row-h`; hover is the muted token; the keyboard-focused row has a 2px inset primary bar plus subtle accent background; number columns right-aligned, mono, tabular; footer shows the count.
- **Selection only when real bulk actions exist.** `selectable` defaults to false. Checkboxes, `x`, `shift+x`, `* a`, `* n` appear only when the page passes actual bulk actions (trash, mark done, assign, export). A checkbox column with nothing to do is a bug.
- **Events are never a table.** Any list of events (activity, telemetry, logs, audit trail, email sends) uses **EventFeed**:
  - row: tinted type icon, actor (avatar, favicon or a source label), event label, one-line summary, RelativeTime (absolute in tooltip);
  - grouped by day ("Today", "Yesterday", date), optional sticky headers;
  - live mode: polling with a sticky "N new" bar, `.` or click inserts, pause/resume;
  - cursor paging with "Load older";
  - `j/k` move, `o`/Enter opens the target;
  - type filters come from the sidebar children, never chips; no checkboxes;
  - one adapter: `{ fetchHead, fetchOlder, mapEvent(e) -> {type, icon, tint, actor, label, summary, at, href} }`.
  The per-record Timeline is a separate component that shares the same row atoms so the two look identical.
- **Conversation lists** (inbox style): sender(s) with message count ("Alex, me (3)"), subject then muted snippet, date at the right (time today, "Nov 24" this year). Unread rows bold; kind shown by a small icon before the sender.
- **Board:** 280px columns, header "Stage - count - sum"; compact cards (name, two attributes, avatar).
- **States, every list and card:** loading is a skeleton in the content's shape; empty says what belongs here plus the one action; error says what failed with a retry. Copy is consistent across the app ("No events in this range", "Trash is empty"). No spinners for local data.
- **Trash (`#`) is recoverable.** `#` moves the focused or selected rows to Trash with a toast "Moved to Trash" + Undo (`z`). One trash store, one Trash page (type icon, name, from, trashed at; `x` select; Restore or Enter restores). No "delete forever" in the UI. On a record page `#` trashes and steps to the next record, or back to the list when it was the last. Implement once in the kit as an optional `onTrash(ids)` on the table and the record page.
- Enrich rows: favicons for sites and domains (stored favicon first, then `/favicon.ico`, then initial-letter tint), avatars for people (photo, then initials), score colour grading (one `ScoreBadge`), and every named entity links to its record.

## Records

A record is a full routed page.

```
header (identity only)                                     [3 of 48  < >]
┌───────────────────────────────────────────┬──────────────────────┐
│ composer (note / reply)  <- data-primary-input │ attribute rail       │
│ timeline, newest first, grouped by day        │  label : value rows  │
│ sections (relations, many-to-many, tables)    │  tasks list          │
└───────────────────────────────────────────┴──────────────────────┘
grid: minmax(0,1fr) 320px, one scroll
```

- **No drawer, peek, side sheet or inline expansion. No top-of-page back link or arrow.** Back is `u` / Esc / browser Back / the breadcrumb.
- **Prev/next** with `[` `]` or `j` `k`, and "n of N" in the header. They step through the list in `?list=`.
- **Header is identity only:** avatar or favicon (32px), name (h1 20px semibold), URL as an external link, a facts row when known (location, size, stack), a one-liner, a source chip. Primary actions at the right. No status, grade or "disqualified" in the header when that state belongs to a relation (see Structured data).
- **One scroll, no tabs.** The Activity timeline is the main column with a composer at the top (notes for non-conversations). Emails, notes, tasks, stage changes, signups are event types in it. Related blocks go in `sections` under the timeline (a chart on top and recent rows below, for example).
- **Rail:** attributes as label/value rows (`--attr-h`), inline-editable, hover shows source and date of a value; then a short Tasks list. Long values wrap or show full on hover, never silently truncate a name.
- **Many-to-many sections** (cohort memberships, group membership) list every relation with its own state, grade and structured reasons, who set it and when. State belongs to the relation, not the entity.
- Actor names: show a human label ("Fit-check agent"), never a raw key id. Fall back to "API key ...last4".
- Every record also gets a Tasks section, and `t` creates a task pre-linked to it.
- Rich records only: tabs, as above. Header and rail stay fixed while the main column switches.
- **Security footgun:** turning a drawer into an `:id` route makes the id attacker-controlled. Validate the id format before any fetch, `encodeURIComponent` it in every URL builder, and never fire a mutation (mark read, claim) from a URL param.

## Conversations (threads)

One `Thread` + `Composer` pair serves every conversation: inbox items, sent email, social threads, approvals, ticket replies.

- **Gmail-style stack,** oldest to newest. Message card: avatar, name, address (muted), time right, plain-text body. **Every message shows in full**; no collapsed messages that expand on click.
- **Quoted text is the one exception:** lines starting with `>` are clamped behind a "Show quoted text" link.
- **Reply composer is always visible**, sticky at the bottom: "Reply to <name>", textarea, Send with a `⌘↵` hint. `r` focuses it, `a` reply-all when more than one other party. It carries `data-primary-input`.
- **⌘Enter (Ctrl+Enter elsewhere) submits**, registered with `allowInInput`. Esc in the box blurs it (back to normal mode); a second Esc goes back to the list.
- **Undo-send:** submit stages the message (as a draft, server side), shows a pinned toast "Sending in 10s" with Undo (`z`), ticks down each second, and sends exactly once when it hits 0. Undo deletes the draft. The timer is module-level so it survives navigation; closing the tab leaves a draft, nothing is sent. The phase machine is `staging -> pending -> sending`, and only `pending` can move on, so a double submit sends once.
- **Safe failure:** if staging fails, say so and keep the text. If the send fails, the draft stays in the thread as a Draft and the toast shows the server's reason. Never clear the box on failure.
- `n` / `p` step to next/previous message (quiet focus ring, scroll into view).
- Approvals keep Approve/Reject in the same layout: the request is the message and the composer is an optional note.
- Where the product never sends (a draft to copy elsewhere), the composer's ⌘Enter is "Copy draft" with a toast; keep an "Open on <site>" link.

## Keyboard model

Theme: **Gmail letters plus vim modes.** Use Gmail's own letter wherever Gmail has one; `g` is the go-modifier.

- **Normal mode:** single keys navigate and act. **`i` enters insert:** it focuses the page's one `data-primary-input` (fallback: the composer, then the search field) with the cursor at the end. **Esc** blurs the field (back to normal); a second Esc does the page's own Esc. Esc in a field never clears text or navigates. Bindings never fire while typing.
- **Go chords:** `g h` home from anywhere, then one letter per section (`g i` inbox, `g c` companies ...). Pick letters once, in one table, and check collisions. The chord's second key is consumed by the chord (`g i` must not also focus a field).
- **Lists:** `j/k`, `o`/Enter, `x`, `shift+x`, `* a`, `* n`, `g g`, `G`, `ctrl+d`/`ctrl+u` (ctrl on every platform, vim-style; `⌘D` is a bookmark), `c` create, `e` done, `#` trash, `b` snooze, `z` undo, `shift+i`/`shift+u` read/unread, `/` search.
- **Records:** `[ ]` or `j k` prev/next, `u`/Esc back, `y` copy link, `t` task, `#`.
- **Threads:** `r`, `a`, `n`, `p`, `⌘Enter`, `z`.
- **Everywhere:** `⌘K`, `?`, `⌘B`, `i`, `p`, theme cycle key, hold `⌘` for hints.
- **One app-wide registry.** Bindings are `{ keys, description, group, handler, allowInInput?, repeat?, hidden? }` registered by scope; scopes stack by priority, a modal scope silences the rest. The `?` sheet, ⌘K, the hint strip and ⌘-hold hints are all generated from the registry, so nothing drifts. Never hard-code a key shown in UI.
- **Every action button has a key.** A button without a binding is a gap; a binding without a visible hint is a gap.
- **Never clash** with the OS, browser or password manager: avoid `⌘\`, `⌘D`, `⌘T`, `⌘W`, `⌘L`, `⌘R`, `⌘P`. Shift on symbols is not counted (`?`, `/`, `#`). `x` and `shift+x` are different bindings.
- **Hold ⌘ for hints:** holding the mod key alone for ~400ms sets `data-hints` on `<html>`; small 11px mono `KeyHint` badges appear bottom-right of sidebar items (replacing the count while shown), header controls and every button with a key. Cancel the timer if any other key goes down (so ⌘K, ⌘B, ⌘C never flash), and hide on release, blur or visibility change. Hints are absolutely positioned, `pointer-events: none`, fade on opacity only, instant under reduced motion. Works while an input has focus.
- **Hint strip:** one quiet line at the bottom of the focused list built from the active scope, spaces between groups (`j/k move   x select   o open`), not middle dots.
- **Old or unconverted pages** get a generic DOM-driven layer: navigation and focus only (`j/k`, `o`, `g g`, `G`, `ctrl+d/u`, `x` on an existing checkbox, `i`, `/`, Esc, `u` to breadcrumb parent). **No destructive or state-changing keys there** (`e`, `#`, `b`, `z`, `shift+i/u`): they would act on real data. Do not steal keys from open menus or dialogs, and reset focus on route change.

## Dashboard and cards

The dashboard is the home page (`/`) and the first sidebar item. There is no redirect from home to the inbox. Every card, row and stat clicks through to its section.

**Sections**
- The page is **labelled sections** (sentence-case 13px/500 heading), ordered by how often you act on them: work queue first (inbox, tasks due), then pipeline, growth, product health, business, then a plugin's own. A widget names its section in its manifest; one `groupSections` function orders them.
- Each section has a **full-width stat strip**, then its cards below.
- Strip: one hairline box, `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))`, right and bottom hairline per tile pulled back 1px so the outer border stays single. Tiles are never crushed or truncated and there are no empty cells.

**StatTile: fixed 4-row anatomy, identical height**
1. title: 12px muted, one line, `title` tooltip
2. value (20px mono tabular) left, **delta chip right** on the same baseline
3. meta: 12px muted, one line ("prev 7d 22", "of 709 users")
4. sparkline: fixed height, e.g. 24px, full tile width

Rows have fixed heights (`grid-template-rows` with no `auto` rows). A missing part leaves blank space of that row's height; it never collapses. The title and value never truncate. The whole tile is the link; tiles have no footer button. A null value renders a dash, never a silent zero.

**Delta colour: always.** Green for up, red for down, grey only at exactly 0 or when there is no previous value. For metrics where up is bad (churn, past due, bounces, failures) pass `goodDirection: "down"`: colour follows good/bad, not direction. Same rule in tiles, tables and funnels.

**Cards**
- **Panel is the only box:** hairline border, radius 8, no shadow. Header: 13px/500 title, optional muted subtitle, right-aligned actions. **No box inside a box.** Content in a Panel (lists, bars, tables, charts) has no border, background or radius of its own beyond hairline row separators.
- **Pack the 12 columns.** Cards declare `sm | md | lg` (3, 6, 12 columns preferred) and are packed into rows in order; a row that falls short grows its cards in proportion. A lone card is full width, a pair 6+6, md+sm is 8+4, three sm are 4+4+4. A pure `packSpans(sizes)` does it. Cards size to their content: **no fixed heights, no dead space.**
- **Every card with a fuller view gets a footer link** (`footer={{ label, to }}`): small quiet text button with an arrow at bottom-left, 12px, naming the destination ("All sources", "Inbox › Feedback"). Enter on a focused card follows it.
- **MiniTable** in cards: 28px rows, hairline separators, right-aligned numbers; its trailing link is the Panel footer.
- **Enrich every row:** favicon or avatar, score badge, links to records. Merge near-duplicate lists (recent runs and recent reports are one "Recent audits").

**Charts** (colour and mark rules: `dataviz`)
- One `ChartFrame` wraps every chart: loading skeleton in the chart's shape, empty ("No data for this range"), error, and an accessible table alternative.
- Series colour is `chartColor(i)` by stable position, never from a filtered list; past eight series fold into "Other".
- **No Y scroll inside a chart.** Charts fit their Panel; a ResizeObserver sizes the SVG.
- **Measure after the data loads.** The measured element often is not mounted on first render (the frame mounts it after loading). A `useSize` that attaches once on mount sees a null ref and leaves the chart at width 0 forever (a legend over an empty plot). Re-check the watched element after every render and re-attach the observer when it changed.
- Hairline grid, 11px mono axis labels, vertical rule plus compact tooltip on hover, dashed last point when the period is incomplete. Legend uses small square swatches, not dots. Animation is opacity only, none under reduced motion. One number formatter (compact, currency, percent) used everywhere.
- **Range control** (24h/7d/30d/90d) is URL state shared by all charts on the page; if the API caps a range, map it and say so.
- If a card has no data say one quiet line ("No data for this range"), never two messages.

**Funnel**
- Vertical, one row per stage: label (fixed column, 13px), solid centred bar sized by `value / topValue`, stats column (fixed width, right aligned, mono): value, % of top, step conversion `x% of previous`, delta chip vs previous period.
- **Cumulative:** for an ordered funnel `value` counts only entities that did every earlier step; keep the unordered `raw` count for the tooltip and table, and note stages reached without the first step ("Not from site").
- **Previous period** is a dashed outline (1.5px, dash 4 3, centred) at the previous width: beyond the bar when previous is larger, inside the fill (contrasting stroke) when smaller. Legend: solid = this period, dashed = previous period, naming both ranges.
- Delta colour per stage always green/red; add an up/down glyph at the bar end in the same colour.
- A stage colour belongs to its position, so filters never repaint it. A stage may link to the filtered list. Only draw the dashed outline when a previous value has a real source. `aria` table fallback; no scrolling.

## Forms and actions

- **Dialogs only for short actions** (a small form, a confirm). Never to show more information; that is a page.
- **Every form and dialog has a submit shortcut** (`⌘↵` / `Ctrl↵`) scoped to it, shown as a muted `Kbd` on the button. Details in `web-ui` Forms.
- **Optimistic updates with rollback.** Apply locally, send, restore on failure and say why. Local-only data says so in its toast ("not saved yet") instead of pretending.
- **Toasts carry Undo** (`z`) for every reversible action, and live in the shell so Undo works after the page that caused it is gone.
- **No mutation from a URL.** Opening a link never marks, claims, sends or deletes.
- **Validate ids** from the route before any fetch and `encodeURIComponent` them in every URL builder. `list=`/return params are same-origin app paths only.
- Destructive or outward-facing actions (send email, bulk change, billing) show the exact effect first and confirm; the dialog confirms with `⌘↵` only once open and focused, never from a page-level shortcut.
- Mutations from old flows keep their guards, confirms and copy byte-identical when restyled.

## Instant feedback on every action

Hard rule: the user never waits for the app to acknowledge them. A click that appears ignored is a bug.

- **Submit:** on press the button shows a spinner in the same frame and the whole form disables (inputs, secondary buttons, the submit shortcut), so a double submit is impossible. Then either success (a toast with Undo where reversible, or the optimistic result already in place) or failure (an inline error beside the field or at the top of the form, form re-enabled, text kept). A button never keeps its normal look while a request is in flight and never stays spinning after it ends.
- **Navigation:** clicking another section, view, record or range paints the target's layout-matched **skeleton or cached data in the same frame**, and the URL changes at once. Never a blank page, a frozen old view, or a click that does nothing for seconds because a loader is running. Loaders must not block the route commit.
- **Full-page loading screens exist only for the very first load of the app** (a cold start with no local data), once, branded, with a progress line. Everything after is inline skeletons or cached data.
- **Every control gives immediate visual feedback:** pressed state on press, pending state while working (spinner inside the control, disabled), selected/checked/toggled state flips at once. Toggles, checkboxes, pins, stars, status changes and drag drops are optimistic: apply locally, send, roll back visibly on failure with the reason.
- Long work (an export, a bulk change) shows progress in a toast that survives navigation, never in a blocked page.
- Measure it: click-to-commit under 100ms warm, zero navigation-blocking requests on a click-through of every sidebar item. Details in `references/pwa-local-first.md`.

## Onboarding and tours

Three separate surfaces, none of which blocks the app: a **setup flow** (get the product connected), a **guided tour** (learn where things are), and a quiet **get-started card**. Each has a permanent entry point in the sidebar footer, so skipping is never a dead end.

**State**
- Onboarding state is per user, on the server (`accountIsNew`, chosen path, `doneAt`, `skipped`, `tourDoneAt`, first-connection timestamps), read through one query with a long stale time. A failed read leaves it undefined and every consumer treats that as "show nothing": the app must work without the endpoint.
- Local flags hold first: when the tour closes write `tour-done:<userId>` to `localStorage` (swallow quota or private-mode errors), then POST the server copy best-effort. "Done" is local OR server, so another device's completion counts. Never throw from persistence.
- The picked setup option (agent, surface) is remembered locally so reopening lands on the right step.

**First-run triggers (decided once, in one gate component mounted in the tenant layout)**
- A new, unfinished account landing on the dashboard home auto-opens the setup chooser **once** (a ref guards re-opening). Anywhere else a new unfinished account sees only the quiet get-started card, which can be dismissed for the session.
- The gate never starts the tour. The chooser's skip closes it, records a `skipped` outcome and hands over to the tour; the tour then offers itself once.
- Other entry points open the same flow: the sidebar items, a `?setup=agent` link from emails and banners (consumed once: dropped with `replace` so Back does not reopen it), a window event.
- The tour marks `<html data-tour-active>` while open (and `?tour=N` counts), and the setup gate checks it so the two never stack.

**Setup flow (modal, 3 steps)**
- Steps: choose the agent or surface, connect it (a copyable snippet or one line to send), try it (a first real action). Dots show `Step n of N`; Back and Next; focus moves to the new step's heading when the control that had it is gone.
- Connection detection polls for the first authenticated call: every 3s, every 10s after 2 minutes, stop at 15 minutes, never while the tab is hidden, and stop when the modal unmounts. On timeout show "still waiting" with help, not an error.
- No secret, key or token appears anywhere in the flow. Every field has a visible label; `⌘↵` continues; `b` back; Esc skips; single-letter shortcuts choose a path (list them in `?`).

**Tour as data**
- A step is `{ id, title, body, anchor, showMe }`. `anchor` is a `data-tour` id on a real sidebar element (null = centred card), `showMe` the page that step shows (null = none). Steps are built from a definition list with conditions (`needs: website | noWebsite | feature`), so steps about things the user does not have are skipped and the list never shifts while navigating (derive "has a website" from the account, not from the current page).
- **A test fails when an anchor or route stops existing in the real nav.** This is what keeps a renamed nav item from leaving the tour pointing at nothing.
- Copy states real numbers from the same constants the product uses (costs, limits), never hand-typed.
- First slide is a welcome (anchor null), last is a closing slide chosen from the user's state (ready, or start a first action on the surface they picked).

**Behaviour**
- Overlay: a ring around the anchor (an outline plus a huge box-shadow scrim, `pointer-events: none`) and a card as a native modal `<dialog>` with `aria-modal`, `aria-labelledby`, `aria-describedby`. The card positions itself next to the anchor, clamped to the viewport, re-measured with a `ResizeObserver` on the document and card; ignore sub-3px jitter so two near sizes cannot loop. Honour reduced motion.
- **Page switches mid-tour:** each step's page is navigated to when the step opens (only if the pathname differs), so the target exists. The step lives in the URL as `?tour=<n>` (1-based, written with `replaceState` once the page has landed, same-origin paths only). A reload resumes at that step; browser Back and Forward restore the step stored in the entry's URL; no param means the tour is left. The origin page is kept in `sessionStorage` (validated as an in-app path) and restored on finish.
- **Missing anchor:** if a target never mounts within ~3s, show the card centred with the text instead of a blank step.
- **Resume, skip, finish:** Esc skips; skip and finish both persist done, strip `?tour`, and navigate back to the origin. A tour that was skipped is re-openable from "Take the tour".
- **Keyboard:** Esc skip, ArrowRight/Enter next (Enter on the last step presses its primary button), ArrowLeft back. Ignored when a modifier is held, when typing in a field, and Enter on a focused button or link goes to that element. Tab is trapped in the card; focus is saved on open and restored on close; focus moves to the card on every step.
- A tour or setup URL param only opens the UI; it never triggers a mutation.

## Installable, offline and local-first

Makes the app pleasant for people who keep it open all day. Full specs, with the numbers: `references/pwa-local-first.md`. Build in this order.

1. **Local-first data.**
   - Keep the app's data in the browser: a query cache with per-dataset freshness (6h for daily or closed data, 5 min for today, live for lists), persisted per user to IndexedDB, plus client collections for the hot entities (inbox items, notifications) synced by a live channel with a poll fallback.
   - Render from the local copy instantly and revalidate behind it; swap in updates progressively with no layout jump.
   - One batched bootstrap on the first cold load seeds the cache under the same keys the pages use. Prefetch on hover or focus.
   - Wipe everything per user on sign-out and on 401/403. The server still authorises every read. **The service worker never caches data responses.**
2. **Installable.** A manifest scoped to the app (id, start_url, scope, standalone with window-controls-overlay, 192/512, maskable and monochrome badge icons, shortcuts, `launch_handler` navigate-existing, screenshots). "Install app" in the bottom-left account menu plus one dismissible in-context card; `beforeinstallprompt` on Chromium, an Add to Home Screen sheet on iOS; hide all install UI when standalone. Unread count in the app badge, the title prefix and a favicon dot.
3. **Service worker.** Precache the app shell, assets cache-first, navigations network-first with an offline shell. Offline banner ("Showing what you had at 10:42"), server-only actions disabled with a tooltip, offline mutations queued and replayed in order. The update flow is the same prompt as auto-refresh: "A new version is ready. Reload", `skipWaiting` only on click.
4. **Browser notifications.** Ask in two stages: a soft in-app card at a moment of value ("Get notified when a new lead arrives") with "Not now" respected and re-asked rarely; only after a yes the native permission request and push subscription. Push only for important events, grouped by tag, with Open and Mark read actions, click-through reusing the open window, and the badge kept in step. iOS push needs the app installed (16.4+) and the ask says so.

## Structured data in UI

- **A typed field registry** (one constant) is the single source for the API validator, the MCP/agent output schema, the filter builder and the rail editor. Every field is optional with a type (enum, string[], number, bool, object[], country code). Adding a field is a registry edit, not a migration.
- **Storage:** a JSON column of values validated against the registry on write (unknown keys refused), a sibling `meta` column per key `{source, by, at}`, and a containment index (GIN `jsonb_path_ops`) so `attributes @> '{"stack":["x"]}'` is fast.
- **Filter builder:** field, then operator (is, contains, any of, exists, >, <), then value, e.g. `stack contains squarespace`. Writes URL params (`?attr.stack=...`), saves as a view, appears as a sidebar child.
- **Facts are not notes.** A fact (stack, size, clients, location, fit result) is a registry field. Notes and comments are for commentary only. A fit result is structured: `{ grade, checks:[{field, rule, actual, pass}], summary }`.
- **Sources are entities:** a lead-source row (kind, name, url) with prospects pointing at it plus the exact page or row. The source chip links to a page listing every record from it.
- **Membership is many-to-many with per-relation state.** An entity can sit in several groups; each membership has its own state, grade and reasons. "Disqualified" exists only on a membership, never on the entity. An entity with no live membership is "Unassigned" (a sidebar child), not "rejected".
- Socials and similar link sets are arrays of `{platform, url, handle?, followers?, checked_at?, source}`; the rail shows platform icons that link out, hover shows stats, quiet when nothing is checked.
- Show provenance on hover (source, who, when) for any value an agent or import wrote.

## Porting an existing dashboard

1. **Inventory.** List every page, tab, card, filter and action of the old app, plus data hooks and the routes that must keep working. Note dead pages: delete them, do not port them.
2. **Map** each item to a section or sidebar view: tabs become sidebar children; separate concerns become separate sections (not tabs of one page); duplicated headline numbers are shown once.
3. **Carry over the lifecycle surfaces:** onboarding or setup flow, tour (re-anchor every `data-tour` id to the new nav and re-run the anchor test), the sidebar footer (docs, support, version, auto-refresh), and the tenant and child switchers with their URL scope. Dropping these in a redesign is the usual loss.
4. **Audit feel:** list every place a click waits (blocking loaders, forms that stay enabled, spinners over a frozen page, full-page loaders after first load) and every ad-hoc colour or duplicate label; plan the cache, bootstrap, skeletons and the single tone/icon map before porting pages.
5. **List what to delete:** tab strips, filter-chip rows, back links and arrows, in-page H1s, duplicate titles, drawers, peeks, inline expansion, checkbox columns with no bulk action, tables of events, nested boxes, per-page containers.
6. **Build the shell and kit first:** tokens, shell, registry and hotkeys, nav tree, DataTable, ViewBar, RecordPage, Thread, EventFeed, Panel, StatTile, charts. Pages are then thin. Ship the version watch and stale-chunk recovery with the shell, not later; then the data layer and, if wanted, the manifest and service worker.
7. **Port section by section.** Reuse data hooks; wrap unconverted pages in the shell (generic keys only) so nothing blocks the rollout. Restyle mutation UIs without changing their logic or copy. Add redirects and a test table for every old URL.
8. **Click through in a real browser** at 1280 and 1440px wide, light and dark, compact and comfortable, with the sidebar in full and rail modes. Use only the keyboard for one full pass, record a Performance trace of a click-through of every sidebar item, and test offline and installed modes. Check browser Back from a record lands on the exact row.
9. **Run the review checklist** below and fix before shipping.

## Review checklist

- [ ] No drawer, sheet, peek or inline row expansion anywhere
- [ ] Row click or Enter opens a routed record with `?list=`; Back and `u` return to the exact row
- [ ] `list=` and ids are validated; ids are `encodeURIComponent`'d; no mutation fires from a URL
- [ ] Header breadcrumb is the only page title; no in-page H1; record breadcrumb stops at the list
- [ ] No top-of-page back link or arrow on records
- [ ] No tab strip on any list; no filter-chip row; views are sidebar children with URL params
- [ ] Any tab on a record is justified, in the URL, and keyed by number
- [ ] Search appears only in the header (⌘K), not the sidebar
- [ ] Counts are pills with correct tone and 99+ cap; nothing at zero
- [ ] One gutter and one content width on every page
- [ ] Event lists use EventFeed, are not tables, and have no checkboxes
- [ ] DataTable selection exists only where bulk actions exist
- [ ] `#` goes to a recoverable Trash with Undo; no hard delete in the UI
- [ ] Every action button has a key, a visible hint and a `?` sheet line; no key clashes with OS or password manager
- [ ] `i` focuses `data-primary-input`; Esc leaves it; no binding fires while typing
- [ ] Holding ⌘ shows hints and ⌘K, ⌘B, ⌘C never flash them
- [ ] Thread shows every message in full, reply box always visible, ⌘Enter submits, undo-send works, failure keeps the text
- [ ] Every form and dialog submits with ⌘↵ and shows the hint
- [ ] Stat tiles share one height with the 4-row anatomy; title and value never truncate
- [ ] Deltas are green or red everywhere (with `goodDirection` for inverted metrics); grey only at 0 or no baseline
- [ ] Panel is the only box; no box inside a box
- [ ] Cards pack the 12 columns with no dead space and no fixed heights; lone card is full width
- [ ] Every card with a fuller view has a footer link
- [ ] Charts have loading, empty and error states, no Y scroll, and size correctly after data loads
- [ ] Funnel is cumulative with "x% of previous" and a dashed previous period only where a source exists
- [ ] Rows show favicons or avatars and link to their records
- [ ] Facts are typed registry fields; notes hold commentary only
- [ ] Group membership is many-to-many; no status shown on the entity that belongs to the relation
- [ ] Dark theme and both densities pass a contrast and layout check
- [ ] Density is dense by default: compact rows, mono tabular numbers, hairlines, no decorative whitespace; a density setting works and is applied before first paint
- [ ] Every status, stage, type, plan, grade and source comes from the one tone/icon map; the same value has the same tone and icon on every page; no raw colours in feature code
- [ ] Colour is never the only carrier of a status (a label or icon accompanies it); same entity type has the same icon everywhere
- [ ] Submit: spinner in the same frame, whole form disabled, no double submit, success toast with Undo or inline error with the form re-enabled and text kept
- [ ] Every nav click changes the URL and paints a skeleton or cached data in the same frame (under 100ms); no blank or frozen page; loaders never block the route commit
- [ ] Full-page loader only on the cold first load; warm reloads skip it
- [ ] Every button and control shows pressed and pending states; toggles and status changes are optimistic with visible rollback
- [ ] Reads go through one cache with per-dataset freshness, persisted per user, wiped on sign-out and 401/403; no fetch in effects; the service worker caches no data
- [ ] Hot lists live in collections synced by a live channel (reconnect with backoff and jitter, resync on reconnect, poll fallback); badges, bell and lists agree
- [ ] A click-through trace proves zero navigation-blocking requests and sub-100ms warm paints
- [ ] Manifest valid and installable; Install app in the account menu and one dismissible card; install UI hidden when standalone; iOS sheet explains push needs install
- [ ] Service worker: shell precache, navigations network-first with offline shell, offline banner, server-only actions disabled offline, offline mutations queued and replayed
- [ ] Notifications use the two-stage ask (soft card, then native prompt after yes); "Not now" respected; push has actions and reuses the open window; badge, title and favicon dot track unread
- [ ] Sign-out wipes caches, IndexedDB and the push subscription
- [ ] One switcher per level at the top, each scoping everything below; scope is in the URL and persists
- [ ] Switchers open by key, filter by typing, list recent and pinned first, and invalidate tenant-scoped queries on switch
- [ ] Sidebar footer has Docs, Support, version label and the profile menu; Setup and Tour re-openable at any time
- [ ] `/version.json` (no-store) plus a focus/interval watch; stale tab shows a non-blocking Refresh prompt and a red version label
- [ ] A failed chunk load triggers one capped reload (never a loop) and an error screen with Reload past the cap
- [ ] Old hashed assets are retained for 24h across deploys
- [ ] First-run setup opens once; the tour never starts the setup gate and vice versa; skip is always available
- [ ] Tour steps are data, anchors and routes are test-checked against the real nav, step is in `?tour=` and resumes on reload and Back
- [ ] Tour and setup are keyboard complete (Esc, arrows, Enter, Tab trap, focus restore) and persist done locally then on the server

## Anti-patterns

| Before | After |
|---|---|
| Row click opens a side drawer | Row click opens a routed record page |
| Row expands inline to show detail | Open the record page |
| Horizontal tabs above a list | Sidebar children with `?view=` |
| Row of filter chips | Sidebar children plus ViewBar Filter and Sort |
| Back arrow at the top of a record | `u`, Esc, breadcrumb, browser Back |
| Page title in an H1 under the breadcrumb | Breadcrumb only |
| Activity as a table with checkboxes | EventFeed, no selection |
| Checkbox column and no bulk actions | `selectable` off |
| Hard delete | `#` to Trash, Undo, Restore |
| Reply box hidden behind a click | Composer always visible, `⌘↵`, undo-send |
| Stat tiles of different heights, truncating titles | 4-row fixed anatomy, equal heights |
| Grey delta when a number fell | Red (or green with `goodDirection`) |
| Bordered list inside a bordered card | Panel only; hairline row separators |
| Card fixed to 320px with empty space beside it | Pack the 12 columns, size to content |
| Funnel of absolute counts | Cumulative, "x% of previous", dashed prior period |
| Chart measured on mount, 0 wide after load | `useSize` re-attaches after every render |
| Stack as a free-text note | Registry field, filterable |
| "Disqualified" chip on a company | Membership state in a Cohorts section |
| Button looks idle while the request runs, form stays editable | Spinner in the same frame, whole form disabled |
| Nav click waits seconds on a loader before anything changes | URL changes and skeleton or cached data paints at once |
| Full-page spinner on every page | Full-page loader once on cold start only |
| Fetch in `useEffect` on every page view | Cached query, persisted per user, revalidate in background |
| Service worker caches API responses | Shell only; data from the per-user local store |
| Native notification prompt on first visit | Soft in-app ask, native prompt only after yes |
| Same status amber on one page and orange on another | One tone/icon map for every vocabulary |
| Hidden shortcut | Hint, `?` sheet, ⌘-hold overlay from one registry |
| `⌘\` or `⌘D` as an app shortcut | A key the OS and password managers don't own |
| Destructive keys on unconverted pages | Navigation and focus only |
| A fake number where there is no source | Dash or "Sample" chip |
