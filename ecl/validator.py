"""Validate ECL records and verify deterministic hashes."""

from __future__ import annotations

import argparse
from pathlib import Path
import json
from typing import Any

from .canonical import compute_record_hash, sha256_json


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_with_jsonschema(record: dict[str, Any], schema: dict[str, Any] | None) -> list[str]:
    if schema is None:
        return []
    try:
        import jsonschema
    except Exception as exc:  # pragma: no cover - environment dependent
        return [f"jsonschema_unavailable:{type(exc).__name__}:{exc}"]
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
        path = "$" + "".join(f".{part}" for part in error.path)
        errors.append(f"{path}:{error.message}")
    return errors


def validate_minimal(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "schema_version",
        "object_type",
        "ecl_id",
        "lineage",
        "state",
        "intent",
        "action",
        "evidence",
        "determinism",
        "audit",
    ]
    for key in required:
        if key not in record:
            errors.append(f"missing:{key}")
    if record.get("schema_version") != "0.1.0-draft":
        errors.append("schema_version:not_0.1.0-draft")
    if record.get("object_type") != "ecl_execution_record":
        errors.append("object_type:not_ecl_execution_record")
    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence:not_object")
        return errors
    hashes = evidence.get("hashes")
    if not isinstance(hashes, dict):
        errors.append("evidence.hashes:not_object")
        return errors
    canonical_hash = hashes.get("canonical_hash")
    expected = compute_record_hash(record)
    if canonical_hash != expected:
        errors.append(f"evidence.hashes.canonical_hash:mismatch:expected:{expected}:actual:{canonical_hash}")
    source_hash = hashes.get("source_trace_hash")
    lineage_hash = record.get("lineage", {}).get("source_trace_hash")
    if source_hash != lineage_hash:
        errors.append("source_trace_hash:mismatch_between_lineage_and_evidence")
    if not evidence.get("event_chain"):
        errors.append("evidence.event_chain:empty")
    return errors


def validate_record(record: dict[str, Any], schema: dict[str, Any] | None = None) -> dict[str, Any]:
    errors = validate_minimal(record)
    errors.extend(validate_with_jsonschema(record, schema))
    try:
        recomputed_hash = compute_record_hash(record) if isinstance(record, dict) and "evidence" in record else None
    except Exception as exc:
        recomputed_hash = None
        errors.append(f"recomputed_canonical_hash:unavailable:{type(exc).__name__}")
    report = {
        "schema_version": "0.1.0",
        "object_type": "ecl_validation_report",
        "record_id": record.get("ecl_id"),
        "valid": not errors,
        "errors": errors,
        "canonical_hash": record.get("evidence", {}).get("hashes", {}).get("canonical_hash"),
        "recomputed_canonical_hash": recomputed_hash,
        "record_hash": sha256_json(record),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an ECL execution record.")
    parser.add_argument("record", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    record = load_json(args.record)
    schema = load_json(args.schema) if args.schema else None
    report = validate_record(record, schema)
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
