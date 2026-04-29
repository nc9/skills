---
name: geist-design
description: Apply the modern developer-tool design aesthetic — the visual language shared by Vercel, Linear, Stripe, Resend, Raycast, Supabase, and similar brands. Use when building marketing pages, dashboards, docs sites, landing pages, or polishing UI to feel "expensive" in the way these brands feel expensive. Common triggers — "make it look like Vercel/Linear", "modern dev tool look", "geist style", "linear style", "make it look polished/premium", or any UI work where the user is referencing this family of brands. Not for consumer-friendly aesthetics (Airbnb, Notion, Headspace), illustration-driven brands (Mailchimp, Slack), or playful/colorful brands (Figma, Miro).
allowed-tools: Read
---

# Geist Aesthetic

This skill captures the design language of modern developer-tool brands — Vercel, Linear, Stripe, Resend, Raycast, Cursor, Supabase, PlanetScale, Modal, Inngest, Liveblocks, Clerk, Neon, Trigger.dev. It's sometimes called "Geist style" (after Vercel's design system), "Linear style" (after Linear), "Refactoring UI aesthetic", or just "modern dev tool design." None of those names are stable. Use whichever the user uses.

The defining property: **the look is built from dozens of small, restrained choices, each individually subtle, that compound into the overall feel.** You can't nail it with one big move. You nail it by getting twenty small things right and resisting the urge to add anything decorative.

## Philosophy in five lines

1. **Aggressive reduction.** Fewer colors, fewer weights, fewer radii, fewer effects. What's removed matters more than what's added.
2. **Hairline borders do the structural work.** 1px low-contrast borders define cards and sections. Drop shadows are mostly absent.
3. **Typography is the visual signature.** Tight letter-spacing, bold display sizes, mono used as UI font, generous body text.
4. **Color is signal, not decoration.** Mostly grays. One accent, used for primary CTAs, links, and status — never as a section background.
5. **Spacing is rigid.** Strict 4px or 8px scale. Big rhythm between sections, tight rhythm within components.

## How to use this skill

Don't load all four supporting files by default — pick what the task needs:

- **Need a specific value** (color, type size, spacing, border, motion) → `tokens.md`
- **Building a hero, section, card, button, table** → `patterns.md` (named motifs with implementations)
- **Final review before declaring done** → `anti-patterns.md` (sorted by severity)
- **Picking a reference brand to match** → `examples.md`

When the user is working on a specific deliverable, prefer concrete patterns from `patterns.md` over inventing your own. Most "Geist-style" UI is composed from a small vocabulary of motifs.

Pair with the `web-ui` skill for interaction, accessibility, and performance — this skill covers visual language only.

## Quick rules (when in doubt)

- **Color**: start with a 12-step gray ramp (Radix `gray` or `slate`, or Tailwind `neutral`/`zinc`). Pick one accent color. Don't add a second.
- **Type**: Geist Sans or Inter for body and headings. Geist Mono, JetBrains Mono, or Berkeley Mono for code AND for small UI labels (eyebrows, version numbers, paths).
- **Headlines**: large (48–80px), bold (600–700), letter-spacing -0.02 to -0.04em, line-height 1.05–1.15.
- **Body**: 15–17px, line-height 1.5–1.65, color slightly softer than pure black/white (use gray-12 / gray-1, not #000 / #fff).
- **Borders**: 1px, color from gray ramp at low contrast (e.g. `rgba(0,0,0,0.08)` light, `rgba(255,255,255,0.10)` dark). Avoid drop shadows; if you must, make them tiny (1–2px blur).
- **Radius**: 6–8px for buttons, 8–12px for cards, 0–2px for marketing pages going extra-Vercel, 9999px (pill) reserved for primary CTAs only.
- **Spacing**: 4px base; 8/12/16/24/32/48/64/96/128/160 px scale. Section spacing 96–160px, card padding 24–32px, component gap 16–24px.
- **Motion**: 150–250ms ease-out. No bounce, no scale-up hover. Translate 2–4px and fade.
- **Imagery**: code snippets, terminals, dashboards, abstract gradients, dot grids. **Not** stock photos, **not** stock illustrations, **not** decorative icons.
- **Dark mode**: assume it. Many of these brands lead with dark. If you're light-only you're probably wrong.

## When NOT to use this skill

- The user is targeting a consumer / non-technical audience and the brand is warm/welcoming (Airbnb, Notion, Headspace, Calm).
- The product is illustration-driven (Mailchimp, Intercom of years past, Slack).
- The brand wants to feel playful/colorful (Figma, Miro, Trello).
- The user wants "fun" or "personality-forward" — this aesthetic is deliberately reserved.
- The product needs a dense data-grid look (Excel, Bloomberg, trading dashboards) — different family.

If the user references one of those reference brands instead, this skill is the wrong fit. Say so and recommend a different direction.

## Application checklist

When applying this skill, the deliverable should:
- Use specific token values from `tokens.md`, not vibes.
- Reference at least one named pattern from `patterns.md` if building a hero/section/card.
- Verify against `anti-patterns.md` before declaring done.
- If using Tailwind, prefer arbitrary values that match the token ranges (`text-[15px]`, `tracking-[-0.02em]`) over the closest preset when the preset is wrong.
- If using shadcn/ui, Radix, or Geist UI as a base, keep the defaults — they're already aligned. Don't override them with worse values.
