"""Deterministic helpers for ECL records."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any


ADAPTER_VERSION = "0.1.0"
CANONICALIZATION = "json-sort-keys-no-whitespace"
HASH_ALGORITHM = "sha256"
GENERATED_BY = "ecl-execution-compact-layer"


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for hashing and reproducible artifacts."""

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return "sha256:" + sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_ref(prefix: str, value: Any) -> str:
    digest = sha256_json(value).removeprefix("sha256:")
    return f"{prefix}:{digest[:16]}"


def _short_hash(value: Any) -> str:
    return sha256_json(value).removeprefix("sha256:")[:16]


def build_event_chain(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Build a deterministic hash chain from source trace events."""

    chain: list[dict[str, str]] = []
    previous = "sha256:" + ("0" * 64)
    for index, event in enumerate(events):
        event_id = str(event.get("event_id") or event.get("id") or event.get("span_id") or f"event-{index:04d}")
        event_type = str(event.get("event_type") or event.get("type") or event.get("run_type") or "event")
        event_ref = str(event.get("event_ref") or event.get("ref") or event_id)
        event_hash = sha256_json({"event": event, "index": index})
        chain_hash = sha256_json({"previous": previous, "event_hash": event_hash})
        chain.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "event_ref": event_ref,
                "event_hash": event_hash,
                "chain_hash": chain_hash,
            }
        )
        previous = chain_hash
    if not chain:
        empty_event = {"event_id": "event-0000", "event_type": "empty_trace", "event_ref": "source:empty"}
        event_hash = sha256_json(empty_event)
        chain.append(
            {
                **empty_event,
                "event_hash": event_hash,
                "chain_hash": sha256_json({"previous": previous, "event_hash": event_hash}),
            }
        )
    return chain


def default_source_map() -> list[dict[str, str]]:
    return [
        {
            "ecl_path": "$.state.persona_ref",
            "source_protocol": "POP",
            "source_path": "$.id or $.persona_id",
            "mapping_type": "reference",
        },
        {
            "ecl_path": "$.intent",
            "source_protocol": "AIP",
            "source_path": "$.intent and $.constraints",
            "mapping_type": "normalized_copy",
        },
        {
            "ecl_path": "$.action",
            "source_protocol": "AIP",
            "source_path": "$.action and execution metadata",
            "mapping_type": "normalized_copy",
        },
        {
            "ecl_path": "$.evidence",
            "source_protocol": "ARO",
            "source_path": "trace events, policy decisions, result references, and receipt/evidence refs",
            "mapping_type": "reference",
        },
        {
            "ecl_path": "$.evidence.hashes",
            "source_protocol": "ECL",
            "source_path": "canonical source trace and ECL record",
            "mapping_type": "derived_hash",
        },
    ]


def default_decisions(adapter_name: str) -> list[dict[str, str]]:
    return [
        {
            "decision_id": "ecl-boundary-001",
            "decision": "preserve_protocol_boundaries",
            "reason": "ECL references POP, AIP, and ARO fields without redefining their source schemas.",
        },
        {
            "decision_id": "ecl-adapter-001",
            "decision": f"use_{adapter_name}",
            "reason": "The source trace shape matched this adapter entrypoint.",
        },
        {
            "decision_id": "ecl-determinism-001",
            "decision": "hash_canonical_json",
            "reason": "Every generated ECL record must be reproducible from sorted-key JSON.",
        },
    ]


def normalize_status(value: Any) -> str:
    text = str(value or "unknown").lower()
    if text in {"completed", "blocked", "failed", "partial"}:
        return text
    if text in {"success", "ok", "succeeded"}:
        return "completed"
    if text in {"error", "errored", "exception"}:
        return "failed"
    return "unknown"


def normalize_execution_mode(value: Any) -> str:
    text = str(value or "unknown").lower()
    if text in {"proposal", "direct", "delegated", "simulation"}:
        return text
    return "unknown"


def normalize_side_effect(value: Any) -> str:
    text = str(value or "unknown").lower()
    if text in {"read_only", "state_change", "external_write"}:
        return text
    if text in {"read-only", "read"}:
        return "read_only"
    if text in {"write", "external-write"}:
        return "external_write"
    return "unknown"


def blank_record_hash(record: dict[str, Any]) -> dict[str, Any]:
    copy = deepcopy(record)
    copy["evidence"]["hashes"]["canonical_hash"] = "sha256:" + ("0" * 64)
    return copy


def compute_record_hash(record: dict[str, Any]) -> str:
    return sha256_json(blank_record_hash(record))


def with_record_hash(record: dict[str, Any]) -> dict[str, Any]:
    copy = deepcopy(record)
    copy["evidence"]["hashes"]["canonical_hash"] = "sha256:" + ("0" * 64)
    copy["evidence"]["hashes"]["canonical_hash"] = compute_record_hash(copy)
    return copy


def make_ecl_record(
    *,
    adapter_name: str,
    source_trace_ref: str,
    source_trace: dict[str, Any],
    generated_at: str,
    checkpoint_ref: str,
    actor_ref: str,
    persona_ref: str,
    runtime_ref: str,
    correlation_id: str,
    intent_summary: str,
    intent_operation: str,
    intent_constraints: dict[str, Any],
    intent_expected_result: dict[str, Any],
    intent_evidence_requirements: dict[str, Any],
    action_name: str,
    action_summary: str,
    execution_mode: str,
    side_effect_class: str,
    tool_ref: str,
    parameters: dict[str, Any],
    result_status: str,
    result_summary: str,
    output_refs: list[str],
    events: list[dict[str, Any]],
    policy_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    source_hash = sha256_json(source_trace)
    event_chain = build_event_chain(events)
    event_chain_hash = sha256_json(event_chain)
    trace_ref = str(source_trace.get("trace_id") or source_trace.get("run_id") or source_trace_ref)
    ecl_id = "ecl:" + _short_hash({"adapter": adapter_name, "source": source_hash, "trace_ref": trace_ref})
    action_ref_payload = {"adapter": adapter_name, "action_name": action_name, "tool_ref": tool_ref}
    result_ref_payload = {"adapter": adapter_name, "status": result_status, "summary": result_summary}
    record = {
        "schema_version": "0.1.0-draft",
        "object_type": "ecl_execution_record",
        "ecl_id": ecl_id,
        "lineage": {
            "source_adapter": adapter_name,
            "source_trace_ref": source_trace_ref,
            "source_trace_hash": source_hash,
            "generated_at": generated_at,
            "checkpoint_ref": checkpoint_ref,
        },
        "state": {
            "execution_status": result_status if result_status in {"completed", "blocked", "failed", "partial"} else "partial",
            "lifecycle_phase": "complete" if result_status == "completed" else "audit",
            "actor_ref": actor_ref or "agent:unknown",
            "persona_ref": persona_ref or "persona:unknown",
            "runtime_ref": runtime_ref or adapter_name,
            "correlation_id": correlation_id or stable_ref("correlation", source_trace),
        },
        "intent": {
            "summary": intent_summary or "Unspecified source trace intent",
            "operation": intent_operation or "unspecified_operation",
            "aip_intent_ref": stable_ref("aip-intent", {"summary": intent_summary, "operation": intent_operation}),
            "constraints": intent_constraints or {},
            "expected_result": intent_expected_result or {},
            "evidence_requirements": intent_evidence_requirements or {},
            "raw_ref": stable_ref("raw-intent", source_trace),
        },
        "action": {
            "name": action_name or "unspecified_action",
            "summary": action_summary or action_name or "Unspecified source trace action",
            "execution_mode": normalize_execution_mode(execution_mode),
            "side_effect_class": normalize_side_effect(side_effect_class),
            "tool_ref": tool_ref or "tool:unknown",
            "parameters_hash": sha256_json(parameters or {}),
            "aip_action_ref": stable_ref("aip-action", action_ref_payload),
            "raw_ref": stable_ref("raw-action", action_ref_payload),
        },
        "evidence": {
            "result_status": result_status,
            "result_summary": result_summary or "No result summary supplied by source trace",
            "aip_result_ref": stable_ref("aip-result", result_ref_payload),
            "aro_evidence_ref": stable_ref("aro-evidence", {"source": source_hash, "events": event_chain_hash}),
            "aro_receipt_ref": stable_ref("aro-receipt", {"source": source_hash, "result": result_ref_payload}),
            "output_refs": output_refs or [],
            "trace_refs": [trace_ref],
            "event_chain": event_chain,
            "policy_decisions": policy_decisions,
            "hashes": {
                "canonical_hash": "sha256:" + ("0" * 64),
                "source_trace_hash": source_hash,
                "event_chain_hash": event_chain_hash,
            },
        },
        "determinism": {
            "canonicalization": CANONICALIZATION,
            "hash_algorithm": HASH_ALGORITHM,
            "adapter_version": ADAPTER_VERSION,
            "generated_by": GENERATED_BY,
        },
        "audit": {
            "decisions": default_decisions(adapter_name),
            "source_map": default_source_map(),
            "validation": [
                {
                    "validator": "ecl.validator",
                    "status": "not_run",
                    "report_ref": "out/ecl_artifacts/validator_report.json",
                }
            ],
        },
    }
    return with_record_hash(record)

