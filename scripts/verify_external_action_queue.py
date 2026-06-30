#!/usr/bin/env python3
"""Verify the post-JSS external action queue without recording actions."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"
ICSE_MANIFEST_PATH = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"
FEEDBACK_STATUS_PATH = ROOT / "post_pub" / "FEEDBACK_REQUEST_STATUS_v0_1.json"

EXPECTED_IDS = [
    "review_video_candidate",
    "upload_youtube_video",
    "record_youtube_url",
    "post_langchain_feedback_request",
    "post_mcp_feedback_request",
    "record_forum_urls",
    "submit_icse_tool_demo",
    "record_icse_submission_evidence",
    "record_third_party_feedback",
    "continue_monthly_maintenance",
]

ALLOWED_PENDING_STATUSES = {
    "pending_human_review",
    "pending_human_upload",
    "waiting_on_youtube_url",
    "pending_human_post",
    "waiting_on_forum_urls",
    "pending_human_submission",
    "waiting_on_hotcrp_evidence",
    "waiting_on_external_response",
    "ongoing_time_dependent",
}

FORBIDDEN_COMPLETED_STATUSES = {
    "accept",
    "accepted",
    "complete",
    "completed",
    "done",
    "posted",
    "published",
    "submitted",
    "uploaded",
}

FALSE_BOUNDARY_FLAGS = [
    "youtube_upload_performed",
    "forum_posts_published",
    "hotcrp_submission_performed",
    "external_feedback_recorded",
    "external_adoption_claim",
    "peer_review_claim",
    "joss_readiness_claim",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, name: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "pass" if condition else "fail",
        "details": details,
    }


def packet_paths(actions: list[dict[str, Any]]) -> list[str]:
    paths: list[str] = []
    for action in actions:
        value = action["input_packet"]
        if isinstance(value, str):
            paths.append(value)
        else:
            paths.extend(value)
    return paths


def verify() -> dict[str, Any]:
    queue = load_json(QUEUE_PATH)
    actions = queue.get("actions", [])
    boundary = queue.get("boundary", {})
    inputs = queue.get("current_verified_inputs", {})
    checks: list[dict[str, Any]] = []

    checks.append(
        check(
            queue.get("status") == "external_actions_queued_not_executed",
            "queue_status_is_not_executed",
            {"status": queue.get("status")},
        )
    )
    checks.append(
        check(
            [action.get("id") for action in actions] == EXPECTED_IDS
            and [action.get("order") for action in actions] == list(range(1, len(EXPECTED_IDS) + 1)),
            "actions_are_ordered_and_expected",
            {
                "ids": [action.get("id") for action in actions],
                "orders": [action.get("order") for action in actions],
            },
        )
    )

    statuses = {action.get("status") for action in actions}
    checks.append(
        check(
            statuses <= ALLOWED_PENDING_STATUSES and not statuses.intersection(FORBIDDEN_COMPLETED_STATUSES),
            "actions_do_not_claim_completion",
            {"statuses": sorted(str(status) for status in statuses)},
        )
    )

    missing_packets = [path for path in packet_paths(actions) if not (ROOT / path).exists()]
    checks.append(
        check(
            not missing_packets,
            "input_packets_exist",
            {"missing_packets": missing_packets},
        )
    )

    boundary_false = {key: boundary.get(key) for key in FALSE_BOUNDARY_FLAGS}
    checks.append(
        check(
            boundary.get("queue_only") is True and all(value is False for value in boundary_false.values()),
            "boundary_flags_preserve_non_adoption_state",
            {"queue_only": boundary.get("queue_only"), **boundary_false},
        )
    )

    video_candidate = ROOT / inputs.get("video_candidate", "")
    actual_video_hash = sha256(video_candidate.read_bytes()).hexdigest() if video_candidate.exists() else None
    checks.append(
        check(
            video_candidate.exists() and actual_video_hash == inputs.get("video_candidate_sha256"),
            "video_candidate_hash_matches_queue",
            {
                "path": inputs.get("video_candidate"),
                "expected_sha256": inputs.get("video_candidate_sha256"),
                "actual_sha256": actual_video_hash,
            },
        )
    )

    icse_manifest = load_json(ICSE_MANIFEST_PATH)
    feedback_status = load_json(FEEDBACK_STATUS_PATH)
    checks.append(
        check(
            inputs.get("video_candidate_sha256") == icse_manifest["video"]["local_candidate_sha256"]
            and inputs.get("make_demo_dependency_hash") == icse_manifest["demo"]["dependency_mode_result_hash"]
            and inputs.get("make_demo_external_recognition_hash")
            == icse_manifest["demo"]["external_recognition_result_hash"]
            and inputs.get("make_demo_dependency_hash")
            == feedback_status["expected_make_demo_hashes"]["dependency_mode_result_hash"]
            and inputs.get("make_demo_external_recognition_hash")
            == feedback_status["expected_make_demo_hashes"]["external_recognition_result_hash"],
            "cross_manifest_hashes_match",
            {
                "dependency_hash": inputs.get("make_demo_dependency_hash"),
                "external_recognition_hash": inputs.get("make_demo_external_recognition_hash"),
                "video_candidate_sha256": inputs.get("video_candidate_sha256"),
            },
        )
    )

    next_action = actions[0] if actions else None
    passed = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_external_action_queue_verification",
        "status": "pass" if passed else "fail",
        "queue_path": str(QUEUE_PATH.relative_to(ROOT)),
        "next_action": {
            "id": next_action.get("id"),
            "status": next_action.get("status"),
            "target": next_action.get("target"),
        }
        if next_action
        else None,
        "checks": checks,
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "youtube_upload_performed": False,
            "forum_posts_published": False,
            "hotcrp_submission_performed": False,
            "external_feedback_recorded": False,
            "external_adoption_claim": False,
            "peer_review_claim": False,
        },
    }


def main() -> int:
    report = verify()
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
