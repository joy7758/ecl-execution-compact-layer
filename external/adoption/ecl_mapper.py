"""Loss-aware external trace to ECL mapper."""

from __future__ import annotations

from typing import Any

from ecl.adapters.langchain import adapt_trace as adapt_langchain_trace
from ecl.adapters.openai_agents import adapt_trace_with_report as adapt_openai_trace_with_report
from ecl.canonical import sha256_json


def map_to_ecl(trace_envelope: dict[str, Any], *, generated_at: str, checkpoint_ref: str) -> dict[str, Any]:
    """Map a normalized external trace envelope into ECL plus loss annotation."""

    runtime = str(trace_envelope["runtime"])
    raw_trace = trace_envelope["raw_trace"]
    source_ref = str(trace_envelope.get("source_ref") or "memory://trace")
    if runtime == "openai":
        payload = adapt_openai_trace_with_report(
            raw_trace,
            source_trace_ref=source_ref,
            generated_at=generated_at,
            checkpoint_ref=checkpoint_ref,
        )
        ecl_record = payload["ecl"]
        loss = _openai_loss_annotation(payload["loss_report"])
    elif runtime == "langchain":
        ecl_record = adapt_langchain_trace(
            raw_trace,
            source_trace_ref=source_ref,
            generated_at=generated_at,
            checkpoint_ref=checkpoint_ref,
        )
        loss = _generic_loss_annotation(
            raw_trace,
            required_fields={
                "model_input": ["inputs"],
                "reasoning": ["metadata", "inputs"],
                "tool_call": ["child_runs"],
                "events": ["child_runs"],
            },
        )
    else:
        raise ValueError(f"unsupported runtime: {runtime}")
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_external_adoption_mapping",
        "runtime": runtime,
        "ecl": ecl_record,
        "loss": loss,
        "mapping": {
            "tool_call": "action",
            "model_input": "intent",
            "reasoning": "intent",
            "runtime_metadata": "state",
            "events": "evidence",
            "outputs": "evidence",
        },
        "deterministic": True,
        "mapping_hash": sha256_json({"runtime": runtime, "ecl": ecl_record, "loss": loss}),
    }


def _openai_loss_annotation(loss_report: dict[str, Any]) -> dict[str, Any]:
    missing = list(loss_report.get("missing_source_fields", []))
    return {
        "type": "structural" if missing else "semantic",
        "missing_fields": sorted(missing),
        "confidence": 1.0 if not missing else 0.75,
    }


def _generic_loss_annotation(raw_trace: dict[str, Any], *, required_fields: dict[str, list[str]]) -> dict[str, Any]:
    missing = []
    for semantic_field, candidate_fields in required_fields.items():
        if not any(field in raw_trace for field in candidate_fields):
            missing.append(semantic_field)
    return {
        "type": "structural" if missing else "semantic",
        "missing_fields": sorted(missing),
        "confidence": 1.0 if not missing else 0.75,
    }
