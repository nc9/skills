---
name: commit
description: Pre-commit workflow - test, lint, format, type-check, atomic commits. Use when user says "commit", "/commit", or wants to commit changes.
allowed-tools: Bash, Read, Glob, Grep
---

# Commit

Pre-commit quality workflow with atomic commits.

## When to Use

- User says "commit", "/commit", "commit my changes"
- After completing a feature or fix
- Before pushing changes

## Workflow

Execute in order. Stop on failure.

### 0. Scope Check

**Only commit changes relevant to this conversation/thread.**

- Review the conversation history and plan file (if present)
- Identify files created/modified as part of this task
- Ignore unrelated changes in the working tree
- If unsure, ask user which changes to include

```bash
# Show all changes, but only stage task-relevant files
git status
```

### 1. Detect Submodules

Check for git submodules:

```bash
git submodule status
```

If submodules exist with changes:
1. Enter each submodule with changes
2. Run full workflow (lint, format, type-check, commit) inside submodule
3. Return to parent repo
4. Stage submodule pointer update

```bash
# Check for submodule changes
git diff --submodule
# Enter submodule
cd <submodule-path>
# ... run workflow ...
cd ..
# Stage submodule update
git add <submodule-path>
```

### 2. Detect Project Type

Check changed files to determine toolchain:

```bash
git diff --cached --name-only
git diff --name-only
```

- `*.ts`, `*.tsx`, `*.js`, `*.jsx` → TypeScript toolchain
- `*.py` → Python toolchain
- Mixed → run both toolchains

### 3. Run Quality Gates

Run **format, lint, typecheck, and tests**. Always prefer project-defined scripts over hardcoded language tooling — most repos already have a `make check` target or a `bun run check` / `npm test` script that bundles their exact toolchain (biome vs oxlint vs eslint, tsc vs tsgo, etc.). Only fall through to language defaults when no project script exists.

#### Detection order

For each gate (format, lint, typecheck, test), try entries top-to-bottom and use the first that exists:

**1. Makefile target** (preferred — projects pin their full toolchain here):
```bash
# Composite gate (covers everything in one shot when present):
make -n check 2>/dev/null && make check
make -n ci 2>/dev/null && make ci

# Per-gate targets:
make -n format 2>/dev/null && make format
make -n lint 2>/dev/null && make lint
make -n typecheck 2>/dev/null && make typecheck
make -n test 2>/dev/null && make test
```

**2. `package.json` scripts** (TypeScript/JS):
```bash
# Composite first — many projects have `check` or `check:strict`:
jq -e '.scripts."check:strict"' package.json && bun run check:strict
jq -e '.scripts.check' package.json && bun run check
jq -e '.scripts.ci' package.json && bun run ci

# Per-gate scripts:
jq -e '.scripts.format' package.json && bun run format
jq -e '.scripts.lint' package.json && bun run lint
jq -e '.scripts.typecheck' package.json && bun run typecheck
jq -e '.scripts.test' package.json && bun run test
```

**3. `pyproject.toml` scripts** (Python):
```bash
# uv-managed task runners vary; check for the convention used in the repo:
uv run -- task check 2>/dev/null || uv run pytest
```

**4. Language defaults** (only if nothing above exists):
```bash
# TypeScript fallback:
bunx biome lint --write .
bunx biome format --write .
bunx tsc --noEmit

# Python fallback:
uv run ruff check --fix .
uv run ruff format .
uv run ty check .          # fallback: uv run basedpyright .
uv run pytest
```

#### What "first available" means

- A composite script (`check`, `check:strict`, `ci`, `make check`) covers all four gates — running it satisfies format + lint + typecheck + test and the per-gate steps below can be skipped.
- If the composite is missing, run the per-gate scripts individually using the same priority order.
- If a per-gate script is missing AND no language default applies (e.g. a Go-only repo), skip that gate with a note rather than inventing a command.

#### Why detection > hardcoding

Hardcoding `bunx biome` or `bunx tsc` will run the wrong tools in projects that use oxlint/oxfmt/tsgo/eslint and either silently produce no findings or emit confusing errors. The project's own scripts encode the right toolchain choice — trust them.

If lint or format mutates files, re-stage the changes before the commit step.

### 4. Extract Issue References

Scan the conversation for issue references from:

- **Linear**: `PROJ-123`, `BACKEND-4ZW` (uppercase prefix + alphanumeric ID)
- **GitHub**: `#123`, `org/repo#123`, or GitHub issue URLs
- **Sentry**: Sentry issue URLs like `https://sentry.io/issues/...` or issue IDs like `PROJ-123`

If found, include in commit message body (not title). Format:

```
type(scope): message

Refs: BACKEND-4ZW
```

For fixes that close an issue:
```
fix(scope): message

Closes: BACKEND-4ZW
```

### 5. Atomic Commits

Group related changes. Each feature/fix gets its own commit.

1. Review changes: `git diff`
2. Stage related files: `git add <files>`
3. Commit with convention format (include issue refs if found)
4. Repeat for remaining changes

## Commit Convention

Format: `type(scope): message`

Scope is **required** - use affected area (api, auth, db, ui, cli).

| Type | Use for |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes (reference issue: `fix(auth): resolve login #123`) |
| `refactor` | Code restructuring (no behaviour change) |
| `perf` | Performance improvements |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `build` | Build system, dependencies, CI/CD |
| `style` | Formatting, whitespace (no logic changes) |
| `chore` | Maintenance, config, tooling |
| `revert` | Reverting a previous commit |
| `hotfix` | Urgent production fixes |

## Examples

```bash
# Single feature
git add src/auth/*.ts
git commit -m "feat(auth): add JWT refresh token support"

# Bug fix with GitHub issue reference
git add src/api/users.ts tests/api/users.test.ts
git commit -m "fix(api): handle null user in profile endpoint #142"

# Fix with Linear issue reference (multiline via heredoc)
git add opennem/tasks/app.py
git commit -m "$(cat <<'EOF'
fix(worker): pass WorkerSettings as positional arg

Sentry ArqIntegration expects settings_cls as args[0], not kwarg.

Closes: BACKEND-4ZW
EOF
)"

# Feature with Sentry issue reference
git add src/error-handler.ts
git commit -m "$(cat <<'EOF'
fix(errors): handle null response in API client

Refs: SENTRY-ABC123
EOF
)"

# Multiple atomic commits from one session
git add src/components/Button.tsx
git commit -m "feat(ui): add loading state to Button"

git add src/utils/format.ts
git commit -m "refactor(utils): extract date formatting helpers"
```

## Notes

- If lint/format changes files, re-stage before commit
- Prefer small, focused commits over large batches
- Keep commit messages concise (<72 chars first line)
- Don't commit generated files, build artifacts, or secrets
- Always check conversation for issue refs (Linear, GitHub, Sentry) and include them
- Use `Closes:` for fixes, `Refs:` for related work
