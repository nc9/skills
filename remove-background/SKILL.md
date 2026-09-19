---
name: remove-background
description: Remove image backgrounds locally with the BiRefNet segmentation model, writing a transparent PNG. Use when asked to remove or cut out a background, isolate a subject, or make a transparent version of a photo. No API key.
allowed-tools: Bash, Read
---

# Remove Background

Local BiRefNet segmentation (`ZhengPeng7/BiRefNet`) on CUDA, MPS or CPU. Output is always RGBA PNG.

## Requirements

No API key. First run is expensive: uv builds a ~790 MB environment (torch, torchvision, transformers, timm, kornia) and downloads ~445 MB of model weights to `~/.cache/huggingface`. Both are cached; later runs start in seconds.

## Command

```bash
./scripts/remove_background <input_image> [options]   # single command, no subcommand
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output path (default `{name}_nobg.png`) |
| `-d, --device` | Force `cuda` \| `mps` \| `cpu` (default auto: CUDA > MPS > CPU) |
| `-c, --crop` | Crop to the foreground bounding box |
| `-p, --padding` | Padding around the crop, px (default 0) |
| `-f, --format` | `json` (default) or `table` |

## Output

JSON: `input`, `output`, `device`, `original_size`, `output_size`, `cropped`, `model`, plus `crop_box` when a box was found.

## Gotchas

- The saved file is always PNG whatever extension `-o` gets; `-f` is the stdout report format, not the image format.
- Inference resizes to 1024x1024 and scales the mask back up, so large images lose edge detail.
- `cropped` echoes the `-c` flag, not whether a crop happened. A fully opaque image yields no bbox: `crop_box` is absent and nothing is cropped.
- MPS falls back to CPU for unsupported ops (`PYTORCH_ENABLE_MPS_FALLBACK=1` is set); use `-d cpu` if MPS misbehaves.

## Examples

```bash
./scripts/remove_background photo.jpg
./scripts/remove_background photo.jpg -c -p 20 -o cutout.png
./scripts/remove_background photo.jpg -d cpu -f table
```
