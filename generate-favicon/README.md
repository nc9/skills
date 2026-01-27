# Generate Favicon

Generate a complete set of favicon files from a single source image. Creates PNG files in all standard sizes, ICO file, and site.webmanifest for PWA support.

## When to Use

- User needs favicons for a website
- User asks to "create a favicon" or "generate favicons"
- User has a logo/icon and needs it in multiple sizes
- User needs Apple touch icons or PWA icons

## Quick Start

```bash
./generate_favicon.py logo.png
```

This creates in `public/`:
- `favicon.ico` (multi-size)
- `favicon-16x16.png`
- `favicon-32x32.png`
- `favicon-48x48.png`
- `apple-touch-icon.png` (180x180)
- `favicon-192x192.png`
- `favicon-512x512.png`
- `site.webmanifest`

## Options

```bash
./generate_favicon.py [OPTIONS] INPUT_PATH
```

| Option | Description | Default |
|--------|-------------|---------|
| `--output, -o` | Output directory | `public` |
| `--name, -n` | Site/app name for manifest | `My Site` |
| `--theme, -t` | Theme color (hex) | `#000000` |
| `--manifest/--no-manifest` | Create site.webmanifest | `true` |

## Examples

### Basic Usage

```bash
./generate_favicon.py logo.png
```

### Custom Output Directory

```bash
./generate_favicon.py logo.png -o static/assets
```

### With Custom Theme

```bash
./generate_favicon.py icon.png -n "My App" -t "#8844dd"
```

### Skip Manifest

```bash
./generate_favicon.py logo.png --no-manifest
```

## Generated Files

| File | Size | Purpose |
|------|------|---------|
| `favicon.ico` | 16, 32, 48px | Legacy browsers, bookmarks |
| `favicon-16x16.png` | 16x16 | Browser tab (small) |
| `favicon-32x32.png` | 32x32 | Browser tab (standard) |
| `favicon-48x48.png` | 48x48 | Browser tab (large) |
| `apple-touch-icon.png` | 180x180 | iOS home screen |
| `favicon-192x192.png` | 192x192 | Android Chrome |
| `favicon-512x512.png` | 512x512 | PWA splash screen |
| `site.webmanifest` | - | PWA manifest |

## Integration

### Next.js App Router

Add to `app/layout.tsx`:

```typescript
export const metadata: Metadata = {
  icons: {
    icon: [
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-48x48.png", sizes: "48x48", type: "image/png" },
      { url: "/favicon.ico", sizes: "any" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
    other: [
      { rel: "icon", url: "/favicon-192x192.png", sizes: "192x192" },
      { rel: "icon", url: "/favicon-512x512.png", sizes: "512x512" },
    ],
  },
  manifest: "/site.webmanifest",
};
```

### HTML (Traditional)

```html
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

## Input Requirements

- Any image format supported by Pillow (PNG, JPG, WebP, etc.)
- Square images work best (1:1 aspect ratio)
- Recommended minimum: 512x512 pixels
- Transparent background recommended for best results
- PNG with alpha channel ideal

## Tips

1. **Source Image**: Use a high-resolution square image (at least 512x512)
2. **Simple Design**: Favicons appear small - keep design simple and bold
3. **Test at Small Sizes**: Verify your icon looks good at 16x16
4. **Transparent Background**: Use PNG with transparency for clean edges
5. **Theme Color**: Match your site's primary color for PWA

## Output

The script prints a summary:

```
Loaded: logo.png (1024x1024)
Output: public/

✓ favicon-16x16.png              16x16    580 bytes
✓ favicon-32x32.png              32x32  1,200 bytes
✓ favicon-48x48.png              48x48  2,200 bytes
✓ apple-touch-icon.png          180x180 18,000 bytes
✓ favicon-192x192.png           192x192 21,000 bytes
✓ favicon-512x512.png           512x512 175,000 bytes
✓ favicon.ico                     multi    602 bytes
✓ site.webmanifest                         440 bytes

Generated 8 files
```

## Dependencies

- `pillow` - Image processing
- `typer` - CLI interface

Both installed automatically via uv script inline dependencies.
