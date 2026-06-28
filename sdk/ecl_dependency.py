"""ECL Dependency SDK v0.1."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from ecl.canonical import sha256_json
from external.adoption.replay_adapter import replay_ecl
from sdk.ecl import ECL

__all__ = ["wrap", "emit", "verify"]


def wrap(trace: dict[str, Any]) -> dict[str, Any]:
    """Wrap an external trace as an ECL object without modifying the runtime."""

    if trace.get("object_type") == "ecl_execution_record":
        return trace
    runtime = _runtime(trace)
    raw_trace = trace.get("trace") if isinstance(trace.get("trace"), dict) else trace
    return ECL.from_trace(
        {
            "runtime": runtime,
            "trace": raw_trace,
            "source_ref": str(trace.get("source_ref") or "dependency://wrap"),
        }
    )


def emit(ecl_object: dict[str, Any]) -> dict[str, Any]:
    """Emit a deterministic dependency payload for an ECL object."""

    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_dependency_emit",
        "ecl_id": ecl_object["ecl_id"],
        "canonical_hash": ecl_object["evidence"]["hashes"]["canonical_hash"],
        "ecl_object": ecl_object,
        "emit_hash": sha256_json(ecl_object),
    }


def verify(ecl_object: dict[str, Any]) -> dict[str, Any]:
    """Validate and replay an ECL object deterministically."""

    validation = ECL.validate(ecl_object)
    out_dir = ROOT / "sdk" / "out" / "dependency" / ecl_object["ecl_id"].replace(":", "_")
    replay = replay_ecl(ecl_object, out_dir=out_dir, schema_path=ECL.SCHEMA_PATH)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_dependency_verify",
        "ecl_id": ecl_object["ecl_id"],
        "valid": bool(validation["valid"] and replay["valid"]),
        "deterministic": bool(replay["deterministic"]),
        "validation": validation,
        "replay": replay,
        "artifact_paths": {
            "execution_trace": str(out_dir / "execution_trace.json"),
            "evidence_bundle": str(out_dir / "evidence_bundle.json"),
            "replay_result": str(out_dir / "replay_result.json"),
        },
    }


def _runtime(trace: dict[str, Any]) -> str:
    explicit = trace.get("runtime")
    if explicit:
        return str(explicit)
    raw_trace = trace.get("trace") if isinstance(trace.get("trace"), dict) else trace
    if "child_runs" in raw_trace or raw_trace.get("run_type"):
        return "langchain"
    return "openai"
