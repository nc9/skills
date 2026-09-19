---
name: commit
description: Pre-commit workflow - project quality gates, submodules, issue refs, atomic commits. Use when user says "commit", "/commit", or wants to commit changes.
allowed-tools: Bash, Read, Glob, Grep
---

# Commit

Adds the owner's gates on top of Claude Code's built-in commit behaviour: run the
project's own quality gates, commit submodules first, carry issue refs into the
message body.

Message convention (`type(scope): message` + the type table) lives in
`~/.claude/CLAUDE.md`, which is always loaded — follow it there, don't restate it.

## When to Use

User says "commit" / "/commit", or work on a feature or fix just finished.

## Workflow

Run in order. Stop on failure.

### 1. Submodules

`git submodule status`. For each submodule with changes: enter it, run this same
workflow (gates → commit) inside it, return to the parent, then
`git add <submodule-path>` to stage the pointer update. The parent commit lands
after its submodules do.

### 2. Quality gates

Run format, lint, typecheck, test — **always preferring project-defined scripts
over hardcoded tooling**. Hardcoding `bunx biome` or `bunx tsc` runs the wrong
tool in an oxlint/oxfmt/tsgo/eslint repo: it either finds nothing or emits
confusing errors. The project's own scripts encode its real toolchain; trust them.

Detection order per gate — first that exists wins:

1. **Task-runner target** — composite `make check` / `make ci` first, then
   per-gate `make format|lint|typecheck|test`; same for a `justfile` or
   `Taskfile.yml`. Probe without running: `make -n <target> 2>/dev/null`.
2. **`package.json` scripts** — composite first (`check:strict`, `check`, `ci`),
   then per-gate (`format`, `lint`, `typecheck`, `test`). Probe with
   `jq -e '.scripts.<name>' package.json`; run via `bun run`.
3. **`pyproject.toml`** — the repo's own task alias if it has one, else
   `uv run pytest`.
4. **Language defaults, only when nothing above exists** —
   TS: `bunx biome lint --write .`, `bunx biome format --write .`, `bunx tsc --noEmit`.
   Python: `uv run ruff check --fix .`, `uv run ruff format .`,
   `uv run ty check .` (fallback `uv run basedpyright .`), `uv run pytest`.

A composite target covers all four gates — running it means the per-gate steps
can be skipped. If a gate has no script and no language default (e.g. a Go-only
repo), skip it with a note rather than inventing a command. If lint or format
mutated files, re-stage before committing.

### 3. Issue references

Scan the conversation for:

- **Linear** — `PROJ-123`, `BACKEND-4ZW` (uppercase prefix + alphanumeric id)
- **GitHub** — `#123`, `org/repo#123`, or an issue URL
- **Sentry** — an issue URL or short issue id

Put them in the message **body**, never the title: `Closes: BACKEND-4ZW` when the
commit closes the issue, `Refs: BACKEND-4ZW` for related work.

### 4. Atomic commits

One commit per feature or fix, covering only what this conversation touched.
When one file's hunks belong in different commits, split them with `git add -p`
or `git apply --cached` per `~/.claude/CLAUDE.md` — never edit-revert-edit the
working tree to isolate a hunk.
