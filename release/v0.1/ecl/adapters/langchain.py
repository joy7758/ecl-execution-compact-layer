"""Adapter from LangChain run JSON to ECL."""

from __future__ import annotations

from typing import Any

from ecl.canonical import make_ecl_record, normalize_status


def _flatten_runs(run: dict[str, Any]) -> list[dict[str, Any]]:
    events = [{k: v for k, v in run.items() if k != "child_runs"}]
    child_runs = run.get("child_runs") or []
    if isinstance(child_runs, list):
        for child in child_runs:
            if isinstance(child, dict):
                events.extend(_flatten_runs(child))
    return events


def _first_tool_run(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in events:
        if str(event.get("run_type") or "").lower() == "tool":
            return event
    return events[0] if events else {}


def adapt_trace(trace: dict[str, Any], *, source_trace_ref: str, generated_at: str, checkpoint_ref: str) -> dict[str, Any]:
    metadata = trace.get("metadata") if isinstance(trace.get("metadata"), dict) else {}
    inputs = trace.get("inputs") if isinstance(trace.get("inputs"), dict) else {}
    outputs = trace.get("outputs") if isinstance(trace.get("outputs"), dict) else {}
    events = _flatten_runs(trace)
    tool_run = _first_tool_run(events)
    parameters = tool_run.get("inputs") if isinstance(tool_run.get("inputs"), dict) else {}
    policy_decisions = metadata.get("policy_decisions") or []
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
    return make_ecl_record(
        adapter_name="langchain_trace",
        source_trace_ref=source_trace_ref,
        source_trace=trace,
        generated_at=generated_at,
        checkpoint_ref=checkpoint_ref,
        actor_ref=str(metadata.get("actor_ref") or trace.get("actor_ref") or "agent:langchain:unknown"),
        persona_ref=str(metadata.get("persona_ref") or trace.get("persona_ref") or "persona:unknown"),
        runtime_ref=str(metadata.get("runtime_ref") or "langchain"),
        correlation_id=str(metadata.get("correlation_id") or trace.get("run_id") or ""),
        intent_summary=str(inputs.get("summary") or trace.get("name") or "LangChain run execution"),
        intent_operation=str(inputs.get("operation") or metadata.get("operation") or trace.get("run_type") or "langchain_run"),
        intent_constraints=inputs.get("constraints") if isinstance(inputs.get("constraints"), dict) else {},
        intent_expected_result=inputs.get("expected_result") if isinstance(inputs.get("expected_result"), dict) else {},
        intent_evidence_requirements=inputs.get("evidence_requirements") if isinstance(inputs.get("evidence_requirements"), dict) else {},
        action_name=str(tool_run.get("name") or trace.get("name") or "langchain_run"),
        action_summary=str(tool_run.get("name") or trace.get("name") or "LangChain run step"),
        execution_mode=str(metadata.get("execution_mode") or "delegated"),
        side_effect_class=str(metadata.get("side_effect_class") or "unknown"),
        tool_ref=str(tool_run.get("name") or "tool:unknown"),
        parameters=parameters,
        result_status=normalize_status(outputs.get("status") or trace.get("status")),
        result_summary=str(outputs.get("summary") or "LangChain run result"),
        output_refs=[str(item) for item in outputs.get("output_refs", [])] if isinstance(outputs.get("output_refs"), list) else [],
        events=events,
        policy_decisions=normalized_decisions,
    )

