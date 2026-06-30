#!/usr/bin/env python3
"""Verify the next human actions packet without performing actions."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "post_pub" / "NEXT_HUMAN_ACTIONS_PACKET_v0_1.json"
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"

EXPECTED_IDS = [
    "review_video_candidate",
    "upload_youtube_video",
    "record_youtube_url",
    "post_langchain_feedback_request",
    "post_mcp_feedback_request",
    "submit_icse_tool_demo",
    "record_third_party_feedback",
    "continue_monthly_maintenance",
]

FALSE_FLAGS = [
    "youtube_upload_performed",
    "forum_posts_published",
    "hotcrp_submission_performed",
    "external_feedback_recorded",
    "external_adoption_claim",
    "peer_review_claim",
    "icse_acceptance_claim",
    "joss_readiness_claim",
    "route_complete",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_post_jss_verifier() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "scripts/verify_post_jss_route.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return {"status": "fail", "stdout": result.stdout, "stderr": result.stderr}
    return json.loads(result.stdout)


def check(condition: bool, name: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "pass" if condition else "fail",
        "details": details,
    }


def verify() -> dict[str, Any]:
    packet = load_json(PACKET_PATH)
    queue = load_json(QUEUE_PATH)
    route = run_post_jss_verifier()
    actions = packet.get("actions", [])
    boundary = packet.get("boundary", {})
    checks: list[dict[str, Any]] = []

    checks.append(
        check(
            packet.get("status") == "human_actions_pending_not_executed"
            and packet.get("source_status") == "actionable_local_gates_pass_future_external_steps_open",
            "packet_status_matches_route_state",
            {"status": packet.get("status"), "source_status": packet.get("source_status")},
        )
    )

    packet_ids = [action.get("id") for action in actions]
    queue_ids = [action.get("id") for action in queue.get("actions", [])]
    checks.append(
        check(
            packet_ids == EXPECTED_IDS and all(action_id in queue_ids for action_id in packet_ids),
            "packet_actions_are_ordered_subset_of_queue",
            {"packet_ids": packet_ids, "queue_ids": queue_ids},
        )
    )

    missing_packets = [
        action["input_packet"]
        for action in actions
        if isinstance(action.get("input_packet"), str) and not (ROOT / action["input_packet"]).exists()
    ]
    checks.append(check(not missing_packets, "input_packets_exist", {"missing_packets": missing_packets}))

    checks.append(
        check(
            boundary.get("packet_only") is True
            and boundary.get("human_actions_pending") is True
            and all(boundary.get(key) is False for key in FALSE_FLAGS),
            "boundary_preserves_pending_external_state",
            {"boundary": boundary},
        )
    )

    route_boundary = route.get("boundary", {})
    checks.append(
        check(
            route.get("status") == "actionable_local_gates_pass_future_external_steps_open"
            and route_boundary.get("route_complete") is False
            and route_boundary.get("writes_external_state") is False,
            "post_jss_route_verifier_still_reports_open_external_steps",
            {"route_status": route.get("status"), "route_boundary": route_boundary},
        )
    )

    passed = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_next_human_actions_packet_verification",
        "status": "pass" if passed else "fail",
        "packet_path": "post_pub/NEXT_HUMAN_ACTIONS_PACKET_v0_1.json",
        "checks": checks,
        "next_action": actions[0] if actions else None,
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "human_actions_pending": True,
            "route_complete": False,
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
