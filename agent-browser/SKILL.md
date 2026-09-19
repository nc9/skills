---
name: agent-browser
description: Control a browser from the CLI with agent-browser - attach to an existing Chrome over CDP or launch one, snapshot the accessibility tree, click/fill by element ref, screenshot, read console and network. Use for any browser interaction, web app testing, or page debugging.
allowed-tools: Bash(agent-browser:*)
---

# agent-browser

Thin pointer to the `agent-browser` CLI. The usage guide ships with the CLI and always matches the installed version, so load it before running commands:

```bash
agent-browser skills get core           # workflows, patterns, troubleshooting
agent-browser skills get core --full    # plus full command reference
agent-browser skills list               # specialised guides (electron, slack, dogfood, ...)
```

Install or update: `bun add -g agent-browser@latest` (check with `agent-browser doctor`).

## Attaching to an existing Chrome

Prefer attaching over launching a fresh browser when the user has a session open.

```bash
agent-browser --cdp 9222 tab list       # Chrome started with --remote-debugging-port=9222
agent-browser --auto-connect tab list   # discover a running Chrome and reuse its auth state
```

- Chrome 136+ ignores `--remote-debugging-port` on the default profile. It only listens when started with a non-default `--user-data-dir`, or when the toggle at `chrome://inspect/#remote-debugging` is on. If attach fails, check what owns the port: `lsof -nP -iTCP:9222 -sTCP:LISTEN`.
- Work in a new tab (`tab new <url>`) unless asked to act on an open one, and never `close` a browser you attached to.

## Core loop

```bash
agent-browser --cdp 9222 snapshot -i -c   # interactive elements only, compact; returns @eN refs
agent-browser --cdp 9222 click @e3
agent-browser --cdp 9222 fill @e5 "text"
```

Refs go stale after navigation or DOM changes: re-snapshot before the next action. Use `--session <name>` to keep parallel tasks isolated, and `--json` when parsing output.
