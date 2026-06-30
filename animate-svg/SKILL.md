---
name: animate-svg
description: Generate looping ANIMATED SVGs (and SVG animations) with Google Gemini Pro via OpenRouter. Use when you need a self-contained animated vector graphic — feature-card motion graphics, hero animations, loaders/spinners, halftone/dot-matrix or ASCII-art motion, animated icons, draw-on line diagrams. Gemini Pro is specifically strong at hand-writing SVG + CSS/SMIL motion. For raster images use generate-image instead; for static technical diagrams use scientific-schematics.
---

# animate-svg

Generate a single, self-contained, infinitely-looping **animated SVG** from a text
description. The output is SVG markup (text you can drop straight into HTML/JSX or save
as a `.svg`), not a raster image.

It routes to **Google Gemini Pro** (`google/gemini-3.1-pro-preview`) over OpenRouter
chat-completions. Gemini Pro is unusually good at authoring SVG geometry plus CSS
`@keyframes` / SMIL motion, which is exactly what this skill needs.

## When to use

- Feature-card / section motion graphics (e.g. one per product feature)
- Halftone / dithered dot-matrix animations (à la Fumadocs) and ASCII/textmode art (à la box.ascii.dev)
- Animated icons, loaders, spinners, progress shimmers
- Draw-on line/blueprint diagrams
- Restyling/refining an existing SVG with `--input`

**Not** for: raster/photographic output → use `generate-image`. Static schematic
diagrams → use `scientific-schematics`.

## Quick start

```bash
scripts/animate_svg "a web browser window rendering a page"
# → animation.svg in the current dir (halftone style, transparent bg)
```

The script prints progress to stderr and writes the `.svg` to `--output`.

## API key

Needs `OPENROUTER_API_KEY` (set in `.env`, exported, or sourced from `~/.secrets`).
Get one at https://openrouter.ai/keys. The script exits with a clear message if it's missing.

## Styles (`--style` / `-st`)

| Style | Look |
|-------|------|
| `halftone` *(default)* | Grid of dots; dot size/opacity encodes the shape; shimmer wave. Newspaper-halftone / Bayer-dither feel. |
| `ascii` | Monospace glyph grid using the `.:-=+*#%@` density ramp; types-in / shimmers. Terminal feel. |
| `line` | Thin clean strokes with `stroke-dashoffset` draw-on. Blueprint / box-drawing. |
| `glyph` | One bold pictographic mark with a single tasteful looping micro-animation. |
| *free text* | Any other string is passed through as the style description. |

## Options

| Flag | Default | Notes |
|------|---------|-------|
| `--output` `-o` | `animation.svg` | Output path |
| `--style` `-st` | `halftone` | See table above |
| `--colors` `-c` | `currentColor + accent` | Palette, e.g. `"green #4a7c3f, orange #c8743a"` |
| `--bg` `-b` | `transparent` | A color, or `transparent`/`none` (no bg rect) |
| `--size` | `400x300` | viewBox `WxH`. No width/height attrs are emitted (CSS sizes it) |
| `--model` `-m` | `google/gemini-3.1-pro-preview` | Any OpenRouter model id |
| `--max-tokens` `-t` | `40000` | Halftone/ascii grids are token-heavy — keep this high |
| `--temperature` `--temp` | `0.8` | Creativity |
| `--reasoning` `-r` | `low` | `minimal\|low\|medium\|high`. Keep **low** for halftone/ascii — high-effort thinking eats the token budget and truncates the SVG |
| `--extra` `-x` | – | Extra instructions appended to the prompt |
| `--input` `-i` | – | Existing `.svg` to refine/restyle |
| `--retries` | `2` | Re-asks if the output isn't valid SVG |

## Guarantees baked into the prompt + validation

- Exactly one `<svg>` root with `xmlns` + explicit `viewBox`, **no** width/height (CSS-sized).
- All motion is in-SVG (CSS `@keyframes` or SMIL), seamless infinite loop.
- Self-contained: no `<script>`, `<image>`, `<foreignObject>`, external fonts/URLs.
- A `@media (prefers-reduced-motion: reduce)` guard disables animation for opt-out users.
- Output is fence-stripped, must start `<svg>`/end `</svg>`, and is parsed with
  **defusedxml** (XXE / billion-laughs safe); `<script>` is rejected.

## Examples

```bash
# Brand-tinted halftone feature graphic, transparent so it sits on a card
scripts/animate_svg "concentric radar sweep scanning a globe" \
  -st halftone -c "muted green #4a7c3f, soft orange #c8743a" -b transparent \
  --size 360x240 -o radar.svg

# ASCII-art terminal motion
scripts/animate_svg "a stack of servers booting up" -st ascii -o servers.svg

# Draw-on line diagram
scripts/animate_svg "data flowing through a pipeline of 3 boxes" -st line -o pipeline.svg

# Refine a previous result
scripts/animate_svg "make the shimmer slower and add more dots at the edges" \
  -i radar.svg -o radar-v2.svg
```

## Tips

- Halftone/ascii output can be large (hundreds of elements). That's expected; it stays
  performant because animation is transform/opacity only.
- For a set of graphics that must feel like a family, reuse the same `--colors`, `--bg`,
  `--size`, and style, and vary only the subject.
- Preview by opening the `.svg` in a browser (it animates on its own).
