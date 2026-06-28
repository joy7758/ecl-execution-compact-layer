#!/usr/bin/env python3
"""Verify local JOSS readiness gates without fabricating external signals."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "paper" / "joss" / "JOSS_GATE_VERIFICATION_v0_1.json"
OUT_MD = ROOT / "paper" / "joss" / "JOSS_GATE_VERIFICATION_v0_1.md"
REQUIRED_FILES = [
    "LICENSE",
    "README.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SUPPORT.md",
    "pyproject.toml",
    "paper/paper.md",
    "paper/paper.bib",
    "paper/joss/paper.md",
    "paper/joss/paper.bib",
    ".github/workflows/tests.yml",
    ".github/workflows/joss-paper.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/research_use_report.yml",
    ".github/ISSUE_TEMPLATE/trace_mapping_case.yml",
    "experiments/TRACE_CORPUS_EVALUATION_v0_1.md",
    "experiments/VALIDATION_MATRIX_EVALUATION_v0_1.md",
    "experiments/MAPPING_COVERAGE_EVALUATION_v0_1.md",
    "paper/joss/ECL_DEVELOPMENT_EVIDENCE_LAYER_v0_1.md",
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def git_dates() -> dict[str, Any]:
    result = run(["git", "log", "--format=%ad", "--date=short"])
    dates = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    unique_dates = sorted(set(dates))
    return {
        "available": result.returncode == 0,
        "first_date": unique_dates[0] if unique_dates else None,
        "last_date": unique_dates[-1] if unique_dates else None,
        "unique_day_count": len(unique_dates),
        "all_dates": unique_dates,
    }


def check_file_presence() -> dict[str, Any]:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    return {
        "status": "pass" if not missing else "fail",
        "missing": missing,
        "checked": REQUIRED_FILES,
    }


def check_standard_paper_mirror() -> dict[str, Any]:
    paper = ROOT / "paper" / "paper.md"
    joss_paper = ROOT / "paper" / "joss" / "paper.md"
    bib = ROOT / "paper" / "paper.bib"
    joss_bib = ROOT / "paper" / "joss" / "paper.bib"
    matches = paper.exists() and joss_paper.exists() and bib.exists() and joss_bib.exists()
    if matches:
        matches = paper.read_text(encoding="utf-8") == joss_paper.read_text(encoding="utf-8")
        matches = matches and bib.read_text(encoding="utf-8") == joss_bib.read_text(encoding="utf-8")
    return {
        "status": "pass" if matches else "fail",
        "paper_mirror_matches": bool(matches),
        "evidence": ["paper/paper.md", "paper/paper.bib", "paper/joss/paper.md", "paper/joss/paper.bib"],
    }


def check_experiment_reports() -> dict[str, Any]:
    trace_report = ROOT / "experiments" / "out" / "trace_corpus_evaluation.json"
    validation_report = ROOT / "experiments" / "out" / "validation_matrix_evaluation.json"
    mapping_report = ROOT / "experiments" / "out" / "mapping_coverage_evaluation.json"
    if not trace_report.exists() or not validation_report.exists() or not mapping_report.exists():
        return {
            "status": "fail",
            "reason": "missing experiment output json",
        }
    trace_payload = json.loads(trace_report.read_text(encoding="utf-8"))
    validation_payload = json.loads(validation_report.read_text(encoding="utf-8"))
    mapping_payload = json.loads(mapping_report.read_text(encoding="utf-8"))
    trace_summary = trace_payload["summary"]
    validation_summary = validation_payload["summary"]
    mapping_summary = mapping_payload["summary"]
    pass_condition = (
        trace_summary["case_count"] == 12
        and trace_summary["valid_count"] == 12
        and trace_summary["deterministic_count"] == 12
        and trace_summary["loss_expectation_met_count"] == 12
        and trace_summary["surface_coverage"] == {"action": 12, "evidence": 12, "intent": 12, "state": 12}
        and validation_summary["case_count"] == 8
        and validation_summary["invalid_detected_count"] == 8
        and validation_summary["expectation_met_count"] == 8
        and mapping_summary["case_count"] == 12
        and mapping_summary["total_source_fields"] == 81
        and mapping_summary["direct_mapped_field_count"] == 80
        and mapping_summary["source_hash_only_field_count"] == 1
        and mapping_summary["loss_missing_field_count"] == 4
    )
    return {
        "status": "pass" if pass_condition else "fail",
        "trace_corpus": {
            "case_count": trace_summary["case_count"],
            "valid_count": trace_summary["valid_count"],
            "deterministic_count": trace_summary["deterministic_count"],
            "surface_coverage": trace_summary["surface_coverage"],
            "evaluation_hash": trace_payload["evaluation_hash"],
        },
        "validation_matrix": {
            "case_count": validation_summary["case_count"],
            "invalid_detected_count": validation_summary["invalid_detected_count"],
            "expectation_met_count": validation_summary["expectation_met_count"],
            "evaluation_hash": validation_payload["evaluation_hash"],
        },
        "mapping_coverage": {
            "case_count": mapping_summary["case_count"],
            "total_source_fields": mapping_summary["total_source_fields"],
            "direct_mapped_field_count": mapping_summary["direct_mapped_field_count"],
            "source_hash_only_field_count": mapping_summary["source_hash_only_field_count"],
            "loss_missing_field_count": mapping_summary["loss_missing_field_count"],
            "evaluation_hash": mapping_payload["evaluation_hash"],
        },
    }


def check_public_history() -> dict[str, Any]:
    dates = git_dates()
    # JOSS expectations include public, substantial, ongoing development. This
    # local check is intentionally conservative: one local development day fails.
    ready = dates["available"] and dates["unique_day_count"] >= 180
    return {
        "status": "pass" if ready else "fail_current_state",
        "ready": bool(ready),
        "evidence": dates,
        "note": "Local git history is not a substitute for verified public repository history.",
    }


def check_development_evidence() -> dict[str, Any]:
    evidence_file = ROOT / "paper" / "joss" / "ECL_DEVELOPMENT_EVIDENCE_LAYER_v0_1.md"
    text = evidence_file.read_text(encoding="utf-8").lower() if evidence_file.exists() else ""
    required_tokens = [
        "engineering_evolution_narrative",
        "decision timeline",
        "rejected alternatives",
        "stabilization evidence",
        "does_not_satisfy_public_history_gate=true",
        "non_fake_history=true",
    ]
    missing = [token for token in required_tokens if token not in text]
    ready = evidence_file.exists() and not missing
    return {
        "status": "pass" if ready else "fail",
        "ready": ready,
        "evidence": {
            "path": str(evidence_file.relative_to(ROOT)),
            "required_tokens_present": not missing,
            "missing_tokens": missing,
        },
        "note": "Engineering evolution narrative is documented, but it does not satisfy the public-history gate.",
    }


def check_research_impact() -> dict[str, Any]:
    paper = ROOT / "paper" / "paper.md"
    research_use = ROOT / "docs" / "research_use" / "ECL_RESEARCH_USE_CASE_v0_1.md"
    text = paper.read_text(encoding="utf-8").lower() if paper.exists() else ""
    research_text = research_use.read_text(encoding="utf-8").lower() if research_use.exists() else ""
    experiments = check_experiment_reports()
    has_statement = "# research impact statement" in text and "# statement of need" in text
    has_developer_workflow = (
        research_use.exists()
        and "developer_research_use=true" in research_text
        and "external_research_use=false" in research_text
        and "third_party_validation=false" in research_text
    )
    has_reproducible_evidence = experiments["status"] == "pass"
    ready = bool(has_statement and has_developer_workflow and has_reproducible_evidence)
    return {
        "status": "pass" if ready else "fail",
        "ready": ready,
        "evidence": {
            "statement_of_need_present": "# statement of need" in text,
            "research_impact_statement_present": "# research impact statement" in text,
            "developer_research_workflow_documented": has_developer_workflow,
            "developer_research_workflow_path": str(research_use.relative_to(ROOT)),
            "experiment_reports_status": experiments["status"],
            "trace_corpus_cases": experiments.get("trace_corpus", {}).get("case_count"),
            "validation_matrix_cases": experiments.get("validation_matrix", {}).get("case_count"),
            "mapping_coverage_cases": experiments.get("mapping_coverage", {}).get("case_count"),
        },
        "note": "This gate checks local research-software significance and reproducible evidence; it does not claim external adoption or third-party validation.",
    }


def check_public_repo_sync() -> dict[str, Any]:
    status = run(["git", "status", "--porcelain", "--untracked-files=all"])
    head = run(["git", "rev-parse", "HEAD"])
    remote = run(["git", "ls-remote", "origin", "refs/heads/main"])
    dirty_lines = [line for line in status.stdout.splitlines() if line.strip()]
    local_head = head.stdout.strip()
    remote_head = remote.stdout.split()[0] if remote.stdout.split() else None
    dirty = bool(dirty_lines)
    remote_matches = bool(local_head and remote_head and local_head == remote_head)
    if dirty:
        gate_status = "fail_uncommitted_changes"
    elif not remote_matches:
        gate_status = "fail_remote_mismatch"
    else:
        gate_status = "pass"
    return {
        "status": gate_status,
        "ready": gate_status == "pass",
        "remote_matches_local_head": remote_matches,
        "remote_query_available": remote.returncode == 0,
        "dirty_worktree": dirty,
        "dirty_entry_count": len(dirty_lines),
        "note": "JOSS submission should point at a public repository containing the submitted software and paper state.",
    }


def check_external_impact_signal() -> dict[str, Any]:
    research_use = ROOT / "docs" / "research_use" / "ECL_RESEARCH_USE_CASE_v0_1.md"
    text = research_use.read_text(encoding="utf-8") if research_use.exists() else ""
    external_false = "external_research_use=false" in text and "third_party_validation=false" in text
    return {
        "status": "unverified" if external_false else "unknown",
        "ready": False,
        "blocking": False,
        "evidence": "No external citation, dependency, independent user report, or third-party validation is recorded in the current worktree.",
        "note": "External adoption is recorded as a strong advisory signal, not as the sole JOSS impact gate.",
    }


def build_payload() -> dict[str, Any]:
    gates = {
        "required_files": check_file_presence(),
        "standard_paper_mirror": check_standard_paper_mirror(),
        "experiment_reports": check_experiment_reports(),
        "development_evidence": check_development_evidence(),
        "research_impact": check_research_impact(),
        "public_repo_sync": check_public_repo_sync(),
        "public_history": check_public_history(),
    }
    advisory_signals = {
        "external_impact": check_external_impact_signal(),
    }
    blocking = [
        gate_id
        for gate_id, gate in gates.items()
        if gate["status"] not in {"pass"}
    ]
    payload = {
        "schema_version": "0.1.0",
        "object_type": "ecl_joss_gate_verification",
        "status": "joss_gate_failed_blockers" if blocking else "joss_gate_passed",
        "date_checked": "2026-06-28",
        "gates": gates,
        "advisory_signals": advisory_signals,
        "blocking_gates": blocking,
        "decision": {
            "content_package_ready": gates["required_files"]["status"] == "pass"
            and gates["standard_paper_mirror"]["status"] == "pass"
            and gates["experiment_reports"]["status"] == "pass"
            and gates["development_evidence"]["status"] == "pass"
            and gates["research_impact"]["status"] == "pass",
            "immediate_joss_submission_recommended": False if blocking else True,
        },
        "boundary": {
            "joss_submission_performed": False,
            "third_party_validation": False,
            "external_impact_verified": False,
            "public_repo_synced": gates["public_repo_sync"]["status"] == "pass",
            "public_history_verified": gates["public_history"]["status"] == "pass",
            "development_evidence_verified": gates["development_evidence"]["status"] == "pass",
            "research_impact_verified": gates["research_impact"]["status"] == "pass",
        },
    }
    return payload


def markdown(payload: dict[str, Any]) -> str:
    rows = [
        "| Gate | Status |",
        "| --- | --- |",
    ]
    for gate_id, gate in sorted(payload["gates"].items()):
        rows.append(f"| `{gate_id}` | `{gate['status']}` |")
    return (
        "# ECL JOSS Gate Verification v0.1\n\n"
        f"Status: {payload['status']}\n\n"
        "## Gate Results\n\n"
        + "\n".join(rows)
        + "\n\n## Advisory Signals\n\n"
        "| Signal | Status | Blocking |\n"
        "| --- | --- | --- |\n"
        + "\n".join(
            f"| `{signal_id}` | `{signal['status']}` | `{str(signal.get('blocking', False)).lower()}` |"
            for signal_id, signal in payload["advisory_signals"].items()
        )
        + "\n\n## Decision\n\n"
        "```text\n"
        f"content_package_ready={str(payload['decision']['content_package_ready']).lower()}\n"
        f"immediate_joss_submission_recommended={str(payload['decision']['immediate_joss_submission_recommended']).lower()}\n"
        f"blocking_gates={payload['blocking_gates']}\n"
        "```\n\n"
        "## Boundary\n\n"
        "```text\n"
        "joss_submission_performed=false\n"
        "third_party_validation=false\n"
        "external_impact_verified=false\n"
        f"public_repo_synced={str(payload['boundary']['public_repo_synced']).lower()}\n"
        f"public_history_verified={str(payload['boundary']['public_history_verified']).lower()}\n"
        f"development_evidence_verified={str(payload['boundary']['development_evidence_verified']).lower()}\n"
        f"research_impact_verified={str(payload['boundary']['research_impact_verified']).lower()}\n"
        "```\n"
    )


def main() -> int:
    payload = build_payload()
    out_json, out_md = output_paths()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    out_md.write_text(markdown(payload), encoding="utf-8")
    print(json.dumps({"status": payload["status"], "blocking_gates": payload["blocking_gates"]}, sort_keys=True))
    return 0 if payload["decision"]["content_package_ready"] else 1


def output_paths() -> tuple[Path, Path]:
    output_dir = os.environ.get("ECL_JOSS_GATE_OUTPUT_DIR")
    if not output_dir:
        return OUT_JSON, OUT_MD
    root = Path(output_dir)
    return root / OUT_JSON.name, root / OUT_MD.name


if __name__ == "__main__":
    raise SystemExit(main())
