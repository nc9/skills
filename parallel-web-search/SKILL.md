---
name: parallel-web-search
description: Performs agentic web search using Parallel AI. Use when user needs current web information, research, fact-checking, news, or real-time data beyond training cutoff.
allowed-tools: Bash, Read
---

# Parallel Web Search

Agentic web search optimized for LLM workflows using Parallel AI API.

## When to Use

- User needs current/real-time information
- User asks about recent events or news
- User needs to fact-check or verify claims
- User wants to research a topic with citations
- User needs information beyond training data cutoff

## Requirements

Environment variable must be set:
- `PARALLEL_API_KEY` - Parallel AI API key

## Command

```bash
./scripts/parallel_search.py search -o "objective" [-q "query"] [-n limit]
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --objective` | Natural language search goal (required) |
| `-q, --query` | Additional keyword queries (can repeat) |
| `-n, --limit` | Max results 1-20 (default: 10) |
| `-c, --max-chars` | Max chars per excerpt (default: 500) |
| `-d, --domain` | Restrict to domains (can repeat) |
| `-f, --format` | Output: `json` (default) or `table` |

## Output Format

Default JSON for LLM parsing:

```json
{
  "objective": "Find recent AI regulation news",
  "queries": ["AI regulation 2024", "EU AI Act"],
  "results": [
    {
      "title": "EU AI Act Implementation Timeline",
      "url": "https://example.com/article",
      "excerpt": "The European Union's AI Act...",
      "publish_date": "2024-12-15"
    }
  ]
}
```

## Examples

Basic search:
```bash
./scripts/parallel_search.py search -o "What are the latest developments in fusion energy?"
```

With keyword queries (improves results):
```bash
./scripts/parallel_search.py search \
  -o "Recent breakthroughs in quantum computing" \
  -q "quantum computing 2024" \
  -q "quantum supremacy"
```

Restrict to specific domains:
```bash
./scripts/parallel_search.py search \
  -o "Climate change research findings" \
  -d "nature.com" \
  -d "science.org" \
  -n 5
```

Human-readable table output:
```bash
./scripts/parallel_search.py search -o "AI safety news" -f table
```

## Best Practices

1. **Use both objective AND queries** - Objective provides context, queries ensure keyword coverage
2. **Be specific** - Include timeframes, sources preferences, or content types
3. **Limit results for efficiency** - Use `-n 5` for quick lookups
4. **Domain filtering** - Use `-d` for authoritative sources on specific topics
