"""Fetch summary data from each service in parallel."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from config.settings import settings

logger = logging.getLogger(__name__)

TIMEOUT = 10.0


async def _fetch(
    client: httpx.AsyncClient,
    name: str,
    url: str,
    headers: dict[str, str],
) -> dict[str, Any] | None:
    try:
        resp = await client.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        logger.warning("Failed to fetch %s from %s", name, url, exc_info=True)
        return None


async def fetch_dashboard(auth_headers: dict[str, str]) -> dict[str, Any]:
    """Call every service's summary endpoint and return aggregated results."""
    fwd = {
        k: v
        for k, v in auth_headers.items()
        if k.lower().startswith("remote-")
    }

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            _fetch(client, "journal", f"{settings.journal_url}/api/v1/stats", fwd),
            _fetch(client, "finance", f"{settings.finance_url}/api/v1/stats/overview", fwd),
            _fetch(client, "wine", f"{settings.wine_url}/api/v1/stats/overview", fwd),
            _fetch(client, "pipeline", f"{settings.pipeline_url}/api/status", fwd),
            _fetch(client, "music", f"{settings.music_url}/api/v1/stats/overview", fwd),
            _fetch(client, "locations", f"{settings.locations_url}/api/v1/stats/overview", fwd),
        )

    keys = ["journal", "finance", "wine", "pipeline", "music", "locations"]
    return {k: v for k, v in zip(keys, results)}
