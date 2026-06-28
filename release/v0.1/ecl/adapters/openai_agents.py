"""Deterministic OpenAI Agents SDK-like trace to ECL adapter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ecl.canonical import make_ecl_record, normalize_status, sha256_json


DEFAULT_GENERATED_AT = "2026-06-28T00:00:00Z"


def _first_tool_event(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in events:
        event_type = str(event.get("type") or event.get("event_type") or "").lower()
        if "tool" in event_type or event.get("tool") or event.get("name"):
            return event
    return events[0] if events else {}


def _trace_events(trace: dict[str, Any]) -> list[dict[str, Any]]:
    events = trace.get("trace_events") or trace.get("spans") or trace.get("events") or trace.get("items") or []
    if not isinstance(events, list):
        return []
    return [event for event in events if isinstance(event, dict)]


def _model_input(trace: dict[str, Any]) -> dict[str, Any]:
    value = trace.get("model_input") or trace.get("input") or {}
    return value if isinstance(value, dict) else {"value": value}


def _reasoning(trace: dict[str, Any], model_input: dict[str, Any]) -> dict[str, Any]:
    value = trace.get("reasoning") or model_input.get("reasoning") or {}
    return value if isinstance(value, dict) else {"summary": value}


def _tool_call(trace: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    value = trace.get("tool_call")
    if isinstance(value, dict):
        return value
    return _first_tool_event(events)


def build_loss_report(trace: dict[str, Any]) -> dict[str, Any]:
    """Report deterministic mapping loss without mutating source trace or schema."""

    missing_source_fields: list[str] = []
    defaults_used: list[str] = []
    if not isinstance(trace.get("model_input") or trace.get("input"), dict):
        missing_source_fields.append("model_input")
        defaults_used.append("model_input:{}")
    input_obj = trace.get("input") if isinstance(trace.get("input"), dict) else {}
    if not isinstance(trace.get("reasoning"), dict) and "reasoning" not in input_obj:
        missing_source_fields.append("reasoning")
        defaults_used.append("reasoning:model_input")
    if not isinstance(trace.get("tool_call"), dict):
        events = _trace_events(trace)
        if _first_tool_event(events):
            defaults_used.append("tool_call:first_trace_event")
        else:
            missing_source_fields.append("tool_call")
            defaults_used.append("tool_call:{}")
    if not _trace_events(trace):
        missing_source_fields.append("trace_events")
        defaults_used.append("trace_events:[]")
    if not isinstance(trace.get("result"), dict):
        missing_source_fields.append("result")
        defaults_used.append("result:{}")
    return {
        "complete": not missing_source_fields,
        "missing_source_fields": sorted(set(missing_source_fields)),
        "defaults_used": sorted(set(defaults_used)),
        "source_trace_hash": sha256_json(trace),
    }


def _normalized_policy_decisions(trace: dict[str, Any], loss_report: dict[str, Any]) -> list[dict[str, Any]]:
    policy_decisions = trace.get("policy_decisions") or []
    if not isinstance(policy_decisions, list):
        policy_decisions = [policy_decisions]
    normalized_decisions = []
    for index, decision in enumerate(policy_decisions):
        if isinstance(decision, dict):
            normalized_decisions.append(
                {
                    "decision_ref": str(decision.get("decision_ref") or decision.get("policy_id") or f"policy-{index:04d}"),
                    "decision": str(decision.get("decision") or "unknown"),
                    "reason": str(decision.get("reason") or decision.get("decision_reason") or ""),
                }
            )
    normalized_decisions.append(
        {
            "decision_ref": "adapter-loss-report",
            "decision": "mapping_complete" if loss_report["complete"] else "mapping_incomplete",
            "reason": "Deterministic OpenAI trace to ECL mapping loss report.",
            "loss_report": loss_report,
        }
    )
    return normalized_decisions


def adapt_trace(trace: dict[str, Any], *, source_trace_ref: str, generated_at: str, checkpoint_ref: str) -> dict[str, Any]:
    agent = trace.get("agent") if isinstance(trace.get("agent"), dict) else {}
    model_input = _model_input(trace)
    reasoning = _reasoning(trace, model_input)
    result = trace.get("result") if isinstance(trace.get("result"), dict) else {}
    events = _trace_events(trace)
    tool_event = _tool_call(trace, events)
    parameters = tool_event.get("parameters") or tool_event.get("input") or tool_event.get("arguments") or {}
    if not isinstance(parameters, dict):
        parameters = {"value": parameters}
    loss_report = build_loss_report(trace)
    return make_ecl_record(
        adapter_name="openai_agents_trace",
        source_trace_ref=source_trace_ref,
        source_trace=trace,
        generated_at=generated_at,
        checkpoint_ref=checkpoint_ref,
        actor_ref=str(agent.get("id") or trace.get("actor_ref") or "agent:openai:unknown"),
        persona_ref=str(agent.get("persona_id") or trace.get("persona_ref") or "persona:unknown"),
        runtime_ref=str(agent.get("runtime") or "openai-agents-sdk"),
        correlation_id=str(trace.get("correlation_id") or trace.get("trace_id") or ""),
        intent_summary=str(reasoning.get("summary") or model_input.get("summary") or trace.get("intent_summary") or "OpenAI Agents trace execution"),
        intent_operation=str(reasoning.get("operation") or model_input.get("operation") or trace.get("operation") or "agent_trace_execution"),
        intent_constraints=model_input.get("constraints") if isinstance(model_input.get("constraints"), dict) else {},
        intent_expected_result=model_input.get("expected_result") if isinstance(model_input.get("expected_result"), dict) else {},
        intent_evidence_requirements=model_input.get("evidence_requirements") if isinstance(model_input.get("evidence_requirements"), dict) else {},
        action_name=str(tool_event.get("name") or tool_event.get("tool") or "agent_step"),
        action_summary=str(tool_event.get("summary") or tool_event.get("name") or "OpenAI Agents trace step"),
        execution_mode=str(tool_event.get("execution_mode") or trace.get("execution_mode") or "delegated"),
        side_effect_class=str(tool_event.get("side_effect_class") or trace.get("side_effect_class") or "unknown"),
        tool_ref=str(tool_event.get("tool") or tool_event.get("name") or "tool:unknown"),
        parameters=parameters,
        result_status=normalize_status(result.get("status") or trace.get("status")),
        result_summary=str(result.get("summary") or trace.get("result_summary") or "OpenAI Agents trace result"),
        output_refs=[str(item) for item in result.get("output_refs", [])] if isinstance(result.get("output_refs"), list) else [],
        events=events,
        policy_decisions=_normalized_policy_decisions(trace, loss_report),
    )


def adapt_trace_with_report(
    trace: dict[str, Any], *, source_trace_ref: str, generated_at: str, checkpoint_ref: str
) -> dict[str, Any]:
    loss_report = build_loss_report(trace)
    return {
        "ecl": adapt_trace(
            trace,
            source_trace_ref=source_trace_ref,
            generated_at=generated_at,
            checkpoint_ref=checkpoint_ref,
        ),
        "loss_report": loss_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert an OpenAI Agents SDK-like trace JSON into ECL.")
    parser.add_argument(
        "trace",
        nargs="?",
        type=Path,
        default=Path("tests/fixtures/openai_agents_trace.json"),
        help="Input trace JSON. Defaults to the local OpenAI fixture.",
    )
    parser.add_argument("--out", type=Path, help="Optional output path.")
    parser.add_argument("--generated-at", default=DEFAULT_GENERATED_AT)
    parser.add_argument("--checkpoint-ref", default="state/ecl_goal_state.json")
    args = parser.parse_args()

    trace = json.loads(args.trace.read_text(encoding="utf-8"))
    payload = adapt_trace_with_report(
        trace,
        source_trace_ref=str(args.trace),
        generated_at=args.generated_at,
        checkpoint_ref=args.checkpoint_ref,
    )
    output = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
