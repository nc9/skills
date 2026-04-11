# Skills Development

This repo contains Claude Code skills - agent-invoked tools for specialized tasks.

Follows the [Agent Skills Specification](https://agentskills.io/specification).

## Structure

```
skills/
├── CLAUDE.md                    # This file
└── <skill-name>/
    ├── SKILL.md                 # Required manifest
    ├── .env.example             # Env var template
    └── scripts/
        └── <script>             # uv script with CLI (no .py extension)
```

## Creating a Skill

### 1. Directory

```bash
mkdir -p skills/<skill-name>/scripts
```

### 2. Script (`scripts/<script>`)

uv script with shebang and inline deps:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "some-client",
#     "python-dotenv",
#     "typer",
# ]
# ///
```

Requirements:
- Use `typer` for CLI
- Use `python-dotenv` for env loading
- Default output: JSON (for LLM consumption)
- Support `--format table` for human review
- Load credentials from env vars only (no .envrc parsing)
- Make executable: `chmod +x`

### 3. SKILL.md

```yaml
---
name: skill-name
description: What it does. When to use it (trigger keywords).
allowed-tools: Bash, Read
---

# Skill Name

## When to Use
- Trigger conditions...

## Requirements
- `ENV_VAR` - description

## Command
\`\`\`bash
./scripts/script [command] [options]
\`\`\`

## Options
| Option | Description |
|--------|-------------|
| `-o` | ... |

## Output Format
JSON structure...

## Examples
...
```

### 4. .env.example

```bash
# Service API Key
SERVICE_API_KEY=your_key_here
```

## Conventions

- Script filenames: `snake_case` (no .py extension)
- Skill directories: `kebab-case`
- Functions/methods: `camelCase`
- Default output: JSON for agents
- Concise excerpts for token efficiency
- Error handling with `typer.Exit(1)`

## Testing Locally

```bash
# Symlink to personal skills
ln -s /path/to/skills/<skill-name> ~/.claude/skills/<skill-name>

# Restart Claude Code to reload
# Ask: "What Skills are available?"
```

## Existing Skills

| Skill | Purpose | API |
|-------|---------|-----|
| `ai-writing-detector` | Detect AI-generated text & plagiarism | [Pangram](https://pangram.cello.so/xGzUNafMfjD) |
| `browserbase` | Fetch pages with proxy + captcha solving | [Browserbase](https://browserbase.com/) |
| `generate-favicon` | Favicon/icon set generation | Pillow (local) |
| `generate-image` | Image generation & editing | OpenRouter (Gemini) |
| `google-indexing` | Submit/remove URLs for Google indexing | Google Indexing API |
| `google-search` | Google search (web, news, images, videos, places, shopping, scholar, patents) | [Serper](https://serper.dev/) |
| `google-search-console` | Search performance & indexing status | Google Search Console API |
| `keyword-research` | SEO keyword data | DataForSEO |
| `optimize-image-web` | WebP conversion + resizing | Pillow (local) |
| `parallel-deep-research` | Deep intelligence reports | Parallel AI |
| `parallel-web-search` | Agentic web search | Parallel AI |
| `remove-background` | AI background removal | BiRefNet (local) |
| `review` | AI code review via Codex | OpenAI Codex |
| `wayback` | Search & fetch archived web pages | Wayback Machine (free) |
