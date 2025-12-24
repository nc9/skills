# Parallel Deep Research

Comprehensive intelligence reports using [Parallel AI](https://parallel.ai/) Task API. Multi-source synthesis with citations.

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/parallel-deep-research

# Install for user (all projects)
npx claude-plugins install @nc9/skills/parallel-deep-research --user
```

## Setup

### 1. Get API Key

Get a Parallel AI API key from [parallel.ai](https://parallel.ai/)

### 2. Configure Environment

Create a `.env` file in your project root:

```bash
PARALLEL_API_KEY=your_api_key_here
```

Or set globally:

```bash
export PARALLEL_API_KEY=your_api_key_here
```

## Usage

```bash
# Basic research
./scripts/parallel_research.py research "Key players in the AI chip market"

# Higher quality (slower)
./scripts/parallel_research.py research "Renewable energy trends 2024" -p ultra

# Markdown output
./scripts/parallel_research.py research "EV battery technology advances" -f markdown

# Extended timeout for complex research
./scripts/parallel_research.py research "Cloud provider competitive analysis" -t 1800
```

## Options

| Option | Description |
|--------|-------------|
| `-p, --processor` | Model: `pro-fast` (default), `pro`, `ultra-fast`, `ultra` |
| `-t, --timeout` | Max wait seconds (default: 600) |
| `-f, --format` | Output: `json` (default) or `markdown` |

## Processors

| Processor | Speed | Quality | Cost |
|-----------|-------|---------|------|
| `pro-fast` | 2-5x faster | Good | Lower |
| `pro` | Standard | Better | Medium |
| `ultra-fast` | 2-5x faster | Better | Medium |
| `ultra` | Standard | Best | Higher |

## Output

```json
{
  "query": "...",
  "processor": "pro-fast",
  "content": {
    "summary": "...",
    "key_developments": [...],
    "companies": [...]
  },
  "basis": [
    {
      "field": "summary",
      "excerpts": [{"url": "...", "text": "..."}]
    }
  ]
}
```

## When to Use

- Thorough multi-source research
- Complex questions requiring synthesis
- Market research / competitive analysis
- Comprehensive reports with citations
- When simple web search is insufficient

## Notes

- Research can take 1-45 minutes depending on complexity
- `pro` and `ultra` models can take 10-45 minutes
- Query must be under 15,000 characters
- `basis` field contains source citations

## Links

- [Parallel AI](https://parallel.ai/)
