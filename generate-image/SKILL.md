---
name: generate-image
description: Generate or edit images using OpenAI gpt-image-2 (default) or Google Gemini 3.1 Flash via OpenRouter. Use for general-purpose image generation — photos, illustrations, artwork, logos, icons, mascots, concept art. For flowcharts, circuits, pathways, and technical diagrams, use the scientific-schematics skill instead.
---

# Generate Image

Generate and edit images via OpenRouter. Defaults to OpenAI `gpt-image-2` (strong instruction following, good for logos/icons/brand work). Gemini 3.1 Flash remains available via `--model`.

## When to Use This Skill

**Use generate-image for:**
- Photos and photorealistic images
- Artistic illustrations and artwork
- Concept art and visual concepts
- Visual assets for presentations or documents
- Image editing and modifications
- Any general-purpose image generation needs

**Use scientific-schematics instead for:**
- Flowcharts and process diagrams
- Circuit diagrams and electrical schematics
- Biological pathways and signaling cascades
- System architecture diagrams
- CONSORT diagrams and methodology flowcharts
- Any technical/schematic diagrams

## Quick Start

Use the `scripts/generate_image` script to generate or edit images:

```bash
# Generate a new image
scripts/generate_image "A beautiful sunset over mountains"

# Edit an existing image
scripts/generate_image "Make the sky purple" --input photo.jpg
```

This generates/edits an image and saves it as `generated_image.png` in the current directory.

## API Key Setup

The skill routes based on model and picks the right key automatically:

- **gpt-image-\*** → OpenAI SDK direct → needs `OPENAI_API_KEY` (get one at https://platform.openai.com/api-keys)
- **google/gemini-\*** → OpenRouter → needs `OPENROUTER_API_KEY` (get one at https://openrouter.ai/keys)

Either or both can be set in `.env`, exported in the shell, or sourced from `~/.secrets`. The script fails with a clear error if the required key is missing for the chosen model.

## Models

- **Default**: `gpt-image-2` (OpenAI) — called via the OpenAI SDK directly. Strong prompt adherence and text rendering. Wins on structured brand work: square icons, wordmark logos, exact-color preservation, color swaps, editorial illustrations with clear subject composition. Supports portrait/landscape sizes and quality tiers via the SDK.
- **Alternative**: `google/gemini-3.1-flash-image-preview` (Nano Banana 2) — called via OpenRouter. Wins on illustrated character/mascot consistency, extended aspect ratios (1:4, 4:1, 1:8, 8:1), and the `0.5K/1K/2K/4K` size tiers. Select with `-m google/gemini-3.1-flash-image-preview`.

### Capability matrix (empirically tested)

| Need | gpt-image-2 (default) | Gemini 3.1 Flash |
|---|---|---|
| Square app icons (preserve existing) | ✅ best | ✅ good |
| Wordmark logos / brand text rendering | ✅ best (correct colors) | ⚠️ drifts on brand colors |
| Edit existing logo/icon preserving layout | ✅ best | ✅ good |
| Color swap on brand mark (e.g. purple → teal) | ✅ clean | ✅ clean |
| Illustrated character / mascot consistency | ⚠️ loses accent colors | ✅ best — pass reference via `-i` |
| Fresh editorial illustration (subject scene) | ✅ richer, more complete | ⚠️ sparser |
| Portrait / landscape (`1024x1536`, `1536x1024`, `auto`) | ✅ via SDK (`--size` or `-a`) | ✅ via `-a` |
| Extended aspect ratios (21:9, 4:1, 1:4, 8:1, 1:8) | ⚠️ mapped to nearest landscape/portrait | ✅ exact aspect honoured |
| Hi-res beyond 1536px | ❌ max edge 1536 | ✅ `--size 2K/4K` |
| Quality tiers (`low`/`medium`/`high`/`auto`) | ✅ `--quality` | ❌ |
| Output format (`png`/`jpeg`/`webp`) | ✅ `--format` | ❌ PNG only |
| `--reasoning` effort for spatial prompts | ❌ | ✅ |
| True transparent PNG (alpha channel) | ❌ API-level rejected (`"Transparent background is not supported for this model"`) | ❌ renders opaque white |
| Input image editing (PNG/JPG/GIF/WebP) | ✅ | ✅ |
| Input SVG | ❌ rasterize first (`qlmanage -t -s 1024 -o dir file.svg`) | ❌ same |

### Routing decision tree

```
Square icon, app mark, wordmark logo?                   → gpt-image-2 (default)
Edit preserving existing layout/colors?                 → gpt-image-2 (default)
  Exception: illustrated character with accent colors   → Gemini + -i ref
Portrait or landscape subject?                          → gpt-image-2 + -a 9:16 / 16:9 (or --size)
Extended aspect (1:4, 4:1, 8:1, 1:8, 21:9 exact)?       → Gemini + -a
Need >1536px on an edge?                                → Gemini + --size 2K/4K
Need webp or jpeg output?                               → gpt-image-2 + --format webp / jpeg
Spatial/compositional reasoning?                        → Gemini + --reasoning high
True transparent PNG?                                   → Generate on chroma bg → remove-background
```

### How aspect/size is mapped for gpt-image-2

The OpenAI Images API uses discrete sizes (`1024x1024`, `1024x1536`, `1536x1024`, `auto`) rather than arbitrary aspect ratios. The skill accepts both and maps automatically:

- `-a 1:1` / portrait ratio (9:16, 2:3, 3:4, 4:5, 1:4, 1:8) → `1024x1536`
- `-a` landscape ratio (16:9, 3:2, 4:3, 5:4, 21:9, 4:1, 8:1) → `1536x1024`
- `--size 1024x1024 | 1024x1536 | 1536x1024 | auto` → passed through literally
- `--size 0.5K/1K/2K/4K` (Gemini tier) → ignored, defaults to `1024x1024`

For exact extended ratios (e.g. a 4:1 banner without letterboxing), use Gemini.

## Common Usage Patterns

### Basic generation
```bash
scripts/generate_image "Your prompt here"
```

### Custom output path
```bash
scripts/generate_image "Abstract art" --output artwork.png
```

### Aspect ratio (works on both models)
```bash
# gpt-image-2 default — portrait / landscape
scripts/generate_image "Tall poster of a tree" -a 9:16 -o tree.png
scripts/generate_image "Wide landscape painting" -a 16:9 -o landscape.png

# Gemini — extended aspect ratios (honoured exactly)
scripts/generate_image "Ultra-wide banner" -a 8:1 -m google/gemini-3.1-flash-image-preview
scripts/generate_image "Vertical poster" -a 1:4 -m google/gemini-3.1-flash-image-preview
```

### Explicit size (gpt-image-2 via SDK)
```bash
scripts/generate_image "Product photo" --size 1536x1024 -o product.png
scripts/generate_image "Portrait shot" --size 1024x1536 -o portrait.png
scripts/generate_image "Let the model choose" --size auto -o auto.png
```

### Quality tier / output format (gpt-image-2 only)
```bash
# Fast iterations
scripts/generate_image "Concept sketch" -q low -o sketch.png

# Final output
scripts/generate_image "Hero banner" -q high --size 1536x1024 -o hero.png

# WebP for smaller files
scripts/generate_image "Blog thumbnail" --format webp -o thumb.webp
```

### Hi-res (Gemini only)
```bash
scripts/generate_image "Detailed architectural shot" --size 4K -m google/gemini-3.1-flash-image-preview
```

### Select a model
```bash
# Default is gpt-image-2 (OpenAI SDK direct)
scripts/generate_image "Company logo" -o logo.png

# Switch to Gemini for extended aspect ratios, hi-res, or mascot work
scripts/generate_image "Ultra-wide banner" -m google/gemini-3.1-flash-image-preview -a 8:1
```

### Logos, icons, mascots (primary use cases)

```bash
# Square app icon — gpt-image-2 default is best here
scripts/generate_image "Flat minimalist fox mark, orange/white, 1024x1024 app icon" -o icon.png

# Icon variant: light-theme version from the dark source
scripts/generate_image "Light-theme variant of the reference icon: white bg, dark letterform, preserve corner badge exactly, keep rounded-square tile proportions" -i icon-dark.png -o icon-light.png

# Icon variant: color swap (preserve everything else)
scripts/generate_image "Exactly the reference icon but recolor the purple accent to teal (#14B8A6). Keep every other element identical: background, letterform, tile shape, corner badge position." -i icon.png -o icon-teal.png

# Wordmark logo with icon mark — gpt-image-2 respects brand colors
scripts/generate_image "Horizontal wordmark: reference icon on the left, 'BrandName' text to the right in bold sans-serif, dark charcoal type, purple accent, white background, generous padding" -i icon.png -o logo-wordmark.png

# Mascot / illustrated character variation — switch to Gemini for accent-color preservation
scripts/generate_image "Same fox character as reference, same proportions and art style, preserve all accent colors (green highlights, red collar), waving pose, white background" -i mascot/fox-1.png -o fox-waving.png -m google/gemini-3.1-flash-image-preview

# Wide wordmark (tight crop, no padding) — requires Gemini for aspect control
scripts/generate_image "'BrandName' wordmark in bold sans-serif, dark on white, purple underline accent, tightly cropped edge to edge" -o logo-wide.png -m google/gemini-3.1-flash-image-preview -a 4:1
```

### Transparent backgrounds — chroma-key workflow

**Neither model produces a true alpha channel via OpenRouter.** gpt-image-2 renders a baked-in checker pattern when asked for "transparent"; Gemini just renders opaque white. The reliable workflow is two-step: generate on a **solid chroma-key color** that doesn't appear in the subject, then segment with the `remove-background` skill.

Why a chroma color instead of plain white: `remove-background` uses BiRefNet AI segmentation (not color keying), so any bg works — but a **high-contrast non-brand color improves segmentation accuracy around thin edges** like text strokes and letterform holes (counters in P/O/B/R/A/D). Good chroma choices: magenta (#FF00FF), chroma-green (#00FF00), chroma-blue (#0000FF). Pick one that doesn't appear anywhere in the subject.

```bash
# 1. Generate the icon/logo on a chroma background
scripts/generate_image "BrandName app icon on a solid magenta (#FF00FF) chroma-key background, no magenta anywhere in the icon itself, icon fills most of the frame" -o icon-chroma.png

# 2. Strip the background → transparent PNG with alpha
~/Projects/skills/remove-background/scripts/remove_background icon-chroma.png -o icon-transparent.png --crop --padding 32

# Verify: should show hasAlpha=yes
sips -g hasAlpha icon-transparent.png
```

Tips for the chroma generation step:
- **Call out the hex** explicitly in the prompt (e.g. `#FF00FF`) — models are more reliable with hex than color names
- **Tell the model NOT to use that color elsewhere** in the subject
- For brand work with purple (`#7C5CFF`), use green/magenta chroma; never use a chroma close to brand colors
- Use `--crop --padding <n>` on `remove-background` to trim the canvas tight to the logo
- `remove-background` output is always PNG with alpha, regardless of input format

### Editing SVG brand assets

`--input` only accepts PNG/JPG/GIF/WebP. Rasterize SVGs first:

```bash
# macOS (uses system renderer, handles web fonts correctly)
qlmanage -t -s 1024 -o ./refs/ brand-icon.svg
# produces ./refs/brand-icon.svg.png

# ImageMagick alternative (may fail on custom fonts)
magick -background none -density 300 brand-icon.svg -resize 1024x1024 brand-icon.png
```

### Edit an existing image
```bash
scripts/generate_image "Make the background blue" --input photo.jpg
```

### Edit with custom output
```bash
scripts/generate_image "Remove the text from the image" --input screenshot.png --output cleaned.png
```

### Higher detail output
```bash
scripts/generate_image "Detailed architectural blueprint of a modern house" --max-tokens 2048
```

### Reproducible generation (seed)
```bash
scripts/generate_image "A red fox in autumn forest" --seed 42 -o fox.png
```

### High creativity
```bash
scripts/generate_image "Abstract dreamscape" --temperature 1.8 -o dream.png
```

### Reasoning for complex prompts
```bash
scripts/generate_image "A technically accurate cross-section of a jet engine" --reasoning high
```

### Multiple images
Run the script multiple times with different prompts or output paths:
```bash
scripts/generate_image "Image 1 description" --output image1.png
scripts/generate_image "Image 2 description" --output image2.png
```

## Script Parameters

- `prompt` (required): Text description of the image to generate, or editing instructions
- `--input` or `-i`: Input image path for editing / reference (enables edit mode)
- `--output` or `-o`: Output file path (default: generated_image.png)
- `--model` or `-m`: Model id. Default `gpt-image-2` (routed via OpenAI SDK). Use `google/gemini-3.1-flash-image-preview` for Gemini (routed via OpenRouter).
- `--aspect-ratio` or `-a`: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 1:4, 4:1, 1:8, 8:1. On gpt-image-2 mapped to nearest `1024x1024` / `1024x1536` / `1536x1024`. On Gemini honoured exactly.
- `--size`: gpt-image-2 → `1024x1024`, `1024x1536`, `1536x1024`, `auto`. Gemini → `0.5K`, `1K` (default), `2K`, `4K`.
- `--quality` or `-q`: gpt-image-2 only. `auto`, `low`, `medium`, `high`.
- `--format`: gpt-image-2 only. `png` (default), `jpeg`, `webp`.
- `--max-tokens` or `-t`: OpenRouter models only. Default 1024.
- `--seed` or `-s`: Seed for reproducible generation (OpenRouter models)
- `--temperature` or `--temp`: Creativity control 0.0-2.0 (OpenRouter models)
- `--reasoning` or `-r`: Reasoning effort `minimal` or `high` (Gemini)
- `--api-key`: Override the auto-picked API key

## Example Use Cases

### For Scientific Documents
```bash
# Generate a conceptual illustration for a paper
scripts/generate_image "Microscopic view of cancer cells being attacked by immunotherapy agents, scientific illustration style" --output figures/immunotherapy_concept.png

# Create a visual for a presentation
scripts/generate_image "DNA double helix structure with highlighted mutation site, modern scientific visualization" --output slides/dna_mutation.png
```

### For Presentations and Posters
```bash
# Title slide background
scripts/generate_image "Abstract blue and white background with subtle molecular patterns, professional presentation style" --output slides/background.png

# Poster hero image
scripts/generate_image "Laboratory setting with modern equipment, photorealistic, well-lit" --output poster/hero.png
```

### For General Visual Content
```bash
# Website or documentation images
scripts/generate_image "Professional team collaboration around a digital whiteboard, modern office" --output docs/team_collaboration.png

# Marketing materials
scripts/generate_image "Futuristic AI brain concept with glowing neural networks" --output marketing/ai_concept.png
```

## Error Handling

The script provides clear error messages for:
- Missing API key (with setup instructions)
- API errors (with status codes)
- Unexpected response formats
- Missing dependencies (requests library)

If the script fails, read the error message and address the issue before retrying.

## Notes

- Images are returned as base64-encoded data URLs and automatically saved as PNG files
- The script supports both `images` and `content` response formats from different OpenRouter models
- Generation time varies by model (typically 5-30 seconds)
- For image editing, the input image is encoded as base64 and sent to the model
- Supported input image formats: PNG, JPEG, GIF, WebP
- Check OpenRouter pricing for cost information: https://openrouter.ai/models

## Image Editing Tips

### General
- Be specific about what changes you want (e.g., "change the sky to sunset colors" vs "edit the sky")
- Reference specific elements in the image when possible
- Both gpt-image-2 and Gemini 3.1 Flash support generation + editing through OpenRouter
- Pass hex codes (`#0E0D14`, `#7C5CFF`) for brand colors — more reliable than color names

### Brand-preservation edits (gpt-image-2)
- Explicitly enumerate what to preserve: "keep the rounded-square tile shape, keep the P letterform, keep the corner badge position and shape"
- Say "exactly the reference but ..." to anchor the model on the source
- gpt-image-2 respects brand colors well; Gemini sometimes drifts (e.g. recolors wordmark text purple if purple is mentioned as an accent)

### Character / mascot consistency (use Gemini)
- Pass the reference via `-i` every call; don't rely on prompt-only consistency
- Prompt with "same character, same art style, same proportions, preserve all accent colors"
- List each accent color explicitly ("preserve the green tail tip, red collar, green mouth")
- gpt-image-2 tends to drop secondary accent colors on illustrated mascots — prefer Gemini here

### Aspect / crop control
- gpt-image-2 **cannot** be prompted into wide aspect or tight crop — it always returns 1024×1024 with padding
- For anything non-square: switch to Gemini with `-a <ratio>` (`1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4, 21:9, 1:4, 4:1, 1:8, 8:1`)
- For hi-res: Gemini with `--size 2K` or `4K`
- Use `--reasoning high` (Gemini only) for spatial/compositional prompts

### Transparency
- Never trust a model prompt for "transparent PNG with alpha" — both models fake it
- Generate on solid chroma bg → `remove-background` skill (see workflow above)
- `remove-background --crop --padding <n>` trims the canvas tight to the subject

### Common failure modes and fixes
| Symptom | Likely cause | Fix |
|---|---|---|
| Output is square when you asked for wide | Forgot `-a` / `--size` flag | Add `-a 16:9` or `--size 1536x1024` |
| Need wider than 16:9 (e.g. 4:1, 21:9 exact) | gpt-image-2 maxes out at 1536×1024 | Switch to Gemini + `-a 4:1` / `21:9` |
| Need bigger than 1536px | gpt-image-2 is capped | Switch to Gemini + `--size 2K` or `4K` |
| API error "Transparent background is not supported" | Asked gpt-image-2 for alpha | Use chroma-key workflow above |
| Wordmark text came out purple/wrong color | Gemini misread accent color spec | Use gpt-image-2 (default) for wordmark work |
| Mascot lost green accent / red collar | Used gpt-image-2 with illustrated ref | Switch to Gemini, list accent colors explicitly |
| Input rejected ("file format") | Passed SVG to `-i` | Rasterize first with `qlmanage -t -s 1024` |
| Error "OPENAI_API_KEY not found" | Default model needs OpenAI key | `source ~/.secrets` or set `OPENAI_API_KEY` in `.env` |
| Error "OPENROUTER_API_KEY not found" | Switched to Gemini without OpenRouter key | Set `OPENROUTER_API_KEY` in `.env` |

## Integration with Other Skills

- **remove-background**: Required for true transparent PNGs — generate on chroma bg, then segment. See "Transparent backgrounds — chroma-key workflow" above.
- **optimize-image-web**: Run after generation to produce WebP/favicon/og-image variants at smaller sizes.
- **scientific-schematics**: Use for technical diagrams, flowcharts, circuits, pathways — not for illustrations.
- **scientific-slides**: Combine with generate-image for visually rich presentations.
- **latex-posters**: Use generate-image for poster visuals and hero images.

## Reference: empirical findings

These recommendations come from head-to-head runs against two real brand kits (a geometric SaaS logo + an illustrated mascot) plus direct SDK probes. Summary:

- gpt-image-2 won 5/8 structured brand tasks (icons, wordmarks, color swaps, editorial illustration)
- Gemini won on wide-aspect banners and illustrated-mascot accent-color preservation
- Neither produces real alpha; transparency requires the chroma-key + `remove-background` flow
- gpt-image-2's transparency is rejected at the API level (`"Transparent background is not supported for this model"`) — confirmed via direct OpenAI SDK probe
- gpt-image-1 (predecessor) does support `background="transparent"` but renders washed-out line-art for icons — not a viable fallback
- OpenAI SDK direct unlocks non-square sizes (`1024x1536`, `1536x1024`, `auto`), quality tiers (`low`/`medium`/`high`), and `png`/`jpeg`/`webp` output for gpt-image-2 — none of which are exposed via the OpenRouter chat-completions route
