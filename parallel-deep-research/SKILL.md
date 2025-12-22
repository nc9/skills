---
name: parallel-deep-research
description: Performs comprehensive deep research using Parallel AI. Use for in-depth analysis, market research, competitive intelligence, or complex multi-faceted questions requiring thorough web exploration.
allowed-tools: Bash, Read
---

# Parallel Deep Research

Comprehensive intelligence reports from natural language queries using Parallel AI Task API.

## When to Use

- User needs thorough, multi-source research on a topic
- User asks complex questions requiring synthesis of multiple sources
- User needs market research or competitive analysis
- User wants comprehensive reports with citations
- Simple web search is insufficient for the depth needed

## Requirements

Environment variable must be set:
- `PARALLEL_API_KEY` - Parallel AI API key

## Command

```bash
./scripts/parallel_research.py research "query" [options]
```

## Options

| Option | Description |
|--------|-------------|
| `-p, --processor` | Model: `pro-fast` (default), `pro`, `ultra-fast`, `ultra` |
| `-t, --timeout` | Max wait in seconds (default: 600) |
| `-f, --format` | Output: `json` (default) or `markdown` |

## Processors

| Processor | Speed | Quality | Cost |
|-----------|-------|---------|------|
| `pro-fast` | 2-5x faster | Good | Lower |
| `pro` | Standard | Better | Medium |
| `ultra-fast` | 2-5x faster | Better | Medium |
| `ultra` | Standard | Best | Higher |

## Output Format

Default JSON for LLM parsing:

```json
{
  "query": "What are the latest developments in fusion energy?",
  "processor": "pro-fast",
  "run_id": "run_abc123",
  "content": {
    "summary": "...",
    "key_developments": [...],
    "companies": [...],
    "timeline": [...]
  },
  "basis": [
    {
      "field": "summary",
      "excerpts": [
        {"url": "https://...", "text": "..."}
      ]
    }
  ]
}
```

## Examples

Basic research:
```bash
./scripts/parallel_research.py research "What are the key players in the AI chip market and their competitive positions?"
```

Higher quality (slower):
```bash
./scripts/parallel_research.py research "Comprehensive analysis of renewable energy trends 2024" -p ultra
```

Human-readable output:
```bash
./scripts/parallel_research.py research "Electric vehicle battery technology advances" -f markdown
```

Extended timeout for complex research:
```bash
./scripts/parallel_research.py research "Deep competitive analysis of cloud providers" -t 1800
```

## Notes

- Research can take 1-45 minutes depending on complexity
- The pro model and ultra models are expensive and can take 10-45 minutes to complete
- Query must be under 15,000 characters
- Status updates print to stderr, results to stdout
- `basis` field contains citations mapping content to sources
