from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def write_run_artifacts(
    *,
    project: str,
    summary: dict[str, Any],
    report_md: str,
    trace_events: list[dict[str, Any]],
    output_dir: Path | None = None,
) -> dict[str, str]:
    """Write standard run artifacts (summary.json, REPORT.md, trace.json)."""
    root = output_dir or Path.cwd() / "reports"
    root.mkdir(parents=True, exist_ok=True)
    trace_dir = root / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)

    summary_path = root / f"{project}-summary.json"
    report_path = root / f"{project}-REPORT.md"
    trace_path = trace_dir / f"{project}-trace.json"

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_path.write_text(report_md, encoding="utf-8")
    trace_path.write_text(
        json.dumps(
            {
                "project": project,
                "generated_at_epoch_s": int(time.time()),
                "events": trace_events,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return {
        "summary": str(summary_path),
        "report": str(report_path),
        "trace": str(trace_path),
    }
