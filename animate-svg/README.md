# animate-svg

Generate looping **animated SVGs** from a text description, using Google Gemini Pro
(`google/gemini-3.1-pro-preview`) over OpenRouter. Output is self-contained SVG markup —
drop it into HTML/JSX or save as `.svg`.

Gemini Pro is specifically good at hand-writing SVG geometry + CSS/SMIL motion, so this
skill leans on it rather than a raster image model.

```bash
export OPENROUTER_API_KEY=...        # https://openrouter.ai/keys
scripts/animate_svg "a radar sweep scanning a globe" -st halftone -o radar.svg
open radar.svg                        # it animates on its own
```

Styles: `halftone` (default) · `ascii` · `line` · `glyph` · or any free-form description.

See [SKILL.md](./SKILL.md) for full options, guarantees, and examples.

## Related skills

- **generate-image** — raster images (photos, icons, illustrations) via gpt-image / Gemini Flash.
