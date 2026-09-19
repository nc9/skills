---
name: generate-favicon
description: Generate a complete favicon set (PNG sizes, multi-size .ico, apple-touch-icon, site.webmanifest) from one source image using Pillow. Use when asked for favicons, app icons, PWA icons, or an Apple touch icon.
allowed-tools: Bash, Read
---

# Generate Favicon

Local, no API key. Resizes one source image into every standard favicon asset.

## Command

```bash
./scripts/generate_favicon logo.png -o public -n "My App" -t "#8844dd"
```

| Option | Default | Description |
|--------|---------|-------------|
| `-o, --output` | `public` | Output directory (created if missing) |
| `-n, --name` | `My Site` | Site/app name written into the manifest |
| `-t, --theme` | `#000000` | Manifest `theme_color` |
| `--manifest / --no-manifest` | manifest | Write `site.webmanifest` |

## Output

Writes `favicon-{16,32,48,192,512}.png`, `apple-touch-icon.png` (180), `favicon.ico`
(16/32/48 in one file), and `site.webmanifest`. Prints a per-file summary plus a
ready-to-paste Next.js `metadata.icons` block (human text, not JSON).

## Gotchas

- Source should be square and ≥512×512; anything non-square is squashed, not cropped.
- Non-RGBA input is converted to RGBA, so a JPEG source gets an opaque background —
  feed it a PNG with alpha for clean edges.
- Design for 16×16 legibility; fine detail disappears at tab size.
- Social cards are not generated here. Standard dimensions if you need them:
  og:image 1200×630, Twitter summary_large_image 1200×675.
