---
name: web-ui
description: Principles for building great web app interfaces. Apply when building or reviewing web UI — components, layouts, interactions, forms, or any user-facing interface work.
---

Apply these principles when generating or modifying UI code. When reviewing existing UI, flag violations with the section reference (e.g. "§3 Feedback: button left in ambiguous state after click"). Not every rule applies to every component — use judgement, but default to following the principle unless there's a clear reason not to.

---

## 1. Performance & Responsiveness

Speed is a design feature.

- Every interaction must resolve — or visibly begin — within **100ms**
- Show loading states **immediately** — before the response arrives, not after
- Use **skeleton loading states** that match the shape of incoming content
- Stagger skeleton resolves — avoid a simultaneous flash when data loads
- **Optimistic UI by default** — assume success, roll back on failure with a clear undo path
- Debounce inputs but show a pending state immediately (spinner on the input, not the page)
- Prioritise the LCP element — load main content first, defer chrome
- Use `content-visibility: auto` on long lists; **virtualise at >50 items** (react-window, tanstack-virtual, etc.)
- Animate layout changes (height, position), not just opacity — prevents jarring reflows
- Wrap all transitions in `prefers-reduced-motion` — animated experiences must degrade gracefully

**Render performance**
- No layout reads in the render path — avoid `getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `getComputedStyle` during render
- Batch DOM reads together, then DOM writes together — never interleave reads and writes
- Prefer **uncontrolled inputs** (`defaultValue` + ref) for high-frequency typing; controlled inputs must be cheap per keystroke

**Resource hints**
- `<link rel="preconnect">` for CDN and third-party asset domains
- Critical fonts: `<link rel="preload" as="font" crossorigin>` with `font-display: swap`

**Hydration safety**
- Inputs with `value` need `onChange` (or use `defaultValue`)
- Date/time rendering: guard against hydration mismatch (server vs client timezone)
- `suppressHydrationWarning` only where truly needed (e.g. timestamps)

---

## 2. Navigation & URL State

The URL is the most underused design tool in web apps.

**URL as source of truth**
- Serialise meaningful state to the URL: filters, sort order, selected tab, pagination, search query, open/closed panels
- Hydrate from URL on mount, not component state
- Use `replaceState` for ephemeral changes (hover, focus); `pushState` for meaningful navigation
- Encode *which item is selected* — don't encode transient state like "modal is open"
- Keep slugs short and readable: `/settings/billing` not `/app?section=3&sub=2&id=billing`

**Navigation structure**
- All navigation reachable in **3 steps or fewer**
- Current location always visible — breadcrumbs or highlighted nav item
- Search is navigation — treat it as a primary nav element, not a utility
- `Escape` closes everything: modals, drawers, dropdowns, command palettes
- Browser back and forward must work correctly throughout the app

---

## 3. Interaction & Feedback

The UI must always acknowledge the user. Silence is broken.

**Immediate feedback**
- UI responds to every action instantly — even if processing takes time
- Show the user's action reflected in the UI before the server confirms it
- Never leave a button in an ambiguous state after click
- Never disable a button without explaining why — tooltip or inline label on hover/focus
- **Hover states on all interactive elements** — visual feedback on pointer enter
- Interactive states increase in contrast: hover > rest, active > hover, focus > rest

**Errors & recovery**
- Error messages prescribe the fix, not just the problem
  - Bad: "Invalid password"
  - Good: "Password must be at least 8 characters"
- Inline errors adjacent to the field — never only at the top of a form
- Roll back failed optimistic updates with a clear undo prompt
- Explain consequences of destructive actions before the user commits

**Destructive actions**
- Require friction, but not a generic modal
- Inline confirmation with a short timeout is usually better than a modal
- Cancel means cancel — no data loss
- Don't make destructive actions visually prominent unless they're the primary action on the page

**Command & keyboard**
- `Cmd+K` / `Ctrl+K` opens a global command palette
- Keyboard shortcuts for everything a power user does repeatedly
- Show shortcuts overlaid on the interface when the user holds a modifier key
- Never hijack right-click
- No product tours — drop users into a useful default state with descriptive text and interface cues

**Animations & interruption**
- Animations must be **interruptible** — respond to new user input mid-animation
- `autoFocus` sparingly: desktop only, single primary input per page; avoid on mobile (it triggers the keyboard)

---

## 4. Visual Hierarchy

Every element sits in a pyramid of importance. Make the hierarchy unambiguous.

**Establishing hierarchy**
- Use colour and weight to signal importance — not just font size
- Bold + normal colour > large + grey for conveying importance
- Reduce contrast to de-emphasise; increase weight to emphasise

**Colour system**
- No more than **3 primary colours** in the UI
- Use HSL when building a colour system — it maps to how humans perceive colour
- Build a shade system: one or two base hues with 5–10 shades each
- Grey text on coloured backgrounds breaks hierarchy — use a de-saturated tint of the background colour instead
- Never rely on colour alone to signal state — always pair with an icon or text label

**Typography**
- Define a type scale with 8–12 sizes and only use those sizes
- Don't centre-align body text — optimise for left-to-right reading
- Use `ch` units for text containers to enforce readable line length (~65–75ch)
- Use `…` (single character ellipsis), not `...`; use curly quotes `""` `''`, not straight quotes
- Non-breaking spaces for units and shortcuts: `10&nbsp;MB`, `⌘&nbsp;K`, brand names with spaces
- `font-variant-numeric: tabular-nums` on number columns and data tables
- `text-wrap: balance` on headings; `text-wrap: pretty` on body paragraphs

**Labels & data**
- Labels are a last resort — emphasise the data itself through weight, size, or colour
- `Label: value` format is for machines; design for humans who scan

**Borders & separation**
- Use **fewer borders** — separate elements with whitespace, background colour contrast, or subtle box shadows
- Accent borders (coloured top or left edge on cards/alerts) add personality without clutter

**Icons**
- Use icon sets designed for the target size — don't scale small icons up
- Never use an icon as the sole indicator of an action — pair with a label, especially on first use

---

## 5. Layout & Spacing

Spacing is a design element. Use it systematically.

**Spacing system**
- Pick a base unit (4px or 8px) and never deviate
- No two adjacent scale values should be closer than ~25% apart
- When in doubt, add more space — designs almost always need more breathing room
- You don't have to fill the whole screen

**Layout method**
- Prefer **flex/grid over JS measurement** for layout — CSS layout is faster and more reliable
- `env(safe-area-inset-*)` on full-bleed layouts for notches and rounded corners
- Avoid unwanted scrollbars: `overflow-x: hidden` on containers that shouldn't scroll horizontally

**Alignment**
- Consistent vertical rhythm throughout every view
- Keep action buttons close to where the user's attention already is (Fitts's Law) — a confirm button under a form beats one in the top-right corner

**Content overflow**
- Use `truncate` / `text-overflow: ellipsis`, `line-clamp-*`, or `overflow-wrap: break-word` as appropriate
- Flex children need `min-w-0` (or `min-width: 0`) for truncation to work
- Anticipate short, average, and very long user inputs in every text container

**Scrolling**
- No visible scrollbars — overlay or thin custom scrollbars
- Animate scroll position changes rather than jumping
- Restore scroll position when the user navigates back

**Empty states**
- Empty states are onboarding opportunities, not afterthoughts
- They must explain what goes here and offer a clear action
- "No data" is not an empty state

---

## 6. Forms

Forms are where users do work. Make that work effortless.

**Validation**
- Validate on blur, not on submit
- Show password strength in real time
- Auto-advance focus on completion (e.g. OTP fields)
- **Focus the first error field** on submit

**Input details**
- Use the correct `input type` — it controls the mobile keyboard (`email`, `tel`, `number`, etc.)
- Set `inputmode` alongside `type` for finer keyboard control (`inputmode="decimal"`, `inputmode="numeric"`)
- Set `autocomplete` and meaningful `name` attributes on inputs — browsers and password managers depend on them
- `autocomplete="off"` on non-auth fields (search, codes, one-time tokens)
- `spellCheck={false}` on emails, codes, usernames, URLs
- Minimum **44x44px** hit target on touch devices
- **Never block paste** — especially on password, email, and confirmation fields
- Support copy/paste from clipboard everywhere it makes sense
- Never clear a form on failed submission
- Session re-authentication must not destroy work in progress

**Labels & placeholders**
- Every input has a visible, persistent label — never use placeholder text as a label
- Placeholder text disappears on input; labels don't
- Labels must be clickable: use `htmlFor` or wrap the input in the `<label>`
- Placeholders end with `…` and show an example pattern (e.g. `name@example.com…`)

**Checkboxes & radios**
- Shared hit target across label + control — no dead zones between them

**Submit behaviour**
- Submit button stays **enabled until the request starts**; show a spinner during the request
- Warn before navigation with unsaved changes (`beforeunload` event / router guard)

---

## 7. Psychology & Cognitive Load

Users don't read interfaces — they scan, pattern-match, and move on.

**Reduce cognitive load**
- **Hick's Law**: Decision time grows with choices — hide advanced options behind progressive disclosure
- **Miller's Law**: Chunk related information — users process groups of ~7 items most naturally
- **Tesler's Law**: Complexity can't be eliminated, only moved. Simplify the UI by absorbing complexity in the app
- Progressive disclosure: reveal features when they become relevant, not all at once

**Memory & attention**
- **Von Restorff effect**: The different element is remembered — use it for one primary CTA, not five
- **Serial position effect**: Users best remember first and last items in a list
- **Peak-end rule**: Users judge by the peak and the end — invest in success states and error recovery, not just the happy path
- **Jakob's Law**: Users expect your app to behave like apps they already know — follow conventions unless there's a strong reason not to

---

## 8. Accessibility

Accessibility is a quality bar, not a checklist. It also makes the app better for everyone.

**Keyboard navigation**
- Every interaction reachable by keyboard — no mouse required
- Tab order follows visual order
- Focus trap in modals: `Tab` cycles within; `Escape` closes and returns focus to the trigger
- When a modal or panel closes, return focus to the element that opened it — never strand focus
- **Skip link** to main content as the first focusable element

**Focus styles**
- Never use `outline: none` without a custom focus indicator replacement
- Use `:focus-visible` instead of `:focus`
- Focus indicator: at least 2px thick, 3:1 contrast ratio
- Use `:focus-within` for compound controls (e.g. a search bar with icon + input)

**Colour & contrast**
- Minimum 4.5:1 contrast ratio for body text; 3:1 for large text
- Test both light and dark themes

**Motion**
- Respect `prefers-reduced-motion`
- Don't autoplay media or animations the user didn't initiate

**Semantic HTML**
- Native HTML elements first, ARIA second — no ARIA is better than wrong ARIA
- Headings in order (h1 > h2 > h3) — screen readers use them to navigate
- Link and button text describes the destination or outcome — "Click here" is not accessible
- `<button>` for actions, `<a>` / `<Link>` for navigation — never `<div onClick>`
- Icon-only buttons need `aria-label`
- Decorative icons: `aria-hidden="true"`

**Live regions & anchors**
- `aria-live="polite"` for async status updates (toast, loading complete, new results)
- `scroll-margin-top` on heading anchors so they aren't hidden behind sticky headers

---

## 9. Copy & Microcopy

The words in the interface are part of the design.

- Active voice, short sentences, max **7 words** per UI label
- Button text is an outcome, not an action: "Save changes" > "Submit"
- Minimal tooltips — if something needs explaining every time, redesign it
- Reassure users about data safety and reversibility before they commit
- No jargon in user-facing labels — write for the least technical user
- **Title Case** for headings and buttons; sentence case for body text
- Use numerals for counts (`3 items`, not `three items`)
- Second person ("you/your") — avoid first person ("we/our")
- `&` over "and" where space is constrained (tabs, breadcrumbs, badges)

**Internationalisation**
- Use `Intl.DateTimeFormat` / `Intl.NumberFormat` for dates, numbers, currencies — never hardcode formats
- Detect language via `Accept-Language` header, not IP geolocation

---

## 10. Animation

Motion should clarify, not decorate.

- Animate only **`transform` and `opacity`** — these run on the compositor and skip layout/paint
- Never `transition: all` — list properties explicitly (`transition: transform 200ms, opacity 200ms`)
- Set correct `transform-origin` to match the element's visual anchor point
- SVG transforms: apply on a `<g>` wrapper with `transform-box: fill-box`
- Animations must be **interruptible** — if the user acts mid-animation, respond immediately
- Wrap everything in `prefers-reduced-motion` — disable or simplify for users who opt out

---

## 11. Images & Media

Images are layout-shifting, bandwidth-heavy elements. Handle them deliberately.

- Every `<img>` needs explicit `width` and `height` attributes (CLS prevention)
- Below the fold: `loading="lazy"`
- Above the fold / hero: `fetchpriority="high"`
- Use modern formats (WebP/AVIF) with `<picture>` fallbacks where needed

---

## 12. Dark Mode, Touch & Platform

Respect the platform the user is on.

**Dark mode & theming**
- `color-scheme: dark` (or `light dark`) on `<html>` — tells the browser to style native controls
- `<meta name="theme-color">` matches the page background colour
- Native `<select>`: set explicit `background-color` and `color` — Windows dark mode defaults are unreadable otherwise

**Touch**
- `touch-action: manipulation` on interactive elements (eliminates 300ms tap delay)
- Set `-webkit-tap-highlight-color` intentionally — don't just disable it
- `overscroll-behavior: contain` in modals and drawers to prevent background scroll
- During drag operations: disable text selection (`user-select: none`), mark dragged elements with `inert`

---

## Anti-Patterns

Flag these in code review — they are common and always wrong.

1. `<div onClick>` instead of `<button>` or `<a>`
2. `outline: none` / `outline: 0` without a replacement focus style
3. `transition: all` — always list specific properties
4. Placeholder text as the only label on an input
5. `event.preventDefault()` on paste events
6. Missing `width`/`height` on `<img>` elements
7. Layout reads (`offsetHeight`, `getBoundingClientRect`) interleaved with DOM writes
8. `autoFocus` on mobile or on more than one element
9. Colour as the sole indicator of state (no icon or text backup)
10. Generic "An error occurred" with no recovery guidance
11. Disabled submit button with no explanation of what's missing
12. `console.log` left in production event handlers
13. Hardcoded date/number formats instead of `Intl.*`
14. `suppressHydrationWarning` used to hide real mismatches
15. Missing `aria-label` on icon-only buttons
