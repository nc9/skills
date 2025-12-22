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
Parallel Deep Research Skill

Performs comprehensive deep research using Parallel AI Task API.
Transforms natural language queries into structured intelligence reports.
"""

from __future__ import annotations

import json
import os
from enum import Enum
from typing import Annotated

import typer
from dotenv import load_dotenv
from parallel import Parallel
from parallel._exceptions import APIError

# --- Config ---

DEFAULT_PROCESSOR = "pro-fast"  # Cheaper, 2-5x faster than pro
DEFAULT_TIMEOUT = 600  # 10 min default, can go up to 45 min

load_dotenv()

app = typer.Typer(help="Deep research using Parallel AI Task API")


# --- Types ---


class Processor(str, Enum):
    pro_fast = "pro-fast"
    pro = "pro"
    ultra_fast = "ultra-fast"
    ultra = "ultra"


class OutputFormat(str, Enum):
    json = "json"
    markdown = "markdown"


# --- Client ---


def getClient() -> Parallel:
    """Create Parallel client from environment."""
    api_key = os.getenv("PARALLEL_API_KEY")

    if not api_key:
        typer.echo("Error: PARALLEL_API_KEY required", err=True)
        raise typer.Exit(1)

    return Parallel(api_key=api_key)


def research(
    client: Parallel,
    query: str,
    processor: str = DEFAULT_PROCESSOR,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """Execute deep research task."""
    # Create task
    typer.echo(f"Starting research (processor={processor})...", err=True)

    task_run = client.task_run.create(
        input=query,
        processor=processor,
    )

    typer.echo(f"Task ID: {task_run.run_id}", err=True)
    typer.echo("Waiting for results...", err=True)

    # Wait for result
    result = client.task_run.result(
        run_id=task_run.run_id,
        api_timeout=timeout,
    )

    # Extract output
    output = result.output

    # Build response
    response = {
        "query": query,
        "processor": processor,
        "run_id": task_run.run_id,
        "content": None,
        "basis": None,
    }

    # Handle content - may be dict or string
    if hasattr(output, "content"):
        content = output.content
        if isinstance(content, str):
            # Try to parse as JSON
            try:
                response["content"] = json.loads(content)
            except json.JSONDecodeError:
                response["content"] = content
        else:
            response["content"] = content

    # Handle basis (citations)
    if hasattr(output, "basis"):
        response["basis"] = output.basis

    return response


# --- Formatters ---


def formatJson(response: dict) -> str:
    """Format as JSON for LLM consumption."""
    return json.dumps(response, indent=2, default=str)


def formatMarkdown(response: dict) -> str:
    """Format as markdown for human reading."""
    lines = []

    lines.append(f"# Research: {response['query']}")
    lines.append("")
    lines.append(f"**Processor:** {response['processor']}")
    lines.append(f"**Run ID:** {response['run_id']}")
    lines.append("")

    # Content
    lines.append("## Findings")
    lines.append("")

    content = response.get("content")
    if isinstance(content, dict):
        lines.append("```json")
        lines.append(json.dumps(content, indent=2, default=str))
        lines.append("```")
    elif isinstance(content, str):
        lines.append(content)
    else:
        lines.append("_No content returned_")

    # Basis/Citations
    basis = response.get("basis")
    if basis:
        lines.append("")
        lines.append("## Sources")
        lines.append("")
        if isinstance(basis, list):
            for item in basis[:10]:  # Limit to 10 sources
                if isinstance(item, dict):
                    field = item.get("field", "unknown")
                    excerpts = item.get("excerpts", [])
                    lines.append(f"### {field}")
                    for exc in excerpts[:2]:
                        if isinstance(exc, dict):
                            url = exc.get("url", "")
                            text = exc.get("text", "")[:200]
                            lines.append(f"- [{url}]({url})")
                            if text:
                                lines.append(f"  > {text}...")
                        lines.append("")
        else:
            lines.append("```json")
            lines.append(json.dumps(basis, indent=2, default=str)[:2000])
            lines.append("```")

    return "\n".join(lines)


# --- Commands ---


@app.command("research")
def researchCmd(
    query: Annotated[str, typer.Argument(help="Research query (max 15000 chars)")],
    processor: Annotated[
        Processor, typer.Option("--processor", "-p", help="Model to use")
    ] = Processor.pro_fast,
    timeout: Annotated[
        int, typer.Option("--timeout", "-t", help="Max wait seconds")
    ] = DEFAULT_TIMEOUT,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """Perform deep research on a topic."""
    # Validate query length
    if len(query) > 15000:
        typer.echo("Error: Query must be under 15000 characters", err=True)
        raise typer.Exit(1)

    client = getClient()

    try:
        response = research(
            client=client,
            query=query,
            processor=processor.value,
            timeout=timeout,
        )

        if format == OutputFormat.markdown:
            typer.echo(formatMarkdown(response))
        else:
            typer.echo(formatJson(response))

    except APIError as e:
        typer.echo(f"API Error: {e}", err=True)
        raise typer.Exit(1)
    except TimeoutError:
        typer.echo(f"Error: Research timed out after {timeout}s", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
