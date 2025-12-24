# Optimize Image for Web

Convert images to optimized WebP format with presets for icons, social cards, and thumbnails.

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/optimize-image-web

# Install for user (all projects)
npx claude-plugins install @nc9/skills/optimize-image-web --user
```

## Setup

No API keys required. Uses Pillow for local image processing.

Pillow is installed automatically via uv when running the script.

## Usage

```bash
# Convert single image
./scripts/optimize_image.py convert image.png -w 800 -q 85

# Generate favicon set
./scripts/optimize_image.py preset logo.png favicon -o ./public

# Generate social media cards
./scripts/optimize_image.py preset banner.png social -o ./assets

# Generate PWA icon set
./scripts/optimize_image.py preset icon.png icon-set -o ./public/icons -p app

# Show image info
./scripts/optimize_image.py info photo.jpg

# List available presets
./scripts/optimize_image.py presets
```

## Commands

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

## Output

```json
{
  "input": "logo.png",
  "preset": "icon-set",
  "original": {"width": 1024, "height": 1024},
  "outputs": [
    {"path": "logo-16x16.webp", "width": 16, "height": 16, "size_kb": 0.5}
  ],
  "quality": 85
}
```
