#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv", "typer", "httpx"]
# ///
"""Exhaustive code review using OpenAI Codex CLI."""

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import httpx
import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    help="Exhaustive code review using OpenAI Codex", no_args_is_help=True
)


@dataclass
class IssueRef:
    type: Literal["github", "linear", "sentry"]
    id: str
    repo: str | None = None  # For github: org/repo


@dataclass
class IssueContext:
    ref: IssueRef
    title: str
    description: str
    comments: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)


def parseIssueRef(ref: str) -> IssueRef | None:
    """Parse issue reference string into IssueRef."""
    ref = ref.strip()

    # GitHub URL: https://github.com/org/repo/issues/123
    if match := re.match(
        r"https?://github\.com/([^/]+/[^/]+)/(?:issues|pull)/(\d+)", ref
    ):
        return IssueRef(type="github", id=match.group(2), repo=match.group(1))

    # GitHub: org/repo#123
    if match := re.match(r"^([^/]+/[^#]+)#(\d+)$", ref):
        return IssueRef(type="github", id=match.group(2), repo=match.group(1))

    # GitHub: #123 (current repo)
    if match := re.match(r"^#(\d+)$", ref):
        return IssueRef(type="github", id=match.group(1))

    # Linear URL: https://linear.app/team/issue/PROJ-123
    if match := re.match(r"https?://linear\.app/[^/]+/issue/([A-Z]+-[A-Z0-9]+)", ref):
        return IssueRef(type="linear", id=match.group(1))

    # Linear: PROJ-123
    if match := re.match(r"^([A-Z]+-[A-Z0-9]+)$", ref):
        return IssueRef(type="linear", id=match.group(1))

    # Sentry URL: https://sentry.io/issues/12345 or https://org.sentry.io/issues/12345
    if match := re.match(r"https?://[^/]*sentry\.io/issues/(\d+)", ref):
        return IssueRef(type="sentry", id=match.group(1))

    # Sentry: sentry:12345
    if match := re.match(r"^sentry:(\d+)$", ref):
        return IssueRef(type="sentry", id=match.group(1))

    return None


def fetchGithubIssue(ref: IssueRef) -> IssueContext | None:
    """Fetch GitHub issue/PR via gh CLI."""
    try:
        for resource in ["issue", "pr"]:
            cmd = [
                "gh",
                resource,
                "view",
                ref.id,
                "--json",
                "title,body,comments,labels",
            ]
            if ref.repo:
                cmd.extend(["--repo", ref.repo])

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return IssueContext(
                    ref=ref,
                    title=data.get("title", ""),
                    description=data.get("body", "") or "",
                    comments=[c.get("body", "") for c in data.get("comments", [])],
                    labels=[label.get("name", "") for label in data.get("labels", [])],
                )
    except Exception as e:
        typer.echo(f"Warning: Failed to fetch GitHub issue {ref.id}: {e}", err=True)
    return None


def fetchLinearIssue(ref: IssueRef) -> IssueContext | None:
    """Fetch Linear issue via GraphQL API."""
    api_key = os.getenv("LINEAR_API_KEY")
    if not api_key:
        typer.echo("Warning: LINEAR_API_KEY not set, skipping Linear issue", err=True)
        return None

    query = """
    query($id: String!) {
      issue(id: $id) {
        title
        description
        comments { nodes { body user { name } } }
        labels { nodes { name } }
      }
    }
    """

    try:
        with httpx.Client() as client:
            resp = client.post(
                "https://api.linear.app/graphql",
                headers={"Authorization": api_key, "Content-Type": "application/json"},
                json={"query": query, "variables": {"id": ref.id}},
            )
            resp.raise_for_status()
            data = resp.json()

            if errors := data.get("errors"):
                typer.echo(f"Warning: Linear API error: {errors}", err=True)
                return None

            issue = data.get("data", {}).get("issue")
            if not issue:
                return None

            return IssueContext(
                ref=ref,
                title=issue.get("title", ""),
                description=issue.get("description", "") or "",
                comments=[
                    f"{c.get('user', {}).get('name', 'Unknown')}: {c.get('body', '')}"
                    for c in issue.get("comments", {}).get("nodes", [])
                ],
                labels=[
                    label.get("name", "")
                    for label in issue.get("labels", {}).get("nodes", [])
                ],
            )
    except Exception as e:
        typer.echo(f"Warning: Failed to fetch Linear issue {ref.id}: {e}", err=True)
    return None


def fetchSentryIssue(ref: IssueRef) -> IssueContext | None:
    """Fetch Sentry issue via REST API."""
    auth_token = os.getenv("SENTRY_AUTH_TOKEN")

    if not auth_token:
        typer.echo(
            "Warning: SENTRY_AUTH_TOKEN not set, skipping Sentry issue", err=True
        )
        return None

    try:
        with httpx.Client() as client:
            headers = {"Authorization": f"Bearer {auth_token}"}

            resp = client.get(
                f"https://sentry.io/api/0/issues/{ref.id}/",
                headers=headers,
            )
            resp.raise_for_status()
            issue = resp.json()

            # Fetch latest event for stack trace
            event_resp = client.get(
                f"https://sentry.io/api/0/issues/{ref.id}/events/latest/",
                headers=headers,
            )
            event_data = ""
            if event_resp.status_code == 200:
                event = event_resp.json()
                if entries := event.get("entries", []):
                    for entry in entries:
                        if entry.get("type") == "exception":
                            event_data = json.dumps(entry.get("data", {}), indent=2)
                            break

            description = issue.get("metadata", {}).get("value", "")
            if event_data:
                description += f"\n\nStack trace:\n```\n{event_data}\n```"

            return IssueContext(
                ref=ref,
                title=issue.get("title", ""),
                description=description,
                labels=[issue.get("level", ""), issue.get("status", "")],
            )
    except Exception as e:
        typer.echo(f"Warning: Failed to fetch Sentry issue {ref.id}: {e}", err=True)
    return None


def fetchIssue(ref: IssueRef) -> IssueContext | None:
    """Fetch issue context based on type."""
    match ref.type:
        case "github":
            return fetchGithubIssue(ref)
        case "linear":
            return fetchLinearIssue(ref)
        case "sentry":
            return fetchSentryIssue(ref)
    return None


def printContext(
    issue_contexts: list[IssueContext],
    plan_path: str | None,
    plan_content: str | None,
    file_paths: list[str],
) -> None:
    """Print gathered context to stderr."""
    if not issue_contexts and not plan_content and not file_paths:
        return

    typer.echo("\n" + "=" * 60, err=True)
    typer.echo("GATHERED CONTEXT", err=True)
    typer.echo("=" * 60, err=True)

    if issue_contexts:
        typer.echo("\n## Related Issues", err=True)
        for ctx in issue_contexts:
            typer.echo(f"\n### {ctx.ref.type.upper()}: {ctx.ref.id}", err=True)
            typer.echo(f"**Title:** {ctx.title}", err=True)
            if ctx.labels:
                typer.echo(
                    f"**Labels:** {', '.join(filter(None, ctx.labels))}", err=True
                )
            if ctx.description:
                # Truncate long descriptions
                desc = (
                    ctx.description[:500] + "..."
                    if len(ctx.description) > 500
                    else ctx.description
                )
                typer.echo(f"\n{desc}", err=True)
            if ctx.comments:
                typer.echo(f"\n**Comments:** ({len(ctx.comments)} total)", err=True)
                for comment in ctx.comments[:2]:
                    truncated = comment[:200] + "..." if len(comment) > 200 else comment
                    typer.echo(f"  - {truncated}", err=True)

    if plan_content:
        typer.echo(f"\n## Plan File: {plan_path}", err=True)
        # Show first few lines
        lines = plan_content.split("\n")[:10]
        typer.echo("\n".join(lines), err=True)
        if len(plan_content.split("\n")) > 10:
            typer.echo("...", err=True)

    if file_paths:
        typer.echo(f"\n## Referenced Files ({len(file_paths)})", err=True)
        for path in file_paths:
            typer.echo(f"  - {path}", err=True)

    typer.echo("\n" + "=" * 60, err=True)
    typer.echo("STARTING CODEX REVIEW", err=True)
    typer.echo("=" * 60 + "\n", err=True)


def hasUncommittedChanges() -> bool:
    """Check if there are any uncommitted changes (staged, unstaged, or untracked)."""
    # Check for staged or unstaged changes
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def promptForCompareTarget() -> tuple[str | None, str | None]:
    """Prompt user for commit or branch to compare against.

    Returns (base_branch, commit_sha) - one will be set, other None.
    """
    typer.echo("\nNo uncommitted changes found.", err=True)
    typer.echo("What would you like to review?\n", err=True)
    typer.echo("  1. Compare current branch against main", err=True)
    typer.echo("  2. Compare current branch against another branch", err=True)
    typer.echo("  3. Review a specific commit", err=True)
    typer.echo("  4. Cancel\n", err=True)

    choice = typer.prompt("Select option", default="1")

    match choice:
        case "1":
            return ("main", None)
        case "2":
            branch = typer.prompt("Enter branch name to compare against")
            return (branch, None)
        case "3":
            commit_sha = typer.prompt("Enter commit SHA")
            return (None, commit_sha)
        case _:
            raise typer.Exit(0)


@app.command()
def codex(
    base: str = typer.Option(None, "--base", "-b", help="Compare against branch"),
    uncommitted: bool = typer.Option(
        False, "--uncommitted", "-u", help="Review staged/unstaged/untracked changes"
    ),
    commit: str = typer.Option(None, "--commit", "-c", help="Review specific commit"),
    issues: str = typer.Option(
        None,
        "--issues",
        "-i",
        help="Issue refs (comma-separated): #123, PROJ-456, sentry:ID",
    ),
    plan: str = typer.Option(None, "--plan", "-p", help="Plan file path for context"),
    files: str = typer.Option(
        None, "--files", "-f", help="Additional files (comma-separated)"
    ),
    title: str = typer.Option(
        None, "--title", "-t", help="Commit/PR title for summary"
    ),
    model: str = typer.Option("gpt-5.1-codex-max", "--model", "-m", help="Codex model"),
):
    """Run exhaustive code review using OpenAI Codex.

    Gathers context from GitHub/Linear/Sentry issues, plan files, and referenced
    files, then runs codex review interactively.

    By default, reviews uncommitted changes. If no uncommitted changes exist,
    prompts for a branch or commit to compare against.
    """
    # Check if codex is installed
    if subprocess.run(["which", "codex"], capture_output=True).returncode != 0:
        typer.echo("Error: codex CLI not found", err=True)
        typer.echo("Install from: https://github.com/openai/codex", err=True)
        raise typer.Exit(1)

    # Determine diff source if not explicitly specified
    explicit_source = uncommitted or commit or base
    if not explicit_source:
        if hasUncommittedChanges():
            uncommitted = True
            typer.echo("Reviewing uncommitted changes...", err=True)
        else:
            base, commit = promptForCompareTarget()

    # Parse and fetch issue references
    issue_contexts: list[IssueContext] = []
    if issues:
        for ref_str in issues.split(","):
            ref = parseIssueRef(ref_str.strip())
            if ref:
                typer.echo(f"Fetching {ref.type} issue {ref.id}...", err=True)
                if ctx := fetchIssue(ref):
                    issue_contexts.append(ctx)
            else:
                typer.echo(
                    f"Warning: Could not parse issue reference: {ref_str}", err=True
                )

    # Read plan file
    plan_content = None
    if plan:
        plan_path = Path(plan)
        if plan_path.exists():
            plan_content = plan_path.read_text()
        else:
            typer.echo(f"Warning: Plan file not found: {plan}", err=True)

    # Collect file paths (don't read content, just validate existence)
    file_paths = []
    if files:
        for path in files.split(","):
            p = Path(path.strip())
            if p.exists() and p.is_file():
                file_paths.append(str(p))
            else:
                typer.echo(f"Warning: File not found: {path}", err=True)

    # Print gathered context
    printContext(issue_contexts, plan, plan_content, file_paths)

    # Build codex command
    cmd = ["codex", "review"]

    # Diff source (mutually exclusive)
    if uncommitted:
        cmd.append("--uncommitted")
    elif commit:
        cmd.extend(["--commit", commit])
    elif base:
        cmd.extend(["--base", base])
    else:
        # Should not reach here, but default to main if somehow no source
        cmd.extend(["--base", "main"])

    # Model override
    cmd.extend(["-c", f'model="{model}"'])

    # Optional title
    if title:
        cmd.extend(["--title", title])

    # Execute codex (replaces this process)
    os.execvp("codex", cmd)


@app.command()
def context(
    issues: str = typer.Option(
        None, "--issues", "-i", help="Issue refs (comma-separated)"
    ),
    plan: str = typer.Option(None, "--plan", "-p", help="Plan file path"),
    files: str = typer.Option(
        None, "--files", "-f", help="Additional files (comma-separated)"
    ),
    output: str = typer.Option(
        "markdown", "--output", "-o", help="Output format: json|markdown"
    ),
):
    """Gather and display context without running review.

    Useful for debugging or preparing context separately.
    """
    # Parse and fetch issue references
    issue_contexts: list[IssueContext] = []
    if issues:
        for ref_str in issues.split(","):
            ref = parseIssueRef(ref_str.strip())
            if ref:
                typer.echo(f"Fetching {ref.type} issue {ref.id}...", err=True)
                if ctx := fetchIssue(ref):
                    issue_contexts.append(ctx)

    # Read plan file
    plan_content = None
    if plan:
        plan_path = Path(plan)
        if plan_path.exists():
            plan_content = plan_path.read_text()

    # Collect file paths and contents
    file_contents = {}
    if files:
        for path in files.split(","):
            p = Path(path.strip())
            if p.exists() and p.is_file():
                try:
                    file_contents[str(p)] = p.read_text()
                except Exception:
                    pass

    if output == "json":
        data = {
            "issues": [
                {
                    "type": ctx.ref.type,
                    "id": ctx.ref.id,
                    "repo": ctx.ref.repo,
                    "title": ctx.title,
                    "description": ctx.description,
                    "labels": ctx.labels,
                    "comments": ctx.comments,
                }
                for ctx in issue_contexts
            ],
            "plan": {"path": plan, "content": plan_content} if plan_content else None,
            "files": [{"path": p, "content": c} for p, c in file_contents.items()],
        }
        typer.echo(json.dumps(data, indent=2))
    else:
        # Markdown output
        if issue_contexts:
            typer.echo("# Related Issues\n")
            for ctx in issue_contexts:
                typer.echo(f"## {ctx.ref.type.upper()}: {ctx.ref.id}")
                typer.echo(f"**Title:** {ctx.title}")
                if ctx.labels:
                    typer.echo(f"**Labels:** {', '.join(filter(None, ctx.labels))}")
                typer.echo(f"\n{ctx.description}\n")
                if ctx.comments:
                    typer.echo("**Comments:**")
                    for comment in ctx.comments[:5]:
                        typer.echo(f"- {comment[:300]}...")
                typer.echo()

        if plan_content:
            typer.echo(f"# Plan: {plan}\n")
            typer.echo(plan_content)
            typer.echo()

        if file_contents:
            typer.echo("# Referenced Files\n")
            for path, content in file_contents.items():
                typer.echo(f"## {path}")
                typer.echo(f"```\n{content[:2000]}\n```")
                typer.echo()


if __name__ == "__main__":
    app()
