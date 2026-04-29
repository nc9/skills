# Anti-patterns

Things that immediately break the Geist aesthetic. Run through this list before declaring a design done. If any of these are present, the result will read as "generic SaaS" or "early-2010s flat" rather than "modern dev tool."

These are sorted roughly by severity — top entries are the most damaging.

---

## Severe (kills the aesthetic instantly)

### Drop shadows on cards

The single most common giveaway. Material-style `box-shadow: 0 4px 16px rgba(0,0,0,0.1)` (or larger) is wrong. Cards in this aesthetic are bordered, not shadowed. Replace with the hairline approach in [tokens.md § Borders](tokens.md#borders) and [§ Shadows](tokens.md#shadows).

### Pure black text on pure white background

`#000000` on `#ffffff` reads heavy and amateur. Use `gray-12` (around `#202020`) on `gray-1` (around `#fcfcfc` or `#fafafa`) — see [tokens.md § Color](tokens.md#color). Vercel uses pure black/white but they have the typography precision to make it work; treat it as an exception, not the default.

### Multiple bright accent colors

One accent color, used sparingly. Two or more accents — "blue for primary, green for success, orange for warning, all visible at once on the same screen" — is the SaaS default and the wrong family. Semantic colors exist (success/warning/danger) but they're tints inside callouts, not first-class brand colors competing on the page. See [tokens.md § Brand accent](tokens.md#brand-accent) and [§ Semantic colors](tokens.md#semantic-colors).

### Accent color used as section background

Big rectangles of brand color ("our hero is a blue rectangle") signal "early 2020s SaaS template." Brand color is for: links, primary CTAs, focus rings, status dots, small icons. Never for backgrounds of substantial UI areas. See [tokens.md § Brand accent](tokens.md#brand-accent).

### Generic stock photography

People in offices smiling at laptops, abstract handshakes, "diverse team collaborating" stock images. Replace with: code snippets, terminal screenshots, product UI screenshots, abstract gradients, dot grids. If you must use a photo, it should be of a real product — yours.

### Decorative illustrations

Mailchimp/Intercom-style flat illustrations of cartoon characters operating tiny products. Different aesthetic family. Use a code snippet or a dashboard screenshot instead.

### Bold weight (700+) for body text or most headlines

Weight restraint is a signature. Most of the system runs on 400 (regular) and 600 (semibold). 700+ feels heavy and breaks the aesthetic. Display sizes are sometimes 700 but only at very large sizes where the negative letter-spacing carries the visual weight. See [tokens.md § Critical typographic rules](tokens.md#critical-typographic-rules).

### Default letter-spacing on display headlines

A 64px headline with `letter-spacing: 0` (the browser default) looks generic. Always use negative letter-spacing on display sizes: -0.02em minimum, -0.04em at 60px+. This single change is responsible for ~30% of the "designed" feel of these brands. See [tokens.md § Type scale](tokens.md#type-scale).

### High line-height on headlines

`line-height: 1.5` on a 56px headline = generic. Tighten to 1.05–1.15 on display sizes. The text should feel condensed, not airy. See [tokens.md § Type scale](tokens.md#type-scale).

---

## Major (significantly weakens the aesthetic)

### Pixelated or low-quality screenshots

Product UI screenshots should be retina-resolution at minimum. Compressed JPGs, small PNGs scaled up, or Loom-style screen recordings with watermarks read as low-effort.

### Inconsistent border-radius

8px buttons next to 16px cards next to 24px modals next to 4px inputs. Pick one scale and stick to it. The most common correct scale: 6–8px buttons, 8–12px cards, 12–16px modals. See [tokens.md § Border radius](tokens.md#border-radius).

### Border-radius too large

20px+ radius on cards reads as friendly/consumer (Notion, Calm, Headspace family) rather than dev-tool. Cap card radius around 12px. Pills (9999px) are fine for primary CTAs only. See [tokens.md § Border radius](tokens.md#border-radius).

### Buttons that scale on hover

`hover:scale-105` is friendly but wrong family. Hover changes are: opacity, border tint, background tint, color. No size changes. No bounce.

### Overly long animations

Page transitions 400ms+, hover effects 300ms+, "spring physics with bounce" — all wrong. 150–250ms ease-out, no overshoot, small translations only. See [tokens.md § Motion](tokens.md#motion).

### Default Material Design components

Material's default look (especially the elevated buttons with their drop shadows, and the FAB) is from a different family. shadcn/ui, Radix, Geist UI, HeroUI all align with this aesthetic; Material UI does not without significant overrides.

### Comic Sans / Papyrus / Lobster / similar display fonts

Obvious. But also: Roboto, Open Sans, Lato, Montserrat — these read as "default Google Fonts" and feel generic. Use Geist Sans, Inter, Söhne, GT America, or similar.

### Code blocks with light syntax theme on dark page (or vice versa)

Code block surface should be at most 1 step different from the page background. Light code on dark page (or vice versa) creates a jarring contrast island that breaks visual flow.

### Code blocks without filename / language indicator

Naked `<pre><code>` blocks are functional but read as "low-effort docs." Add a title bar with filename + copy button. This is table stakes for the aesthetic.

### Sidebar items too tall or too low-contrast

Docs sidebars in this aesthetic are dense (32–36px row height, 14–15px text). 48px+ rows with 16px text reads as "generic docs SaaS." 14px text with `text-gray-400` (way too low contrast) reads as "unfinished." Active state should be clearly visible.

### Generic "card with icon, title, description" features

Three columns of cards with rounded icon backgrounds, big titles, gray descriptions, with no visual restraint or rhythm — looks like every Bootstrap landing page. Differentiate via: hairline borders, mono labels, dense typography, tasteful spacing rhythm.

---

## Subtle (still wrong, but less obvious)

### Saturated, vibrant colors

Even when using brand color, prefer slightly desaturated values. Linear's brand blue is "subtle desaturated blue" — that's deliberate. Bright `#0066ff` reads brighter than the family.

### Default Google Fonts loading

`<link href="https://fonts.googleapis.com/css2?family=Roboto">` is a tell. These brands self-host or use system fonts. If you need Inter or Geist, self-host them or use the official npm packages.

### Three font families on one page

Sans for body + sans for headings + mono for code is the maximum. Adding a serif for "elegance" or a script font for "personality" pulls you out of the family.

### Gradient text on headlines

`background-clip: text` rainbow gradients on big headlines were a mid-2020s trend that aged badly. The Geist family rarely uses gradient text; when it does, it's a single subtle gradient (e.g. white to gray-11) for emphasis on one or two words, not the whole headline.

### Glassmorphism

`backdrop-filter: blur(20px)` with semi-transparent panels was an Apple-Vercel-Linear-overlap moment in 2021–2022. Since then it's mostly retreated. Used sparingly for navbars over scrolled content (Vercel still does this) but not for cards or modals.

### Hard-coded margins instead of consistent spacing scale

24px here, 27px there, 31px somewhere else. Stick to the spacing scale (8/12/16/24/32/48/64/96/128/160). Inconsistent spacing is one of the things the eye registers as "amateur" without knowing why. See [tokens.md § Spacing](tokens.md#spacing).

### Big page borders or cards-within-page-borders

A 1280px content area with a 1px border around the entire viewport reads as "wrapped in a card" and is wrong. Page is the canvas; cards are within it.

### Small numbers in default sans font for code

Ports, version numbers, prices, counts — these read better in mono. Defaulting to body sans for "v1.2.3" or "$49/mo" misses a chance to apply the mono-as-UI-font signature.

### Decorative dividers

Thick horizontal rules, dotted dividers, dividers with star-icon centers ("✦"), gradient dividers. Pure-grayed 1px dividers only. Or just use spacing.

### Avatars with colored ring borders

Status rings around avatars in bright colors. Better: small status dot adjacent to the avatar, hairline avatar border.

### Pluralized icon buttons in navbars

Github + Twitter + LinkedIn + YouTube + Slack + Discord all crammed into the topnav as a bar of icon buttons. Pick 1–2 most relevant. Move the rest to the footer.

### Footer with a large signup form

Big "subscribe to our newsletter" CTAs in footers feel marketing-heavy. The aesthetic prefers a small inline signup or just a link to a signup page.

### Cookies banner that takes up half the screen

Most of these brands have a small dismissible bar at the bottom or a tasteful corner toast. Avoid the "modal that blocks the page" pattern.

### Loading spinners with brand color

Spinners are 99% gray in this aesthetic. Adding brand color to a spinner makes it feel like every loading state is a "look at our brand!" moment.

### Status indicators with text labels duplicating the color

"🟢 Active" with green dot and green text saying "Active" is redundant. Either the dot or the text, not both with the color repeated.

### Buttons with icons AND chevrons AND arrows

"Get started →" is fine. "📦 Get started →↗" is overdoing it. One affordance per button.

---

## Easy fixes when you've gone wrong

If a design feels "off" but you can't pinpoint why, run through this checklist:

1. Replace shadows with hairline borders.
2. Bump body text to 15–17px.
3. Add `letter-spacing: -0.02em` (or tighter) to all headlines.
4. Tighten line-height on headlines to 1.1.
5. Reduce border-radius if it's >12px on cards.
6. Remove any second accent color.
7. Add a mono eyebrow label above each section headline.
8. Replace stock photos with code snippets or product UI.
9. Reduce hover transform amplitude (no scale, just opacity).
10. Change background from pure white/black to gray-1 / gray-12.

Eight of these ten rarely fail to improve the result.
