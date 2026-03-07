---
name: web-ui
description: A principles-first style guide for building great web app interfaces. Apply when building or reviewing web UI — components, layouts, interactions, forms, or any user-facing interface work. Covers performance, navigation, interaction, visual hierarchy, layout, forms, psychology, accessibility, copy, and brand.
---

## 1. Performance & Responsiveness

Speed is a design feature.

- Every interaction must resolve — or visibly begin — within **100ms**
- Show loading states **immediately** — before the response arrives, not after
- Use **skeleton loading states** that match the shape of the incoming content
- Stagger skeleton resolves — avoid a simultaneous flash when data loads
- **Optimistic UI by default** — assume success, roll back on failure with a clear undo path
- Debounce inputs but show a pending state immediately (spinner on the input, not the page)
- Prioritise the LCP element — load main content visibly first, defer chrome
- Use `content-visibility: auto` on long lists
- Animate layout changes (height, position), not just opacity — prevents jarring reflows
- Wrap all transitions in `prefers-reduced-motion` — animated experiences must degrade gracefully

> Perceived speed matters as much as actual speed. A spinner that appears instantly feels faster than a blank screen that resolves in half the time.

---

## 2. Navigation & URL State

The URL is the most underused design tool in web apps.

**URL as source of truth**
- Serialise everything meaningful to the URL: filters, sort order, selected tab, pagination, search query, open/closed panels
- Treat the URL as the source of truth, not component state — hydrate from URL on mount
- Use `replaceState` for ephemeral changes (hover, focus); `pushState` for meaningful navigation
- Encode *which item is selected* — don't encode transient state like "modal is open"
- Keep slugs short and readable: `/settings/billing` not `/app?section=3&sub=2&id=billing`
- Persistent, resumable state — users should never lose where they were

**Navigation structure**
- All navigation is reachable in **3 steps or fewer**
- Current location is always visible — breadcrumbs or highlighted nav item
- Search is navigation — treat it as a primary nav element, not a utility
- `Escape` closes everything: modals, drawers, dropdowns, command palettes
- Browser back and forward must work correctly throughout the app

> URL state costs almost nothing with `nuqs` (Next.js) or native `URLSearchParams`, and eliminates an entire class of "how do I share this?" support requests.

---

## 3. Interaction & Feedback

The UI must always acknowledge the user. Silence is broken.

**Immediate feedback**
- UI responds to every user action instantly — even if processing takes time
- Show the user's action reflected in the UI before the server confirms it
- Never leave a button in an ambiguous state after it's been clicked
- Never disable a button without explaining why — tooltip or inline label on hover/focus

**Errors & recovery**
- Error messages must prescribe the fix, not just describe the problem
  - Bad: "Invalid password"
  - Good: "Password must be at least 8 characters"
- Inline errors appear adjacent to the field — never only at the top of a form
- Roll back failed optimistic updates with a clear undo prompt
- Reassure users before loss — explain consequences of destructive actions before they commit

**Destructive actions**
- Require friction, but not a generic modal
- Inline confirmation with a short timeout is usually better than a modal
- **Honest one-click cancel** — cancel means cancel, with no data loss
- If a destructive action isn't the primary action on the page, don't make it visually prominent

**Command & keyboard**
- Keyboard shortcut ALL navigation
- Holding down command shows keyboard shortcuts
- `Cmd+K` / `Ctrl+K` opens a global command palette
- Keyboard shortcuts for everything a power user will do repeatedly
- Show keyboard shortcuts overlaid on the current interface when the user holds a modifier key
- Never hijack right-click
- No product tours — drop users into a useful default state, but guide them with desriprive text and interface

---

## 4. Visual Hierarchy

Every element sits somewhere in a pyramid of importance. Make the hierarchy unambiguous.

**Establishing hierarchy**
- Use colour and weight to signal importance — not just font size
- Bold + normal colour > large + grey for conveying importance
- Design in greyscale first — solve hierarchy through layout, weight, and spacing before adding colour
- Reduce contrast to de-emphasise; increase weight to emphasise

**Colour system**
- No more than **3 primary colours** in the UI
- Use HSL, not hex, when building a colour system — it maps to how humans think about colour
- Build a shade system: one or two base hues with 5–10 shades each
- Grey text on coloured backgrounds breaks hierarchy — use a de-saturated tint of the background colour instead
- Never rely on colour alone to signal state (error, warning, success) — always pair with an icon or text label

**Typography**
- Define a type scale with 8–12 sizes and only ever use those sizes
- Optimise for left-to-right reading — don't centre-align body text
- Use `ch` units for text containers to enforce readable line length (~65–75ch)
- Active voice, short sentences — maximum 7 words per UI label or CTA
- Button text is an outcome, not an action: "Save changes" > "Submit", "Delete account" > "Confirm"

**Labels & data**
- Labels are a last resort — emphasise the data itself through weight, size, or colour
- `Label: value` format is for machines. Design for humans who scan

**Borders & separation**
- Use **fewer borders** — separate elements with whitespace, background colour contrast, or subtle box shadows
- Box shadows, spacing, and background tones do the same job with less visual noise
- Accent borders (coloured top or left edge on cards/alerts) add personality without clutter

---

## 5. Layout & Spacing

Spacing is a design element. Use it systematically.

**Spacing system**
- Pick a base unit (4px or 8px) and never deviate
- No two adjacent scale values should be closer than ~25% apart
- When in doubt, add more space — designs almost always need more breathing room
- You don't have to fill the whole screen

**Alignment**
- Optical alignment over geometric — trust the eye over the ruler
- Consistent vertical rhythm throughout every view
- Keep action buttons close to where the user's attention already is (Fitts's Law)
  - A confirm button under a form beats one in the top-right corner

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
- Inline errors appear adjacent to the field — never only at the top
- Show password strength in real time
- Auto-advance focus on completion (e.g. OTP fields)

**Input details**
- Use the correct `input type` attribute — it controls the keyboard on mobile (`email`, `tel`, `number`, etc.)
- Minimum **44×44px** hit target on touch devices
- Support copy/paste from clipboard everywhere it makes sense
- Never clear a form on failed submission
- Allow session re-authentication without losing form data — a timeout must not destroy work in progress

**Labels**
- Every input has a visible, persistent label — don't rely on placeholder text as a label
- Placeholder text disappears when the user starts typing; labels don't

---

## 7. Psychology & Cognitive Load

Users don't read interfaces — they scan, pattern-match, and move on.

**Reduce cognitive load**
- **Hick's Law**: Decision time increases with the number of choices — hide advanced options behind progressive disclosure
- **Miller's Law**: Chunk related information together — users process groups of ~7 items most naturally
- **Tesler's Law**: Complexity cannot be eliminated, only moved. If you simplify the UI, the app must absorb the complexity instead
- Progressive disclosure: reveal features at the moment they become relevant, not all at once

**Memory & attention**
- **Von Restorff effect**: The element that differs from the rest is the one that's remembered — use it deliberately for your one primary CTA, not for five things at once
- **Serial position effect**: Users best remember the first and last items in a list
- **Peak-end rule**: Users judge the whole experience by how it felt at its peak and at its end — invest in success states and error recovery, not just the happy path
- **Jakob's Law**: Users expect your app to behave like apps they already know — follow conventions unless you have a strong reason not to

> The aesthetic-usability effect is real: people perceive visually polished interfaces as more usable, even before they interact with them.

---

## 8. Accessibility & Keyboard

Accessibility is not a checklist. It is a quality bar. It also makes the app better for everyone.

**Keyboard navigation**
- Every interaction is reachable by keyboard — no mouse required
- Tab order must follow visual order — if DOM order diverges from layout, keyboard users experience a different page than mouse users
- Focus trap in modals: `Tab` cycles within the modal; `Escape` closes it and returns focus to the trigger element
- When a modal or panel closes, return focus to the element that opened it — never leave focus stranded

**Focus styles**
- Never use `outline: none` without replacing it with a custom focus indicator
- Use `:focus-visible` instead of `:focus` — clean for mouse users, visible for keyboard users
- Focus indicator must be at least 2px thick with a 3:1 contrast ratio
- Test by putting the mouse away for 5 minutes and navigating with the keyboard only

**Colour & contrast**
- Minimum 4.5:1 contrast ratio for body text; 3:1 for large text
- Don't rely on colour alone to signal state — pair every colour signal with an icon or text label
- Test both light and dark themes

**Motion**
- Respect `prefers-reduced-motion` — wrap all transitions so animated experiences degrade gracefully
- Don't autoplay media or animations that the user didn't initiate

**Semantic HTML**
- Native HTML elements first, ARIA second — no ARIA is better than wrong ARIA
- Use correct `input` types — they determine mobile keyboard layout and assistive technology behaviour
- Headings must be in order (h1 → h2 → h3) — they are how screen readers navigate a page
- Link and button text must describe the destination or outcome — "Click here" is not an accessible label

---

## 9. Copy & Microcopy

The words in the interface are part of the design.

- Active voice, short sentences, maximum **7 words** per UI label
- Button text is an outcome, not an action
- Error messages prescribe the fix — don't just describe the problem
- Very minimal tooltips — if something needs explaining every time, redesign it
- Reassure users about data safety and reversibility before they commit
- Empty states explain what goes here and offer a next step
- No jargon in user-facing labels — write for the least technical person who will use this

---

## 10. Brand & Assets

- Provide a **copyable SVG logo** — designers and partners shouldn't need to ask
- Maintain a minimal brand kit: primary colour, typeface, logo variants, usage rules
- Short, memorable URL slugs — they get copied, shared, and typed by hand
- Don't scale icons designed for small sizes up — use icon sets designed for the target size
- Icons should never be the sole indicator of an action — pair with a label, especially on first use

---

## Quick Reference Checklist

Use this when reviewing any UI before shipping.

**Performance**
- [ ] Every interaction acknowledges the user within 100ms
- [ ] Skeleton states in place before real data loads
- [ ] `prefers-reduced-motion` respected

**Navigation**
- [ ] Meaningful state is in the URL
- [ ] Browser back/forward works
- [ ] Current location visible at all times
- [ ] Escape closes overlays

**Interaction**
- [ ] Optimistic updates implemented
- [ ] All errors prescribe a fix
- [ ] Destructive actions have appropriate friction
- [ ] Cmd+K command palette available

**Visual**
- [ ] Greyscale hierarchy works before colour is applied
- [ ] Colour is not the only signal for state
- [ ] Fewer borders — whitespace and bg contrast used instead

**Forms**
- [ ] Validation on blur, not submit
- [ ] No form cleared on failed submission
- [ ] Correct `input type` on every field

**Accessibility**
- [ ] Tab through the entire app without a mouse
- [ ] Focus is never stranded after modal close
- [ ] `:focus-visible` styles implemented
- [ ] Contrast ratios pass at 4.5:1

**Copy**
- [ ] All button text describes an outcome
- [ ] All empty states have a CTA
- [ ] No placeholder-as-label
