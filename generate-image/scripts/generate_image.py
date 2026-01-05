#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "typer",
# ]
# ///
"""
Generate Image Skill

Generate and edit images using OpenRouter API with Google Gemini 3 Pro.
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Annotated

import requests
import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(help="Generate and edit images using OpenRouter API")

# --- Config ---

DEFAULT_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_OUTPUT = "generated_image.png"

MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]


# --- Helpers ---


def loadImageAsBase64(image_path: Path) -> str:
    """Load an image file and return it as a base64 data URL."""
    if not image_path.exists():
        typer.echo(f"Error: Image file not found: {image_path}", err=True)
        raise typer.Exit(1)

    mime_type = MIME_TYPES.get(image_path.suffix.lower(), "image/png")

    with open(image_path, "rb") as f:
        image_data = f.read()

    base64_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"


def saveBase64Image(base64_data: str, output_path: Path) -> None:
    """Save base64 encoded image to file."""
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]

    image_data = base64.b64decode(base64_data)
    with open(output_path, "wb") as f:
        f.write(image_data)


def getApiKey(api_key: str | None = None) -> str:
    """Get API key from argument or environment."""
    key = api_key or os.getenv("OPENROUTER_API_KEY")

    if not key:
        typer.echo("Error: OPENROUTER_API_KEY not found", err=True)
        typer.echo("\nSet in .env file:", err=True)
        typer.echo("  OPENROUTER_API_KEY=your-api-key-here", err=True)
        typer.echo("\nOr export:", err=True)
        typer.echo("  export OPENROUTER_API_KEY=your-api-key-here", err=True)
        typer.echo("\nGet key: https://openrouter.ai/keys", err=True)
        raise typer.Exit(1)

    return key


def generateImage(
    prompt: str,
    output_path: Path,
    api_key: str,
    input_image: Path | None = None,
    aspect_ratio: str | None = None,
) -> dict:
    """Generate or edit an image using OpenRouter API."""
    is_editing = input_image is not None

    if is_editing:
        typer.echo(f"Editing: {input_image}", err=True)
        typer.echo(f"Model: {DEFAULT_MODEL}", err=True)
        image_data_url = loadImageAsBase64(input_image)
        message_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}},
        ]
    else:
        typer.echo(f"Generating: {prompt[:50]}...", err=True)
        typer.echo(f"Model: {DEFAULT_MODEL}", err=True)
        message_content = prompt

    request_body = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": message_content}],
        "modalities": ["image", "text"],
    }

    if aspect_ratio:
        request_body["image_config"] = {"aspect_ratio": aspect_ratio}

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=request_body,
    )

    if response.status_code != 200:
        typer.echo(f"API Error ({response.status_code}): {response.text}", err=True)
        raise typer.Exit(1)

    result = response.json()

    if not result.get("choices"):
        typer.echo("Error: No choices in response", err=True)
        typer.echo(f"Response: {json.dumps(result, indent=2)}", err=True)
        raise typer.Exit(1)

    message = result["choices"][0]["message"]
    images = extractImages(message)

    if not images:
        typer.echo("Error: No image in response", err=True)
        if message.get("content"):
            typer.echo(f"Content: {message['content']}", err=True)
        raise typer.Exit(1)

    image = images[0]
    image_url = image.get("image_url", {}).get("url") or image.get("url")

    if not image_url:
        typer.echo(f"Error: Unexpected image format: {image}", err=True)
        raise typer.Exit(1)

    saveBase64Image(image_url, output_path)
    typer.echo(f"Saved: {output_path}", err=True)

    return result


def extractImages(message: dict) -> list[dict]:
    """Extract images from API response message."""
    images = []

    if message.get("images"):
        images = message["images"]
    elif message.get("content"):
        content = message["content"]
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image":
                    images.append(part)

    return images


# --- Commands ---


@app.command()
def generate(
    prompt: Annotated[
        str, typer.Argument(help="Image description or editing instructions")
    ],
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Output file path")
    ] = Path(DEFAULT_OUTPUT),
    input: Annotated[
        Path | None, typer.Option("--input", "-i", help="Input image for editing")
    ] = None,
    aspect_ratio: Annotated[
        str | None,
        typer.Option(
            "--aspect-ratio",
            "-a",
            help="Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)",
        ),
    ] = None,
    api_key: Annotated[
        str | None, typer.Option("--api-key", help="OpenRouter API key")
    ] = None,
) -> None:
    """Generate or edit an image."""
    key = getApiKey(api_key)
    generateImage(prompt, output, key, input, aspect_ratio)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    prompt: Annotated[str | None, typer.Argument(help="Image description")] = None,
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Output file path")
    ] = Path(DEFAULT_OUTPUT),
    input: Annotated[
        Path | None, typer.Option("--input", "-i", help="Input image for editing")
    ] = None,
    aspect_ratio: Annotated[
        str | None,
        typer.Option(
            "--aspect-ratio",
            "-a",
            help="Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)",
        ),
    ] = None,
    api_key: Annotated[
        str | None, typer.Option("--api-key", help="OpenRouter API key")
    ] = None,
) -> None:
    """Generate or edit images using OpenRouter API."""
    if ctx.invoked_subcommand is None and prompt:
        key = getApiKey(api_key)
        generateImage(prompt, output, key, input, aspect_ratio)
    elif ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
