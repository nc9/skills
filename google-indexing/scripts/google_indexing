#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-api-python-client",
#     "google-auth",
#     "google-auth-httplib2",
#     "python-dotenv",
#     "typer",
# ]
# ///
"""Google Indexing API — submit, remove, and check URL indexing status."""

from __future__ import annotations

import json
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import typer
from dotenv import load_dotenv

app = typer.Typer(help="Google Indexing API: submit, remove, status, quota")


# --- Types ---


class OutputFormat(str, Enum):
    json = "json"
    table = "table"


# --- Helpers ---


def loadKeyFile(key_file: str | None = None) -> str:
    """Resolve service account JSON key path: arg → env → .env chain."""
    if key_file:
        p = Path(key_file)
        if not p.exists():
            typer.echo(f"Error: key file not found: {key_file}", err=True)
            raise typer.Exit(1)
        return key_file

    val = os.getenv("GOOGLE_INDEXING_KEY_FILE")
    if val:
        return val

    env_paths = [
        Path.cwd() / ".env",
        Path.home() / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            val = os.getenv("GOOGLE_INDEXING_KEY_FILE")
            if val:
                return val

    typer.echo(
        "Error: GOOGLE_INDEXING_KEY_FILE not found. Set it via:\n"
        "  - CLI flag: --key-file /path/to/key.json\n"
        "  - Environment variable: export GOOGLE_INDEXING_KEY_FILE=/path/to/key.json\n"
        "  - .env file with GOOGLE_INDEXING_KEY_FILE=/path/to/key.json",
        err=True,
    )
    raise typer.Exit(1)


def buildService(key_file: str):
    """Build authenticated Indexing API service."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    scopes = ["https://www.googleapis.com/auth/indexing"]
    creds = service_account.Credentials.from_service_account_file(
        key_file, scopes=scopes
    )
    return build("indexing", "v3", credentials=creds, cache_discovery=False)


def readUrls(
    urls: list[str] | None = None,
    file: str | None = None,
) -> list[str]:
    """Resolve URLs from args, --file, or stdin pipe."""
    result: list[str] = []

    if urls:
        result.extend(urls)

    if file:
        p = Path(file)
        if not p.exists():
            typer.echo(f"Error: file not found: {file}", err=True)
            raise typer.Exit(1)
        lines = p.read_text().splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)

    if not result and not sys.stdin.isatty():
        for line in sys.stdin:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                result.append(stripped)

    if not result:
        typer.echo(
            "Error: no URLs provided. Pass as arguments, --file, or pipe via stdin.",
            err=True,
        )
        raise typer.Exit(1)

    return result


def checkUrls(urls: list[str]) -> list[str]:
    """Check URLs are live. Exits on 404, warns on other 4xx, returns valid URLs."""
    valid: list[str] = []
    has_404 = False

    for url in urls:
        try:
            req = Request(url, method="HEAD")
            req.add_header("User-Agent", "Mozilla/5.0 (compatible; Googlebot/2.1)")
            with urlopen(req, timeout=10):
                valid.append(url)
        except HTTPError as e:
            if e.code == 404:
                typer.echo(f"Error: 404 Not Found — {url}", err=True)
                has_404 = True
            elif 400 <= e.code < 500:
                typer.echo(
                    f"Warning: {e.code} for {url} (likely bot detection, Google crawler should be fine)",
                    err=True,
                )
                valid.append(url)
            else:
                typer.echo(f"Warning: {e.code} for {url}", err=True)
                valid.append(url)
        except URLError as e:
            typer.echo(f"Error: cannot reach {url} — {e.reason}", err=True)
            has_404 = True
        except Exception as e:
            typer.echo(f"Warning: could not check {url} — {e}", err=True)
            valid.append(url)

    if has_404:
        typer.echo("\nAborting: fix 404 URLs before submitting to Google.", err=True)
        raise typer.Exit(1)

    return valid


def publishUrls(
    service,
    urls: list[str],
    notification_type: str,
    batch_size: int = 100,
) -> list[dict]:
    """Batch-publish URL notifications. Returns per-URL results."""

    results: list[dict] = []
    batch_size = min(batch_size, 100)

    for chunk_start in range(0, len(urls), batch_size):
        chunk = urls[chunk_start : chunk_start + batch_size]
        batch_results: dict[str, dict] = {}

        def _callback(request_id, response, exception):
            url = request_id
            if exception:
                batch_results[url] = {
                    "url": url,
                    "success": False,
                    "type": notification_type,
                    "notify_time": None,
                    "error": str(exception),
                }
            else:
                # publish returns urlNotificationMetadata at top level
                # or nested — handle both
                meta = response.get("urlNotificationMetadata", response)
                latest = meta.get("latestUpdate", meta.get("latestRemove", {})) or {}
                notify_time = latest.get("notifyTime") or response.get("notifyTime")
                batch_results[url] = {
                    "url": url,
                    "success": True,
                    "type": notification_type,
                    "notify_time": notify_time,
                    "error": None,
                }

        batch = service.new_batch_http_request(callback=_callback)
        for url in chunk:
            body = {"url": url, "type": notification_type}
            batch.add(
                service.urlNotifications().publish(body=body),
                request_id=url,
            )
        try:
            batch.execute()
        except Exception as e:
            for url in chunk:
                if url not in batch_results:
                    batch_results[url] = {
                        "url": url,
                        "success": False,
                        "type": notification_type,
                        "notify_time": None,
                        "error": str(e),
                    }

        # preserve order
        for url in chunk:
            results.append(
                batch_results.get(
                    url,
                    {
                        "url": url,
                        "success": False,
                        "type": notification_type,
                        "notify_time": None,
                        "error": "Unknown error",
                    },
                )
            )

    return results


def getStatus(service, urls: list[str]) -> list[dict]:
    """Get notification metadata for each URL."""
    results: list[dict] = []
    for url in urls:
        try:
            meta = service.urlNotifications().getMetadata(url=url).execute()
            latest_update = meta.get("latestUpdate")
            latest_remove = meta.get("latestRemove")
            results.append(
                {
                    "url": url,
                    "latest_update": {
                        "type": latest_update.get("type"),
                        "notify_time": latest_update.get("notifyTime"),
                    }
                    if latest_update
                    else None,
                    "latest_remove": {
                        "type": latest_remove.get("type"),
                        "notify_time": latest_remove.get("notifyTime"),
                    }
                    if latest_remove
                    else None,
                    "error": None,
                }
            )
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "permission" in error_msg.lower():
                error_msg += (
                    " (Hint: ensure service account is Owner in Search Console)"
                )
            results.append(
                {
                    "url": url,
                    "latest_update": None,
                    "latest_remove": None,
                    "error": error_msg,
                }
            )
    return results


def formatSubmitTable(command: str, results: list[dict]) -> str:
    """Format submit/remove results as table."""
    succeeded = sum(1 for r in results if r["success"])
    failed = len(results) - succeeded
    lines = [
        f"{'Command':<12} {command}",
        f"{'Total':<12} {len(results)}",
        f"{'Succeeded':<12} {succeeded}",
        f"{'Failed':<12} {failed}",
        "",
        f"{'URL':<60} {'Status':<10} {'Time':<25}",
        "-" * 95,
    ]
    for r in results:
        status = "OK" if r["success"] else "FAIL"
        time = r["notify_time"] or (r.get("error") or "")[:25]
        lines.append(f"{r['url'][:60]:<60} {status:<10} {time:<25}")
    return "\n".join(lines)


def formatStatusTable(results: list[dict]) -> str:
    """Format status results as table."""
    lines = [
        f"{'URL':<55} {'Last Update':<25} {'Last Remove':<25}",
        "-" * 105,
    ]
    for r in results:
        if r["error"]:
            lines.append(f"{r['url'][:55]:<55} ERROR: {r['error'][:45]}")
            continue
        update = r["latest_update"]["notify_time"] if r["latest_update"] else "-"
        remove = r["latest_remove"]["notify_time"] if r["latest_remove"] else "-"
        lines.append(f"{r['url'][:55]:<55} {update:<25} {remove:<25}")
    return "\n".join(lines)


def _publishCommand(
    command: str,
    notification_type: str,
    urls: list[str] | None,
    key_file: str | None,
    format: OutputFormat,
    file: str | None,
    batch_size: int,
) -> None:
    """Shared logic for submit and remove commands."""
    resolved = readUrls(urls, file)
    resolved = checkUrls(resolved)
    kf = loadKeyFile(key_file)
    service = buildService(kf)
    results = publishUrls(service, resolved, notification_type, batch_size)

    succeeded = sum(1 for r in results if r["success"])
    output = {
        "command": command,
        "total": len(results),
        "succeeded": succeeded,
        "failed": len(results) - succeeded,
        "results": results,
    }

    if format == OutputFormat.table:
        typer.echo(formatSubmitTable(command, results))
    else:
        typer.echo(json.dumps(output, indent=2))


# --- Commands ---


@app.command()
def submit(
    urls: Annotated[Optional[list[str]], typer.Argument(help="URLs to submit")] = None,
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
    file: Annotated[
        Optional[str], typer.Option("--file", help="File with URLs, one per line")
    ] = None,
    batch_size: Annotated[
        int, typer.Option("--batch-size", "-b", help="Batch size (max 100)")
    ] = 100,
) -> None:
    """Notify Google that URLs are new or updated (URL_UPDATED)."""
    _publishCommand("submit", "URL_UPDATED", urls, key_file, format, file, batch_size)


@app.command()
def remove(
    urls: Annotated[Optional[list[str]], typer.Argument(help="URLs to remove")] = None,
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
    file: Annotated[
        Optional[str], typer.Option("--file", help="File with URLs, one per line")
    ] = None,
    batch_size: Annotated[
        int, typer.Option("--batch-size", "-b", help="Batch size (max 100)")
    ] = 100,
) -> None:
    """Notify Google that URLs have been deleted (URL_DELETED)."""
    _publishCommand("remove", "URL_DELETED", urls, key_file, format, file, batch_size)


@app.command()
def status(
    urls: Annotated[Optional[list[str]], typer.Argument(help="URLs to check")] = None,
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
    file: Annotated[
        Optional[str], typer.Option("--file", help="File with URLs, one per line")
    ] = None,
) -> None:
    """Check last notification timestamps for URLs."""
    resolved = readUrls(urls, file)
    kf = loadKeyFile(key_file)
    service = buildService(kf)
    results = getStatus(service, resolved)

    if format == OutputFormat.table:
        typer.echo(formatStatusTable(results))
    else:
        typer.echo(json.dumps({"results": results}, indent=2))


@app.command()
def quota(
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """Display API quota limits (static, no API call needed)."""
    data = {
        "quotas": [
            {
                "name": "Publish requests",
                "limit": 200,
                "period": "per day",
                "resets": "midnight PT",
            },
            {
                "name": "Metadata reads",
                "limit": 600,
                "period": "per minute",
                "resets": "rolling",
            },
            {
                "name": "Batch size",
                "limit": 100,
                "period": "per request",
                "resets": "n/a",
            },
        ]
    }

    if format == OutputFormat.table:
        lines = [
            f"{'Quota':<25} {'Limit':>8} {'Period':<15} {'Resets':<15}",
            "-" * 65,
        ]
        for q in data["quotas"]:
            lines.append(
                f"{q['name']:<25} {q['limit']:>8} {q['period']:<15} {q['resets']:<15}"
            )
        typer.echo("\n".join(lines))
    else:
        typer.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    app()
