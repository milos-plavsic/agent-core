"""Helpers for sequential multi-source researcher nodes."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

StateT = TypeVar("StateT", bound=dict)


def merge_ranked_results(
    state: StateT,
    *,
    results_key: str = "search_results",
    id_key: str = "id",
    score_key: str = "relevance",
    limit: int = 10,
) -> StateT:
    """Deduplicate by id and keep top-scoring rows."""
    rows = list(state.get(results_key, []))
    rows.sort(key=lambda r: float(r.get(score_key, 0)), reverse=True)
    seen: set[str] = set()
    unique: list[dict] = []
    for row in rows:
        rid = str(row.get(id_key, ""))
        if not rid or rid in seen:
            continue
        seen.add(rid)
        unique.append(row)
    return {**state, results_key: unique[:limit]}  # type: ignore[return-value]


def chain_nodes(*nodes: Callable[[StateT], StateT]) -> Callable[[StateT], StateT]:
    """Compose LangGraph node callables left-to-right."""

    def _run(state: StateT) -> StateT:
        cur = state
        for node in nodes:
            cur = node(cur)
        return cur

    return _run
