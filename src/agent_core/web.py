from __future__ import annotations

import urllib.parse

import httpx


def fetch_wikipedia_summary(topic: str, *, timeout_s: float = 8.0) -> dict[str, object]:
    """Fetch a short Wikipedia extract for live research augmentation."""
    title = topic.strip().replace(" ", "_")
    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + urllib.parse.quote(title, safe="")
    )
    with httpx.Client(timeout=timeout_s) as client:
        resp = client.get(url, headers={"User-Agent": "ResearchAnalyst/1.0"})
        if resp.status_code == 404:
            search_url = "https://en.wikipedia.org/w/api.php"
            search = client.get(
                search_url,
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": topic,
                    "format": "json",
                    "srlimit": 1,
                },
                headers={"User-Agent": "ResearchAnalyst/1.0"},
            )
            search.raise_for_status()
            hits = search.json().get("query", {}).get("search", [])
            if not hits:
                return {"source": "wikipedia", "content": "", "used_fallback": True}
            title = hits[0]["title"].replace(" ", "_")
            url = (
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + urllib.parse.quote(title, safe="")
            )
            resp = client.get(url, headers={"User-Agent": "ResearchAnalyst/1.0"})
        resp.raise_for_status()
        data = resp.json()
    extract = str(data.get("extract", ""))
    return {
        "source": "wikipedia",
        "title": str(data.get("title", topic)),
        "content": extract,
        "url": str(data.get("content_urls", {}).get("desktop", {}).get("page", "")),
        "used_fallback": len(extract) < 40,
        "latency_ms": int(resp.elapsed.total_seconds() * 1000),
    }
