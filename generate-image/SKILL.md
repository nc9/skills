---
name: generate-image
description: Generate or edit images using Google Gemini. Use for general-purpose image generation including photos, illustrations, artwork, visual assets, concept art, and any image that isn't a technical diagram or schematic. For flowcharts, circuits, pathways, and technical diagrams, use the scientific-schematics skill instead.
---

# Generate Image

Generate and edit high-quality images using Google Gemini 3 Pro via OpenRouter.

## When to Use This Skill

**Use generate-image for:**
- Photos and photorealistic images
- Artistic illustrations and artwork
- Concept art and visual concepts
- Visual assets for presentations or documents
- Image editing and modifications
- Any general-purpose image generation needs

**Use scientific-schematics instead for:**
- Flowcharts and process diagrams
- Circuit diagrams and electrical schematics
- Biological pathways and signaling cascades
- System architecture diagrams
- CONSORT diagrams and methodology flowcharts
- Any technical/schematic diagrams

## Quick Start

Use the `scripts/generate_image.py` script to generate or edit images:

```bash
# Generate a new image
scripts/generate_image.py "A beautiful sunset over mountains"

# Edit an existing image
scripts/generate_image.py "Make the sky purple" --input photo.jpg
```

This generates/edits an image and saves it as `generated_image.png` in the current directory.

## API Key Setup

**CRITICAL**: The script requires an OpenRouter API key. Before running, check if the user has configured their API key:

1. Look for a `.env` file in the project directory or parent directories
2. Check for `OPENROUTER_API_KEY=<key>` in the `.env` file
3. If not found, inform the user they need to:
   - Create a `.env` file with `OPENROUTER_API_KEY=your-api-key-here`
   - Or set the environment variable: `export OPENROUTER_API_KEY=your-api-key-here`
   - Get an API key from: https://openrouter.ai/keys

The script will automatically detect the `.env` file and provide clear error messages if the API key is missing.

## Model

**Model**: `google/gemini-3-pro-image-preview` - High quality, supports generation + editing

## Common Usage Patterns

### Basic generation
```bash
scripts/generate_image.py "Your prompt here"
```

### Custom output path
```bash
scripts/generate_image.py "Abstract art" --output artwork.png
```

### Specify aspect ratio (Gemini models)
```bash
scripts/generate_image.py "A panoramic mountain landscape" --aspect-ratio 16:9
scripts/generate_image.py "Social media story image" -a 9:16
```

### Edit an existing image
```bash
scripts/generate_image.py "Make the background blue" --input photo.jpg
```

### Edit with custom output
```bash
scripts/generate_image.py "Remove the text from the image" --input screenshot.png --output cleaned.png
```

### Higher detail output
```bash
scripts/generate_image.py "Detailed architectural blueprint of a modern house" --max-tokens 2048
```

### Multiple images
Run the script multiple times with different prompts or output paths:
```bash
scripts/generate_image.py "Image 1 description" --output image1.png
scripts/generate_image.py "Image 2 description" --output image2.png
```

## Script Parameters

- `prompt` (required): Text description of the image to generate, or editing instructions
- `--input` or `-i`: Input image path for editing (enables edit mode)
- `--output` or `-o`: Output file path (default: generated_image.png)
- `--aspect-ratio` or `-a`: Aspect ratio for generated image. Supported: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3
- `--max-tokens` or `-t`: Max output tokens (default: 1024). Increase for more detailed/complex images
- `--api-key`: OpenRouter API key (overrides .env file)

## Example Use Cases

### For Scientific Documents
```bash
# Generate a conceptual illustration for a paper
python scripts/generate_image.py "Microscopic view of cancer cells being attacked by immunotherapy agents, scientific illustration style" --output figures/immunotherapy_concept.png

# Create a visual for a presentation
python scripts/generate_image.py "DNA double helix structure with highlighted mutation site, modern scientific visualization" --output slides/dna_mutation.png
```

### For Presentations and Posters
```bash
# Title slide background
python scripts/generate_image.py "Abstract blue and white background with subtle molecular patterns, professional presentation style" --output slides/background.png

# Poster hero image
python scripts/generate_image.py "Laboratory setting with modern equipment, photorealistic, well-lit" --output poster/hero.png
```

### For General Visual Content
```bash
# Website or documentation images
python scripts/generate_image.py "Professional team collaboration around a digital whiteboard, modern office" --output docs/team_collaboration.png

# Marketing materials
python scripts/generate_image.py "Futuristic AI brain concept with glowing neural networks" --output marketing/ai_concept.png
```

## Error Handling

The script provides clear error messages for:
- Missing API key (with setup instructions)
- API errors (with status codes)
- Unexpected response formats
- Missing dependencies (requests library)

If the script fails, read the error message and address the issue before retrying.

## Notes

- Images are returned as base64-encoded data URLs and automatically saved as PNG files
- The script supports both `images` and `content` response formats from different OpenRouter models
- Generation time varies by model (typically 5-30 seconds)
- For image editing, the input image is encoded as base64 and sent to the model
- Supported input image formats: PNG, JPEG, GIF, WebP
- Check OpenRouter pricing for cost information: https://openrouter.ai/models

## Image Editing Tips

- Be specific about what changes you want (e.g., "change the sky to sunset colors" vs "edit the sky")
- Reference specific elements in the image when possible
- For best results, use clear and detailed editing instructions
- Gemini 3 Pro supports both generation and editing through OpenRouter

## Integration with Other Skills

- **scientific-schematics**: Use for technical diagrams, flowcharts, circuits, pathways
- **generate-image**: Use for photos, illustrations, artwork, visual concepts
- **scientific-slides**: Combine with generate-image for visually rich presentations
- **latex-posters**: Use generate-image for poster visuals and hero images
