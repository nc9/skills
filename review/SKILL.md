---
name: review
description: |
  Exhaustive local code review using OpenAI Codex via MCP. Returns a structured
  verdict (0-5 score) + prioritized issues with file:line citations, covering
  correctness, security, spec conformance, performance, maintainability, and
  tests. Use when user says "review", "/review", "review my changes", or wants
  AI-powered code analysis before committing or opening a PR. Gathers context
  from GitHub/Linear/Sentry issues, plan files, REVIEW.md/CLAUDE.md, and the
  driving conversation.
allowed-tools: Bash, Read, Write, Glob, Grep, mcp__codex__codex, mcp__codex__codex-reply
---

# Review

Local, high-signal code review. The skill builds a bundle of context on disk,
hands it to Codex via MCP, and renders the structured JSON verdict back to
the user.

## When to Use

- User says "review", "/review", "review my changes".
- Before committing non-trivial work.
- Before opening a PR.
- After addressing review feedback — to confirm resolution.

## Workflow

### 1. Assemble the bundle

Run `prepare` to gather disk-side context (git diff, issues, plan, conventions).
It prints the bundle directory path as the last line of stdout.

```bash
./scripts/review prepare \
  --issues "#123,PROJ-456" \
  --plan ./plan.md \
  --title "Refactor auth flow"
```

`prepare` writes:

- `CHANGES.diff` — the unified diff
- `CHANGED_FILES.txt` — touched paths
- `ISSUES.md` — fetched GitHub / Linear / Sentry context
- `PLAN.md` — `--plan` argument or most recent `~/.claude/plans/*.md`
- `CONVENTIONS.md` — repo `REVIEW.md` + `CLAUDE.md` + user `~/.claude/CLAUDE.md`
- `REFERENCED_FILES.md` — contents of `--files` paths
- `AGENT_CONTEXT.md` — **placeholder; you fill this in next**
- `REVIEW_PROMPT.md` — the full reviewer prompt (copied from this skill)
- `MANIFEST.json` — file list + metadata

Default source: uncommitted changes if any exist, otherwise prompts for a base
branch or commit.

### 2. Write AGENT_CONTEXT.md

Only you (the agent) have the conversation context. Overwrite the placeholder
`<bundle>/AGENT_CONTEXT.md` with what's not on disk:

- **User request** — quote the original ask and any clarifying turns.
- **User feedback** — corrections, preferences, course-corrections during the
  work.
- **Plan iteration** — key decisions and tradeoffs that shaped the change,
  especially things not captured in the plan file.
- **Task summary** — one-paragraph description of what was built and why.

Be concrete. This is the canonical statement of intent the reviewer uses for
spec-conformance judgments.

### 3. Invoke Codex via MCP

Read `<bundle>/REVIEW_PROMPT.md` and pass its contents to `mcp__codex__codex`
along with the bundle path. Recommended config:

```json
{
  "approval-policy": "never",
  "sandbox": "workspace-write"
}
```

Prompt shape:

> {REVIEW_PROMPT.md contents}
>
> Review bundle directory: `<absolute bundle path>`
>
> Read every file in that directory (check MANIFEST.json for the list) before
> producing your JSON response.

Capture the returned `threadId` from `structuredContent.threadId`.

### 4. Verification pass (required)

Call `mcp__codex__codex-reply` with the same `threadId`:

> For each issue you returned, re-read the file and lines cited in `evidence`.
> Drop any finding where the citation does not substantiate the claim (wrong
> file, wrong line, code doesn't match the description, or you inferred from
> naming rather than reading). Return the updated JSON object — same schema,
> only verified findings. Recompute `severity_counts` and `score` accordingly.

This single step is the biggest quality lever — it suppresses hallucinated
findings that name functions or lines that don't exist.

### 5. Parse, persist, render

- Parse the final JSON. If Codex wrapped it in prose or code fences, strip
  them and retry parsing; if it still doesn't parse, send one more
  `codex-reply` asking for valid JSON only.
- Write the verified JSON to `<bundle>/review.json`.
- Render a human summary to the user:
  - Score + verdict headline (e.g. `4/5 — ready-with-nits`).
  - One-line `summary`.
  - `spec_alignment` paragraph.
  - Issues grouped by severity (critical → high → medium → nit →
    pre_existing), each with `title`, `files[].path:lines`, and one-line
    description. Deep-dive details available in `review.json`.
  - `strengths` and `improvements` bullets if present.
  - Path to `<bundle>` so the user can inspect raw artifacts.

Keep the rendered output terse — the user can read `review.json` for detail.

## Fallback: Codex MCP unavailable

If `mcp__codex__codex` isn't loaded in the session, fall back to the Codex
CLI with the same bundle:

```bash
codex exec \
  --cd <bundle path> \
  --sandbox workspace-write \
  --ask-for-approval never \
  "$(cat <bundle>/REVIEW_PROMPT.md)

Review bundle directory: <bundle path>
Read every file in that directory before producing your JSON response."
```

Then run a second `codex exec` against the same working directory for the
verification pass, referencing the JSON written in step 1. Parse and render
as in step 5.

## Output schema

See `REVIEW_PROMPT.md` for the full schema. Summary:

```json
{
  "score": 0,
  "verdict": "ship | ready-with-nits | needs-changes | significant-changes | rethink",
  "summary": "...",
  "severity_counts": { "critical": 0, "high": 0, "medium": 0, "nit": 0, "pre_existing": 0 },
  "spec_alignment": "...",
  "issues": [
    {
      "id": "R-001",
      "severity": "critical | high | medium | nit | pre_existing",
      "category": "bug | security | spec | performance | maintainability | tests",
      "title": "...",
      "description": "...",
      "files": [{ "path": "...", "lines": "..." }],
      "suggested_fix": "...",
      "confidence": "high | medium | low",
      "evidence": "file:line — justification"
    }
  ],
  "strengths": [],
  "improvements": []
}
```

### Verdict ladder

| Score | Verdict | Meaning |
|-------|---------|---------|
| 5 | `ship` | No blockers — commit as-is |
| 4 | `ready-with-nits` | Commit OK — address nits when convenient |
| 3 | `needs-changes` | Address feedback before commit |
| 2 | `significant-changes` | Non-trivial rework required |
| 0-1 | `rethink` | Design/spec-level concerns |

## Command

```bash
./scripts/review prepare [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--base, -b BRANCH` | Compare against branch |
| `--uncommitted, -u` | Review staged/unstaged/untracked changes (default when changes exist) |
| `--commit, -c SHA` | Review specific commit |
| `--issues, -i REFS` | Issue refs (comma-separated): `#123`, `PROJ-456`, `sentry:12345`, or URLs |
| `--plan, -p PATH` | Plan file path (default: most recent `~/.claude/plans/*.md`) |
| `--files, -f PATHS` | Additional files (comma-separated) |
| `--title, -t TEXT` | Commit/PR title recorded in `MANIFEST.json` |
| `--bundle-dir PATH` | Override bundle location (default: `~/.claude/review-bundles/<iso>`) |

## Requirements

- `mcp__codex__codex` + `mcp__codex__codex-reply` tools loaded (preferred), **or**
  `codex` CLI installed and authenticated (fallback).
- Codex MCP server: set `client_session_timeout_seconds` high (e.g. `360000`)
  in your MCP client config — reviews routinely run many minutes.
- `gh` CLI for GitHub issues.
- `LINEAR_API_KEY` (optional) for Linear issues.
- `SENTRY_AUTH_TOKEN`, `SENTRY_ORG` (optional) for Sentry issues.

## Per-repo customization — REVIEW.md

Drop a `REVIEW.md` at the repo root to inject house rules (skip paths, nit
caps, mandatory checks). It concatenates into `CONVENTIONS.md` in every bundle
and overrides the generic prompt where they conflict. See `REVIEW.md.example`
in this skill for a template.

## Examples

```bash
# Most common: review uncommitted changes, auto-pick latest plan
./scripts/review prepare

# Explicitly review staged/unstaged, include linked issue
./scripts/review prepare --uncommitted --issues "#142"

# Review the last commit
./scripts/review prepare --commit HEAD

# Branch-diff review against main
./scripts/review prepare --base main
```
