# Generate Image

Image generation and editing. Routes by model: `gpt-image-*` goes to the OpenAI Images
API via the OpenAI SDK, `google/gemini-*` goes to OpenRouter.

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/generate-image

# Install for user (all projects)
npx claude-plugins install @nc9/skills/generate-image --user
```

## Setup

Set the key for whichever route you use (`.env` in the project root, or exported):

```bash
OPENAI_API_KEY=...       # default gpt-image-* models — https://platform.openai.com/api-keys
OPENROUTER_API_KEY=...   # google/gemini-* models — https://openrouter.ai/keys
```

## Usage

```bash
# Generate (default model: gpt-image-2.5-sunburst)
./scripts/generate_image "A sunset over mountains" -o sunset.png

# Edit an existing image
./scripts/generate_image "Make the sky purple" -i photo.jpg -o edited.png

# Switch to Gemini for exact wide aspects, 2K/4K output, or mascot consistency
./scripts/generate_image "Ultra-wide banner" -m google/gemini-3.1-flash-image -a 8:1
```

See [SKILL.md](./SKILL.md) for the model capability matrix, routing rules, the
transparent-background workflow, and failure modes.
