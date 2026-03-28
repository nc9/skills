#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
#     "typer",
# ]
# ///
"""
Image optimization for web - converts to WebP with size presets.
"""

from __future__ import annotations

import json
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Annotated

import typer
from PIL import Image

app = typer.Typer(help="Optimize images for web (WebP conversion, resizing)")


# --- Presets ---


class Preset(str, Enum):
    # Icons
    favicon = "favicon"
    icon_set = "icon-set"
    # Social
    og = "og"
    twitter = "twitter"
    social = "social"
    # Thumbnails
    thumb = "thumb"
    thumb_lg = "thumb-lg"
    # Custom
    custom = "custom"


PRESET_SIZES = {
    "favicon": [(16, 16), (32, 32), (48, 48)],
    "icon-set": [
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
        (512, 512),
    ],
    "og": [(1200, 630)],
    "twitter": [(1200, 675)],
    "social": [(1200, 630), (1200, 675)],
    "thumb": [(150, 150)],
    "thumb-lg": [(300, 300)],
}


class OutputFormat(str, Enum):
    json = "json"
    files = "files"


# --- Core ---


def optimizeImage(
    img: Image.Image,
    width: int | None = None,
    height: int | None = None,
    quality: int = 85,
    keep_aspect: bool = True,
) -> tuple[bytes, int, int]:
    """Resize and convert image to WebP."""
    # Convert to RGB if necessary (for transparency, use RGBA)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")

    orig_w, orig_h = img.size

    # Calculate target size
    if width and height:
        if keep_aspect:
            img.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
    elif width:
        ratio = width / orig_w
        new_h = int(orig_h * ratio)
        img = img.resize((width, new_h), Image.Resampling.LANCZOS)
    elif height:
        ratio = height / orig_h
        new_w = int(orig_w * ratio)
        img = img.resize((new_w, height), Image.Resampling.LANCZOS)

    # Convert to WebP
    buf = BytesIO()
    img.save(buf, format="WEBP", quality=quality, method=6)
    return buf.getvalue(), img.size[0], img.size[1]


def processPreset(
    img: Image.Image,
    preset: str,
    quality: int,
) -> list[dict]:
    """Process image for all sizes in a preset."""
    sizes = PRESET_SIZES.get(preset, [])
    results = []

    for w, h in sizes:
        data, final_w, final_h = optimizeImage(img, w, h, quality, keep_aspect=True)
        results.append(
            {
                "width": final_w,
                "height": final_h,
                "size_bytes": len(data),
                "size_kb": round(len(data) / 1024, 2),
                "data": data,
            }
        )

    return results


# --- Commands ---


@app.command("convert")
def convertCmd(
    input_path: Annotated[Path, typer.Argument(help="Input image path")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path (default: same name .webp)"),
    ] = None,
    width: Annotated[
        int | None, typer.Option("--width", "-w", help="Target width")
    ] = None,
    height: Annotated[
        int | None, typer.Option("--height", "-h", help="Target height")
    ] = None,
    quality: Annotated[
        int, typer.Option("--quality", "-q", help="WebP quality 1-100")
    ] = 85,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """Convert single image to WebP with optional resizing."""
    if not input_path.exists():
        typer.echo(f"Error: File not found: {input_path}", err=True)
        raise typer.Exit(1)

    try:
        img = Image.open(input_path)
    except Exception as e:
        typer.echo(f"Error opening image: {e}", err=True)
        raise typer.Exit(1)

    orig_w, orig_h = img.size
    data, final_w, final_h = optimizeImage(img, width, height, quality)

    # Determine output path
    if output is None:
        output = input_path.with_suffix(".webp")

    # Write file
    output.write_bytes(data)

    result = {
        "input": str(input_path),
        "output": str(output),
        "original": {"width": orig_w, "height": orig_h},
        "optimized": {
            "width": final_w,
            "height": final_h,
            "size_bytes": len(data),
            "size_kb": round(len(data) / 1024, 2),
        },
        "quality": quality,
    }

    if format == OutputFormat.json:
        typer.echo(json.dumps(result, indent=2))
    else:
        typer.echo(f"Saved: {output} ({result['optimized']['size_kb']} KB)")


@app.command("preset")
def presetCmd(
    input_path: Annotated[Path, typer.Argument(help="Input image path")],
    preset: Annotated[Preset, typer.Argument(help="Size preset")],
    output_dir: Annotated[
        Path | None, typer.Option("--output-dir", "-o", help="Output directory")
    ] = None,
    quality: Annotated[
        int, typer.Option("--quality", "-q", help="WebP quality 1-100")
    ] = 85,
    prefix: Annotated[
        str, typer.Option("--prefix", "-p", help="Output filename prefix")
    ] = "",
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """Generate multiple sizes from a preset (icons, social cards, etc.)."""
    if not input_path.exists():
        typer.echo(f"Error: File not found: {input_path}", err=True)
        raise typer.Exit(1)

    if preset == Preset.custom:
        typer.echo("Error: Use 'convert' command for custom sizes", err=True)
        raise typer.Exit(1)

    try:
        img = Image.open(input_path)
    except Exception as e:
        typer.echo(f"Error opening image: {e}", err=True)
        raise typer.Exit(1)

    # Output dir
    if output_dir is None:
        output_dir = input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process preset
    results = processPreset(img, preset.value, quality)
    orig_w, orig_h = img.size

    # Generate filenames and save
    base = prefix or input_path.stem
    outputs = []

    for r in results:
        filename = f"{base}-{r['width']}x{r['height']}.webp"
        out_path = output_dir / filename
        out_path.write_bytes(r["data"])
        outputs.append(
            {
                "path": str(out_path),
                "width": r["width"],
                "height": r["height"],
                "size_kb": r["size_kb"],
            }
        )

    response = {
        "input": str(input_path),
        "preset": preset.value,
        "original": {"width": orig_w, "height": orig_h},
        "outputs": outputs,
        "quality": quality,
    }

    if format == OutputFormat.json:
        typer.echo(json.dumps(response, indent=2))
    else:
        typer.echo(f"Generated {len(outputs)} images:")
        for o in outputs:
            typer.echo(f"  {o['path']} ({o['size_kb']} KB)")


@app.command("info")
def infoCmd(
    input_path: Annotated[Path, typer.Argument(help="Input image path")],
) -> None:
    """Show image info (dimensions, format, size)."""
    if not input_path.exists():
        typer.echo(f"Error: File not found: {input_path}", err=True)
        raise typer.Exit(1)

    try:
        img = Image.open(input_path)
    except Exception as e:
        typer.echo(f"Error opening image: {e}", err=True)
        raise typer.Exit(1)

    file_size = input_path.stat().st_size

    info = {
        "path": str(input_path),
        "format": img.format,
        "mode": img.mode,
        "width": img.size[0],
        "height": img.size[1],
        "size_bytes": file_size,
        "size_kb": round(file_size / 1024, 2),
    }

    typer.echo(json.dumps(info, indent=2))


@app.command("presets")
def presetsCmd() -> None:
    """List available size presets."""
    info = {
        "presets": {
            name: [{"width": w, "height": h} for w, h in sizes]
            for name, sizes in PRESET_SIZES.items()
        }
    }
    typer.echo(json.dumps(info, indent=2))


if __name__ == "__main__":
    app()
