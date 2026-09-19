---
name: review
description: Codex-backed second-opinion code review — 0-5 verdict plus prioritized issues with file:line citations, covering correctness, security, spec conformance and performance. Use when the user says "review", "/review", "review my changes".
allowed-tools: Bash, Read, Write, Glob, Grep, mcp__codex__codex, mcp__codex__codex-reply
---

# Review

Local, high-signal code review: build a bundle of context on disk, hand it to
Codex via MCP, render the structured JSON verdict back to the user.

## vs. the built-ins

This is the **second-opinion** review — a different vendor's model reads the
change, catching what own-model review is blind to. Claude Code's built-ins are
complementary: `/code-review` (own-model review of the diff, with `--fix` and
`--comment` for inline PR comments), `/simplify` (quality-only; does not hunt
bugs), `/security-review` (security pass over branch changes).

## When to Use

User says "review", "/review", "review my changes"; before committing
non-trivial work or opening a PR; after addressing feedback, to confirm
resolution.

## Workflow

### 1. Assemble the bundle

`prepare` gathers disk-side context and prints the bundle directory path as the
last line of stdout.

```bash
./scripts/review prepare \
  --issues "#123,PROJ-456" \
  --plan ./plan.md \
  --title "Refactor auth flow"
```

It writes: `CHANGES.diff` (unified diff), `CHANGED_FILES.txt`, `ISSUES.md`
(fetched GitHub / Linear / Sentry context), `PLAN.md` (`--plan`, else most recent
`~/.claude/plans/*.md`), `CONVENTIONS.md` (repo `REVIEW.md` + `CLAUDE.md` + user
`~/.claude/CLAUDE.md`), `REFERENCED_FILES.md` (contents of `--files`),
`REVIEW_PROMPT.md` (reviewer prompt, copied from this skill), `MANIFEST.json`,
and `AGENT_CONTEXT.md` — **a placeholder you fill in next**.

Default source: uncommitted changes if any exist, otherwise prompts for a base
branch or commit.

### 2. Write AGENT_CONTEXT.md

Only you (the agent) have the conversation context. Overwrite the placeholder
with what's not on disk: the **user request** (quote the original ask and
clarifying turns), **user feedback** (corrections and course-corrections during
the work), **plan iteration** (decisions and tradeoffs that shaped the change,
especially ones the plan file missed), and a one-paragraph **task summary**.

Be concrete. This is the canonical statement of intent the reviewer uses for
spec-conformance judgments.

### 3. Invoke the reviewer

Reviewer priority is **Codex → Claude**. Read `<bundle>/REVIEW_PROMPT.md` and
pass its contents to `mcp__codex__codex` with the bundle path. Recommended
config:

```json
{
  "approval-policy": "never",
  "sandbox": "workspace-write",
  "model": "gpt-6-astra",
  "config": { "model_reasoning_effort": "medium" }
}
```

Model policy (2026-09-07): reviews run on **`gpt-6-astra` at medium reasoning**.
That model needs Codex CLI ≥ 0.154.0-alpha.3 (`npm i -g @openai/codex@alpha`,
and `bun install -g @openai/codex@alpha` if a bun-global `codex` shadows it on
PATH; check `codex --version`). If the MCP answers "requires a newer version of
Codex", the MCP server process is still the old binary: reconnect it (`/mcp`)
or restart the session, and until then use the CLI form below with the same
model flags.

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

Parse the final JSON; if Codex wrapped it in prose or fences, strip them and
retry, then send one more `codex-reply` asking for valid JSON only. Write the
verified JSON to `<bundle>/review.json`.

Render terse — the user reads `review.json` for detail: score + verdict headline
(e.g. `4/5 — ready-with-nits`), one-line `summary`, `spec_alignment`, then issues
grouped by severity (critical → high → medium → nit → pre_existing) with
`title`, `files[].path:lines` and a one-line description; `strengths` /
`improvements` if present; the `<bundle>` path for raw artifacts.

## Fallback: `claude -p` (on ANY Codex error)

On **any** Codex failure — MCP tool not loaded, usage/credit limit, timeout, auth
error, empty or non-JSON output, anything else — switch to a headless Claude
review with the SAME bundle. It runs on Anthropic credits, independent of Codex's
OpenAI quota, so a Codex outage never blocks the review. Never abandon the review
because Codex failed; this is a first-class path, not a last resort.

Run a single self-verifying pass (step 4's "re-read your citations" is folded
into the prompt, since `claude -p` is naturally one-shot):

```bash
claude -p "$(cat <bundle>/REVIEW_PROMPT.md)

Review bundle directory: <bundle path>
Read every file in that directory (check MANIFEST.json) before producing your JSON
response. You MAY read files in the working repository to verify cross-file findings.
Before emitting, RE-READ each finding's cited file:line and DROP any you cannot
substantiate (wrong file/line, code doesn't match, or inferred from naming).
Recompute severity_counts and score. Return ONLY the JSON object — no prose, no fences." \
  --model opus \
  --permission-mode bypassPermissions \
  > <bundle>/review.json
```

- `--permission-mode bypassPermissions` lets the headless reviewer read bundle +
  repo without prompts (the prompt is read-only by intent). For least-privilege,
  use `--allowedTools "Read Grep Glob Bash"` instead.
- `--model opus` for review quality; omit to use the user's default model.
- stdout is the JSON object. If it won't parse after stripping fences, re-run the
  same `claude -p` appending "Your previous output did not parse as JSON. Return
  ONLY the JSON object." Then persist and render as in step 5.

### Older fallback: Codex CLI

The CLI hits the same backend and credits as the MCP — if the MCP failure was a
credit/usage limit, the CLI fails identically, so go straight to `claude -p`. Use
the CLI only when the MCP tool is merely *not loaded* in the session:

```bash
codex exec --cd <bundle path> --sandbox workspace-write \
  -m gpt-6-astra -c model_reasoning_effort=medium --skip-git-repo-check \
  "$(cat <bundle>/REVIEW_PROMPT.md)

Review bundle directory: <bundle path>
Read every file in that directory before producing your JSON response." < /dev/null
```

`< /dev/null` matters when the shell is not a TTY (background jobs, agents):
`codex exec` otherwise blocks on "Reading additional input from stdin..." until
the timeout and produces nothing. Use `-o <file>` to capture the final message.

## Output schema

`REVIEW_PROMPT.md` in this skill is the single source of truth for the JSON
schema, the severity ladder, and the 0–5 verdict ladder (`ship` →
`ready-with-nits` → `needs-changes` → `significant-changes` → `rethink`). Read it
there rather than restating it.

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

- Codex MCP (`mcp__codex__codex` + `mcp__codex__codex-reply`), preferred; the
  `claude` CLI as the always-available fallback.
- Codex CLI ≥ 0.154.0-alpha.3 for `gpt-6-astra` (see model policy above).
- Codex MCP server: set `client_session_timeout_seconds` high (e.g. `360000`) —
  reviews routinely run many minutes.
- `gh` CLI for GitHub issues. Optional: `LINEAR_API_KEY`; `SENTRY_AUTH_TOKEN` +
  `SENTRY_ORG`.

## Per-repo customization — REVIEW.md

Drop a `REVIEW.md` at the repo root to inject house rules (skip paths, nit caps,
mandatory checks). It concatenates into `CONVENTIONS.md` in every bundle and
overrides the generic prompt where they conflict. See `REVIEW.md.example` in this
skill for a template.

## Examples

```bash
./scripts/review prepare                                  # uncommitted, auto-pick latest plan
./scripts/review prepare --uncommitted --issues "#142"    # with linked issue
./scripts/review prepare --commit HEAD                    # last commit
./scripts/review prepare --base main                      # branch diff
```
