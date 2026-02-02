---
name: review
description: |
  Exhaustive code review using OpenAI Codex. Use when user says "review",
  "/review", "review my changes", or wants AI-powered code analysis.
  Gathers context from GitHub/Linear/Sentry issues.
allowed-tools: Bash, Read, Glob, Grep
---

# Review

Exhaustive AI-powered code review via OpenAI Codex.

## When to Use
- User says "review", "/review", "review my changes"
- Before creating PR
- After completing feature work

## Workflow

### 1. Gather Issue References
Scan conversation for:
- GitHub: #123, org/repo#123, GitHub URLs
- Linear: PROJ-123, Linear URLs
- Sentry: sentry:ID, Sentry URLs

### 2. Read Plan File (if exists)
Check for active plan in conversation or ~/.claude/plans/

### 3. Read Referenced Files
If user mentions @file.ts or specific files, include content.

### 4. Run Review
```bash
# Default: reviews uncommitted changes if any exist
./scripts/review.py codex \
  --issues "#123,PROJ-456" \
  --plan ./plan.md \
  --files "src/api.ts"

# If no uncommitted changes, prompts for branch/commit to compare
```

## Command

```bash
./scripts/review.py codex [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--base, -b BRANCH` | Compare against branch |
| `--uncommitted, -u` | Review staged/unstaged/untracked changes (default if changes exist) |
| `--commit, -c SHA` | Review specific commit |
| `--issues, -i REFS` | Issue refs: #123, PROJ-456, sentry:ID, or URLs |
| `--plan, -p PATH` | Plan file for context |
| `--files, -f PATHS` | Additional files (comma-separated) |
| `--title, -t TEXT` | Commit/PR title for summary |
| `--model, -m MODEL` | Codex model (default: gpt-5.1-codex-max) |

## Context Command

Gather context without running review:

```bash
./scripts/review.py context [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--issues, -i REFS` | Issue refs (comma-separated) |
| `--plan, -p PATH` | Plan file path |
| `--files, -f PATHS` | Additional files (comma-separated) |
| `--output, -o FORMAT` | json or markdown (default: markdown) |

## Requirements

- `codex` CLI installed and authenticated
- `LINEAR_API_KEY` - (optional) Linear API key for Linear issues
- `SENTRY_AUTH_TOKEN` - (optional) Sentry auth token
- `SENTRY_ORG` - (optional) Sentry org slug

## Output

The script displays gathered context to stderr, then launches codex review interactively.
Codex outputs its review directly to the terminal.

## Examples

```bash
# Default: review uncommitted changes (or prompt if none)
./scripts/review.py codex

# Explicitly review uncommitted changes
./scripts/review.py codex --uncommitted

# Review changes against specific branch
./scripts/review.py codex --base main

# Review with GitHub issue context
./scripts/review.py codex --issues "#123"

# Review with plan file
./scripts/review.py codex --plan ./plan.md

# Gather context as JSON (without running review)
./scripts/review.py context --issues "#123" --output json
```
