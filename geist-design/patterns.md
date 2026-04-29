# Patterns

Named motifs that compose into the Geist aesthetic. Reference these by name when building or reviewing UI. Each pattern includes when to use it and a sketch of the implementation.

---

## Page & Section Patterns

### Hairline-bordered card

The defining card style. 1px low-contrast border, no drop shadow, slight surface elevation via background color.

```
Surface bg:    1 step lighter than page (e.g. #0a0a0a page → #111 card)
Border:        1px solid rgba(255,255,255,0.10) (dark)  /  rgba(0,0,0,0.08) (light)
Padding:       24–32px
Radius:        8–12px
Hover:         border alpha 0.10 → 0.16, no scale
```

Tailwind/JSX:

```jsx
<div className="rounded-[10px] border border-black/[0.08] bg-neutral-50 p-7 transition-colors hover:border-black/[0.16] dark:border-white/10 dark:bg-neutral-900 dark:hover:border-white/[0.16]">
  {children}
</div>
```

When to use: feature cards, pricing cards, content cards on docs/marketing. Most of the cards on Vercel, Linear, Resend, and Supabase are this exact pattern.

### Mono eyebrow + headline + lede

The canonical section opener. Three lines, three roles.

```
[MONO EYEBROW LABEL]              ← 12px mono, uppercase, gray-11
Big confident headline            ← 48–64px, weight 600, -0.03em
A one-sentence description        ← 17–18px, gray-11, max-width 60ch
that sells the section.
```

Spacing: 16px between eyebrow and headline, 24px between headline and lede.

Tailwind/JSX:

```jsx
<header className="space-y-4">
  <p className="font-mono text-xs uppercase tracking-wider text-neutral-500">Eyebrow label</p>
  <h2 className="text-5xl font-semibold tracking-[-0.03em] leading-[1.1] text-neutral-900 dark:text-neutral-50">
    Big confident headline
  </h2>
  <p className="max-w-[60ch] text-[17px] leading-[1.55] text-neutral-500">
    A one-sentence description that sells the section.
  </p>
</header>
```

This pattern alone makes a page read as "modern dev tool." Without it, even with perfect tokens, the page will feel generic.

### Beam / spotlight hero

Vercel's signature hero. Single radial gradient behind centered content, fades into page background.

```css
.beam {
  background: radial-gradient(
    ellipse 60% 50% at 50% 0%,
    rgba(120, 119, 198, 0.15),
    transparent 70%
  );
}
```

Tailwind/JSX (arbitrary value):

```jsx
<section className="relative bg-[radial-gradient(ellipse_60%_50%_at_50%_0%,rgba(120,119,198,0.15),transparent_70%)]">
  {children}
</section>
```

Variations: brand-accent color instead of purple. Multiple stacked beams for richer hero. Animated slow drift is acceptable but optional.

When to use: marketing homepage hero only. Not on subpages, not on docs.

### Dot grid background

5–10% opacity radial-gradient pattern, tiled. Adds "engineered" feel without competing with content.

```css
.dot-grid {
  background-image: radial-gradient(
    circle, rgba(255,255,255,0.06) 1px, transparent 1px
  );
  background-size: 16px 16px;
}
```

When to use: hero sections (combined with beam), feature section backgrounds, footer. Keep opacity low — if you can see the dots clearly without looking, they're too strong.

### Lattice / grid lines

Same idea as dot grid but with linear gradients forming a fine grid:

```css
.grid-lines {
  background-image:
    linear-gradient(rgba(0,0,0,0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.05) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

Common on Vercel, Linear, dev-tool docs. Works light or dark. Keep opacity 5–10%.

### Aurora border

Animated gradient that slowly rotates around a card or button. Common on Vercel CTAs, AI product launches. Subtle but distinctive.

Implementation: conic gradient with slow rotation animation, masked to a 1–2px ring around the element.

When to use: hero CTA, "new" feature callouts, premium plan cards. Sparingly — if every card has aurora, none of them do.

---

## Component Patterns

### Primary CTA button

```
Background:   pure black (light mode) / pure white (dark mode) / brand accent
Text:         opposite of background
Padding:      10–12px vertical, 16–20px horizontal
Radius:       6–8px (or 9999px pill — pick one across the app)
Font:         15px, weight 500–600, letter-spacing -0.005em
Border:       none (the contrast is the affordance)
Hover:        opacity 0.9 OR brightness shift, no scale
Focus:        2px ring in brand accent, offset 2px
```

Tailwind/JSX:

```jsx
<button className="rounded-md bg-neutral-900 px-5 py-2.5 text-[15px] font-medium tracking-[-0.005em] text-neutral-50 transition-opacity hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:bg-neutral-50 dark:text-neutral-900">
  Get started
</button>
```

### Secondary / ghost button

```
Background:   transparent or gray-3
Text:         gray-12 (high contrast)
Border:       1px hairline (matches card border)
Padding:      same as primary
Hover:        background gray-3 → gray-4
```

Crucial: secondary is gray, **not** a lighter brand color. "Outlined blue button" is wrong family.

### Pill button (special case)

Reserved for the most important action on a page. Often used by Supabase, Stripe for "Start now"-style CTAs.

```
Radius:       9999px
Padding:      12–14px vertical, 24–32px horizontal
Font:         15px, weight 500
```

If you use pills, use them only for primary global CTAs. Mixing pill + 8px-radius buttons reads as inconsistent.

### Status badge / pill

```
Padding:      4px 10px
Radius:       9999px (or 4px for "tag" style)
Font:         12–13px, weight 500
Border:       1px hairline
Bg:           tint of state color at ~10% alpha on dark, ~6% on light
Text:         state color full strength
```

Tailwind/JSX:

```jsx
<span className="inline-flex items-center rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-600 dark:text-emerald-400">
  Active
</span>
```

E.g. "Active" badge: green text, green-tinted background, green-tinted border.

### Code block with title bar

```
[ filename.ts                                  📋 ]    ← 36px title bar
{                                                       ← code area
  "key": "value"
}
```

Title bar: mono filename, gray-11 color, 13px. Copy button on right, appears on hover. Code area: padded 20px, mono 13–14px, syntax-highlighted. Single 1px border around the whole thing.

### Code block with line highlighting

Lines marked with `// [!code highlight]` get a subtle background tint (6–10% accent color alpha) and a 2px left border in accent color. Other lines stay normal. Annotations (`// (1)`) become numbered markers that expand to tooltips.

### Tabs (synced)

The "pick npm vs pnpm" tab UX. Across the page, all tabs with the same group sync.

```
Tab bar:      36–40px tall, hairline border bottom
Inactive tab: gray-11 text, no background
Active tab:   gray-12 text, brand-accent or gray-12 bottom border (2px)
Hover:        gray-12 text, no background change
```

Persist active selection in localStorage by group name.

### Sidebar navigation (docs)

```
Width:           240–280px
Bg:              gray-1 or transparent (no separation from page)
Group label:     12–13px, weight 600, gray-11, uppercase OR title-case
Item:            14–15px, weight 400, gray-11 → gray-12 on hover
Active item:     gray-12 + brand accent left border (2px) OR gray-12 + gray-3 bg
Indent per level: 16px
Item height:     32–36px (compact)
Section gap:     20–24px
```

Critical: docs sidebars in this aesthetic are **dense**. 32–36px row height, 14–15px text, low contrast inactive states. Not "spacious" the way generic docs sites are.

### Search command (Cmd+K)

The slide-down command palette. Almost universal in this aesthetic.

```
Trigger button:  text-input look in topnav showing "Search... ⌘K"
Modal:           max-width 640px, vertically positioned ~20% from top
Input:           48–56px tall, no border (just bottom hairline)
Result row:      48px, icon + title + breadcrumb path on right (mono, gray-11)
Active row:      gray-3 background
Footer:          mono hints "↵ Open · ↑↓ Navigate · ⌘K Close"
```

Use Radix Command, kbar, or cmdk by pacocoursey.

### Keyboard shortcut display

```
Press <Kbd>⌘</Kbd>+<Kbd>K</Kbd> to open
```

Each `<Kbd>`:
```
Padding:    2px 6px
Font:       11–12px mono, weight 500
Bg:         gray-2
Border:     1px hairline
Border-bot: 2px hairline (subtle "physical key" look — optional)
Radius:     4px
```

### Toast / inline notification

```
Bg:           page bg + 1 step elevation
Border:       1px hairline (or accent-tinted for state)
Padding:      12–16px
Icon:         left, 16–20px Lucide
Text:         14–15px
Dismiss:      top-right, ghost button
Radius:       8px
Width:        max 380px
Position:     bottom-right, 24px from edge
```

Critical: no large drop shadow. Border-only elevation, possibly with a tiny `0 1px 2px` shadow if absolutely necessary.

---

## Marketing Page Patterns

### Logo grid (social proof)

A row or grid of customer logos in monochrome.

```
Layout:        3–6 columns desktop, 2 columns mobile
Logo treatment: grayscale, 60–70% opacity, width 80–120px
Hover:         opacity → 100%, transition 200ms
Background:    sometimes hairline border per cell
Section label: mono eyebrow above ("TRUSTED BY")
```

Don't use full-color logos here — the desaturation is part of the aesthetic.

### Pricing card

```
3–4 cards in a row, equal width, hairline borders
Featured plan: brand-accent border (1px) instead of neutral, OR slightly elevated bg
Plan name:     14–15px, weight 600, mono optional
Price:         48–56px, weight 600, -0.02em
Period:        14px gray-11 next to price
Features:      14–15px list with check/X icons (Lucide)
CTA:           full-width button in card
```

Don't add background gradients to pricing cards. Don't use bright color-block tiers. Differentiation is via the accent border on the recommended plan, nothing more.

### Feature grid

```
2–3 columns
Each cell:
  Icon (24–32px Lucide, brand accent)
  Headline (18–20px, weight 600)
  Description (15–16px, gray-11, 2–3 lines)
  Optional "Learn more" link (small, brand accent)
Hairline border between cells (or hairline-bordered cards)
Padding inside cell: 24–32px
```

### Testimonial

```
Quote text:       18–20px, weight 400, line-height 1.5
Author block:     avatar (32–40px) + name (14px weight 500) + role/co (13px gray-11)
Background:       transparent OR hairline-bordered card
Quote mark:       optional mono "—" before name, subtle
```

Avoid: large quote-mark glyphs, italic styling, color tints. Restrained quote treatment fits the aesthetic.

### Comparison table

```
Header row:       mono labels OR weight 600 sans
Cells:            14–15px, gray-12 (yes) / gray-11 (no/dash)
Check / X icons:  16px Lucide, in brand accent (yes) / gray-7 (no)
Borders:          horizontal hairlines only (no vertical)
Highlight column: brand-accent column header bg at ~5% alpha
Row hover:        gray-2 bg
```

### Footer

```
Bg:               same as page or 1 step darker (subtle)
Top border:       1px hairline
Padding:          64–96px vertical
Layout:           4–6 column grid
Column heading:   13–14px weight 600 OR mono uppercase
Column links:     14px gray-11 → gray-12 on hover, 12–14px row height
Bottom row:       small print + social icons + copyright, mono optional
```

### Changelog entry

```
Date:           mono 13–14px gray-11
Version:        mono "v1.2.3" small badge, brand-accent tinted
Headline:       20–24px weight 600
Body:           markdown, normal prose
Tags:           pills in semantic colors (feature/fix/breaking)
Separator:      hairline between entries, generous margin
```

---

## Page-Level Patterns

### Docs page layout (the Tangly use case)

```
Topnav:           60–64px, hairline bottom border, logo + tabs + search + theme
Sidebar:          240–280px, hairline right border (or no border)
Content:          max-width 760–860px, 32–48px horizontal padding
TOC right:        200–220px, sticky, hairline left border (or no border)
Footer:           "Last updated · Edit on GitHub" 13–14px gray-11
```

The whole page divides into roughly equal-width sidebar / content / TOC at large viewports. At medium, TOC collapses. At small, sidebar slides in from left.

### Blog post layout

```
Hero image:       optional, full-width, 16:9 ratio
Title block:      max-width 720px, centered
Eyebrow:          mono category label
Title:            48–56px weight 600 -0.03em
Meta:             author avatar + name + date + read time (mono)
Content:          max-width 720px (narrower than docs)
Body:             17px line-height 1.65, more generous than docs
Footer:           author bio card with hairline border
```

### Marketing landing page

Stack of sections, each section ~96–160px vertical padding. Sections alternate between page-bg and 1-step-darker bg for subtle rhythm.

Order (typical):
1. Hero (beam + headline + CTA + product screenshot)
2. Logo grid (social proof)
3. Feature grid or 3 feature highlights
4. Code/product showcase
5. Quote/testimonial
6. Pricing or "see all features" link
7. Final CTA
8. Footer

Each section uses the eyebrow + headline + lede pattern at the top. This rhythm is what makes the page read as "considered."

---

## Anti-component shortcuts

A useful trick when you want to add visual interest without breaking the aesthetic:

- Add a hairline border instead of a shadow.
- Add a gradient instead of an illustration.
- Add a mono label instead of a colored badge.
- Add a dot grid instead of a photo.
- Add a tighter letter-spacing instead of a heavier weight.
- Add a code snippet instead of a hero image.

Each of these substitutions keeps you in the aesthetic. The reverse — replacing borders with shadows, gradients with illustrations, mono with color, etc — pulls you out of it.
