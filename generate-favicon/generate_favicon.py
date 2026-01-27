#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
#     "typer",
# ]
# ///
"""
Generate Favicon Skill

Create a complete set of favicon files from a single source image.
Generates PNG, ICO, and web manifest files optimized for all platforms.
"""

from pathlib import Path
from typing import Annotated

import typer
from PIL import Image

app = typer.Typer(help="Generate favicon files from a source image")

# Standard favicon sizes for web, mobile, and PWA
FAVICON_SIZES = {
    "favicon-16x16.png": (16, 16),
    "favicon-32x32.png": (32, 32),
    "favicon-48x48.png": (48, 48),
    "apple-touch-icon.png": (180, 180),  # iOS
    "favicon-192x192.png": (192, 192),  # Android Chrome
    "favicon-512x512.png": (512, 512),  # PWA
}


@app.command()
def generate(
    input_path: Annotated[Path, typer.Argument(help="Source image file")],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", help="Output directory")
    ] = Path("public"),
    name: Annotated[
        str, typer.Option("--name", "-n", help="Site/app name for manifest")
    ] = "My Site",
    theme_color: Annotated[
        str, typer.Option("--theme", "-t", help="Theme color (hex)")
    ] = "#000000",
    create_manifest: Annotated[
        bool, typer.Option("--manifest/--no-manifest", help="Create site.webmanifest")
    ] = True,
) -> None:
    """Generate complete favicon set from source image."""

    if not input_path.exists():
        typer.echo(f"Error: Input file not found: {input_path}", err=True)
        raise typer.Exit(1)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load source image
    try:
        img = Image.open(input_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
    except Exception as e:
        typer.echo(f"Error loading image: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Loaded: {input_path} ({img.width}x{img.height})")
    typer.echo(f"Output: {output_dir}/")
    typer.echo()

    # Generate PNG files
    created_files = []
    for filename, size in FAVICON_SIZES.items():
        output_path = output_dir / filename
        resized = img.resize(size, Image.Resampling.LANCZOS)
        resized.save(output_path, "PNG")
        file_size = output_path.stat().st_size
        created_files.append((filename, size, file_size))
        typer.echo(f"✓ {filename:30} {size[0]:3}x{size[1]:3} {file_size:>6,} bytes")

    # Generate ICO file with multiple sizes
    ico_path = output_dir / "favicon.ico"
    img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_48 = img.resize((48, 48), Image.Resampling.LANCZOS)
    img_16.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    ico_size = ico_path.stat().st_size
    typer.echo(f"✓ {'favicon.ico':30} multi   {ico_size:>6,} bytes")

    # Generate site.webmanifest
    if create_manifest:
        manifest_path = output_dir / "site.webmanifest"
        manifest_content = f"""{{
  "name": "{name}",
  "short_name": "{name}",
  "icons": [
    {{
      "src": "/favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }},
    {{
      "src": "/favicon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }}
  ],
  "theme_color": "{theme_color}",
  "background_color": "#ffffff",
  "display": "standalone"
}}
"""
        manifest_path.write_text(manifest_content)
        manifest_size = manifest_path.stat().st_size
        typer.echo(f"✓ {'site.webmanifest':30}         {manifest_size:>6,} bytes")

    typer.echo()
    typer.echo(f"Generated {len(created_files) + 1 + (1 if create_manifest else 0)} files")

    # Print Next.js metadata example
    typer.echo()
    typer.echo("Next.js metadata config:")
    typer.echo("=" * 60)
    print(
        """
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
"""
    )


if __name__ == "__main__":
    app()
