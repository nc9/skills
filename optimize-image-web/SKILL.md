---
name: optimize-image-web
description: Optimizes images for web by converting to WebP format with optional resizing. Use when user needs to optimize images, generate favicons, create icon sets, make social media cards (og:image, twitter), or create thumbnails.
allowed-tools: Bash, Read
---

# Optimize Image for Web

Convert images to optimized WebP format with size presets for icons, social cards, and thumbnails.

## When to Use

- User needs to optimize images for web performance
- User asks for favicon or icon set generation
- User needs og:image or twitter card images
- User wants to resize and compress images
- User mentions WebP conversion
- User needs thumbnails at specific sizes

## Requirements

No API keys required. Uses Pillow for image processing.

## Commands

### Convert Single Image

```bash
./scripts/optimize_image.py convert image.png -w 800 -q 85
```

### Generate Preset Sizes

```bash
./scripts/optimize_image.py preset image.png favicon
./scripts/optimize_image.py preset logo.png icon-set
./scripts/optimize_image.py preset hero.jpg og
```

### Show Image Info

```bash
./scripts/optimize_image.py info image.png
```

### List Available Presets

```bash
./scripts/optimize_image.py presets
```

## Options

### convert

| Option | Description |
|--------|-------------|
| `-o, --output` | Output path (default: same name .webp) |
| `-w, --width` | Target width in pixels |
| `-h, --height` | Target height in pixels |
| `-q, --quality` | WebP quality 1-100 (default: 85) |
| `-f, --format` | Output: `json` (default) or `files` |

### preset

| Option | Description |
|--------|-------------|
| `-o, --output-dir` | Output directory |
| `-p, --prefix` | Filename prefix |
| `-q, --quality` | WebP quality 1-100 (default: 85) |
| `-f, --format` | Output: `json` (default) or `files` |

## Presets

| Preset | Sizes | Use Case |
|--------|-------|----------|
| `favicon` | 16, 32, 48 | Browser favicons |
| `icon-set` | 16-512 | Full icon set for PWA/apps |
| `og` | 1200x630 | Open Graph (Facebook, LinkedIn) |
| `twitter` | 1200x675 | Twitter cards |
| `social` | og + twitter | All social platforms |
| `thumb` | 150x150 | Small thumbnails |
| `thumb-lg` | 300x300 | Large thumbnails |

## Output Format

Default JSON for LLM parsing:

```json
{
  "input": "logo.png",
  "preset": "icon-set",
  "original": {"width": 1024, "height": 1024},
  "outputs": [
    {"path": "logo-16x16.webp", "width": 16, "height": 16, "size_kb": 0.5},
    {"path": "logo-32x32.webp", "width": 32, "height": 32, "size_kb": 1.2}
  ],
  "quality": 85
}
```

## Examples

Optimize hero image for web:
```bash
./scripts/optimize_image.py convert hero.jpg -w 1920 -q 80
```

Generate favicons from logo:
```bash
./scripts/optimize_image.py preset logo.png favicon -o ./public
```

Generate social media cards:
```bash
./scripts/optimize_image.py preset banner.png social -o ./assets
```

Generate icon set for PWA:
```bash
./scripts/optimize_image.py preset icon.png icon-set -o ./public/icons -p app
```

Check original image details:
```bash
./scripts/optimize_image.py info photo.jpg
```
