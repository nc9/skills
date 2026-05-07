---
name: web-ui
description: Principles for building great web app interfaces — performance, layout, interactions, forms, accessibility, animation, and motion craft. Apply when building or reviewing web UI, including transitions, gestures, and component polish.
---

Taste is trained, not innate — develop it by studying interfaces that feel right and reverse-engineering why. Most of the details users will love are details they'll never consciously notice; the aggregate of invisible correctness is what makes software feel great. Beauty is leverage — good defaults and good motion are real differentiators.

Apply these principles when generating or modifying UI code. When reviewing existing UI, flag violations with the section reference (e.g. "§3 Feedback: button left in ambiguous state after click"). For motion/animation/transition issues, use a markdown table with `| Before | After | Why |` columns — one row per issue. Not every rule applies to every component — use judgement, but default to following the principle unless there's a clear reason not to.

Example motion-review table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; avoid `all` |
| `transform: scale(0)` on enter | `transform: scale(0.95); opacity: 0` | Nothing in the real world appears from nothing |
| `ease-in` on dropdown | `ease-out` with custom curve | `ease-in` delays the moment the user is watching most closely |

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
- Gate hover effects behind `@media (hover: hover) and (pointer: fine)` — touch devices fire hover on tap and produce false positives (see §12)

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
- Respect `prefers-reduced-motion` — but reduced ≠ none. Keep opacity and color transitions that aid comprehension; remove movement and position animations
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

Motion clarifies, never decorates. Every animation answers two questions: *should this animate at all*, and *what is the purpose*.

**Decision framework — frequency dictates everything**

| User sees animation | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette toggle) | No animation. Ever. |
| Tens of times/day (hover, list nav) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare/first-time (onboarding, celebrations) | Can add delight |

**Never animate keyboard-initiated actions** — Cmd+K, hotkeys, etc. Animation makes repeated actions feel sluggish. Raycast has no open/close animation; that's optimal for something used hundreds of times a day.

**Purpose** — every animation must justify itself: spatial consistency (toast enters/exits same direction so swipe-to-dismiss feels right), state indication (morphing button), feedback (button scales on press), preventing jarring change (fade between states). "It looks cool" + frequent usage = no animation.

**Easing**
- Enter/exit → `ease-out` (instant feedback, fast start)
- On-screen movement / morphing → `ease-in-out`
- Hover, color → `ease`
- Constant motion (marquee, progress bar) → `linear`
- **Never `ease-in` for UI** — it delays the moment the user is watching most closely; a 180ms `ease-out` feels faster than a 180ms `ease-in`

Built-in CSS easings are weak. Define custom curves once and reuse:

```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1); /* iOS-like */
}
```

Don't hand-craft curves — use easing.dev or easings.co.

**Duration**

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltip, small popover | 125–200ms |
| Dropdown, select | 150–250ms |
| Modal, drawer | 200–500ms |
| Marketing / explanatory | Can be longer |

UI animations stay **under 300ms**. A 180ms dropdown feels more responsive than a 400ms one.

**Perceived performance** — speed is partly perception. A faster spinner makes the same load time feel quicker. After the first tooltip is open, subsequent tooltips on the same toolbar should appear instantly (no delay, no animation) — the toolbar feels faster.

**Hardware acceleration**
- Animate **`transform` and `opacity` only** — they skip layout and paint and run on the compositor. `padding`, `margin`, `height`, `width`, `top`/`left` trigger all three rendering steps.
- Never `transition: all` — list properties explicitly: `transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out)`
- Set `transform-origin` to match the element's visual anchor — default `center` is wrong for almost every popover (see §13)
- SVG transforms: apply on a `<g>` wrapper with `transform-box: fill-box`

**Under load: CSS beats JS**
- CSS animations run off the main thread. Framer Motion `x`/`y` shorthand uses `requestAnimationFrame` and drops frames when the browser is busy loading/painting.
- For hardware-accelerated Framer Motion, use the full transform string: `<motion.div animate={{ transform: "translateX(100px)" }} />` — not `animate={{ x: 100 }}`
- For programmatic control with CSS performance, use the Web Animations API:

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

**Transitions vs keyframes**
- CSS transitions can be **interrupted and retargeted** mid-animation — keyframes restart from zero
- Use transitions for any rapidly-triggered UI (toasts, list reorder, drag state)
- Reserve keyframes for one-shot decoration (loading spinner, marketing reveal)

**Springs**
- Use for: drag with momentum, gestures interruptible mid-motion, decorative mouse-tracking, "alive" elements (Apple Dynamic Island)
- Apple's parameterisation is easier to reason about: `{ type: "spring", duration: 0.5, bounce: 0.2 }`
- Keep bounce subtle (0.1–0.3); avoid bounce in most professional UI
- Springs maintain velocity when interrupted — ideal for gestures users may reverse

**`@starting-style`** — modern CSS entry animation, no `useEffect(setMounted, true)` needed:

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms var(--ease-out), transform 400ms var(--ease-out);

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

Fall back to a `data-mounted` attribute pattern where browser support isn't there yet.

**CSS variable inheritance footgun** — changing a CSS var on a parent recalculates styles for every descendant. In a drawer with many items, updating `--swipe-amount` on the container is expensive. Set `transform` directly on the dragged element:

```js
// Bad: recalcs all children
container.style.setProperty('--swipe-amount', `${distance}px`);

// Good: only this element
element.style.transform = `translateY(${distance}px)`;
```

**Asymmetric enter/exit** — slow when the user is deciding, snappy when the system responds. Hold-to-delete: 2s linear while pressed; 200ms `ease-out` snap-back on release.

**Stagger** — when multiple elements enter together, delay each by 30–80ms after the previous. Long stagger delays make the interface feel slow. Stagger is decorative — never block interaction while it plays.

**`clip-path` is an animation tool**
- `clip-path: inset(top right bottom left)` defines a rectangular clip; each value eats from that side. `inset(0 100% 0 0)` is fully hidden from the right
- Tabs with perfect color transitions: render the tab list twice (one default, one styled active), clip the active copy so only the active tab shows, animate the clip on change
- Hold-to-delete: clip-path overlay from `inset(0 100% 0 0)` to `inset(0 0 0 0)` over 2s linear on `:active`, snap back 200ms `ease-out` on release
- Image reveals on scroll: `inset(0 0 100% 0)` → `inset(0 0 0 0)` triggered by `IntersectionObserver`
- Comparison sliders: overlay two images, clip the top one with `inset(0 50% 0 0)`, drive the right inset from drag position — no extra DOM, fully GPU

**Debugging**
- Slow-mo: temporarily 2–5x duration to reveal timing issues invisible at full speed
- Chrome DevTools → Animations panel for frame-stepping coordinated properties
- Test gestures on real devices (USB-tether iPhone via Safari remote devtools); simulators miss inertia and touch latency
- Review animations the next day with fresh eyes — issues you missed during build will jump out

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

## 13. Component Polish

Small details compound. These rules apply everywhere a user can interact, hover, or wait for a popover.

**Buttons feel responsive**

```css
.button {
  transition: transform 160ms var(--ease-out);
}
.button:active {
  transform: scale(0.97);
}
```

Subtle (0.95–0.98). Applies to any pressable element. `scale()` shrinks children too — icons and text shrink in proportion, which is correct.

**Never animate from `scale(0)`** — nothing in the real world appears from nothing. Start from `scale(0.95)` (or higher) combined with `opacity: 0`. A barely-visible initial scale makes entrances feel natural.

**Origin-aware popovers** — popovers should scale from their trigger, not from center. Default `transform-origin: center` is wrong for almost every popover. **Modals are exempt** — they appear centered in the viewport, not anchored to a trigger.

```css
/* Radix UI */
.popover-content { transform-origin: var(--radix-popover-content-transform-origin); }
/* Base UI */
.popover-content { transform-origin: var(--transform-origin); }
```

**Tooltips — skip delay after the first** — first tooltip uses delay (prevents accidental activation); once one is open, hovering adjacent tooltips opens them instantly. Feels faster without defeating the initial protection.

```css
.tooltip {
  transition: opacity 125ms var(--ease-out), transform 125ms var(--ease-out);
  transform-origin: var(--transform-origin);
}
.tooltip[data-starting-style],
.tooltip[data-ending-style] { opacity: 0; transform: scale(0.97); }
.tooltip[data-instant] { transition-duration: 0ms; }
```

**Blur to mask imperfect crossfades** — when two states cross-fade and you can see both at once, add `filter: blur(2px)` during the transition. Blur blends the two states into one perceived transformation. Keep blur < 20px (Safari paints heavy blur expensively).

**Combine press feedback patterns** — `scale(0.97)` on `:active` + brief `filter: blur(2px)` on the content during state change = polished button transition.

---

## 14. Gestures & Drag

Drag interactions feel right when they obey real-world physics.

**Momentum-based dismissal** — don't require dragging past a threshold; calculate velocity and dismiss on a flick:

```js
const elapsed = Date.now() - dragStart;
const velocity = Math.abs(distance) / elapsed;
if (Math.abs(distance) >= SWIPE_THRESHOLD || velocity > 0.11) dismiss();
```

**Damping at boundaries** — when a user drags past the natural limit, apply increasing friction instead of a hard stop. The further they drag, the less the element moves. Real things slow to a stop, they don't snap to walls.

**Pointer capture** — once drag starts, call `setPointerCapture` so the gesture continues even if the pointer leaves element bounds.

**Multi-touch protection** — ignore additional touch points after the initial drag begins; otherwise switching fingers mid-drag teleports the element.

```js
function onPress(e) {
  if (isDragging) return;
  // start drag…
}
```

**Drag hygiene** — `user-select: none` on the dragged element (prevents text selection mid-drag); mark transient siblings with `inert` so they can't receive input during drag.

---

## 15. Building Loved Components

When authoring shared components or library-grade primitives, the bar is higher. Distillation of what makes Sonner-class components stick:

- **Zero-config DX** — single mount, no hooks/context required to use. Insert `<Toaster />` once, call `toast()` from anywhere. Friction kills adoption.
- **Good defaults beat many options** — most users never customise; ship beautiful out of the box.
- **Handle edge cases invisibly** — pause toast timers when the tab is hidden; fill gaps between stacked toasts with pseudo-elements so hover states stay live; capture pointer during drag. Users never notice; that's the goal.
- **Transitions over keyframes for dynamic UI** — toasts/lists are added rapidly; transitions retarget, keyframes restart.
- **Cohesion** — match motion personality to the component. A playful component can be bouncier; a professional dashboard should be crisp and fast. A toast library that uses `ease` (not `ease-out`) at slightly slower than typical durations *feels* elegant — design the easing to match the vibe.
- **Review the next day** — bugs invisible at full speed surface with fresh eyes and slow-mo.
- **Documentation as product** — interactive examples + ready-to-paste snippets. Let people touch the component before they commit.

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
16. Entry animation from `scale(0)` — start at `scale(0.95)` with `opacity: 0`
17. `ease-in` on UI elements — use `ease-out` or a custom curve
18. `transform-origin: center` on popovers (modals are exempt)
19. Animation on keyboard-initiated actions (Cmd+K, hotkeys)
20. UI animation longer than 300ms
21. Hover effect without `@media (hover: hover) and (pointer: fine)` gate
22. Keyframes on rapidly-triggered elements (toasts, list reorder, drag state)
23. Framer Motion `x`/`y` props on hot animations under main-thread load — use `transform: "translateX()"`
24. Symmetric enter/exit timing on press-and-hold patterns — release should always be snappy
25. Updating CSS variables on a parent for per-item drag positions — set `transform` directly on the element
