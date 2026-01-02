# Claude Code Skills

My collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for specialized tasks like keyword research, web search, image generation, and optimization.

Skills are agent-invoked tools that extend Claude Code's capabilities. When you describe a task, Claude automatically uses the appropriate skill.

## Prerequisites

### uv (Python package manager)

Skills use [uv](https://docs.astral.sh/uv/) for running Python scripts with inline dependencies.

**Install uv:**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via Homebrew
brew install uv
```

## Installation

Install skills using [claude-plugins](https://claude-plugins.dev):

```bash
# Install to current project
npx claude-plugins install @nc9/skills/keyword-research
npx claude-plugins install @nc9/skills/parallel-web-search
npx claude-plugins install @nc9/skills/parallel-deep-research
npx claude-plugins install @nc9/skills/optimize-image-web
npx claude-plugins install @nc9/skills/generate-image
npx claude-plugins install @nc9/skills/remove-background

# Install for user (all projects)
npx claude-plugins install @nc9/skills/keyword-research --user
```

### Alternative: Manual Installation

Register the skills repository in Claude Code:

```
/plugin marketplace add nc9/skills
```

Then install individual skills:

```
/plugin install keyword-research@nc9-skills
```

Or browse via UI: `/plugin` → `Browse and install plugins` → `nc9-skills`

## Skills

| Skill | Description | API Required |
|-------|-------------|--------------|
| [keyword-research](./keyword-research/) | search keyword suggestions, search volume, CPC, competition data | [DataForSEO](https://dataforseo.com/) |
| [parallel-web-search](./parallel-web-search/) | Agentic web search with citations for current information | [Parallel AI](https://parallel.ai/) |
| [parallel-deep-research](./parallel-deep-research/) | Comprehensive research reports with multi-source synthesis | [Parallel AI](https://parallel.ai/) |
| [optimize-image-web](./optimize-image-web/) | WebP conversion, favicons, social cards, thumbnails | None (local) |
| [generate-image](./generate-image/) | AI image generation/editing via FLUX, Gemini | [OpenRouter](https://openrouter.ai/) |
| [remove-background](./remove-background/) | AI background removal using BiRefNet | None (local) |

## Configuration

Each skill requiring API keys needs environment variables. Create a `.env` file in your project or set them globally:

```bash
# DataForSEO (keyword-research)
DATAFORSEO_USERNAME=your_email
DATAFORSEO_PASSWORD=your_api_password

# Parallel AI (parallel-web-search, parallel-deep-research)
PARALLEL_API_KEY=your_api_key

# OpenRouter (generate-image)
OPENROUTER_API_KEY=your_api_key
```

See individual skill READMEs for detailed setup.

## Usage

After installing, just describe what you need:

- "Find keyword ideas for 'python tutorial'"
- "Search the web for recent AI regulation news"
- "Research the competitive landscape of cloud providers"
- "Optimize this image for web and generate favicons"
- "Generate an illustration of a sunset over mountains"
- "Remove the background from this photo"

Claude automatically invokes the appropriate skill.

## Links

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Skills Specification](https://agentskills.io/specification)
- [Parallel AI](https://parallel.ai/) - Powers web search and deep research skills
