---
name: app-ui
description: Build or redesign an admin, dashboard, internal tool, CRM, back office, data app or app shell as a keyboard-first, Linear/Attio-style application. Covers the sidebar shell, views as sidebar children, full record pages (no drawers), Gmail-style threads, EventFeed, dashboard stat tiles and cards, funnels, forms, structured data in UI, a Gmail-plus-vim keymap, a porting procedure and a review checklist. Use on "admin redesign", "dashboard", "internal tool", "CRM", "app shell", "Linear style", "Attio style", "keyboard-first", or when porting an old tabbed dashboard.
---

Distilled from a real redesign of a data-heavy admin (reference implementation, private). Product-neutral: apply it to any CRUD, CRM, ops or analytics app. These are rules, not suggestions; deviate only when the user says so.

Scope split: this skill is the **app model** (shell, navigation, records, lists, dashboards, keys). Component and motion craft (focus, forms, transitions, accessibility details) is in `web-ui`. Chart colour and marks are in `dataviz`. Design tokens, focus rings and the visual floor are in `hallmark`. Do not restate those here; load them when you reach that layer.

Full keymap table: `references/keymap.md`.

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
- **Footer:** the user menu. Avatar plus name; menu holds theme (system/light/dark), density (comfortable/compact), timezone (a short list plus "More"), Settings, Keyboard shortcuts, Sign out. User-level settings live in one scrolling page, no tabs.
- **Workspace switcher** (when multi-tenant) is the sidebar header: initials, check on the active one, `g w`. Routes carry the workspace (`/w/<ws>/...`); in-app code uses canonical paths and a thin link/navigate wrapper translates at the edge.

**Header breadcrumb is the page title**
- Format: `workspace › section › view`. Earlier segments are muted links, the last is foreground weight 500. Always shown, also when the sidebar is collapsed. The view segment comes from the sidebar tree.
- Record pages: the breadcrumb stops at the list it came from. The record header keeps avatar and name, which is the entity's identity, not a second title.
- Empty and coming-soon pages are an EmptyState with nothing above it.

**One gutter, one width.** Every page uses the same horizontal padding and the same max width (or full width for tables). No page invents its own container.

**Tokens and density.** Radius 4/6/8, hairline borders, warm or neutral surfaces, one primary (brand) colour for primary action, selection and focus; everything else neutral. Chip tints are a small fixed set mapped from status in one place. Row height, view-bar height and UI text size come from CSS variables driven by a `data-density` attribute (comfortable 40px rows, compact 32px). Components read the variables, never fixed pixel sizes. Dark theme is a token swap on `:root[data-theme=dark]`; verify 4.5:1 for text and chips with a script, not by eye. Prefs (theme, density, clock, hint delay) sit in one typed store behind an interface so a server table can replace localStorage, applied before first paint.

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
3. **List what to delete:** tab strips, filter-chip rows, back links and arrows, in-page H1s, duplicate titles, drawers, peeks, inline expansion, checkbox columns with no bulk action, tables of events, nested boxes, per-page containers.
4. **Build the shell and kit first:** tokens, shell, registry and hotkeys, nav tree, DataTable, ViewBar, RecordPage, Thread, EventFeed, Panel, StatTile, charts. Pages are then thin.
5. **Port section by section.** Reuse data hooks; wrap unconverted pages in the shell (generic keys only) so nothing blocks the rollout. Restyle mutation UIs without changing their logic or copy. Add redirects and a test table for every old URL.
6. **Click through in a real browser** at 1280 and 1440px wide, light and dark, compact and comfortable, with the sidebar in full and rail modes. Use only the keyboard for one full pass. Check browser Back from a record lands on the exact row.
7. **Run the review checklist** below and fix before shipping.

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
| Hidden shortcut | Hint, `?` sheet, ⌘-hold overlay from one registry |
| `⌘\` or `⌘D` as an app shortcut | A key the OS and password managers don't own |
| Destructive keys on unconverted pages | Navigation and focus only |
| A fake number where there is no source | Dash or "Sample" chip |
