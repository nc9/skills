# Example Usage

This shows how the favicon skill was used to create favicons for nikcub.me.

## Step 1: Generate Base Image

First, an AI-generated image was created using the `generate-image` skill:

```bash
uv run /Users/n/.claude/skills/generate-image/scripts/generate_image.py \
  --output favicon-base.png \
  --aspect-ratio 1:1 \
  "A simple, minimalist favicon design: A bold capital letter 'N' in white color,
   using an elegant serif font (similar to Garamond or Charter), perfectly centered
   on a solid rich violet-purple background (color #8844dd). The design should be
   extremely clean and minimal, with the N taking up about 60% of the space."
```

## Step 2: Generate Favicon Set

Then used this skill to generate all favicon variations:

```bash
./generate_favicon.py favicon-base.png \
  -n "Nik Cubrilovic" \
  -t "#8844dd"
```

Output:
```
Loaded: favicon-base.png (1024x1024)
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

## Step 3: Integrate with Next.js

Added to `src/app/layout.tsx`:

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
  title: "Nik Cubrilovic",
};
```

## Result

A complete, production-ready favicon set that works across:
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile devices (iOS, Android)
- Progressive Web Apps
- Legacy browsers (via .ico)

Total file size: ~220KB for all variations.
