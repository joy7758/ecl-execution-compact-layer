"""External trace loader for ECL adoption hooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ecl.canonical import sha256_json


SUPPORTED_RUNTIMES = {"openai", "langchain"}


def load_trace(path: str | Path, *, runtime: str) -> dict[str, Any]:
    """Load an external runtime trace into a deterministic normalized envelope."""

    runtime_name = runtime.lower().strip()
    if runtime_name not in SUPPORTED_RUNTIMES:
        raise ValueError(f"unsupported runtime: {runtime}")
    trace_path = Path(path)
    raw_trace = json.loads(trace_path.read_text(encoding="utf-8"))
    return normalize_trace(raw_trace, runtime=runtime_name, source_ref=str(trace_path))


def normalize_trace(raw_trace: dict[str, Any], *, runtime: str, source_ref: str = "memory://trace") -> dict[str, Any]:
    """Normalize runtime-specific trace containers without inferring semantics."""

    runtime_name = runtime.lower().strip()
    if runtime_name == "openai":
        events = raw_trace.get("trace_events") or raw_trace.get("spans") or raw_trace.get("events") or raw_trace.get("items") or []
    elif runtime_name == "langchain":
        events = _flatten_langchain_runs(raw_trace)
    else:
        raise ValueError(f"unsupported runtime: {runtime}")
    if not isinstance(events, list):
        events = []
    normalized_events = [
        {
            "index": index,
            "event_id": str(event.get("event_id") or event.get("span_id") or event.get("run_id") or event.get("id") or f"event-{index:04d}"),
            "event_type": str(event.get("event_type") or event.get("type") or event.get("run_type") or "event"),
            "event_hash": sha256_json(event),
        }
        for index, event in enumerate(events)
        if isinstance(event, dict)
    ]
    return {
        "raw_trace": raw_trace,
        "runtime": runtime_name,
        "source_ref": source_ref,
        "normalized_events": normalized_events,
        "raw_trace_hash": sha256_json(raw_trace),
    }


def _flatten_langchain_runs(run: dict[str, Any]) -> list[dict[str, Any]]:
    event = {key: value for key, value in run.items() if key != "child_runs"}
    events = [event]
    child_runs = run.get("child_runs") or []
    if isinstance(child_runs, list):
        for child in child_runs:
            if isinstance(child, dict):
                events.extend(_flatten_langchain_runs(child))
    return events

