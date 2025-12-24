# Keyword Research

SEO keyword research using the DataForSEO API. Get keyword suggestions, search volume, CPC, and competition data.

## Installation

```bash
# Install to current project
npx claude-plugins install @nc9/skills/keyword-research

# Install for user (all projects)
npx claude-plugins install @nc9/skills/keyword-research --user
```

## Setup

### 1. Get API Credentials

Create an account at [dataforseo.com](https://dataforseo.com/) and get your API credentials from [app.dataforseo.com](https://app.dataforseo.com/)

### 2. Configure Environment

Create a `.env` file in your project root:

```bash
DATAFORSEO_USERNAME=your_login_email
DATAFORSEO_PASSWORD=your_api_password
```

Or set globally:

```bash
export DATAFORSEO_USERNAME=your_login_email
export DATAFORSEO_PASSWORD=your_api_password
```

## Usage

```bash
# Keyword suggestions (contains seed term)
./scripts/keyword_research.py suggestions "python tutorial" -n 20

# Related keywords (semantically related)
./scripts/keyword_research.py related "python tutorial" -n 20

# Multiple seeds
./scripts/keyword_research.py suggestions "react hooks" "vue composition api" -n 20

# Table format for human review
./scripts/keyword_research.py suggestions "ai tools" -f table
```

## Options

| Option | Description |
|--------|-------------|
| `-n, --limit` | Max results per seed (default: 50) |
| `-f, --format` | Output: `json` (default) or `table` |

## Output

```json
{
  "seed": "ai tools",
  "keywords": [
    {
      "keyword": "ai tools for development",
      "search_volume": 2900,
      "cpc": 25.48,
      "competition": 0.09,
      "competition_level": "LOW"
    }
  ]
}
```

## Metrics

| Field | Description |
|-------|-------------|
| `search_volume` | Monthly searches (Google US) |
| `cpc` | Cost per click in USD |
| `competition` | 0-1 scale (higher = more competitive) |
| `competition_level` | LOW, MEDIUM, or HIGH |
