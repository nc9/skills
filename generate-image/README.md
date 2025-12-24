# Generate Image

AI image generation and editing using OpenRouter models (FLUX, Gemini).

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/generate-image

# Install for user (all projects)
npx claude-plugins install @nc9/skills/generate-image --user
```

## Setup

### 1. Get API Key

Get an OpenRouter API key from [openrouter.ai/keys](https://openrouter.ai/keys)

### 2. Configure Environment

Create a `.env` file in your project root:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

Or set globally:

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

## Usage

```bash
# Generate image
./scripts/generate_image.py "A sunset over mountains"

# Edit existing image
./scripts/generate_image.py "Make the sky purple" --input photo.jpg

# Specify model
./scripts/generate_image.py "A cat in space" --model "black-forest-labs/flux.2-pro"

# Custom output path
./scripts/generate_image.py "Abstract art" --output artwork.png
```

## Models

| Model | Quality | Editing Support |
|-------|---------|-----------------|
| `google/gemini-3-pro-image-preview` (default) | High | Yes |
| `black-forest-labs/flux.2-pro` | High | Yes |
| `black-forest-labs/flux.2-flex` | Good | No (generation only) |

## Options

| Option | Description |
|--------|-------------|
| `--input, -i` | Input image for editing |
| `--model, -m` | OpenRouter model ID |
| `--output, -o` | Output file path (default: generated_image.png) |
| `--api-key` | API key (overrides .env) |

## When to Use

- Photos and photorealistic images
- Artistic illustrations and artwork
- Concept art and visual concepts
- Image editing and modifications

