---
name: remove-background
description: Remove backgrounds from images using AI segmentation. Use when user asks to remove, delete, or make transparent backgrounds from photos or images.
allowed-tools: Bash, Read
---

# Remove Background

Remove image backgrounds using BiRefNet_lite model. Runs locally on CPU, MPS (Apple Silicon), or CUDA.

## When to Use

- User wants to remove background from an image
- User wants a transparent PNG version of an image
- User wants to isolate a subject from its background

## Requirements

No API keys required. Model downloads automatically on first run (~100MB, cached).

## Command

```bash
./scripts/remove_background.py <input_image> [options]
```

## Options

| Option | Description |
|--------|-------------|
| `input` | Input image path (required) |
| `-o, --output` | Output path (default: `{name}_nobg.png`) |
| `--device` | Force device: cuda/mps/cpu (default: auto-detect) |
| `-f, --format` | Output: json (default) or table |

## Examples

```bash
# Basic usage - outputs photo_nobg.png
./scripts/remove_background.py photo.jpg

# Custom output path
./scripts/remove_background.py photo.jpg -o transparent.png

# Force CPU (if MPS has issues)
./scripts/remove_background.py photo.jpg --device cpu

# Human-readable output
./scripts/remove_background.py photo.jpg --format table
```

## Output Format

JSON (default):
```json
{
  "input": "photo.jpg",
  "output": "photo_nobg.png",
  "device": "mps",
  "original_size": [1920, 1080],
  "model": "ZhengPeng7/BiRefNet_lite"
}
```

## Notes

- First run downloads model (~100MB), subsequent runs use cache
- Output is always PNG with alpha channel (transparency)
- Device auto-detection: CUDA > MPS > CPU
- MPS (Apple Silicon) may have some op fallbacks to CPU
