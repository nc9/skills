# Claude Code Skills

My collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills — agent-invoked tools for specialized tasks like image generation, SEO, research, and content work.

Skills extend Claude Code automatically based on context. Describe what you need; Claude picks the right skill.

## Prerequisites

### uv (Python package manager)

Python-based skills use [uv](https://docs.astral.sh/uv/) for inline-dependency scripts.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via Homebrew
brew install uv
```

### Node (for the `skills` installer)

`npx` ships with Node — install Node 18+ from [nodejs.org](https://nodejs.org/) or via `brew install node` if you don't already have it.

## Installation

Use [`npx skills`](https://github.com/vercel-labs/skills) (by Vercel Labs) to install from this repo.

### Preview available skills

```bash
npx skills add nc9/skills --list
```

### Install to the current project

```bash
# one skill
npx skills add nc9/skills --skill generate-image

# multiple skills
npx skills add nc9/skills --skill generate-image --skill remove-background --skill google-search
```

### Install globally (all projects)

```bash
npx skills add nc9/skills --skill generate-image -g
```

### Install everything, non-interactively (CI/CD)

```bash
npx skills add nc9/skills --all -g -a claude-code -y
```

### Other useful commands

```bash
npx skills list                       # show installed
npx skills update                     # pull latest
npx skills remove generate-image      # uninstall
npx skills find <keyword>             # search
```

Install a single skill from a subpath URL:

```bash
npx skills add https://github.com/nc9/skills/tree/main/generate-image
```

## Skills

### Image & design

| Skill | Description | API |
|---|---|---|
| [generate-image](./generate-image/) | Image generation & editing (OpenAI gpt-image-2 default, Gemini 3.1 Flash alt) | [OpenAI](https://platform.openai.com/) + [OpenRouter](https://openrouter.ai/) |
| [remove-background](./remove-background/) | AI background removal using BiRefNet | None (local) |
| [optimize-image-web](./optimize-image-web/) | WebP conversion, favicons, social cards, thumbnails | None (local) |
| [generate-favicon](./generate-favicon/) | Favicon / icon set generation | None (local) |

### Search & research

| Skill | Description | API |
|---|---|---|
| [google-search](./google-search/) | Google search — web, news, images, videos, places, shopping, scholar, patents | [Serper](https://serper.dev/) |
| [parallel-web-search](./parallel-web-search/) | Agentic web search with citations | [Parallel AI](https://parallel.ai/) |
| [parallel-deep-research](./parallel-deep-research/) | Deep research reports with multi-source synthesis | [Parallel AI](https://parallel.ai/) |
| [wayback](./wayback/) | Search & fetch archived web pages | Wayback Machine (free) |
| [browserbase](./browserbase/) | Fetch pages through proxy + captcha solving | [Browserbase](https://browserbase.com/) |

### SEO & indexing

| Skill | Description | API |
|---|---|---|
| [keyword-research](./keyword-research/) | Keyword ideas, volume, CPC, competition | [DataForSEO](https://dataforseo.com/) |
| [google-indexing](./google-indexing/) | Submit / remove / check URL indexing | [Google Cloud](https://console.cloud.google.com/) (free) |
| [google-search-console](./google-search-console/) | Search analytics, URL inspection, sitemaps | [Google Cloud](https://console.cloud.google.com/) (free) |

### Writing & content

| Skill | Description | API |
|---|---|---|
| [write-content](./write-content/) | Blog posts, articles, content pieces with research + humanization | — |
| [humanizer](./humanizer/) | Remove signs of AI writing — 65 patterns, narrative-first strategy | None (local) |
| [ai-writing-detector](./ai-writing-detector/) | Detect AI-generated text / plagiarism | [Pangram](https://pangram.cello.so/) |

### Engineering workflow

| Skill | Description | API |
|---|---|---|
| [commit](./commit/) | Pre-commit workflow — test, lint, format, type-check, atomic commits | None (local) |
| [review](./review/) | Exhaustive AI code review via OpenAI Codex, with GitHub/Linear/Sentry context | [OpenAI](https://platform.openai.com/) |
| [web-ui](./web-ui/) | Principles for building great web app interfaces | None (local) |

## Configuration

Skills requiring API keys read from `.env` or environment variables. Set them per project or globally:

```bash
# generate-image (OpenAI SDK direct for gpt-image-2)
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...          # only if using Gemini via OpenRouter

# google-search
SERPER_API_KEY=...

# parallel-web-search, parallel-deep-research
PARALLEL_API_KEY=...

# keyword-research
DATAFORSEO_USERNAME=your_email
DATAFORSEO_PASSWORD=your_api_password

# google-indexing, google-search-console
GOOGLE_INDEXING_KEY_FILE=/path/to/service-account-key.json

# ai-writing-detector
PANGRAM_API_KEY=...

# browserbase
BROWSERBASE_API_KEY=...
BROWSERBASE_PROJECT_ID=...

# review
OPENAI_API_KEY=sk-...                 # shared with generate-image
```

See each skill's `SKILL.md` for detailed setup.

## Usage

After install, describe what you need:

- "Generate an app icon for my SaaS, purple corner badge"
- "Remove the background from this photo"
- "Find keyword ideas for 'python tutorial'"
- "Search Google for recent AI regulation news"
- "Research the competitive landscape of cloud providers"
- "Fetch the archived version of example.com from 2023"
- "Submit these URLs to Google for indexing"
- "Show top search queries for my site"
- "Write a blog post about WebGPU, humanize the output"
- "Review my changes before I commit"

Claude picks the right skill automatically.

## Links

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [`npx skills` installer](https://github.com/vercel-labs/skills)
- [Skills Specification](https://agentskills.io/specification)
