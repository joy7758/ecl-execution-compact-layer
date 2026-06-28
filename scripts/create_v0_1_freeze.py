#!/usr/bin/env python3
"""Create the v0.1 local freeze snapshot."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FREEZE_DIR = ROOT / "release" / "v0.1-local-freeze"

FREEZE_INPUTS = [
    ("SPEC.md", "SPEC.md"),
    ("CHANGE_POLICY.md", "CHANGE_POLICY.md"),
    ("schemas/ecl-execution-compact-layer.schema.json", "schema.json"),
    ("mappings/pop-aip-aro-crosswalk.json", "crosswalk.json"),
    ("ecl/validator.py", "validator.py"),
    ("ecl/canonical.py", "canonical.py"),
    ("tests/fixtures/openai_agents_trace.json", "sample_traces/openai_agents_trace.json"),
    ("tests/fixtures/langchain_trace.json", "sample_traces/langchain_trace.json"),
    ("out/ecl_artifacts/evidence_bundle.json", "evidence_bundle.json"),
    ("out/ecl_artifacts/validator_report.json", "validator_report.json"),
    ("out/ecl_artifacts/execution_trace.json", "execution_trace.json"),
    ("out/ecl_artifacts/decision_log.json", "decision_log.json"),
    ("out/ecl_artifacts/schema_diff.json", "schema_diff.json"),
    ("out/ecl_artifacts/ecl_from_openai_agents_trace.json", "records/ecl_from_openai_agents_trace.json"),
    ("out/ecl_artifacts/ecl_from_langchain_trace.json", "records/ecl_from_langchain_trace.json"),
]


def generated_at() -> str:
    return os.environ.get("ECL_GENERATED_AT", "2026-06-28T00:00:00Z")


def file_hash(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def copy_inputs() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_name, target_name in FREEZE_INPUTS:
        source = ROOT / source_name
        target = FREEZE_DIR / target_name
        if not source.exists():
            raise FileNotFoundError(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        entries.append(
            {
                "source_path": str(source.relative_to(ROOT)),
                "freeze_path": str(target.relative_to(ROOT)),
                "bytes": target.stat().st_size,
                "sha256": file_hash(target),
            }
        )
    return entries


def write_manifest(entries: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = {
        "schema_version": "0.1.0",
        "object_type": "ecl_v0_1_local_freeze_hash_manifest",
        "freeze_id": "v0.1-local-freeze",
        "generated_at": generated_at(),
        "status": "local_semantic_freeze",
        "entries": entries,
        "boundary": {
            "public_release": False,
            "external_validation": False,
            "standard_claim": False,
            "ecosystem_adoption_claim": False
        },
        "reproduction_commands": [
            "python3 scripts/build_artifacts.py --resume-from latest --verify-state --continue-exact",
            "python3 scripts/create_v0_1_freeze.py --overwrite",
            "python3 -m unittest discover -s tests"
        ],
        "snapshot_hash": "sha256:" + ("0" * 64),
    }
    manifest["snapshot_hash"] = "sha256:" + sha256(
        canonical_json({k: v for k, v in manifest.items() if k != "snapshot_hash"}).encode("utf-8")
    ).hexdigest()
    manifest_path = FREEZE_DIR / "hash_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the ECL v0.1 local freeze snapshot.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing local freeze snapshot.")
    args = parser.parse_args()

    if FREEZE_DIR.exists():
        if not args.overwrite:
            raise FileExistsError(f"{FREEZE_DIR} already exists; use --overwrite to replace the local snapshot")
        shutil.rmtree(FREEZE_DIR)
    FREEZE_DIR.mkdir(parents=True)
    entries = copy_inputs()
    manifest = write_manifest(entries)
    print(json.dumps({"freeze_dir": str(FREEZE_DIR), "snapshot_hash": manifest["snapshot_hash"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

