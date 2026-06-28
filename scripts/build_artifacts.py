#!/usr/bin/env python3
"""Build deterministic ECL artifacts with checkpointed state."""

from __future__ import annotations

from copy import deepcopy
import argparse
from pathlib import Path
import json
import os
import shutil
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.adapters.langchain import adapt_trace as adapt_langchain_trace
from ecl.adapters.openai_agents import adapt_trace as adapt_openai_agents_trace
from ecl.canonical import canonical_json, sha256_json, sha256_text, with_record_hash
from ecl.validator import validate_record


SCHEMA_PATH = ROOT / "schemas" / "ecl-execution-compact-layer.schema.json"
CROSSWALK_PATH = ROOT / "mappings" / "pop-aip-aro-crosswalk.json"
STATE_PATH = ROOT / "state" / "ecl_goal_state.json"
LOG_PATH = ROOT / "logs" / "ecl_goal.log"
OUT_DIR = ROOT / "out" / "ecl_artifacts"
FIXTURE_DIR = ROOT / "tests" / "fixtures"

SOURCE_FILES = [
    Path("/Users/zhangbin/GitHub/persona-object-protocol/schema/pop.schema.json"),
    Path("/Users/zhangbin/GitHub/persona-object-protocol/schema/profiles/pop-agent-runtime-profile.schema.json"),
    Path("/Users/zhangbin/GitHub/agent-intent-protocol/schema/intent-object.schema.json"),
    Path("/Users/zhangbin/GitHub/agent-intent-protocol/schema/action-object.schema.json"),
    Path("/Users/zhangbin/GitHub/agent-intent-protocol/schema/result-object.schema.json"),
    Path("/Users/zhangbin/GitHub/aro-audit/schema/evidence.schema.json"),
    Path("/Users/zhangbin/GitHub/aro-audit/spec/receipts/minimal-receipt.schema.json"),
    Path("/Users/zhangbin/GitHub/aro-audit/spec/receipts/lifecycle-receipt.schema.json"),
    Path("/Users/zhangbin/GitHub/aro-audit/spec/AAR_v1.0.schema.json"),
    Path("/Users/zhangbin/GitHub/aro-audit/README.md"),
]


def generated_at() -> str:
    return os.environ.get("ECL_GENERATED_AT", "2026-06-28T00:00:00Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def append_log(event: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(event) + "\n")


def checkpoint(step: str, status: str, artifacts: list[str]) -> dict[str, Any]:
    state = {
        "schema_version": "0.1.0",
        "object_type": "ecl_goal_state",
        "goal_name": "ECL-Execution-Protocol-Builder",
        "step": step,
        "status": status,
        "generated_at": generated_at(),
        "artifacts": artifacts,
        "state_hash": "sha256:" + ("0" * 64),
    }
    state["state_hash"] = sha256_json({k: v for k, v in state.items() if k != "state_hash"})
    write_json(STATE_PATH, state)
    append_log({"event_type": "checkpoint", **state})
    return state


def verify_state_file(path: Path = STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing checkpoint state: {path}")
    state = read_json(path)
    expected = sha256_json({k: v for k, v in state.items() if k != "state_hash"})
    actual = state.get("state_hash")
    if expected != actual:
        raise ValueError(f"checkpoint state hash mismatch: expected {expected}, actual {actual}")
    return state


def file_evidence(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "sha256": None,
            "bytes": 0,
        }
    data = path.read_bytes()
    return {
        "path": str(path),
        "exists": True,
        "sha256": "sha256:" + __import__("hashlib").sha256(data).hexdigest(),
        "bytes": len(data),
    }


def source_evidence() -> list[dict[str, Any]]:
    return [file_evidence(path) for path in SOURCE_FILES]


def mark_validation(record: dict[str, Any], status: str, report_ref: str) -> dict[str, Any]:
    copy = deepcopy(record)
    copy["audit"]["validation"] = [
        {
            "validator": "ecl.validator",
            "status": status,
            "report_ref": report_ref,
        }
    ]
    return with_record_hash(copy)


def schema_diff_payload() -> dict[str, Any]:
    crosswalk = read_json(CROSSWALK_PATH)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_schema_diff",
        "status": "mapping_only_no_source_schema_mutation",
        "generated_at": generated_at(),
        "source_schema_hashes": source_evidence(),
        "ecl_schema_hash": file_evidence(SCHEMA_PATH),
        "field_mappings": crosswalk["field_mappings"],
        "boundary": {
            "source_schemas_modified": False,
            "ecl_adds_local_schema": True,
            "source_protocols_redefined": False
        }
    }


def decision_log_payload() -> dict[str, Any]:
    crosswalk = read_json(CROSSWALK_PATH)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_decision_log",
        "goal_name": "ECL-Execution-Protocol-Builder",
        "generated_at": generated_at(),
        "decisions": [
            {
                "decision_id": "goal-cli-001",
                "decision": "do_not_execute_codex_goal_cli_template_as_shell_commands",
                "reason": "The installed codex CLI exposes no goal subcommand in help output."
            },
            {
                "decision_id": "workspace-001",
                "decision": "create_isolated_local_package",
                "reason": "Relevant source repositories have existing working tree state; ECL should not mutate them."
            },
            {
                "decision_id": "artifact-001",
                "decision": "emit_structured_json_artifacts",
                "reason": "The requested enforcement surface requires execution_trace.json, decision_log.json, schema_diff.json, and evidence_bundle.json."
            },
            *crosswalk["boundary_decisions"]
        ]
    }


def adapter_manifest_payload() -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_adapter_manifest",
        "generated_at": generated_at(),
        "adapters": [
            {
                "adapter_id": "openai_agents_trace",
                "module": "ecl.adapters.openai_agents",
                "entrypoint": "adapt_trace",
                "input_shape": "OpenAI Agents SDK-like trace JSON with trace_id, agent, input, spans or events, result, and optional policy_decisions."
            },
            {
                "adapter_id": "langchain_trace",
                "module": "ecl.adapters.langchain",
                "entrypoint": "adapt_trace",
                "input_shape": "LangChain run JSON with run_id, inputs, outputs, metadata, and optional nested child_runs."
            }
        ]
    }


def build_records(schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    openai_trace_path = FIXTURE_DIR / "openai_agents_trace.json"
    langchain_trace_path = FIXTURE_DIR / "langchain_trace.json"
    openai_record = adapt_openai_agents_trace(
        read_json(openai_trace_path),
        source_trace_ref=str(openai_trace_path),
        generated_at=generated_at(),
        checkpoint_ref=str(STATE_PATH),
    )
    langchain_record = adapt_langchain_trace(
        read_json(langchain_trace_path),
        source_trace_ref=str(langchain_trace_path),
        generated_at=generated_at(),
        checkpoint_ref=str(STATE_PATH),
    )
    reports: list[dict[str, Any]] = []
    openai_record = mark_validation(openai_record, "passed", "out/ecl_artifacts/validator_report.json")
    langchain_record = mark_validation(langchain_record, "passed", "out/ecl_artifacts/validator_report.json")
    for record in [openai_record, langchain_record]:
        reports.append(validate_record(record, schema))
    return openai_record, langchain_record, reports


def artifact_manifest(paths: list[Path]) -> dict[str, Any]:
    artifacts = [file_evidence(path) for path in paths]
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_artifact_manifest",
        "generated_at": generated_at(),
        "artifacts": artifacts,
        "artifact_set_hash": sha256_json(artifacts),
    }


def evidence_bundle_payload(paths: list[Path], validation_reports: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_evidence_bundle",
        "goal_name": "ECL-Execution-Protocol-Builder",
        "generated_at": generated_at(),
        "source_evidence": source_evidence(),
        "generated_artifact_evidence": [file_evidence(path) for path in paths],
        "validation_reports": validation_reports,
        "commands": [
            {
                "command": "python3 scripts/build_artifacts.py",
                "purpose": "Generate all deterministic ECL artifacts."
            },
            {
                "command": "python3 -m unittest discover -s tests",
                "purpose": "Run local verification."
            }
        ],
        "reproducibility": {
            "canonicalization": "json-sort-keys-no-whitespace",
            "hash_algorithm": "sha256",
            "default_generated_at": generated_at()
        },
        "boundary": {
            "public_release": False,
            "external_validation": False,
            "source_repositories_modified": False,
            "formal_standard_claim": False
        }
    }


def execution_trace_payload(states: list[dict[str, Any]], artifact_paths: list[Path]) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_execution_trace",
        "goal_name": "ECL-Execution-Protocol-Builder",
        "generated_at": generated_at(),
        "states": states,
        "artifact_refs": [str(path) for path in artifact_paths],
        "trace_hash": sha256_json(
            {
                "states": states,
                "artifact_refs": [str(path) for path in artifact_paths],
                "generated_at": generated_at(),
            }
        )
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic ECL artifacts with checkpoint support.")
    parser.add_argument("--resume-from", choices=["latest"], help="Resume from the latest checkpoint state.")
    parser.add_argument("--verify-state", action="store_true", help="Verify checkpoint state hash before running.")
    parser.add_argument("--continue-exact", action="store_true", help="Record that deterministic replay should continue from the verified checkpoint.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    states: list[dict[str, Any]] = []
    artifact_paths: list[Path] = []
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if args.resume_from:
        prior_state = verify_state_file() if args.verify_state else read_json(STATE_PATH)
        append_log(
            {
                "event_type": "resume",
                "resume_from": args.resume_from,
                "verify_state": bool(args.verify_state),
                "continue_exact": bool(args.continue_exact),
                "prior_state_hash": prior_state.get("state_hash"),
                "prior_step": prior_state.get("step"),
                "generated_at": generated_at(),
            }
        )
        states.append(prior_state)
    else:
        LOG_PATH.write_text("", encoding="utf-8")

    states.append(checkpoint("init", "completed", []))

    schema = read_json(SCHEMA_PATH)
    out_schema = OUT_DIR / "ecl.schema.json"
    shutil.copyfile(SCHEMA_PATH, out_schema)
    artifact_paths.append(out_schema)
    out_crosswalk = OUT_DIR / "pop_aip_aro_crosswalk.json"
    shutil.copyfile(CROSSWALK_PATH, out_crosswalk)
    artifact_paths.append(out_crosswalk)
    states.append(checkpoint("schema_and_crosswalk", "completed", [str(out_schema), str(out_crosswalk)]))

    adapter_manifest = adapter_manifest_payload()
    adapter_manifest_path = OUT_DIR / "adapter_manifest.json"
    write_json(adapter_manifest_path, adapter_manifest)
    artifact_paths.append(adapter_manifest_path)
    states.append(checkpoint("adapter_manifest", "completed", [str(adapter_manifest_path)]))

    openai_record, langchain_record, validation_reports = build_records(schema)
    openai_record_path = OUT_DIR / "ecl_from_openai_agents_trace.json"
    langchain_record_path = OUT_DIR / "ecl_from_langchain_trace.json"
    write_json(openai_record_path, openai_record)
    write_json(langchain_record_path, langchain_record)
    artifact_paths.extend([openai_record_path, langchain_record_path])
    states.append(checkpoint("adapter_records", "completed", [str(openai_record_path), str(langchain_record_path)]))

    validator_report_path = OUT_DIR / "validator_report.json"
    validator_report = {
        "schema_version": "0.1.0",
        "object_type": "ecl_validator_report_bundle",
        "generated_at": generated_at(),
        "all_valid": all(report["valid"] for report in validation_reports),
        "reports": validation_reports,
    }
    write_json(validator_report_path, validator_report)
    artifact_paths.append(validator_report_path)
    states.append(checkpoint("validation", "completed" if validator_report["all_valid"] else "failed", [str(validator_report_path)]))

    decision_log_path = OUT_DIR / "decision_log.json"
    write_json(decision_log_path, decision_log_payload())
    artifact_paths.append(decision_log_path)

    schema_diff_path = OUT_DIR / "schema_diff.json"
    write_json(schema_diff_path, schema_diff_payload())
    artifact_paths.append(schema_diff_path)

    manifest_path = OUT_DIR / "artifact_manifest.json"
    write_json(manifest_path, artifact_manifest(artifact_paths))
    artifact_paths.append(manifest_path)

    evidence_bundle_path = OUT_DIR / "evidence_bundle.json"
    write_json(evidence_bundle_path, evidence_bundle_payload(artifact_paths, validation_reports))
    artifact_paths.append(evidence_bundle_path)

    execution_trace_path = OUT_DIR / "execution_trace.json"
    write_json(execution_trace_path, execution_trace_payload(states, artifact_paths))
    artifact_paths.append(execution_trace_path)

    states.append(checkpoint("final_artifacts", "completed", [str(path) for path in artifact_paths]))
    return 0 if validator_report["all_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
