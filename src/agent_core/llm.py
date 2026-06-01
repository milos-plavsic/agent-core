from __future__ import annotations

import os

import httpx


def _api_key() -> str:
    return (
        os.environ.get("LLM_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )


def llm_available() -> bool:
    return bool(_api_key())


def complete_text(
    prompt: str,
    *,
    system: str = "You are a concise technical assistant.",
    model: str | None = None,
    max_tokens: int = 800,
) -> str:
    """OpenAI-compatible chat completion; requires LLM_API_KEY (or OPENAI_API_KEY)."""
    api_key = _api_key()
    if not api_key:
        raise RuntimeError("LLM_API_KEY is not set")

    base = (
        os.environ.get("LLM_BASE_URL", "").strip()
        or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    ).rstrip("/")
    model_name = (
        model
        or os.environ.get("LLM_MODEL", "").strip()
        or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    )
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
    return str(data["choices"][0]["message"]["content"]).strip()
