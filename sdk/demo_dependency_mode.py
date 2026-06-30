#!/usr/bin/env python3
"""Cross-runtime ECL dependency mode demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ecl_dependency as ecl
from ecl.canonical import sha256_json


FIXTURES = {
    "openai": ROOT / "tests" / "fixtures" / "openai_agents_trace.json",
    "langchain": ROOT / "tests" / "fixtures" / "langchain_trace.json",
}
OUT_DIR = ROOT / "sdk" / "out" / "dependency_mode"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def relative_ref(path: Path | str) -> str:
    return str(Path(path).resolve().relative_to(ROOT))


def run_runtime(runtime: str, fixture: Path) -> dict[str, Any]:
    trace = {"runtime": runtime, "trace": read_json(fixture), "source_ref": f"sdk/demo_dependency_mode.py:{runtime}"}
    ecl_object = ecl.wrap(trace)
    emitted = ecl.emit(ecl_object)
    verified = ecl.verify(ecl_object)
    runtime_dir = OUT_DIR / runtime
    write_json(runtime_dir / "ecl_object.json", ecl_object)
    write_json(runtime_dir / "emit.json", emitted)
    write_json(runtime_dir / "verify.json", verified)
    return {
        "runtime": runtime,
        "ecl_ref": relative_ref(runtime_dir / "ecl_object.json"),
        "replay_result": verified["replay"],
        "evidence_bundle": relative_ref(verified["artifact_paths"]["evidence_bundle"]),
        "valid": verified["valid"],
        "deterministic": verified["deterministic"],
        "verification_hash": verified["replay"]["verification_hash"],
    }


def main() -> int:
    results = {runtime: run_runtime(runtime, fixture) for runtime, fixture in FIXTURES.items()}
    summary = {
        "schema_version": "0.1.0",
        "object_type": "ecl_dependency_mode_demo_result",
        "dependency_mode": True,
        "results": results,
        "all_valid": all(item["valid"] for item in results.values()),
        "all_deterministic": all(item["deterministic"] for item in results.values()),
    }
    summary["result_hash"] = sha256_json(summary)
    write_json(OUT_DIR / "dependency_mode_result.json", summary)
    print(json.dumps({"all_deterministic": summary["all_deterministic"], "all_valid": summary["all_valid"], "result_hash": summary["result_hash"]}, sort_keys=True))
    return 0 if summary["all_valid"] and summary["all_deterministic"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
