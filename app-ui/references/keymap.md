# Keymap: Gmail letters plus vim modes

One app-wide registry. Every row below is a binding `{ keys, description, group, handler }` in a scope; the `?` sheet, ⌘K, the hint strip and ⌘-hold hints are generated from it. Use `mod` for ⌘ on macOS and Ctrl elsewhere. `ctrl+d` and `ctrl+u` are real ctrl on every platform.

Rules that apply to every row:
- Bindings never fire while typing (inputs, textareas, selects, contenteditable, `role=textbox|combobox|searchbox|spinbutton`) unless marked `allowInInput`. IME composition is always ignored.
- Open dialogs, menus and listboxes own their keys; page bindings do not fire from inside them.
- `x` and `shift+x` are different bindings. Shift is not counted on symbols (`?`, `/`, `#`, `*`).
- Chords (`g c`, `* a`): press the first key, then the second within 1 second. The second key is consumed by the chord.
- Scopes stack by priority; the same keys in a higher scope shadow a lower one; a modal scope silences everything below.
- Reserved by OS, browser or password manager, never bind: `⌘\`, `⌘D`, `⌘T`, `⌘W`, `⌘L`, `⌘R`, `⌘P`, `⌘Q`, `⌘Tab`, `⌘Space`.

## Everywhere

| Keys | Action |
|---|---|
| `⌘K` | Command menu (nav, actions, recent records, pin/unpin, theme, density, switch workspace) |
| `?` | Shortcut sheet (searchable, grouped by scope); lists "Hold ⌘ to show shortcuts" |
| `/` | Focus the search or filter field |
| `⌘B` | Toggle sidebar between full and rail |
| `i` | Insert mode: focus the page's `data-primary-input` (then the composer, then `data-search-input`), cursor at end |
| `Esc` | In a field: blur (normal mode), never clear or navigate. Second Esc: the page's own Esc |
| `p` | Pin or unpin the focused sidebar row (sidebar focus only) |
| `shift+t` | Cycle theme: system, light, dark |
| hold `⌘` ~400ms | Show key hints on sidebar items, header controls and buttons; cancelled by any other key |

## Go chords

`g h` is always Home (the dashboard) from any section. Choose the other letters once, keep them mnemonic, check collisions against every other `g x` and against single-key bindings.

| Keys | Go to |
|---|---|
| `g h` | Home (dashboard) |
| `g i` | Inbox |
| `g c` | Companies / primary list |
| `g p` | People |
| `g b` | Board |
| `g a` | Announcements / content |
| `g u` | Users |
| `g s` | Social |
| `g o` | Schedule |
| `g t` | Sent |
| `g m` | Mailboxes |
| `g v` | Activity |
| `g w` | Workspace switcher |
| `g ,` | Settings |

The set above is the reference implementation's; a new app picks its own sections but keeps `g h`, `g ,` and the pattern.

## Lists (list scope)

| Keys | Action |
|---|---|
| `j` / `k` (and arrows) | Move focus down / up (repeat allowed) |
| `o` / `Enter` | Open the focused row's record (carries `?list=`) |
| `g g` / `G` | First / last row |
| `ctrl+d` / `ctrl+u` | Half a page down / up (focus moves by half the visible rows) |
| `x` | Select the focused row (only when bulk actions exist) |
| `shift+x` | Range select |
| `* a` / `* n` | Select all / none |
| `c` | Create (where the list has a primary action) |
| `e` | Done / archive |
| `#` | Move to Trash (toast with Undo) |
| `b` | Snooze |
| `z` | Undo the last action |
| `shift+i` / `shift+u` | Mark read / unread |
| `.` | Insert the "N new" events (EventFeed live mode) |
| `s` | Snooze or similar secondary action where `b` is taken (tasks) |

## Records (record scope)

| Keys | Action |
|---|---|
| `]` / `[` or `j` / `k` | Next / previous record in the `?list=` list; header shows "n of N" |
| `u` / `Esc` | Back to the exact list URL, row focused |
| `#` | Trash this record, step to the next (or back to the list if last) |
| `y` | Copy the permalink |
| `t` | New task pre-linked to this record |
| `i` | Focus the notes composer at the top of the timeline |
| `1` to `6` | Switch tab (rich records with tabs only) |
| `ctrl+d` / `ctrl+u` | Scroll the main column by half its height |

## Threads (thread scope)

| Keys | Action |
|---|---|
| `r` | Focus the composer (reply) |
| `a` | Reply all (only with more than one other party) |
| `n` / `p` | Next / previous message (quiet focus ring, scroll into view) |
| `⌘Enter` | Send from inside the composer (`allowInInput`) |
| `Esc` | Leave the composer; second Esc goes back to the list |
| `z` | Undo the last send (undo-send window) or reply |
| `e`, `#`, `shift+u` | Same as list scope, applied to the open thread |

## Dialogs and forms

| Keys | Action |
|---|---|
| `⌘Enter` | Primary action of the form or dialog; hint shown on the button; scoped to it; ignored while disabled or busy |
| `Esc` | Close the dialog |

## Generic layer for unconverted pages

Mounted once in the shell, active only when no list or record scope is registered. Navigation and focus only.

| Keys | Action |
|---|---|
| `j` / `k` | Move a focus marker (`data-kb-focus`) through the first visible `table tbody tr` or `[role=row]` / `[data-row]` list; focus kept by index on re-render, reset on route change |
| `o` / `Enter` | Click the focused row's first `a[href]`, or the row |
| `g g` / `G`, `ctrl+d` / `ctrl+u` | First / last row, half page |
| `x` | Toggle the focused row's checkbox if it has one |
| `i` / `/` | First visible text input in the main area / the search input |
| `Esc` | Blur |
| `u` | Go to the breadcrumb's parent |

Never bind `e`, `#`, `b`, `z`, `shift+i` or `shift+u` here: those change real data and the page has no scoped, reviewed handlers yet.

## Hint display

- `KeyHint keys="g i"`: 11px mono, muted text on muted background, radius 4, hidden unless `html[data-hints]`, absolutely positioned, `pointer-events: none`, fade is opacity only, instant under reduced motion.
- Placement: right edge of a sidebar row (temporarily replaces the count), bottom-right corner of rail icons, header controls and keyed buttons.
- Hint strip: one line at the bottom of the focused list, generated from the scope: `j/k move   x select   o open   e done   # trash`.
- Hints read keys from the registry (`useBindingKeys(id)`); never hard-code a key that already has a binding.
