"""Minimal ECL SDK v0.1."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import make_ecl_record
from ecl.validator import validate_record
from external.adoption.ecl_mapper import map_to_ecl
from external.adoption.replay_adapter import replay_ecl
from external.adoption.trace_loader import normalize_trace


class ECL:
    """Minimal deterministic SDK facade."""

    GENERATED_AT = "2026-06-28T00:00:00Z"
    SCHEMA_PATH = ROOT / "schemas" / "ecl-execution-compact-layer.schema.json"

    @staticmethod
    def create(state: dict[str, Any], intent: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        """Create an ECL object from structured state, intent, and action inputs."""

        source_trace = {
            "state": state,
            "intent": intent,
            "action": action,
        }
        return make_ecl_record(
            adapter_name="manual_ecl",
            source_trace_ref="sdk://manual-create",
            source_trace=source_trace,
            generated_at=ECL.GENERATED_AT,
            checkpoint_ref="sdk://checkpoint",
            actor_ref=str(state.get("actor_ref") or "agent:sdk:unknown"),
            persona_ref=str(state.get("persona_ref") or "persona:unknown"),
            runtime_ref=str(state.get("runtime_ref") or "sdk"),
            correlation_id=str(state.get("correlation_id") or "sdk-correlation"),
            intent_summary=str(intent.get("summary") or "SDK-created ECL intent"),
            intent_operation=str(intent.get("operation") or "sdk_create"),
            intent_constraints=dict(intent.get("constraints") or {}),
            intent_expected_result=dict(intent.get("expected_result") or {}),
            intent_evidence_requirements=dict(intent.get("evidence_requirements") or {}),
            action_name=str(action.get("name") or "sdk_action"),
            action_summary=str(action.get("summary") or "SDK-created ECL action"),
            execution_mode=str(action.get("execution_mode") or "direct"),
            side_effect_class=str(action.get("side_effect_class") or "read_only"),
            tool_ref=str(action.get("tool_ref") or "tool:sdk"),
            parameters=dict(action.get("parameters") or {}),
            result_status=str(state.get("execution_status") or "completed"),
            result_summary=str(state.get("result_summary") or "SDK-created ECL record."),
            output_refs=list(state.get("output_refs") or []),
            events=list(state.get("events") or [{"event_id": "sdk-0001", "event_type": "sdk_create", "event_ref": "sdk://manual-create"}]),
            policy_decisions=list(state.get("policy_decisions") or []),
        )

    @staticmethod
    def validate(ecl_object: dict[str, Any]) -> dict[str, Any]:
        """Validate an ECL object against the frozen schema and hash rules."""

        import json

        schema = json.loads(ECL.SCHEMA_PATH.read_text(encoding="utf-8"))
        return validate_record(ecl_object, schema)

    @staticmethod
    def replay(ecl_object: dict[str, Any]) -> dict[str, Any]:
        """Replay an ECL object into deterministic local artifacts."""

        return replay_ecl(ecl_object, out_dir=ROOT / "sdk" / "out" / "replay", schema_path=ECL.SCHEMA_PATH)

    @staticmethod
    def to_trace(runtime_output: dict[str, Any]) -> dict[str, Any]:
        """Convert runtime output into a deterministic trace envelope."""

        runtime = str(runtime_output.get("runtime") or "openai")
        raw_trace = runtime_output.get("trace") if isinstance(runtime_output.get("trace"), dict) else runtime_output
        return normalize_trace(raw_trace, runtime=runtime, source_ref=str(runtime_output.get("source_ref") or "sdk://runtime-output"))

    @staticmethod
    def from_trace(trace: dict[str, Any]) -> dict[str, Any]:
        """Convert a trace envelope or runtime output into an ECL object."""

        envelope = trace if {"raw_trace", "runtime", "normalized_events"}.issubset(trace) else ECL.to_trace(trace)
        return map_to_ecl(
            envelope,
            generated_at=ECL.GENERATED_AT,
            checkpoint_ref="sdk://checkpoint",
        )["ecl"]

