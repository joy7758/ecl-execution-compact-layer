#!/usr/bin/env python3
"""Minimal deterministic citation reproducibility demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from ecl.canonical import sha256_json
from mcp import ecl_server_stub as ecl

OUTPUT_ROOT = ROOT / "examples" / "out" / "citation_seed"
TRACE_FIXTURES = {
    "openai": ROOT / "tests" / "fixtures" / "openai_agents_trace.json",
    "langchain": ROOT / "tests" / "fixtures" / "langchain_trace.json",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_runtime(runtime: str, trace_path: Path) -> dict[str, Any]:
    ecl_object = ecl.wrap(
        {
            "runtime": runtime,
            "trace": read_json(trace_path),
            "source_ref": f"examples/citation_repro_demo.py:{runtime}",
        }
    )
    emission = ecl.emit(ecl_object)
    verification = ecl.verify(ecl_object)
    runtime_dir = OUTPUT_ROOT / runtime
    write_json(runtime_dir / "ecl_object.json", ecl_object)
    write_json(runtime_dir / "emit.json", emission)
    write_json(runtime_dir / "verify.json", verification)
    return {
        "runtime": runtime,
        "ecl_ref": str(runtime_dir / "ecl_object.json"),
        "emit_ref": str(runtime_dir / "emit.json"),
        "verify_ref": str(runtime_dir / "verify.json"),
        "ecl_id": ecl_object["ecl_id"],
        "canonical_hash": emission["canonical_hash"],
        "emit_hash": emission["emit_hash"],
        "valid": verification["valid"],
        "deterministic": verification["deterministic"],
        "verification_hash": verification["replay"]["verification_hash"],
    }


def main() -> int:
    results = {
        runtime: run_runtime(runtime, trace_path)
        for runtime, trace_path in TRACE_FIXTURES.items()
    }
    summary = {
        "schema_version": "0.1.0",
        "object_type": "ecl_citation_repro_demo_result",
        "status": "local_pre_adoption_reproducibility_seed",
        "results": results,
        "all_valid": all(item["valid"] for item in results.values()),
        "all_deterministic": all(item["deterministic"] for item in results.values()),
        "boundary": {
            "public_release": False,
            "third_party_validation": False,
            "ecosystem_adoption": False,
            "network_calls": False,
            "schema_modified": False,
        },
    }
    summary["result_hash"] = sha256_json(summary)
    write_json(OUTPUT_ROOT / "citation_seed_result.json", summary)
    print(
        json.dumps(
            {
                "all_deterministic": summary["all_deterministic"],
                "all_valid": summary["all_valid"],
                "result_hash": summary["result_hash"],
            },
            sort_keys=True,
        )
    )
    return 0 if summary["all_valid"] and summary["all_deterministic"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
