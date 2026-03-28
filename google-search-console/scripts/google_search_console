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
"""Google Search Console — inspect URLs, search analytics, sitemaps, and properties."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

app = typer.Typer(help="Google Search Console: inspect, performance, sitemaps, sites")


# --- Types ---


class OutputFormat(str, Enum):
    json = "json"
    table = "table"


# --- Helpers ---


def loadKeyFile(key_file: str | None = None) -> str:
    """Resolve service account JSON key path: arg -> env -> .env chain."""
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


def buildService(key_file: str):
    """Build authenticated Search Console API service."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(
        key_file, scopes=scopes
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def handleApiError(e: Exception) -> None:
    """Handle Google API errors with helpful messages."""
    from googleapiclient.errors import HttpError

    if isinstance(e, HttpError):
        status = e.resp.status
        msg = str(e)
        if "accessNotConfigured" in msg or "has not been used" in msg:
            typer.echo(
                "Error: Search Console API not enabled for this project.\n"
                "Enable it at: https://console.developers.google.com/apis/api/searchconsole.googleapis.com/overview",
                err=True,
            )
        elif status == 403:
            typer.echo(
                f"Error: Permission denied. Ensure service account has access in Search Console.\n{msg}",
                err=True,
            )
        elif status == 429:
            typer.echo("Error: API quota exceeded. Try again later.", err=True)
        else:
            typer.echo(f"Error: API returned {status}: {msg}", err=True)
    else:
        typer.echo(f"Error: {e}", err=True)
    raise typer.Exit(1)


def fetchSites(key_file: str) -> list[dict]:
    """Fetch all verified Search Console properties."""
    service = buildService(key_file)
    try:
        resp = service.sites().list().execute()
    except Exception as e:
        handleApiError(e)
    entries = resp.get("siteEntry", [])
    return [
        {
            "site_url": e.get("siteUrl"),
            "permission_level": e.get("permissionLevel"),
        }
        for e in entries
    ]


def hintSites(key_file: str) -> None:
    """Print available sites as a hint when --site is missing."""
    try:
        sites = fetchSites(key_file)
        if sites:
            typer.echo("\nAvailable properties:", err=True)
            for s in sites:
                typer.echo(f"  {s['site_url']}", err=True)
    except Exception:
        pass


# --- Inspect ---


def inspectUrls(service, urls: list[str], site_url: str) -> list[dict]:
    """Inspect indexing status for each URL."""
    results: list[dict] = []
    for url in urls:
        try:
            body = {"inspectionUrl": url, "siteUrl": site_url}
            resp = service.urlInspection().index().inspect(body=body).execute()
            result = resp.get("inspectionResult", {})
            index_status = result.get("indexStatusResult", {})

            results.append(
                {
                    "url": url,
                    "verdict": index_status.get("verdict"),
                    "coverage_state": index_status.get("coverageState"),
                    "last_crawl_time": index_status.get("lastCrawlTime"),
                    "page_fetch_state": index_status.get("pageFetchState"),
                    "robots_txt_state": index_status.get("robotsTxtState"),
                    "indexing_state": index_status.get("indexingState"),
                    "google_canonical": index_status.get("googleCanonical"),
                    "user_canonical": index_status.get("userCanonical"),
                    "crawled_as": index_status.get("crawledAs"),
                    "referring_urls": index_status.get("referringUrls", []),
                    "sitemaps": index_status.get("sitemap", []),
                    "error": None,
                }
            )
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "permission" in error_msg.lower():
                error_msg += (
                    " (Hint: ensure service account has access in Search Console)"
                )
            results.append(
                {
                    "url": url,
                    "verdict": None,
                    "coverage_state": None,
                    "last_crawl_time": None,
                    "page_fetch_state": None,
                    "robots_txt_state": None,
                    "indexing_state": None,
                    "google_canonical": None,
                    "user_canonical": None,
                    "crawled_as": None,
                    "referring_urls": [],
                    "sitemaps": [],
                    "error": error_msg,
                }
            )
    return results


def formatInspectTable(results: list[dict]) -> str:
    """Format inspect results as table."""
    lines = [
        f"{'URL':<55} {'Verdict':<10} {'Fetch':<12} {'Indexing':<20} {'Crawled':<8}",
        "-" * 105,
    ]
    for r in results:
        if r["error"]:
            lines.append(f"{r['url'][:55]:<55} ERROR: {r['error'][:48]}")
            continue
        verdict = r["verdict"] or "-"
        fetch = r["page_fetch_state"] or "-"
        indexing = r["indexing_state"] or "-"
        crawled = r["crawled_as"] or "-"
        lines.append(
            f"{r['url'][:55]:<55} {verdict:<10} {fetch:<12} {indexing:<20} {crawled:<8}"
        )
    return "\n".join(lines)


# --- Performance ---


def queryPerformance(
    service,
    site_url: str,
    start_date: str,
    end_date: str,
    dimension: str = "query",
    query_filter: str | None = None,
    page_filter: str | None = None,
    limit: int = 1000,
) -> dict:
    """Query search analytics data."""
    body: dict = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": [dimension],
        "rowLimit": min(limit, 25000),
    }

    filters = []
    if query_filter:
        filters.append(
            {"dimension": "query", "operator": "contains", "expression": query_filter}
        )
    if page_filter:
        filters.append(
            {"dimension": "page", "operator": "contains", "expression": page_filter}
        )
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]

    try:
        resp = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    except Exception as e:
        handleApiError(e)
    rows = resp.get("rows", [])

    return {
        "site": site_url,
        "start_date": start_date,
        "end_date": end_date,
        "dimension": dimension,
        "rows": [
            {
                "keys": row.get("keys", []),
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0), 4),
                "position": round(row.get("position", 0), 1),
            }
            for row in rows
        ],
    }


def formatPerformanceTable(data: dict) -> str:
    """Format performance data as table."""
    dimension = data["dimension"]
    lines = [
        f"Site: {data['site']}  |  {data['start_date']} to {data['end_date']}  |  Dimension: {dimension}",
        "",
        f"{'Key':<50} {'Clicks':>8} {'Impressions':>12} {'CTR':>8} {'Position':>10}",
        "-" * 90,
    ]
    for row in data["rows"]:
        key = ", ".join(row["keys"])[:50]
        ctr_pct = f"{row['ctr'] * 100:.1f}%"
        lines.append(
            f"{key:<50} {row['clicks']:>8,} {row['impressions']:>12,} {ctr_pct:>8} {row['position']:>10.1f}"
        )
    if not data["rows"]:
        lines.append("  (no data)")
    return "\n".join(lines)


# --- Sitemaps ---


def listSitemaps(service, site_url: str) -> list[dict]:
    """List submitted sitemaps for a property."""
    try:
        resp = service.sitemaps().list(siteUrl=site_url).execute()
    except Exception as e:
        handleApiError(e)
    entries = resp.get("sitemap", [])
    return [
        {
            "path": e.get("path"),
            "last_submitted": e.get("lastSubmitted"),
            "last_downloaded": e.get("lastDownloaded"),
            "is_pending": e.get("isPending", False),
            "is_sitemaps_index": e.get("isSitemapsIndex", False),
            "warnings": int(e.get("warnings", 0)),
            "errors": int(e.get("errors", 0)),
        }
        for e in entries
    ]


def formatSitemapsTable(sitemaps: list[dict]) -> str:
    """Format sitemaps as table."""
    lines = [
        f"{'Path':<60} {'Submitted':<22} {'Warnings':>8} {'Errors':>8}",
        "-" * 100,
    ]
    for s in sitemaps:
        submitted = (s["last_submitted"] or "-")[:22]
        lines.append(
            f"{s['path'][:60]:<60} {submitted:<22} {s['warnings']:>8} {s['errors']:>8}"
        )
    if not sitemaps:
        lines.append("  (no sitemaps)")
    return "\n".join(lines)


# --- Sites ---


def formatSitesTable(sites: list[dict]) -> str:
    """Format sites as table."""
    lines = [
        f"{'Site URL':<50} {'Permission':<20}",
        "-" * 70,
    ]
    for s in sites:
        lines.append(f"{s['site_url'][:50]:<50} {s['permission_level']:<20}")
    if not sites:
        lines.append("  (no sites)")
    return "\n".join(lines)


# --- Commands ---


@app.command()
def inspect(
    urls: Annotated[Optional[list[str]], typer.Argument(help="URLs to inspect")] = None,
    site: Annotated[
        Optional[str],
        typer.Option(
            "--site", "-s", help="Search Console property (e.g. sc-domain:example.com)"
        ),
    ] = None,
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
    """Check URL indexing status (verdict, crawl state, canonical, mobile)."""
    kf = loadKeyFile(key_file)

    if not site:
        typer.echo(
            "Error: --site is required (e.g. --site sc-domain:example.com)", err=True
        )
        hintSites(kf)
        raise typer.Exit(1)

    resolved = readUrls(urls, file)
    service = buildService(kf)
    results = inspectUrls(service, resolved, site)

    if format == OutputFormat.table:
        typer.echo(formatInspectTable(results))
    else:
        typer.echo(json.dumps({"site": site, "results": results}, indent=2))


@app.command()
def performance(
    site: Annotated[
        Optional[str],
        typer.Option(
            "--site", "-s", help="Search Console property (e.g. sc-domain:example.com)"
        ),
    ] = None,
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
    dimension: Annotated[
        str,
        typer.Option(
            "--dimension", "-d", help="Dimension: query, page, country, device, date"
        ),
    ] = "query",
    days: Annotated[
        int, typer.Option("--days", help="Days back from today (default: 28)")
    ] = 28,
    start_date: Annotated[
        Optional[str],
        typer.Option("--start-date", help="Start date YYYY-MM-DD (overrides --days)"),
    ] = None,
    end_date: Annotated[
        Optional[str], typer.Option("--end-date", help="End date YYYY-MM-DD")
    ] = None,
    query: Annotated[
        Optional[str],
        typer.Option("--query", "-q", help="Filter by search query (contains)"),
    ] = None,
    page: Annotated[
        Optional[str],
        typer.Option("--page", "-p", help="Filter by page URL (contains)"),
    ] = None,
    limit: Annotated[
        int, typer.Option("--limit", "-n", help="Max rows (up to 25000)")
    ] = 1000,
) -> None:
    """Search analytics — top queries, pages, clicks, impressions, CTR, position."""
    kf = loadKeyFile(key_file)

    if not site:
        typer.echo(
            "Error: --site is required (e.g. --site sc-domain:example.com)", err=True
        )
        hintSites(kf)
        raise typer.Exit(1)

    if start_date:
        sd = start_date
    else:
        sd = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    ed = end_date or datetime.now().strftime("%Y-%m-%d")

    service = buildService(kf)
    data = queryPerformance(service, site, sd, ed, dimension, query, page, limit)

    if format == OutputFormat.table:
        typer.echo(formatPerformanceTable(data))
    else:
        typer.echo(json.dumps(data, indent=2))


@app.command()
def sitemaps(
    site: Annotated[
        Optional[str],
        typer.Option(
            "--site", "-s", help="Search Console property (e.g. sc-domain:example.com)"
        ),
    ] = None,
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """List submitted sitemaps for a property."""
    kf = loadKeyFile(key_file)

    if not site:
        typer.echo(
            "Error: --site is required (e.g. --site sc-domain:example.com)", err=True
        )
        hintSites(kf)
        raise typer.Exit(1)

    service = buildService(kf)
    results = listSitemaps(service, site)

    if format == OutputFormat.table:
        typer.echo(formatSitemapsTable(results))
    else:
        typer.echo(json.dumps({"site": site, "sitemaps": results}, indent=2))


@app.command()
def sites(
    key_file: Annotated[
        Optional[str],
        typer.Option("--key-file", "-k", help="Service account JSON key path"),
    ] = None,
    format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Output format")
    ] = OutputFormat.json,
) -> None:
    """List verified Search Console properties."""
    kf = loadKeyFile(key_file)
    results = fetchSites(kf)

    if format == OutputFormat.table:
        typer.echo(formatSitesTable(results))
    else:
        typer.echo(json.dumps({"sites": results}, indent=2))


if __name__ == "__main__":
    app()
