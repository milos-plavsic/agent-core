"""Confidence-gated eval loop for LangGraph and plain-Python services."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypedDict

from agent_core.evals import score_text_answer
from agent_core.policy import confidence_label, decide_loop


class LoopState(TypedDict, total=False):
    task: str
    context: str
    answer: str
    iteration: int
    max_iterations: int
    confidence_threshold: float
    confidence_score: float
    confidence_label: str
    continue_loop: bool
    stop_reason: str
    trace_events: list[dict[str, Any]]


Proposer = Callable[[LoopState], str]
ContextFetcher = Callable[[str], str]


def run_confidence_loop(
    *,
    task: str,
    fetch_context: ContextFetcher,
    propose: Proposer,
    confidence_threshold: float = 0.72,
    max_iterations: int = 3,
) -> LoopState:
    """Run propose → score → gate until confidence or iteration limit."""
    state: LoopState = {
        "task": task,
        "context": "",
        "answer": "",
        "iteration": 0,
        "max_iterations": max_iterations,
        "confidence_threshold": confidence_threshold,
        "confidence_score": 0.0,
        "trace_events": [],
    }

    while True:
        state["iteration"] = int(state.get("iteration", 0)) + 1
        state["context"] = fetch_context(task)
        state["answer"] = propose(state)
        ev = score_text_answer(state["answer"], state["context"], state["iteration"])
        state["confidence_score"] = float(ev["confidence_score"])
        state["confidence_label"] = confidence_label(state["confidence_score"])
        decision = decide_loop(
            confidence_score=state["confidence_score"],
            confidence_threshold=confidence_threshold,
            iteration=state["iteration"],
            max_iterations=max_iterations,
        )
        state["continue_loop"] = decision["continue_loop"]
        state["stop_reason"] = decision["stop_reason"]
        state["trace_events"].append(
            {
                "iteration": state["iteration"],
                "confidence": state["confidence_score"],
                "stop_reason": state["stop_reason"],
            }
        )
        if not state["continue_loop"]:
            break

    return state
