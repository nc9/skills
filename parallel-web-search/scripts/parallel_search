#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "parallel-web",
#     "python-dotenv",
#     "typer",
# ]
# ///
"""
Parallel Web Search Skill

Performs agentic web search using Parallel AI API.
Optimized for LLM consumption with concise, token-efficient results.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Annotated

import typer
from dotenv import load_dotenv
from parallel import Parallel
from parallel._exceptions import APIError

# --- Config ---

DEFAULT_MAX_RESULTS = 10
DEFAULT_MAX_CHARS = 500  # Concise for agentic workflows
DEFAULT_PROCESSOR = "pro"

load_dotenv()

app = typer.Typer(help="Agentic web search using Parallel AI API")


# --- Types ---

class OutputFormat(str, Enum):
    json = "json"
    table = "table"


# --- Models ---

@dataclass
class SearchResult:
    """Normalized search result."""

    title: str
    url: str
    excerpt: str
    publish_date: str | None = None


@dataclass
class SearchResponse:
    """Response containing search results."""

    objective: str
    queries: list[str]
    results: list[SearchResult]


# --- Client ---

def getClient() -> Parallel:
    """Create Parallel client from environment."""
    api_key = os.getenv("PARALLEL_API_KEY")

    if not api_key:
        typer.echo("Error: PARALLEL_API_KEY required", err=True)
        raise typer.Exit(1)

    return Parallel(api_key=api_key)


def search(
    client: Parallel,
    objective: str,
    queries: list[str] | None = None,
    max_results: int = DEFAULT_MAX_RESULTS,
    max_chars: int = DEFAULT_MAX_CHARS,
    allowed_domains: list[str] | None = None,
) -> SearchResponse:
    """Perform agentic web search."""
    # Build request params
    params: dict = {
        "objective": objective,
        "max_results": max_results,
        "max_chars_per_result": max_chars,
        "processor": DEFAULT_PROCESSOR,
    }

    # Add search queries if provided (improves results per best practices)
    if queries:
        params["search_queries"] = queries

    # Add domain filter if provided
    if allowed_domains:
        params["source_policy"] = {"allowed_domains": allowed_domains}

    # Execute search
    response = client.beta.search(**params)

    # Parse results
    results = []
    for item in response.results:
        # Handle excerpt - may be string or list
        excerpt = ""
        if hasattr(item, "excerpt") and item.excerpt:
            excerpt = item.excerpt if isinstance(item.excerpt, str) else str(item.excerpt)
        elif hasattr(item, "excerpts") and item.excerpts:
            excerpt = " ".join(str(e) for e in item.excerpts[:3])

        results.append(
            SearchResult(
                title=item.title or "",
                url=item.url or "",
                excerpt=excerpt,
                publish_date=getattr(item, "publish_date", None),
            )
        )

    return SearchResponse(
        objective=objective,
        queries=queries or [],
        results=results,
    )


# --- Formatters ---

def formatTable(response: SearchResponse) -> str:
    """Format search results as table."""
    lines = []
    lines.append(f"Objective: {response.objective}")
    if response.queries:
        lines.append(f"Queries: {', '.join(response.queries)}")
    lines.append("")
    lines.append(f"{'#':<3} {'Title':<50} {'URL':<40}")
    lines.append("-" * 95)

    for i, r in enumerate(response.results, 1):
        title = r.title[:48] + ".." if len(r.title) > 50 else r.title
        url = r.url[:38] + ".." if len(r.url) > 40 else r.url
        lines.append(f"{i:<3} {title:<50} {url:<40}")
        if r.excerpt:
            # Wrap excerpt
            excerpt = r.excerpt[:200] + "..." if len(r.excerpt) > 200 else r.excerpt
            lines.append(f"    {excerpt}")
        lines.append("")

    return "\n".join(lines)


def formatJson(response: SearchResponse) -> str:
    """Format results as JSON for LLM consumption."""
    data = {
        "objective": response.objective,
        "queries": response.queries,
        "results": [
            {
                "title": r.title,
                "url": r.url,
                "excerpt": r.excerpt,
                "publish_date": r.publish_date,
            }
            for r in response.results
        ],
    }
    return json.dumps(data, indent=2)


# --- Commands ---

@app.command("search")
def searchCmd(
    objective: Annotated[str, typer.Option("--objective", "-o", help="Natural language search goal")],
    queries: Annotated[list[str] | None, typer.Option("--query", "-q", help="Additional keyword queries")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n", help="Max results (1-20)")] = DEFAULT_MAX_RESULTS,
    max_chars: Annotated[int, typer.Option("--max-chars", "-c", help="Max chars per excerpt")] = DEFAULT_MAX_CHARS,
    domains: Annotated[list[str] | None, typer.Option("--domain", "-d", help="Allowed domains")] = None,
    format: Annotated[OutputFormat, typer.Option("--format", "-f", help="Output format")] = OutputFormat.json,
) -> None:
    """Perform agentic web search."""
    # Validate limit
    if not 1 <= limit <= 20:
        typer.echo("Error: --limit must be between 1 and 20", err=True)
        raise typer.Exit(1)

    client = getClient()

    try:
        response = search(
            client=client,
            objective=objective,
            queries=queries,
            max_results=limit,
            max_chars=max_chars,
            allowed_domains=domains,
        )

        if format == OutputFormat.table:
            typer.echo(formatTable(response))
        else:
            typer.echo(formatJson(response))

    except APIError as e:
        typer.echo(f"API Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
