---
name: web-ui
description: Principles for building great web app interfaces — performance, layout, interactions, forms, accessibility, animation, and motion craft. Apply when building or reviewing web UI, including transitions, gestures, and component polish.
---

Taste is trained, not innate — develop it by studying interfaces that feel right and reverse-engineering why. Most of the details users will love are details they'll never consciously notice; the aggregate of invisible correctness is what makes software feel great. Beauty is leverage — good defaults and good motion are real differentiators.

Apply these principles when generating or modifying UI code. When reviewing existing UI, flag violations with the section name (e.g. "Fundamentals › Feedback: button left in ambiguous state after click"). For motion/animation/transition issues, use a markdown table with `| Before | After | Why |` columns — one row per issue. Not every rule applies to every component — use judgement, but default to following the principle unless there's a clear reason not to.

Example motion-review table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; avoid `all` |
| `transform: scale(0)` on enter | `transform: scale(0.95); opacity: 0` | Nothing in the real world appears from nothing |
| `ease-in` on dropdown | `ease-out` with custom curve | `ease-in` delays the moment the user is watching most closely |

**Scope note:** the typographic rules below (curly quotes, `…`, Title Case, non-breaking spaces) govern **UI chrome** — labels, buttons, headings, empty states. They do not govern long-form prose rendered from markdown or a CMS.

---

## 1. Fundamentals — checklist

The specific, easy-to-forget half of the web interface guidelines. The rest (semantic HTML, sensible contrast, keyboard reachability) you do by default; these are the ones that get missed.

**Performance & rendering**
- Show the loading state *before* the response, not after; skeletons match the shape of incoming content and stagger their resolve
- Optimistic UI by default — assume success, roll back with a clear undo path
- `content-visibility: auto` on long lists; virtualise at >50 items
- No layout reads (`getBoundingClientRect`, `offsetHeight`, `getComputedStyle`) in the render path; batch all reads, then all writes
- Uncontrolled inputs (`defaultValue` + ref) for high-frequency typing
- `preconnect` third-party origins; `preload` critical fonts with `font-display: swap`
- Every `<img>` has explicit `width`/`height` (CLS); `loading="lazy"` below the fold, `fetchpriority="high"` for the hero
- Hydration: inputs with `value` need `onChange`; guard date rendering against server-vs-client timezone; `suppressHydrationWarning` only for genuinely unfixable timestamps, never to silence a real mismatch

**URL & navigation**
- Serialise meaningful state to the URL (filters, sort, tab, pagination, query, open panels) and hydrate from it on mount, not from component state
- `replaceState` for ephemeral changes, `pushState` for real navigation; encode *which item is selected*, not "modal is open"
- `Escape` closes everything; back/forward work everywhere; restore scroll position on back; `Cmd/Ctrl+K` opens a command palette

**Interaction & feedback**
- Never leave a button ambiguous after click; never disable one without explaining why
- States escalate contrast: hover > rest, active > hover, focus > rest
- Gate hover behind `@media (hover: hover) and (pointer: fine)` — touch fires hover on tap
- Errors prescribe the fix ("Password must be at least 8 characters") and sit inline beside the field, never only at the top
- Destructive actions need friction, not a generic modal — inline confirm with a short timeout usually beats one

**Hierarchy & type**
- ≤3 primary colours, shades built in HSL; never signal state with colour alone
- Bold + normal colour beats large + grey; grey text on a coloured background breaks hierarchy — use a desaturated tint of that background
- Fixed type scale (8–12 sizes); `ch` units for a 65–75ch measure; don't centre body text
- `font-variant-numeric: tabular-nums` on number columns; `text-wrap: balance` on headings, `pretty` on body
- `…` not `...`; curly quotes; `&nbsp;` in units and shortcuts (`10&nbsp;MB`, `⌘&nbsp;K`)
- Fewer borders — whitespace, background contrast or a subtle shadow instead

**Layout**
- One spacing base (4 or 8px), adjacent steps ≥25% apart; flex/grid over JS measurement
- `env(safe-area-inset-*)` on full-bleed layouts
- Flex children need `min-width: 0` or truncation silently fails
- Plan for short, average and very long content in every text container
- Empty states are onboarding — say what goes here and offer an action

**Forms**
- Validate on blur; focus the first error field on submit; auto-advance on completion (OTP)
- Correct `type` **and** `inputmode` (`decimal`, `numeric`) — they control the mobile keyboard
- Meaningful `name` + `autocomplete`; `spellcheck={false}` on emails, codes, usernames, URLs
- **Never block paste** — no `preventDefault` on paste, especially password and confirmation fields
- Visible, persistent, clickable label on every input (`htmlFor` or wrapping `<label>`); a placeholder is not a label
- Submit stays enabled until the request starts, then spins; never clear a form on failed submission; warn on unsaved-change navigation
- 44×44px minimum touch target; shared hit target across checkbox/radio + label; `autoFocus` desktop-only and once per page

**Accessibility**
- Skip link to main content as the first focusable element
- `:focus-visible` over `:focus`; never `outline: none` without a replacement (≥2px, 3:1); `:focus-within` for compound controls
- Focus trap in modals; on close return focus to the trigger — never strand focus
- `aria-label` on icon-only buttons, `aria-hidden` on decorative icons, `aria-live="polite"` for async status
- `scroll-margin-top` on heading anchors so sticky headers don't cover them
- `prefers-reduced-motion`: reduced ≠ none — keep opacity and colour, drop movement

**Copy & platform**
- ≤7 words per label; button text is an outcome ("Save changes", not "Submit"); Title Case headings and buttons, sentence case body
- `Intl.DateTimeFormat` / `Intl.NumberFormat` — never hardcode formats; detect language from `Accept-Language`, not IP
- `color-scheme` on `<html>` + matching `<meta name="theme-color">`; native `<select>` needs explicit `background-color`/`color` (Windows dark mode)
- `touch-action: manipulation` on interactive elements; `overscroll-behavior: contain` in modals and drawers

---

## 2. Animation

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
- Set `transform-origin` to match the element's visual anchor — default `center` is wrong for almost every popover (see Component Polish)
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
- Animations must be interruptible — respond to new user input mid-animation

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

## 3. Component Polish

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

## 4. Gestures & Drag

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

## 5. Building Loved Components

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
