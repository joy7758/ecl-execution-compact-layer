#!/usr/bin/env python3
"""Aggregate the post-JSS route gates without claiming external completion."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run_json(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return {
            "status": "fail",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "fail",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "error": f"invalid json output: {exc}",
        }
    payload["returncode"] = result.returncode
    return payload


def check(condition: bool, name: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "pass" if condition else "fail",
        "details": details,
    }


def verify_zenodo_and_citation_surfaces() -> dict[str, Any]:
    publication_status = load_text("release/v0.1/PUBLICATION_ACTIVATION_STATUS_v0_1.md")
    zenodo_status = load_text("release/v0.1/ZENODO_DOI_ACTION_STATUS_v0_1.md")
    citation = load_text("CITATION.cff")
    release_manifest = load_json("release/v0.1/RELEASE_MANIFEST_v0_1.json")
    details = {
        "zenodo_record": "https://zenodo.org/records/21003766",
        "version_doi": "10.5281/zenodo.21003766",
        "publication_status_mentions_doi": "10.5281/zenodo.21003766" in publication_status,
        "zenodo_status_mentions_publish": "publish_performed=true" in zenodo_status,
        "citation_mentions_doi": "10.5281/zenodo.21003766" in citation,
        "release_manifest_status": release_manifest.get("status"),
        "release_manifest_boundary_doi": release_manifest.get("boundary", {}).get("zenodo_version_doi"),
        "release_manifest_zenodo_doi": release_manifest.get("zenodo", {}).get("version_doi"),
    }
    return check(
        details["publication_status_mentions_doi"]
        and details["zenodo_status_mentions_publish"]
        and details["citation_mentions_doi"]
        and details["release_manifest_boundary_doi"] == "10.5281/zenodo.21003766"
        and details["release_manifest_zenodo_doi"] == "10.5281/zenodo.21003766",
        "zenodo_doi_and_citation_surfaces",
        details,
    )


def verify_technical_report_surface() -> dict[str, Any]:
    readme = load_text("paper/technical_report/README.md")
    md_path = ROOT / "paper/technical_report/ECL_TECHNICAL_REPORT_v0_1.md"
    pdf_path = ROOT / "paper/technical_report/ECL_TECHNICAL_REPORT_v0_1.pdf"
    details = {
        "markdown_exists": md_path.exists(),
        "pdf_exists": pdf_path.exists(),
        "readme_boundary_mentions_not_arxiv": "not an arXiv submission" in readme,
        "readme_mentions_doi": "10.5281/zenodo.21003766" in readme,
    }
    return check(
        details["markdown_exists"]
        and details["pdf_exists"]
        and details["readme_boundary_mentions_not_arxiv"]
        and details["readme_mentions_doi"],
        "technical_report_surface",
        details,
    )


def verify_jss_state_and_joss_deferral() -> dict[str, Any]:
    arxiv_jss_status = load_text("ARXIV_JSS_SUBMISSION_STATUS.md")
    jss_record = load_text("paper/jss/JSS_DECISION_RECORD_v0_1.md")
    joss_plan = load_text("post_pub/JOSS_SIX_MONTH_READINESS_PLAN.md")
    maturation = load_text("paper/joss/JOSS_PUBLIC_HISTORY_MATURATION_PLAN_v0_1.md")
    details = {
        "jss_rejected_and_closed": "jss_rejected_and_closed=true" in arxiv_jss_status
        and "Status: prescreen_reject_rejected_and_closed" in jss_record,
        "jss_manuscript_number": "JSSOFTWARE-D-26-01460" in arxiv_jss_status,
        "joss_six_month_plan_exists": "Status: post_jss_rejection_maturation_plan" in joss_plan,
        "public_history_gate_fails_currently": "public_history_gate_status=fail_current_state" in maturation,
        "earliest_safe_review_date": "earliest_safe_review_date_utc=2026-12-29" in maturation,
    }
    return check(all(details.values()), "jss_closed_and_joss_deferral_recorded", details)


def verify_single_script_gate(name: str, command: list[str]) -> dict[str, Any]:
    payload = run_json(command)
    return check(
        payload.get("status") == "pass",
        name,
        {
            "command": " ".join(command),
            "status": payload.get("status"),
            "boundary": payload.get("boundary", {}),
            "next_action": payload.get("next_action"),
            "recorded_slot_count": payload.get("recorded_slot_count"),
            "next_human_actions": payload.get("next_human_actions"),
        },
    )


def verify_external_pending_state() -> dict[str, Any]:
    queue = load_json("post_pub/EXTERNAL_ACTION_QUEUE_v0_1.json")
    intake = load_json("post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json")
    feedback = load_json("post_pub/FEEDBACK_REQUEST_STATUS_v0_1.json")
    boundary = queue["boundary"]
    intake_boundary = intake["boundary"]
    feedback_boundary = feedback["boundary"]
    false_keys = [
        "youtube_upload_performed",
        "forum_posts_published",
        "hotcrp_submission_performed",
        "external_feedback_recorded",
        "external_adoption_claim",
        "peer_review_claim",
        "joss_readiness_claim",
    ]
    details = {
        "queue_status": queue.get("status"),
        "queue_false_flags": {key: boundary.get(key) for key in false_keys},
        "intake_recorded": intake_boundary.get("external_action_recorded"),
        "feedback_recorded": feedback_boundary.get("external_feedback_recorded"),
        "next_action_id": queue["actions"][0]["id"],
        "next_action_status": queue["actions"][0]["status"],
    }
    return check(
        queue.get("status") == "external_actions_queued_not_executed"
        and all(value is False for value in details["queue_false_flags"].values())
        and intake_boundary.get("external_action_recorded") is False
        and feedback_boundary.get("external_feedback_recorded") is False,
        "external_actions_remain_pending_not_claimed",
        details,
    )


def verify() -> dict[str, Any]:
    checks = [
        verify_zenodo_and_citation_surfaces(),
        verify_technical_report_surface(),
        verify_jss_state_and_joss_deferral(),
        verify_single_script_gate(
            "external_action_queue_verifier",
            [sys.executable, "scripts/verify_external_action_queue.py"],
        ),
        verify_single_script_gate(
            "external_action_evidence_intake_validator",
            [sys.executable, "scripts/validate_external_action_evidence_intake.py"],
        ),
        verify_single_script_gate(
            "icse_tool_demo_package_verifier",
            [sys.executable, "scripts/verify_icse_tool_demo_package.py"],
        ),
        verify_external_pending_state(),
    ]
    local_gates_pass = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_post_jss_route_verification",
        "status": "actionable_local_gates_pass_future_external_steps_open"
        if local_gates_pass
        else "fail",
        "checks": checks,
        "completed_local_surfaces": [
            "GitHub Release v0.1 and Zenodo DOI",
            "Technical Report Markdown/PDF",
            "ICSE 2027 local tool-demo package",
            "External action queue",
            "External action evidence intake template",
            "Safe dissemination and feedback request surfaces",
        ],
        "open_external_steps": [
            "human review of local video candidate",
            "YouTube upload if the video is approved",
            "forum feedback request posts if the author chooses to post them",
            "HotCRP submission when the author performs it",
            "real third-party feedback or reproducibility reports",
            "six-month public maintenance window before any JOSS reassessment",
        ],
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "route_complete": False,
            "youtube_upload_performed": False,
            "hotcrp_submission_performed": False,
            "external_feedback_recorded": False,
            "peer_review_claim": False,
            "external_adoption_claim": False,
            "joss_readiness_claim": False,
        },
    }


def main() -> int:
    report = verify()
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "actionable_local_gates_pass_future_external_steps_open" else 1


if __name__ == "__main__":
    raise SystemExit(main())
