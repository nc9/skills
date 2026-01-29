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

### 3. Run Tests

Check for test entry points in order:

**1. Makefile (preferred):**
```bash
make -n test 2>/dev/null && make test
# OR default target
make -n 2>/dev/null && make
```

**2. package.json (TypeScript/JS):**
```bash
# Check for test script
jq -e '.scripts.test' package.json && bun run test
```

**3. pytest (Python):**
```bash
# Check for pytest config or test files
uv run pytest
```

Run first available. Skip with note if none found.

### 4. Lint

**TypeScript:**
```bash
bunx biome lint --write .
```

**Python:**
```bash
uv run ruff check --fix .
```

### 5. Format

**TypeScript:**
```bash
bunx biome format --write .
```

**Python:**
```bash
uv run ruff format .
```

### 6. Type Check

**TypeScript:**
```bash
bunx tsc --noEmit
```

**Python:**
```bash
uv run ty check .
# fallback if ty unavailable:
uv run basedpyright .
```

### 7. Extract Issue References

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

### 8. Atomic Commits

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
