#!/usr/bin/env python3
"""Evaluate the local ECL synthetic trace corpus deterministically."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import canonical_json, sha256_json
from external.adoption.ecl_mapper import map_to_ecl
from external.adoption.replay_adapter import replay_ecl
from external.adoption.trace_loader import normalize_trace


GENERATED_AT = "2026-06-28T00:00:00Z"
CORPUS = ROOT / "experiments" / "trace_corpus" / "corpus_manifest.json"
OUT_DIR = ROOT / "experiments" / "out" / "trace_corpus"
REPORT_JSON = ROOT / "experiments" / "out" / "trace_corpus_evaluation.json"
REPORT_MD = ROOT / "experiments" / "TRACE_CORPUS_EVALUATION_v0_1.md"


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
    envelope = normalize_trace(case["trace"], runtime=runtime, source_ref=f"experiments/trace_corpus/{case_id}")
    mapped = map_to_ecl(envelope, generated_at=GENERATED_AT, checkpoint_ref=f"experiments://{case_id}/checkpoint")
    replay_dir = OUT_DIR / "artifacts" / case_id
    first = replay_ecl(mapped["ecl"], out_dir=replay_dir)
    second = replay_ecl(mapped["ecl"], out_dir=replay_dir)
    loss_fields = list(mapped["loss"].get("missing_fields", []))
    result = {
        "case_id": case_id,
        "runtime": runtime,
        "category": case["category"],
        "tags": sorted(case.get("tags", [])),
        "expected_loss": bool(case.get("expected_loss")),
        "loss_detected": bool(loss_fields),
        "loss_fields": sorted(loss_fields),
        "loss_type": mapped["loss"].get("type"),
        "normalized_event_count": len(envelope["normalized_events"]),
        "ecl_id": mapped["ecl"]["ecl_id"],
        "valid": bool(first["valid"]),
        "deterministic": first["artifact_hashes"] == second["artifact_hashes"] and first["verification_hash"] == second["verification_hash"],
        "verification_hash": first["verification_hash"],
        "mapping_hash": mapped["mapping_hash"],
        "mapping": mapped["mapping"],
    }
    result["expectation_met"] = result["loss_detected"] == result["expected_loss"]
    return result


def summarize(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    runtimes = sorted({result["runtime"] for result in results})
    tags = sorted({tag for result in results for tag in result["tags"]})
    by_runtime = {
        runtime: sum(1 for result in results if result["runtime"] == runtime)
        for runtime in runtimes
    }
    surfaces = ["state", "intent", "action", "evidence"]
    surface_coverage = {
        surface: sum(1 for result in results if surface in set(result["mapping"].values()))
        for surface in surfaces
    }
    surface_coverage_by_runtime = {
        runtime: {
            surface: sum(
                1
                for result in results
                if result["runtime"] == runtime and surface in set(result["mapping"].values())
            )
            for surface in surfaces
        }
        for runtime in runtimes
    }
    loss_type_counts = {
        loss_type: sum(1 for result in results if result["loss_type"] == loss_type)
        for loss_type in sorted({result["loss_type"] for result in results})
    }
    return {
        "case_count": len(results),
        "runtime_count": len(runtimes),
        "by_runtime": by_runtime,
        "tag_count": len(tags),
        "tags": tags,
        "valid_count": sum(1 for result in results if result["valid"]),
        "deterministic_count": sum(1 for result in results if result["deterministic"]),
        "loss_expected_count": sum(1 for case in cases if case.get("expected_loss")),
        "loss_detected_count": sum(1 for result in results if result["loss_detected"]),
        "loss_expectation_met_count": sum(1 for result in results if result["expectation_met"]),
        "total_normalized_events": sum(result["normalized_event_count"] for result in results),
        "max_normalized_events": max(result["normalized_event_count"] for result in results),
        "surface_coverage": surface_coverage,
        "surface_coverage_by_runtime": surface_coverage_by_runtime,
        "loss_type_counts": loss_type_counts,
    }


def markdown_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    rows = [
        "| Case | Runtime | Category | Events | Loss | Valid | Deterministic |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for result in payload["results"]:
        loss = ",".join(result["loss_fields"]) if result["loss_fields"] else "none"
        rows.append(
            f"| `{result['case_id']}` | {result['runtime']} | {result['category']} | {result['normalized_event_count']} | {loss} | {str(result['valid']).lower()} | {str(result['deterministic']).lower()} |"
        )
    return (
        "# ECL Trace Corpus Evaluation v0.1\n\n"
        "Status: synthetic_corpus_evaluated\n\n"
        "Scope: This evaluation uses a local synthetic stress corpus. It is not production trace evidence, third-party validation, or benchmark evidence.\n\n"
        "## Summary\n\n"
        f"- Cases: {summary['case_count']}\n"
        f"- Runtimes: {summary['by_runtime']}\n"
        f"- Valid cases: {summary['valid_count']}/{summary['case_count']}\n"
        f"- Deterministic cases: {summary['deterministic_count']}/{summary['case_count']}\n"
        f"- Loss expectation met: {summary['loss_expectation_met_count']}/{summary['case_count']}\n"
        f"- Surface coverage: {summary['surface_coverage']}\n"
        f"- Surface coverage by runtime: {summary['surface_coverage_by_runtime']}\n"
        f"- Loss type counts: {summary['loss_type_counts']}\n"
        f"- Total normalized events: {summary['total_normalized_events']}\n"
        f"- Tags: {', '.join(summary['tags'])}\n\n"
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
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    results = [evaluate_case(case) for case in cases]
    payload = {
        "schema_version": "0.1.0",
        "object_type": "ecl_trace_corpus_evaluation",
        "generated_at": GENERATED_AT,
        "corpus": str(CORPUS),
        "corpus_hash": sha256_json(manifest),
        "summary": summarize(cases, results),
        "results": results,
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
    return 0 if all(result["valid"] and result["deterministic"] and result["expectation_met"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
