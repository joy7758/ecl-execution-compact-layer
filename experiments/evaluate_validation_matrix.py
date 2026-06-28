#!/usr/bin/env python3
"""Evaluate ECL validator rejection behavior with deterministic mutations."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import canonical_json, sha256_json
from ecl.validator import validate_record
from external.adoption.ecl_mapper import map_to_ecl
from external.adoption.trace_loader import normalize_trace


GENERATED_AT = "2026-06-28T00:00:00Z"
CORPUS = ROOT / "experiments" / "trace_corpus" / "corpus_manifest.json"
SCHEMA = ROOT / "schemas" / "ecl-execution-compact-layer.schema.json"
REPORT_JSON = ROOT / "experiments" / "out" / "validation_matrix_evaluation.json"
REPORT_MD = ROOT / "experiments" / "VALIDATION_MATRIX_EVALUATION_v0_1.md"


Mutation = Callable[[dict[str, Any]], None]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def base_record() -> dict[str, Any]:
    manifest = read_json(CORPUS)
    case = manifest["cases"][0]
    envelope = normalize_trace(case["trace"], runtime=case["runtime"], source_ref=f"experiments/trace_corpus/{case['case_id']}")
    mapped = map_to_ecl(envelope, generated_at=GENERATED_AT, checkpoint_ref=f"experiments://{case['case_id']}/checkpoint")
    return mapped["ecl"]


def mutation_cases() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "missing_state",
            "description": "Remove the state surface.",
            "expected_valid": False,
            "mutate": lambda record: record.pop("state", None),
        },
        {
            "case_id": "wrong_schema_version",
            "description": "Change schema_version outside the frozen v0.1 schema.",
            "expected_valid": False,
            "mutate": lambda record: record.__setitem__("schema_version", "0.2.0"),
        },
        {
            "case_id": "tampered_canonical_hash",
            "description": "Replace evidence.hashes.canonical_hash with a fixed invalid hash.",
            "expected_valid": False,
            "mutate": lambda record: record["evidence"]["hashes"].__setitem__("canonical_hash", "sha256:" + ("0" * 64)),
        },
        {
            "case_id": "source_hash_mismatch",
            "description": "Make evidence source_trace_hash disagree with lineage source_trace_hash.",
            "expected_valid": False,
            "mutate": lambda record: record["evidence"]["hashes"].__setitem__("source_trace_hash", "sha256:" + ("1" * 64)),
        },
        {
            "case_id": "empty_event_chain",
            "description": "Remove event-chain evidence.",
            "expected_valid": False,
            "mutate": lambda record: record["evidence"].__setitem__("event_chain", []),
        },
        {
            "case_id": "additional_root_property",
            "description": "Add a root property not allowed by the schema.",
            "expected_valid": False,
            "mutate": lambda record: record.__setitem__("unexpected_root_property", True),
        },
        {
            "case_id": "invalid_action_mode",
            "description": "Use an action execution_mode outside the allowed enum.",
            "expected_valid": False,
            "mutate": lambda record: record["action"].__setitem__("execution_mode", "nondeterministic"),
        },
        {
            "case_id": "missing_evidence_hashes",
            "description": "Remove the required evidence.hashes object.",
            "expected_valid": False,
            "mutate": lambda record: record["evidence"].pop("hashes", None),
        },
    ]


def evaluate_mutation(case: dict[str, Any], original: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    record = deepcopy(original)
    mutate: Mutation = case["mutate"]
    mutate(record)
    report = validate_record(record, schema)
    return {
        "case_id": case["case_id"],
        "description": case["description"],
        "expected_valid": case["expected_valid"],
        "actual_valid": bool(report["valid"]),
        "expectation_met": bool(report["valid"]) == bool(case["expected_valid"]),
        "error_count": len(report["errors"]),
        "errors": report["errors"][:5],
        "record_hash": report["record_hash"],
    }


def markdown_report(payload: dict[str, Any]) -> str:
    rows = [
        "| Case | Expected valid | Actual valid | Error count |",
        "| --- | --- | --- | ---: |",
    ]
    for result in payload["results"]:
        rows.append(
            f"| `{result['case_id']}` | {str(result['expected_valid']).lower()} | {str(result['actual_valid']).lower()} | {result['error_count']} |"
        )
    summary = payload["summary"]
    return (
        "# ECL Validation Matrix Evaluation v0.1\n\n"
        "Status: synthetic_negative_validation_evaluated\n\n"
        "Scope: This evaluation mutates one local synthetic ECL record to test validator rejection behavior. It is not production trace evidence, third-party validation, or benchmark evidence.\n\n"
        "## Summary\n\n"
        f"- Baseline valid: {str(summary['baseline_valid']).lower()}\n"
        f"- Mutation cases: {summary['case_count']}\n"
        f"- Expected invalid cases: {summary['expected_invalid_count']}\n"
        f"- Invalid cases detected: {summary['invalid_detected_count']}\n"
        f"- Expectations met: {summary['expectation_met_count']}/{summary['case_count']}\n"
        f"- Evaluation hash: {payload['evaluation_hash']}\n\n"
        "## Case Results\n\n"
        + "\n".join(rows)
        + "\n\n## Boundary\n\n"
        "```text\n"
        "synthetic_mutation=true\n"
        "external_api_calls=false\n"
        "third_party_validation=false\n"
        "benchmark_result=false\n"
        "```\n"
    )


def main() -> int:
    schema = read_json(SCHEMA)
    original = base_record()
    baseline_report = validate_record(original, schema)
    results = [evaluate_mutation(case, original, schema) for case in mutation_cases()]
    payload = {
        "schema_version": "0.1.0",
        "object_type": "ecl_validation_matrix_evaluation",
        "generated_at": GENERATED_AT,
        "base_record_id": original["ecl_id"],
        "baseline": {
            "valid": bool(baseline_report["valid"]),
            "error_count": len(baseline_report["errors"]),
            "record_hash": baseline_report["record_hash"],
        },
        "summary": {
            "baseline_valid": bool(baseline_report["valid"]),
            "case_count": len(results),
            "expected_invalid_count": sum(1 for result in results if not result["expected_valid"]),
            "invalid_detected_count": sum(1 for result in results if not result["actual_valid"]),
            "expectation_met_count": sum(1 for result in results if result["expectation_met"]),
        },
        "results": results,
        "boundary": {
            "synthetic_mutation": True,
            "external_api_calls": False,
            "third_party_validation": False,
            "benchmark_result": False,
        },
    }
    payload["evaluation_hash"] = sha256_json(payload)
    write_json(REPORT_JSON, payload)
    write_text(REPORT_MD, markdown_report(payload))
    print(canonical_json({"evaluation_hash": payload["evaluation_hash"], "summary": payload["summary"]}))
    return 0 if baseline_report["valid"] and all(result["expectation_met"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
