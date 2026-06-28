"""Local MCP-style ECL anchor stub.

This module exposes only thin deterministic wrappers over sdk.ecl_dependency.
It is agent-readable by design: each public function has one direct delegate.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SDK_DIR = ROOT / "sdk"
for path in (str(ROOT), str(SDK_DIR)):
    if path in sys.path:
        sys.path.remove(path)
for path in (str(SDK_DIR), str(ROOT)):
    sys.path.insert(0, path)

import ecl_dependency as dependency

__all__ = ["wrap", "emit", "verify"]


def wrap(trace: dict[str, Any]) -> dict[str, Any]:
    """Return dependency.wrap(trace) without mutating the host trace."""

    return dependency.wrap(trace)


def emit(ecl_object: dict[str, Any]) -> dict[str, Any]:
    """Return dependency.emit(ecl_object) without adding server state."""

    return dependency.emit(ecl_object)


def verify(ecl_object: dict[str, Any]) -> dict[str, Any]:
    """Return dependency.verify(ecl_object) without runtime hooks."""

    return dependency.verify(ecl_object)


def _load_trace_fixture() -> dict[str, Any]:
    trace_path = ROOT / "tests" / "fixtures" / "openai_agents_trace.json"
    return {
        "runtime": "openai",
        "trace": json.loads(trace_path.read_text(encoding="utf-8")),
        "source_ref": "mcp/ecl_server_stub.py:self_check",
    }


def _self_check() -> dict[str, Any]:
    ecl_object = wrap(_load_trace_fixture())
    emission = emit(ecl_object)
    validation_result = verify(ecl_object)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_mcp_anchor_stub_self_check",
        "tools": ["ecl.wrap", "ecl.emit", "ecl.verify"],
        "deterministic": bool(validation_result["deterministic"]),
        "valid": bool(validation_result["valid"]),
        "ecl_id": ecl_object["ecl_id"],
        "canonical_hash": emission["canonical_hash"],
        "emit_hash": emission["emit_hash"],
        "verification_hash": validation_result["replay"]["verification_hash"],
        "artifact_paths": validation_result["artifact_paths"],
    }


def main() -> int:
    result = _self_check()
    out_dir = ROOT / "mcp" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ecl_server_stub_result.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] and result["deterministic"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
