#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "torch",
#     "torchvision",
#     "transformers",
#     "pillow",
#     "typer",
#     "einops",
#     "kornia",
#     "timm",
# ]
# ///
"""
Remove image backgrounds using BiRefNet_lite model.
"""

from __future__ import annotations

import json
import os
from enum import Enum
from pathlib import Path
from typing import Annotated

import torch
import typer
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# Enable MPS fallback for unsupported ops
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

app = typer.Typer(help="Remove backgrounds from images using AI segmentation")

MODEL_NAME = "ZhengPeng7/BiRefNet_lite"

# Image transform for model input
transformImage = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


class OutputFormat(str, Enum):
    json = "json"
    table = "table"


def getDevice(requested: str | None = None) -> str:
    """Detect best available device or validate requested device."""
    if requested:
        if requested == "cuda" and not torch.cuda.is_available():
            typer.echo("Warning: CUDA not available, falling back to CPU", err=True)
            return "cpu"
        if requested == "mps" and not torch.backends.mps.is_available():
            typer.echo("Warning: MPS not available, falling back to CPU", err=True)
            return "cpu"
        return requested

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def loadModel(device: str) -> AutoModelForImageSegmentation:
    """Load BiRefNet_lite model."""
    torch.set_float32_matmul_precision("high")
    model = AutoModelForImageSegmentation.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
    )
    model.to(device)
    # Set to inference mode
    model.requires_grad_(False)
    return model


def removeBackground(
    img: Image.Image,
    model: AutoModelForImageSegmentation,
    device: str,
) -> Image.Image:
    """Remove background from image, return RGBA with transparency."""
    original_size = img.size
    img_rgb = img.convert("RGB")

    # Prepare input tensor
    input_tensor = transformImage(img_rgb).unsqueeze(0).to(device)

    # Run inference
    with torch.no_grad():
        preds = model(input_tensor)[-1].sigmoid().cpu()

    # Create mask
    pred = preds[0].squeeze()
    mask = transforms.ToPILImage()(pred)
    mask = mask.resize(original_size, Image.Resampling.LANCZOS)

    # Apply mask as alpha channel
    result = img_rgb.copy()
    result.putalpha(mask)

    return result


@app.command()
def main(
    input_path: Annotated[Path, typer.Argument(help="Input image path")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path (default: {name}_nobg.png)"),
    ] = None,
    device: Annotated[
        str | None,
        typer.Option("--device", "-d", help="Device: cuda/mps/cpu (default: auto)"),
    ] = None,
    format: Annotated[
        OutputFormat,
        typer.Option("--format", "-f", help="Output format"),
    ] = OutputFormat.json,
) -> None:
    """Remove background from an image."""
    if not input_path.exists():
        typer.echo(f"Error: File not found: {input_path}", err=True)
        raise typer.Exit(1)

    # Determine output path
    if output is None:
        output = input_path.with_stem(f"{input_path.stem}_nobg").with_suffix(".png")

    # Setup device and model
    selected_device = getDevice(device)

    if format == OutputFormat.table:
        typer.echo(f"Loading model on {selected_device}...")

    model = loadModel(selected_device)

    # Load and process image
    try:
        img = Image.open(input_path)
    except Exception as e:
        typer.echo(f"Error opening image: {e}", err=True)
        raise typer.Exit(1)

    original_size = img.size

    if format == OutputFormat.table:
        typer.echo("Removing background...")

    result = removeBackground(img, model, selected_device)

    # Save result
    result.save(output, "PNG")

    response = {
        "input": str(input_path),
        "output": str(output),
        "device": selected_device,
        "original_size": list(original_size),
        "model": MODEL_NAME,
    }

    if format == OutputFormat.json:
        typer.echo(json.dumps(response, indent=2))
    else:
        typer.echo(f"Saved: {output}")
        typer.echo(f"Size: {original_size[0]}x{original_size[1]}")
        typer.echo(f"Device: {selected_device}")


if __name__ == "__main__":
    app()
