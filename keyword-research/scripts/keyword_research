#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "dataforseo-client",
#     "python-dotenv",
#     "typer",
# ]
# ///
"""
Keyword Research Skill

Performs keyword research for SEO/blog/news/landing page purposes
using the DataForSEO API.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated

import typer
from dotenv import load_dotenv

import dataforseo_client
from dataforseo_client.api.dataforseo_labs_api import DataforseoLabsApi
from dataforseo_client.models.dataforseo_labs_google_keyword_suggestions_live_request_info import (
    DataforseoLabsGoogleKeywordSuggestionsLiveRequestInfo,
)
from dataforseo_client.models.dataforseo_labs_google_related_keywords_live_request_info import (
    DataforseoLabsGoogleRelatedKeywordsLiveRequestInfo,
)
from dataforseo_client.rest import ApiException

# --- Config ---

DEFAULT_LOCATION_CODE = 2840  # US
DEFAULT_LANGUAGE_CODE = "en"
DEFAULT_LIMIT = 50

load_dotenv()

app = typer.Typer(help="Keyword research using DataForSEO API")


# --- Types ---

class OutputFormat(str, Enum):
    json = "json"
    table = "table"


# --- Models ---

@dataclass
class KeywordResult:
    """Normalized keyword result."""

    keyword: str
    search_volume: int
    cpc: float
    competition: float
    competition_level: str | None = None


@dataclass
class KeywordResponse:
    """Response containing keyword results."""

    keywords: list[KeywordResult]
    seed: str | None = None


# --- Client ---

@dataclass
class DataForSEOClient:
    """Client for DataForSEO API."""

    username: str
    password: str
    location_code: int = DEFAULT_LOCATION_CODE
    language_code: str = DEFAULT_LANGUAGE_CODE
    _config: dataforseo_client.Configuration = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._config = dataforseo_client.Configuration(
            username=self.username,
            password=self.password,
        )

    def getKeywordSuggestions(
        self,
        keyword: str,
        limit: int = DEFAULT_LIMIT,
        include_seed: bool = True,
    ) -> KeywordResponse:
        """Get keyword suggestions for a seed keyword."""
        with dataforseo_client.ApiClient(self._config) as api_client:
            api = DataforseoLabsApi(api_client)
            request = DataforseoLabsGoogleKeywordSuggestionsLiveRequestInfo(
                keyword=keyword,
                location_code=self.location_code,
                language_code=self.language_code,
                include_seed_keyword=include_seed,
                limit=limit,
            )
            response = api.google_keyword_suggestions_live([request])

        return self._parseResponse(response, seed=keyword)

    def getRelatedKeywords(
        self,
        keyword: str,
        limit: int = DEFAULT_LIMIT,
    ) -> KeywordResponse:
        """Get related keywords for a seed keyword."""
        with dataforseo_client.ApiClient(self._config) as api_client:
            api = DataforseoLabsApi(api_client)
            request = DataforseoLabsGoogleRelatedKeywordsLiveRequestInfo(
                keyword=keyword,
                location_code=self.location_code,
                language_code=self.language_code,
                limit=limit,
            )
            response = api.google_related_keywords_live([request])

        return self._parseResponse(response, seed=keyword)

    def _parseResponse(self, response, seed: str | None = None) -> KeywordResponse:
        """Parse API response into normalized KeywordResponse."""
        keywords = []

        if response.tasks:
            for task in response.tasks:
                if task.result:
                    for result in task.result:
                        items = getattr(result, "items", None) or []
                        for item in items:
                            kw_info = getattr(item, "keyword_info", None)
                            if kw_info:
                                keywords.append(
                                    KeywordResult(
                                        keyword=item.keyword,
                                        search_volume=kw_info.search_volume or 0,
                                        cpc=kw_info.cpc or 0.0,
                                        competition=kw_info.competition or 0.0,
                                        competition_level=kw_info.competition_level,
                                    )
                                )

        return KeywordResponse(keywords=keywords, seed=seed)


# --- Helpers ---

def getClient() -> DataForSEOClient:
    """Create client from environment variables."""
    username = os.getenv("DATAFORSEO_USERNAME")
    password = os.getenv("DATAFORSEO_PASSWORD")

    if not username or not password:
        typer.echo(
            "Error: DATAFORSEO_USERNAME and DATAFORSEO_PASSWORD required",
            err=True,
        )
        raise typer.Exit(1)

    return DataForSEOClient(username=username, password=password)


def formatTable(response: KeywordResponse) -> str:
    """Format keyword data as table."""
    lines = []
    lines.append(f"{'Keyword':<40} {'Volume':>10} {'CPC':>8} {'Comp':>6} {'Level':<10}")
    lines.append("-" * 78)

    for kw in response.keywords:
        level = kw.competition_level or "n/a"
        lines.append(
            f"{kw.keyword[:40]:<40} {kw.search_volume:>10,} "
            f"${kw.cpc:>6.2f} {kw.competition:>6.2f} {level:<10}"
        )

    return "\n".join(lines)


def formatJson(results: list[KeywordResponse]) -> str:
    """Format results as JSON for LLM consumption."""
    data = [
        {
            "seed": r.seed,
            "keywords": [
                {
                    "keyword": kw.keyword,
                    "search_volume": kw.search_volume,
                    "cpc": kw.cpc,
                    "competition": kw.competition,
                    "competition_level": kw.competition_level,
                }
                for kw in r.keywords
            ],
        }
        for r in results
    ]
    return json.dumps(data, indent=2)


# --- Commands ---

@app.command()
def suggestions(
    seeds: Annotated[list[str], typer.Argument(help="Seed keywords to research")],
    limit: Annotated[int, typer.Option("--limit", "-n", help="Max results per seed")] = DEFAULT_LIMIT,
    format: Annotated[OutputFormat, typer.Option("--format", "-f", help="Output format")] = OutputFormat.json,
) -> None:
    """Get keyword suggestions for seed keywords."""
    client = getClient()
    results: list[KeywordResponse] = []

    for seed in seeds:
        try:
            response = client.getKeywordSuggestions(seed, limit=limit)
            results.append(response)

            if format == OutputFormat.table:
                typer.echo(f"\n=== {seed} ===\n")
                typer.echo(formatTable(response))

        except ApiException as e:
            typer.echo(f"Error for '{seed}': {e}", err=True)

    if format == OutputFormat.json:
        typer.echo(formatJson(results))


@app.command()
def related(
    seeds: Annotated[list[str], typer.Argument(help="Seed keywords to research")],
    limit: Annotated[int, typer.Option("--limit", "-n", help="Max results per seed")] = DEFAULT_LIMIT,
    format: Annotated[OutputFormat, typer.Option("--format", "-f", help="Output format")] = OutputFormat.json,
) -> None:
    """Get related keywords for seed keywords."""
    client = getClient()
    results: list[KeywordResponse] = []

    for seed in seeds:
        try:
            response = client.getRelatedKeywords(seed, limit=limit)
            results.append(response)

            if format == OutputFormat.table:
                typer.echo(f"\n=== {seed} ===\n")
                typer.echo(formatTable(response))

        except ApiException as e:
            typer.echo(f"Error for '{seed}': {e}", err=True)

    if format == OutputFormat.json:
        typer.echo(formatJson(results))


if __name__ == "__main__":
    app()
