---
name: animate-svg
description: Generate looping animated SVGs (CSS keyframes / SMIL) with Gemini Pro via OpenRouter. Use for self-contained animated vector graphics — motion graphics, hero animations, loaders, halftone/ASCII motion, animated icons, draw-on line diagrams.
allowed-tools: Bash, Read
---

# animate-svg

Generate one self-contained, infinitely-looping animated SVG from a text description.
Output is SVG markup (drop into HTML/JSX or save as `.svg`), not a raster image — for
raster use `generate-image`.

Routes to `google/gemini-3.1-pro-preview` over OpenRouter chat-completions; Gemini Pro
is unusually good at hand-authoring SVG geometry plus CSS `@keyframes` / SMIL motion.

## Requirements

- `OPENROUTER_API_KEY` — https://openrouter.ai/keys

## Command

```bash
./scripts/animate_svg "a web browser window rendering a page" -o browser.svg
```

Progress goes to stderr, the `.svg` to `--output`.

## Options

| Flag | Default | Notes |
|------|---------|-------|
| `-o, --output` | `animation.svg` | Output path |
| `-st, --style` | `halftone` | `halftone` (dot grid + shimmer), `ascii` (`.:-=+*#%@` glyph grid), `line` (`stroke-dashoffset` draw-on), `glyph` (one bold mark, micro-animation), or free text passed through |
| `-c, --colors` | `currentColor + accent` | e.g. `"green #4a7c3f, orange #c8743a"` |
| `-b, --bg` | `transparent` | A color, or `transparent`/`none` (no bg rect) |
| `--size` | `400x300` | viewBox `WxH`; no width/height attrs emitted (CSS sizes it) |
| `-m, --model` | `google/gemini-3.1-pro-preview` | Any OpenRouter model id |
| `-t, --max-tokens` | `40000` | Halftone/ascii grids are token-heavy — keep high |
| `--temp, --temperature` | `0.8` | |
| `-r, --reasoning` | `low` | `minimal\|low\|medium\|high` |
| `-x, --extra` | – | Extra instructions appended to the prompt |
| `-i, --input` | – | Existing `.svg` to refine/restyle |
| `--retries` | `2` | Re-asks if output isn't valid SVG |

## Gotchas

- Keep `--reasoning low` for halftone/ascii: high-effort thinking eats the token budget
  and truncates the SVG mid-element.
- Output is validated: one `<svg>` root with `xmlns` + `viewBox` and no width/height, no
  `<script>`/`<image>`/`<foreignObject>`/external URLs, parsed with defusedxml. A
  `@media (prefers-reduced-motion: reduce)` guard is baked into the prompt.
- Halftone/ascii output runs to hundreds of elements — expected, and still cheap because
  motion is transform/opacity only.
- For a family of graphics, hold `--colors`, `--bg`, `--size` and style constant and vary
  only the subject.
