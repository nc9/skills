# Global semantic labels, tones and icons

One vocabulary, defined once, used everywhere. The rule: **a semantic value has exactly one tone and one icon in the whole app.** Users learn "amber = waiting" once and then read every list, record, card, badge, chart legend and sidebar count at a glance.

## The token set

- A small fixed set of tones: `green`, `blue`, `violet`, `amber`, `red`, `grey` (add one only if a real meaning needs it). Each tone is two tokens, a soft background and a readable foreground (`--chip-green-bg`, `--chip-green-fg`), with light and dark values, contrast checked at 4.5:1 for the pair. Surfaces and text use their own tokens; chart series use `--chart-1..8`; scores use `--score-good|ok|poor`.
- Components take a tone name, never a raw colour: `<Chip tone="green">`, `<TintIcon icon tone>`. Class names are literal so the build can see them.
- **Semantic tone map** is one module: `STATUS_TONE[value] -> { tone, icon, label }`, grouped by vocabulary:

  | Vocabulary | Examples (value: tone) |
  |---|---|
  | status | active: green, pending: amber, failed: red, paused: grey, running: blue |
  | stage | new: grey, contacted: blue, replied: violet, converted: green, lost: grey |
  | type / kind | one tone per kind, stable across the app (email: blue, agent: violet, billing: green, support: amber) |
  | plan | free: grey, pro: blue, team: violet |
  | grade / score | A green, B blue, C amber, D red; numeric scores use the score tokens |
  | source | each source has one icon and tone (directory, referral, import, manual) |
  | delta | up good: green, down bad: red, grey only at 0 or no baseline; metrics where up is bad invert |

- Every page that needs a chip calls the map. No page decides "this one looks better orange". A new value is a one-line edit in the map, and a test fails when a value used in data has no entry.
- **The text says the value; colour only helps scanning.** Never colour alone (colour-blind users, greyscale print): a label or a distinct icon always accompanies the tone. No decorative status dots on their own.

## Chips and icons

- **Chip:** 20px tall, rounded 6px, 12px/500 text, optional 12px icon, soft background plus foreground from the tone. One size.
- **TintIcon:** a lucide icon on a soft tinted rounded square (24px with 14px icon in lists, 20px with 12px in sidebar children). Used for event types in EventFeed and Timeline, source markers and card headers.
- **Same entity type, same icon, everywhere:** a company is always the same icon in the sidebar, command menu, record header, breadcrumb, list rows, timeline and dashboard card. Keep an `ENTITY_ICON` map next to the tone map. Where a thing has a real identity (site favicon, person avatar), the identity wins over the generic icon; the generic icon is the fallback.
- Counts: unread/attention counts use the primary (filled) tone, everything else the grey pill.

## Applying it

1. Inventory every label that appears as a chip, badge, dot, coloured text or legend in the old app.
2. Merge synonyms into one vocabulary (the same state called three things, coloured three ways).
3. Assign each value a tone and icon in the map; check that values meaning "bad", "good", "waiting" and "neutral" use red, green, amber and grey consistently across vocabularies.
4. Replace every ad-hoc colour with the component. Grep for raw colour utilities in feature code; it should be zero.
5. Check dark mode and both densities.
