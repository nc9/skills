# Parallel Web Search

Agentic web search using [Parallel AI](https://parallel.ai/). Get current web information with citations.

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/parallel-web-search

# Install for user (all projects)
npx claude-plugins install @nc9/skills/parallel-web-search --user
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
# Basic search
./scripts/parallel_search.py search -o "Latest developments in fusion energy"

# With keyword queries (improves results)
./scripts/parallel_search.py search \
  -o "Recent quantum computing breakthroughs" \
  -q "quantum computing 2024" \
  -q "quantum supremacy"

# Restrict to specific domains
./scripts/parallel_search.py search \
  -o "Climate change research" \
  -d "nature.com" \
  -d "science.org" \
  -n 5

# Table format for review
./scripts/parallel_search.py search -o "AI safety news" -f table
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --objective` | Search goal (required) |
| `-q, --query` | Additional keyword queries (repeatable) |
| `-n, --limit` | Max results 1-20 (default: 10) |
| `-c, --max-chars` | Max chars per excerpt (default: 500) |
| `-d, --domain` | Restrict to domains (repeatable) |
| `-f, --format` | Output: `json` (default) or `table` |

## Output

```json
{
  "objective": "Find recent AI regulation news",
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

## When to Use

- Current/real-time information
- Recent events or news
- Fact-checking claims
- Research with citations
- Information beyond training cutoff

## Links

- [Parallel AI](https://parallel.ai/)
