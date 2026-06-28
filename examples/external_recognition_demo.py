#!/usr/bin/env python3
"""Deterministic external recognition demo for OpenAI and LangChain traces."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import sha256_json
from external.adoption.ecl_mapper import map_to_ecl
from external.adoption.replay_adapter import replay_ecl
from external.adoption.trace_loader import load_trace


GENERATED_AT = "2026-06-28T00:00:00Z"
OUTPUT_ROOT = Path("examples/out/external_recognition")
TRACE_FIXTURES = {
    "openai": Path("tests/fixtures/openai_agents_trace.json"),
    "langchain": Path("tests/fixtures/langchain_trace.json"),
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_runtime(runtime: str, trace_path: Path) -> dict[str, Any]:
    envelope = load_trace(trace_path, runtime=runtime)
    mapped = map_to_ecl(
        envelope,
        generated_at=GENERATED_AT,
        checkpoint_ref=f"examples/out/external_recognition/{runtime}/checkpoint.json",
    )
    runtime_dir = OUTPUT_ROOT / runtime
    replay = replay_ecl(mapped["ecl"], out_dir=runtime_dir)
    write_json(runtime_dir / "ecl_object.json", mapped["ecl"])
    write_json(runtime_dir / "loss.json", mapped["loss"])
    return {
        "runtime": runtime,
        "ecl_ref": str(runtime_dir / "ecl_object.json"),
        "replay_result_ref": str(runtime_dir / "replay_result.json"),
        "evidence_bundle_ref": str(runtime_dir / "evidence_bundle.json"),
        "valid": replay["valid"],
        "deterministic": replay["deterministic"],
        "loss": mapped["loss"],
        "artifact_hashes": replay["artifact_hashes"],
        "verification_hash": replay["verification_hash"],
    }


def main() -> int:
    results = {
        runtime: run_runtime(runtime, trace_path)
        for runtime, trace_path in TRACE_FIXTURES.items()
    }
    summary = {
        "schema_version": "0.1.0",
        "object_type": "ecl_external_recognition_demo_result",
        "generated_at": GENERATED_AT,
        "results": results,
        "all_valid": all(item["valid"] for item in results.values()),
        "all_deterministic": all(item["deterministic"] for item in results.values()),
    }
    summary["result_hash"] = sha256_json(summary)
    write_json(OUTPUT_ROOT / "recognition_demo_result.json", summary)
    print(json.dumps({"all_deterministic": summary["all_deterministic"], "all_valid": summary["all_valid"], "result_hash": summary["result_hash"]}, sort_keys=True))
    return 0 if summary["all_valid"] and summary["all_deterministic"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

