---
name: generate-image
description: Generate or edit raster images with OpenAI gpt-image-2.5 (default, via the OpenAI SDK) or Google Gemini 3.1 Flash Image (via OpenRouter). Use for photos, illustrations, artwork, logos, icons, mascots, and edits to existing images.
allowed-tools: Bash, Read
---

# Generate Image

```bash
./scripts/generate_image "A red fox in autumn forest" -o fox.png
./scripts/generate_image "Make the sky purple" -i photo.jpg -o edited.png
```

## Requirements

Routing picks the key automatically; only the one for the chosen model is needed.

- `OPENAI_API_KEY` — for `gpt-image-*` (default route, OpenAI Images API via the OpenAI SDK, **not** OpenRouter)
- `OPENROUTER_API_KEY` — for `google/gemini-*` (OpenRouter chat-completions)

## Models

| | `gpt-image-2.5-sunburst` (default) | `google/gemini-3.1-flash-image` |
|---|---|---|
| **Fresh** flat-vector app icons | ⚠️ raster shimmer, wobbly geometry, jaggies on downscale | ✅ best — `--size 2K -r high` |
| **Edit** existing icon (layout preserved, color swap, light/dark) | ✅ best — adheres rigidly to the reference | ✅ good |
| Wordmark logos / brand text | ✅ best, correct brand colors | ⚠️ drifts on brand colors |
| Illustrated character / mascot consistency | ⚠️ drops accent colors | ✅ best — pass the reference via `-i` |
| Fresh editorial illustration | ✅ richer | ⚠️ sparser |
| Extended aspects (21:9, 4:1, 1:4, 8:1, 1:8) | ⚠️ `-a` maps to nearest portrait/landscape; exact via `--size WxH` within 1:3–3:1 | ✅ honoured exactly |
| Resolution | ✅ `--size WxH`, multiples of 16, ≤3840/edge | ✅ `--size 0.5K/1K/2K/4K` |
| Quality tiers | ✅ `-q auto\|low\|medium\|high\|xhigh\|max` | ❌ |
| Output format | ✅ `--format png\|jpeg\|webp` | ❌ PNG only |
| `-r/--reasoning` effort | ❌ | ✅ `minimal`/`high` |
| Seed / temperature | ❌ | ✅ |
| True alpha channel | ❌ | ❌ renders opaque |
| Input image for editing | ✅ PNG/JPG/GIF/WebP | ✅ same |

`gpt-image-2.5-flare` is the cheaper/faster OpenAI sibling; same flags.

### Routing

```
Fresh flat-vector icon, crisp edges?        → Gemini + --size 2K -r high
Wordmark / brand-color logo?                → default
Edit preserving existing layout/colors?     → default
  …illustrated character w/ accent colors   → Gemini + -i ref
Exact extended aspect (4:1, 8:1, 1:8)?      → Gemini + -a
>3840px on an edge?                         → Gemini + --size 4K
webp / jpeg output, or quality tier?        → default + --format / -q
True transparent PNG?                       → chroma bg → remove-background
```

## Options

| Flag | Applies to | Notes |
|------|-----------|-------|
| `prompt` (positional) | both | Description, or editing instruction with `-i` |
| `-i, --input` | both | Reference/source image (enables edit mode) |
| `-o, --output` | both | Default `generated_image.png` |
| `-m, --model` | both | Default `gpt-image-2.5-sunburst` |
| `-a, --aspect-ratio` | both | `1:1 16:9 9:16 4:3 3:4 3:2 2:3 4:5 5:4 21:9 1:4 4:1 1:8 8:1` |
| `--size` | both | gpt-image: `WxH` or `auto`. Gemini: `0.5K/1K/2K/4K` (ignored on gpt-image) |
| `-q, --quality` | gpt-image | `auto low medium high xhigh max` |
| `--format` | gpt-image | `png` (default), `jpeg`, `webp` |
| `-t, --max-tokens` | Gemini | Default 1024 |
| `-s, --seed`, `--temp` | Gemini | Reproducibility / creativity |
| `-r, --reasoning` | Gemini | `minimal`, `high` |
| `--api-key` | both | Overrides the auto-picked key |

The output file extension does **not** set the format — `--format` does (gpt-image only);
Gemini always returns PNG bytes regardless of the filename you give `-o`.

### Aspect → size mapping (gpt-image)

`-a` maps to discrete sizes: portrait ratios (`9:16 2:3 3:4 4:5 1:4 1:8`) → `1024x1536`,
landscape (`16:9 3:2 4:3 5:4 21:9 4:1 8:1`) → `1536x1024`, otherwise `1024x1024`. For an
exact ratio pass `--size WxH` instead (multiples of 16, 1:3–3:1, ≤3840/edge); anything
wider than 3:1 needs Gemini.

## Transparent backgrounds — chroma-key workflow

No route returns a real alpha channel (gpt-image rejects `background=transparent` at the
API level; Gemini renders opaque). Generate on a solid chroma color, then segment:

```bash
./scripts/generate_image "BrandName app icon on a solid magenta #FF00FF chroma-key background, no magenta anywhere in the icon itself, icon fills the frame" -o icon-chroma.png
../remove-background/scripts/remove_background icon-chroma.png -o icon.png --crop --padding 32
sips -g hasAlpha icon.png   # expect hasAlpha=yes
```

`remove-background` uses BiRefNet segmentation, not color keying, so any background works
— but a high-contrast non-brand chroma improves edge accuracy around thin strokes and
letterform counters. Name the hex in the prompt (models track hex better than color
names) and tell the model not to use it elsewhere.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Square output when you asked for wide | No `-a`/`--size` | Add `-a 16:9` or `--size 1536x1024` |
| Need wider than 3:1 | gpt-image caps at 1:3–3:1 | Gemini + `-a 4:1` / `8:1` |
| Icon edges wobble / look like a bad SVG | gpt-image drawing fresh vector | Gemini + `--size 2K -r high` |
| `Transparent background is not supported` | Asked gpt-image for alpha | Chroma-key workflow above |
| `Error: No image in response` (Gemini) | Reasoning returned text only | Retry without `-r high`, or simplify |
| Wordmark text came out the wrong color | Gemini misread the accent spec | Use the default gpt-image model |
| Mascot lost its accent colors | gpt-image on an illustrated ref | Gemini, list each accent color explicitly |
| Input rejected on format | Passed an SVG to `-i` | Rasterize: `qlmanage -t -s 1024 -o ./refs icon.svg` |
| `OPENAI_API_KEY not found` | Default model is OpenAI-routed | Set it, or `-m google/gemini-3.1-flash-image` |

## Prompting notes

- Pass hex codes for brand colors; enumerate what to preserve on an edit ("keep the
  rounded-square tile, the letterform, the corner badge position") and anchor with
  "exactly the reference but …".
- For character consistency pass the reference via `-i` on every call and list each
  accent color; prompt-only consistency drifts.
- Pair with `remove-background` for alpha.
