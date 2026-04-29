# Tokens

Concrete value ranges for the Geist aesthetic. When in doubt, reach for these. Specific brand variations follow each section.

**Sections**: [Color](#color) · [Typography](#typography) · [Spacing](#spacing) · [Borders](#borders) · [Shadows](#shadows) · [Gradients](#gradients) · [Motion](#motion) · [Iconography](#iconography) · [Code blocks](#code-blocks-a-critical-surface-for-this-aesthetic) · [Imagery](#imagery-and-decoration) · [Component refs](#component-level-token-references)

---

## Color

### Grayscale (does 90% of the work)

Use a 12-step neutral ramp. Both Radix `gray` and Tailwind `neutral`/`zinc` work. The system has 12 steps because you need granular contrast control: backgrounds, surfaces, hovers, borders, subtle text, primary text, all need their own step.

**Light mode reference values** (Radix gray, P3 → sRGB):

```
gray-1   #fcfcfc   App background
gray-2   #f9f9f9   Subtle background (alternating sections, sidebar)
gray-3   #f0f0f0   UI element background (button hover)
gray-4   #e8e8e8   Hovered UI element background
gray-5   #e0e0e0   Active / Selected UI element background
gray-6   #d9d9d9   Subtle borders and separators
gray-7   #cecece   UI element borders and focus rings
gray-8   #bbbbbb   Hovered UI element borders
gray-9   #8d8d8d   Solid backgrounds (rare, only for very specific states)
gray-10  #838383   Hovered solid backgrounds
gray-11  #646464   Low-contrast text
gray-12  #202020   High-contrast text
```

**Dark mode**: Radix `grayDark` provides equivalents. Backgrounds run `#0a0a0a → #1a1a1a → #2a2a2a` rough range, text inverts.

**Critical rule**: text is almost never pure `#000` on `#fff`. Use `gray-12` on `gray-1`. Pure black text feels heavy and wrong in this aesthetic. Vercel does use pure black/white in some places, but they're the exception that proves the rule — they have the typography precision to pull it off.

### Background

Light: `#fafafa` is a very common page background. Pure `#ffffff` works but feels colder. Vercel uses pure white; Linear uses warm grays.

Dark: `#0a0a0a` (almost-black) is the standard. Pure `#000000` is Vercel-specific. Supabase: `#171717`. Linear's dark theme runs warmer.

### Surface elevation

Build elevation through **borders, not shadows**. A "raised" card on dark background:
- Background: `#0a0a0a` (page)
- Card surface: `#0f0f0f` or `#111111` (slight lift)
- Card border: `rgba(255, 255, 255, 0.08)` (1px hairline)

On dark, the border carries the entire elevation signal. This is the single most distinctive thing about the aesthetic — and the thing most clones get wrong.

### Brand accent

Pick exactly one. Common choices and their owners (rough):
- **Black/White only** — Vercel, Cursor (austerity)
- **Indigo / Purple** — Stripe (#635bff), Linear (desaturated blue), Superhuman
- **Emerald** — Supabase (#3ecf8e)
- **Cyan / Teal** — Modal, Liveblocks
- **Orange / Red** — Raycast, Resend
- **Yellow** — ClickHouse

Use the accent for: links, primary CTA backgrounds, focus rings, status indicators (online dot, pending), and small icon highlights. **Do not** use it as a section background. **Do not** use it in body text. **Do not** add a second accent — secondary actions are gray, not blue.

### Semantic colors

Keep restrained — typically one shade per state, not a ramp:
```
success: #16a34a or #00c573 (Supabase green works)
warning: #ea580c or #f97316
danger:  #dc2626 or #ef4444
info:    matches brand accent
```

Use only in callouts, badges, and toasts. Not in marketing.

---

## Typography

### Font families

**Sans-serif (primary)**:
- Geist Sans — Vercel's typeface, designed for this aesthetic. Free.
- Inter — the universal default. Use Inter Variable. Linear uses this.
- Söhne — Stripe and others. Premium license.
- Circular — Supabase. Premium license.
- GT America — common in higher-end brands.

When in doubt, **Geist Sans** or **Inter Variable**. Both are free, well-supported, and instantly readable as part of this family.

**Monospace**:
- Geist Mono — pairs with Geist Sans, free.
- JetBrains Mono — universal default for code.
- Berkeley Mono — premium, used by Linear.
- IBM Plex Mono — open source, slightly distinct character.
- Source Code Pro — common, slightly older feel.

Mono is used **as a UI font**, not just for code. Eyebrow labels, version numbers, paths, status text. This is a key signature of the aesthetic.

### Type scale

```
Display XL    72–90px / 1.05 / -0.04em / 700   (hero headlines, used sparingly)
Display L     56–64px / 1.10 / -0.035em / 700  (section headlines)
Display M     40–48px / 1.15 / -0.03em / 600   (subsection / page titles)
Heading L     30–32px / 1.25 / -0.02em / 600
Heading M     24px    / 1.30 / -0.015em / 600
Heading S     18–20px / 1.40 / -0.01em / 600
Body L        17px    / 1.55 / 0 / 400          (long-form prose)
Body M        15–16px / 1.55 / 0 / 400          (default)
Body S        13–14px / 1.50 / 0 / 400          (secondary, captions)
Mono Label    12–13px / 1.40 / 0.05em / 500     (uppercase eyebrows)
Mono UI       13–14px / 1.40 / 0 / 400          (versions, paths, code inline)
```

Format: `font-size / line-height-multiplier / letter-spacing / weight`

### Critical typographic rules

- **Negative letter-spacing on display sizes is non-negotiable.** Without it, headlines look generic. -0.02em minimum, -0.04em on the largest sizes. Inter Variable supports this; Geist is designed for it.
- **Line-height tightens at large sizes.** 1.05–1.15 on display, 1.4–1.6 on body. Mintlify-style "looks generic" output usually has 1.5+ line-height on headlines, which kills the look.
- **Weight restraint.** Most of the system runs on 400 (regular) and 600 (semibold). Skip 500 unless it's nav/buttons. Skip 700 (bold) unless headlines need it. Supabase famously uses **only 400 and 500 across the entire site** — hierarchy comes from size, not weight.
- **Body text is bigger than you think.** 16px is the floor for marketing. 15px for dense UI. Below 14px is for labels only. Big body text reads as "considered."
- **Eyebrow labels are mono and uppercase.** 12–13px Mono, uppercase, letter-spacing 0.05–0.1em, gray-11 color, used above section headlines:
  ```
  PLATFORM
  Build the next generation of apps
  ```
  This single pattern anchors a page as "modern dev tool" instantly.

---

## Spacing

Strict 4px base, but the practical scale is 8-aligned for most things:

```
0    — 0
1    — 4px     hairline gaps, icon-text gap
2    — 8px     base unit
3    — 12px    tight component gap
4    — 16px    default component padding, paragraph margin
5    — 20px    
6    — 24px    card padding (small), gap between paragraphs
8    — 32px    card padding (default), section header to content
10   — 40px
12   — 48px    sub-section gap
16   — 64px    sub-section gap (large)
20   — 80px
24   — 96px    section gap (small marketing)
32   — 128px   section gap (default marketing)
40   — 160px   section gap (large hero areas)
```

### Spacing rhythm rules

- **Marketing has dramatic vertical rhythm.** 96–160px between major sections.
- **Components have tight rhythm.** 16–24px gaps within a card; 24–32px padding inside it.
- **The ratio matters.** Section spacing should be roughly 4–6x component spacing. Get this ratio wrong and the page feels cramped or spread-out regardless of absolute values.
- **Horizontal rhythm**: gutters scale with viewport. Mobile 16–24px, tablet 32–48px, desktop 64–96px. Max content width 1280–1440px for marketing, 720–800px for prose.

---

## Borders

```
Width:        1px (always — never 2px+)
Light color:  rgba(0, 0, 0, 0.08)   or   gray-6 (#d9d9d9)
Dark color:   rgba(255, 255, 255, 0.10)   or  #2a2a2a flat
Hover state:  bump alpha to 0.14 / 0.16
Focus ring:   2px outline in brand accent at 50% alpha, offset 2px
```

### Border radius

```
Buttons:        6–8px
Inputs:         6–8px
Cards:          8–12px
Code blocks:    8–12px
Modal:          12–16px
Pills (CTAs):   9999px — reserved for primary CTAs and tabs
Sharp edges:    0–2px — Vercel marketing pages, gives a more "engineered" look
```

**Pick one radius scale and stick to it.** Mixing 8px buttons with 16px cards on the same page reads as inconsistent.

---

## Shadows

The aesthetic mostly **does not use shadows**. Depth comes from borders + surface color.

When you do use a shadow:
```
Subtle:   0 1px 2px rgba(0, 0, 0, 0.04)
Standard: 0 4px 12px rgba(0, 0, 0, 0.08)
Modal:    0 16px 40px rgba(0, 0, 0, 0.12)
```

These are an order of magnitude smaller and softer than typical Material-style shadows. If your shadow is the first thing you notice, it's wrong.

---

## Gradients

Used **purposefully and sparingly**. Common motifs in `patterns.md`:
- **Beam / spotlight** (Vercel hero) — radial, single color, low opacity, behind content.
- **Aurora** — slow conic-gradient animation around a card or button.
- **Brand wash** — soft linear gradient between two close hues, used as background texture.
- **Border gradient** — gradient applied to a 1px border, fades from accent to neutral.

What gradients should NOT do: be the dominant element of a section. They're texture, not focus.

---

## Motion

```
Duration:    150ms (micro), 200ms (standard), 250–300ms (page-level)
Easing:      cubic-bezier(0.16, 1, 0.3, 1)   (ease-out-expo) — preferred
             cubic-bezier(0.4, 0, 0.2, 1)    (Material ease-in-out) — acceptable
Hover:       opacity, color, border tint changes — NOT scale-up
Enter/exit:  fade + translate 2–4px (not 8–16px)
```

Bouncy spring physics: don't. Big scale transforms: don't. Page transitions: usually subtle fade or just instant. The aesthetic reads as "considered restraint" — fast, small, deliberate motion supports that. Big motion fights it.

---

## Iconography

- **Lucide** is the default in this aesthetic. Stroke-based, 1.5–2px stroke width, 16px or 20px size.
- **Phosphor Icons** also fits.
- **Heroicons** (outline) is fine but slightly more generic.
- Avoid: Font Awesome (too round/old), Material Icons (different family), filled icons with bright colors.

Icon stroke should match text weight visually. Don't mix stroke widths within a UI.

---

## Code blocks (a critical surface for this aesthetic)

These brands compete on code blocks. Defaults that match:

- Background: `#0a0a0a` (dark) or `#fafafa` (light) — slightly off page background
- Border: 1px hairline, same as cards
- Padding: 20–24px
- Font: Geist Mono / JetBrains Mono / Berkeley Mono, 13–14px, line-height 1.6
- Syntax theme: GitHub Light / GitHub Dark, Vesper, or One Dark Pro
- Title bar: 36–40px tall with filename in mono, slightly muted
- Copy button: top-right, appears on hover, 24×24px
- Line highlighting: subtle background tint at 6–10% opacity
- No drop shadow on the code block itself

Do not use VS Code default or "atom one" themes — they read as old. Recent Shiki themes (Vesper, Catppuccin, GitHub Dark Default) match the aesthetic better.

---

## Imagery and decoration

What works:
- Code snippets with syntax highlighting (the canonical hero asset)
- Terminal screenshots with realistic prompts
- Product UI screenshots, especially showing dashboards
- Abstract gradient blobs (low saturation)
- Dot grids and lattice backgrounds (5–10% opacity)
- Generated noise textures at very low opacity
- Subtle aurora animations behind text

What doesn't work in this aesthetic:
- Stock photography of people in offices
- Illustrated mascots or characters
- Bright color-block sections
- 3D shapes/objects unless they're abstract gradient spheres (Stripe-style)
- Decorative icons in body content
- Heavy drop shadows on anything

---

## Component-level token references

If using shadcn/ui, the defaults align well. Don't override radius, border, or color system unless you know what you're doing. Theme via the brand accent only.

If using Geist UI, you're already in the aesthetic — defaults are correct.

If using Tailwind from scratch:
```js
// tailwind.config.js — minimal additions
extend: {
  fontFamily: {
    sans: ['Geist Sans', 'Inter', 'system-ui', 'sans-serif'],
    mono: ['Geist Mono', 'JetBrains Mono', 'monospace'],
  },
  letterSpacing: {
    tighter: '-0.04em',
    tight: '-0.02em',
  },
  // ... use Tailwind defaults for colors (neutral/zinc) and spacing
}
```

Resist the urge to expand the config. The aesthetic comes from restraint, not customization.
