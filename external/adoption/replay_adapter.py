"""External replay adapter for ECL adoption hooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from demo.replay_demo import replay
from ecl.canonical import sha256_json


def replay_ecl(ecl_record: dict[str, Any], *, out_dir: str | Path, schema_path: str | Path | None = None) -> dict[str, Any]:
    """Replay an ECL record and return deterministic verification metadata."""

    schema_file = Path(schema_path) if schema_path else Path("schemas/ecl-execution-compact-layer.schema.json")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    output_dir = Path(out_dir)
    payload = replay(ecl_record, schema, input_ref=Path("memory://external-adoption-ecl"), out_dir=output_dir)
    artifact_hashes = {
        "execution_trace": _file_hash(output_dir / "execution_trace.json"),
        "evidence_bundle": _file_hash(output_dir / "evidence_bundle.json"),
        "replay_result": _file_hash(output_dir / "replay_result.json"),
    }
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_external_replay_verification",
        "deterministic": True,
        "valid": bool(payload["replay_result"]["valid"]),
        "artifact_hashes": artifact_hashes,
        "verification_hash": sha256_json(artifact_hashes),
    }


def _file_hash(path: Path) -> str:
    import hashlib

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

