#!/usr/bin/env python3
"""Deterministic ECL replay demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.canonical import canonical_json, sha256_json
from ecl.validator import validate_record


DEFAULT_INPUT = ROOT / "out" / "ecl_artifacts" / "ecl_from_openai_agents_trace.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "ecl-execution-compact-layer.schema.json"
DEFAULT_OUT = ROOT / "demo" / "out"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def stable_ref(path: Path) -> str:
    raw = str(path)
    if raw.startswith("memory:"):
        return raw
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return raw


def replay(record: dict[str, Any], schema: dict[str, Any], *, input_ref: Path, out_dir: Path) -> dict[str, Any]:
    validation_report = validate_record(record, schema)
    input_hash = sha256_json(record)
    event_chain = record["evidence"]["event_chain"]
    generated_at = record["lineage"]["generated_at"]
    execution_hash = sha256_json(
        {
            "canonical_hash": record["evidence"]["hashes"]["canonical_hash"],
            "event_chain_hash": record["evidence"]["hashes"].get("event_chain_hash"),
            "input_hash": input_hash,
            "valid": validation_report["valid"],
        }
    )
    execution_trace = {
        "schema_version": "0.1.0",
        "object_type": "ecl_replay_execution_trace",
        "generated_at": generated_at,
        "input_ref": stable_ref(input_ref),
        "input_hash": input_hash,
        "record_id": record["ecl_id"],
        "validation_valid": validation_report["valid"],
        "event_count": len(event_chain),
        "event_chain_tail": event_chain[-1]["chain_hash"],
        "execution_hash": execution_hash,
    }
    replay_result = {
        "schema_version": "0.1.0",
        "object_type": "ecl_replay_result",
        "generated_at": generated_at,
        "record_id": record["ecl_id"],
        "valid": validation_report["valid"],
        "deterministic": True,
        "execution_hash": execution_hash,
        "output_refs": [
            stable_ref(out_dir / "execution_trace.json"),
            stable_ref(out_dir / "evidence_bundle.json"),
            stable_ref(out_dir / "replay_result.json"),
        ],
    }
    evidence_bundle = {
        "schema_version": "0.1.0",
        "object_type": "ecl_replay_evidence_bundle",
        "generated_at": generated_at,
        "record_id": record["ecl_id"],
        "input_ref": stable_ref(input_ref),
        "input_hash": input_hash,
        "validation_report": validation_report,
        "execution_trace_hash": sha256_json(execution_trace),
        "replay_result_hash": sha256_json(replay_result),
        "execution_hash": execution_hash,
        "boundary": {
            "external_api_calls": False,
            "randomness": False,
            "schema_modified": False,
        },
    }

    write_json(out_dir / "execution_trace.json", execution_trace)
    write_json(out_dir / "replay_result.json", replay_result)
    write_json(out_dir / "evidence_bundle.json", evidence_bundle)
    return {
        "execution_trace": execution_trace,
        "evidence_bundle": evidence_bundle,
        "replay_result": replay_result,
        "output_digest": sha256_json(
            {
                "execution_trace": execution_trace,
                "evidence_bundle": evidence_bundle,
                "replay_result": replay_result,
            }
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay a local ECL record deterministically.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    payload = replay(read_json(args.input), read_json(args.schema), input_ref=args.input, out_dir=args.out_dir)
    print(canonical_json({"output_digest": payload["output_digest"], "valid": payload["replay_result"]["valid"]}))
    return 0 if payload["replay_result"]["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
