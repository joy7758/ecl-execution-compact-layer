#!/usr/bin/env python3
"""Evaluate deterministic field-level mapping coverage for the trace corpus."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import canonical_json, sha256_json
from external.adoption.ecl_mapper import map_to_ecl
from external.adoption.trace_loader import normalize_trace


GENERATED_AT = "2026-06-28T00:00:00Z"
CORPUS = ROOT / "experiments" / "trace_corpus" / "corpus_manifest.json"
REPORT_JSON = ROOT / "experiments" / "out" / "mapping_coverage_evaluation.json"
REPORT_MD = ROOT / "experiments" / "MAPPING_COVERAGE_EVALUATION_v0_1.md"

FIELD_RULES = {
    "openai": {
        "trace_id": ["state"],
        "correlation_id": ["state"],
        "agent": ["state"],
        "model_input": ["intent"],
        "input": ["intent"],
        "reasoning": ["intent"],
        "tool_call": ["action"],
        "trace_events": ["evidence"],
        "spans": ["evidence"],
        "events": ["evidence"],
        "items": ["evidence"],
        "result": ["evidence"],
        "outputs": ["evidence"],
    },
    "langchain": {
        "id": ["state"],
        "run_id": ["state"],
        "name": ["state"],
        "run_type": ["state"],
        "tags": ["state"],
        "metadata": ["state", "intent"],
        "inputs": ["intent"],
        "prompt": ["intent"],
        "child_runs": ["action", "evidence"],
        "serialized": ["action"],
        "tool_input": ["action"],
        "tool_name": ["action"],
        "outputs": ["evidence"],
        "error": ["evidence"],
        "events": ["evidence"],
    },
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    runtime = str(case["runtime"])
    case_id = str(case["case_id"])
    raw_trace = case["trace"]
    envelope = normalize_trace(raw_trace, runtime=runtime, source_ref=f"experiments/trace_corpus/{case_id}")
    mapped = map_to_ecl(envelope, generated_at=GENERATED_AT, checkpoint_ref=f"experiments://{case_id}/checkpoint")
    rules = FIELD_RULES[runtime]
    fields = []
    direct_mapped_count = 0
    hash_only_count = 0
    surfaces: set[str] = set()
    for field_name in sorted(raw_trace):
        field_surfaces = rules.get(field_name, [])
        if field_surfaces:
            retention = "direct_mapping"
            direct_mapped_count += 1
            surfaces.update(field_surfaces)
        else:
            retention = "source_hash_only"
            hash_only_count += 1
        fields.append(
            {
                "field": field_name,
                "retention": retention,
                "surfaces": field_surfaces,
            }
        )
    missing_fields = sorted(mapped["loss"].get("missing_fields", []))
    return {
        "case_id": case_id,
        "runtime": runtime,
        "category": case["category"],
        "field_count": len(fields),
        "direct_mapped_field_count": direct_mapped_count,
        "source_hash_only_field_count": hash_only_count,
        "surface_count": len(surfaces),
        "surfaces": sorted(surfaces),
        "loss_missing_fields": missing_fields,
        "loss_missing_count": len(missing_fields),
        "fields": fields,
        "raw_trace_hash": envelope["raw_trace_hash"],
        "mapping_hash": mapped["mapping_hash"],
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    runtimes = sorted({result["runtime"] for result in results})
    surfaces = ["state", "intent", "action", "evidence"]
    return {
        "case_count": len(results),
        "runtime_count": len(runtimes),
        "by_runtime": {
            runtime: sum(1 for result in results if result["runtime"] == runtime)
            for runtime in runtimes
        },
        "total_source_fields": sum(result["field_count"] for result in results),
        "direct_mapped_field_count": sum(result["direct_mapped_field_count"] for result in results),
        "source_hash_only_field_count": sum(result["source_hash_only_field_count"] for result in results),
        "loss_missing_field_count": sum(result["loss_missing_count"] for result in results),
        "cases_with_source_hash_only_fields": sum(1 for result in results if result["source_hash_only_field_count"]),
        "cases_with_loss": sum(1 for result in results if result["loss_missing_count"]),
        "surface_presence": {
            surface: sum(1 for result in results if surface in result["surfaces"])
            for surface in surfaces
        },
        "surface_presence_by_runtime": {
            runtime: {
                surface: sum(
                    1
                    for result in results
                    if result["runtime"] == runtime and surface in result["surfaces"]
                )
                for surface in surfaces
            }
            for runtime in runtimes
        },
    }


def markdown_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    rows = [
        "| Case | Runtime | Fields | Direct mapped | Source hash only | Loss fields |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for result in payload["results"]:
        loss = ",".join(result["loss_missing_fields"]) if result["loss_missing_fields"] else "none"
        rows.append(
            f"| `{result['case_id']}` | {result['runtime']} | {result['field_count']} | {result['direct_mapped_field_count']} | {result['source_hash_only_field_count']} | {loss} |"
        )
    return (
        "# ECL Mapping Coverage Evaluation v0.1\n\n"
        "Status: synthetic_mapping_coverage_evaluated\n\n"
        "Scope: This evaluates field-level coverage over the local synthetic trace corpus. Direct mapping means a source top-level field maps to an ECL surface. Source-hash-only means the source field is not projected into a surface but remains covered by the raw trace hash. This is not production trace evidence, third-party validation, or benchmark evidence.\n\n"
        "## Summary\n\n"
        f"- Cases: {summary['case_count']}\n"
        f"- Runtimes: {summary['by_runtime']}\n"
        f"- Total source fields: {summary['total_source_fields']}\n"
        f"- Direct mapped source fields: {summary['direct_mapped_field_count']}\n"
        f"- Source-hash-only fields: {summary['source_hash_only_field_count']}\n"
        f"- Loss missing fields: {summary['loss_missing_field_count']}\n"
        f"- Cases with source-hash-only fields: {summary['cases_with_source_hash_only_fields']}\n"
        f"- Cases with loss: {summary['cases_with_loss']}\n"
        f"- Surface presence: {summary['surface_presence']}\n"
        f"- Surface presence by runtime: {summary['surface_presence_by_runtime']}\n"
        f"- Evaluation hash: {payload['evaluation_hash']}\n\n"
        "## Case Results\n\n"
        + "\n".join(rows)
        + "\n\n## Boundary\n\n"
        "```text\n"
        "synthetic_corpus=true\n"
        "external_api_calls=false\n"
        "third_party_validation=false\n"
        "benchmark_result=false\n"
        "```\n"
    )


def main() -> int:
    manifest = read_json(CORPUS)
    cases = manifest["cases"]
    results = [evaluate_case(case) for case in cases]
    payload = {
        "schema_version": "0.1.0",
        "object_type": "ecl_mapping_coverage_evaluation",
        "generated_at": GENERATED_AT,
        "corpus": str(CORPUS),
        "corpus_hash": sha256_json(manifest),
        "summary": summarize(results),
        "results": results,
        "field_rules": FIELD_RULES,
        "boundary": {
            "synthetic_corpus": True,
            "external_api_calls": False,
            "third_party_validation": False,
            "benchmark_result": False,
        },
    }
    payload["evaluation_hash"] = sha256_json(payload)
    write_json(REPORT_JSON, payload)
    write_text(REPORT_MD, markdown_report(payload))
    print(canonical_json({"evaluation_hash": payload["evaluation_hash"], "summary": payload["summary"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
