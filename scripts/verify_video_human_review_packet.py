#!/usr/bin/env python3
"""Verify the local ICSE video human-review packet without approving it."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "paper" / "workshop" / "video" / "VIDEO_HUMAN_REVIEW_PACKET_v0_1.json"
ICSE_MANIFEST_PATH = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"
ASSET_MANIFEST_PATH = ROOT / "paper" / "workshop" / "video" / "VIDEO_ASSET_MANIFEST_v0_1.json"
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"

FALSE_FLAGS = [
    "video_approved",
    "youtube_upload_performed",
    "hotcrp_submission_performed",
    "external_feedback_recorded",
    "external_adoption_claim",
    "peer_review_claim",
    "icse_acceptance_claim",
    "joss_readiness_claim",
    "route_complete",
]

STALE_COUNT_PATTERNS = [
    "Ran 78 tests",
    "Ran 98 tests",
    "seventy eight tests",
    "ninety eight tests",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check(condition: bool, name: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "status": "pass" if condition else "fail",
        "details": details,
    }


def stale_count_hits(paths: list[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in STALE_COUNT_PATTERNS:
            if pattern in text:
                hits.append({"path": rel(path), "pattern": pattern})
    return hits


def verify() -> dict[str, Any]:
    packet = load_json(PACKET_PATH)
    icse_manifest = load_json(ICSE_MANIFEST_PATH)
    asset_manifest = load_json(ASSET_MANIFEST_PATH)
    queue = load_json(QUEUE_PATH)
    candidate = packet.get("candidate", {})
    decision = packet.get("decision", {})
    boundary = packet.get("boundary", {})
    checks: list[dict[str, Any]] = []

    checks.append(
        check(
            packet.get("object_type") == "ecl_icse_video_human_review_packet"
            and packet.get("status") == "pending_human_review_not_approved",
            "packet_status_is_pending_review",
            {"object_type": packet.get("object_type"), "status": packet.get("status")},
        )
    )

    video_path = ROOT / candidate.get("video", "")
    caption_path = ROOT / candidate.get("caption", "")
    referenced_packets = [
        ROOT / candidate.get("qa_report", ""),
        ROOT / candidate.get("asset_manifest", ""),
        ROOT / candidate.get("youtube_handoff", ""),
    ]
    missing_files = [
        rel(path)
        for path in [video_path, caption_path, *referenced_packets]
        if not path.exists()
    ]
    checks.append(check(not missing_files, "candidate_and_packets_exist", {"missing_files": missing_files}))

    actual_video_hash = file_sha256(video_path) if video_path.exists() else None
    actual_caption_hash = file_sha256(caption_path) if caption_path.exists() else None
    manifest_video_hash = icse_manifest.get("video", {}).get("local_candidate_sha256")
    asset_video_hash = asset_manifest.get("candidate_video", {}).get("sha256")
    queue_video_hash = queue.get("current_verified_inputs", {}).get("video_candidate_sha256")
    checks.append(
        check(
            actual_video_hash == candidate.get("video_sha256")
            and actual_video_hash == manifest_video_hash
            and actual_video_hash == asset_video_hash
            and actual_video_hash == queue_video_hash
            and actual_caption_hash == candidate.get("caption_sha256"),
            "candidate_hashes_match_manifests_and_queue",
            {
                "actual_video_sha256": actual_video_hash,
                "packet_video_sha256": candidate.get("video_sha256"),
                "icse_manifest_video_sha256": manifest_video_hash,
                "asset_manifest_video_sha256": asset_video_hash,
                "queue_video_sha256": queue_video_hash,
                "actual_caption_sha256": actual_caption_hash,
                "packet_caption_sha256": candidate.get("caption_sha256"),
            },
        )
    )

    duration = float(candidate.get("duration_seconds", 0))
    checks.append(
        check(
            180 <= duration <= 300
            and icse_manifest.get("video", {}).get("duration_between_three_and_five_minutes") is True
            and asset_manifest.get("verified_requirements", {}).get("duration_between_three_and_five_minutes") is True
            and asset_manifest.get("verified_requirements", {}).get("captions_bounded_inside_video_duration") is True,
            "duration_and_caption_requirements_hold",
            {
                "duration_seconds": duration,
                "duration_human": candidate.get("duration_human"),
                "icse_duration_between_three_and_five": icse_manifest.get("video", {}).get("duration_between_three_and_five_minutes"),
                "asset_duration_between_three_and_five": asset_manifest.get("verified_requirements", {}).get("duration_between_three_and_five_minutes"),
                "captions_bounded": asset_manifest.get("verified_requirements", {}).get("captions_bounded_inside_video_duration"),
            },
        )
    )

    text_paths = [
        caption_path,
        ROOT / "paper/workshop/video/voiceover_text.txt",
        ROOT / "paper/workshop/video/make_demo_output.txt",
    ]
    hits = stale_count_hits(text_paths)
    checks.append(
        check(
            asset_manifest.get("verified_requirements", {}).get("avoids_fixed_test_count_claim") is True
            and not hits,
            "video_review_assets_avoid_fixed_test_count_claims",
            {"stale_count_hits": hits},
        )
    )

    checks.append(
        check(
            decision.get("review_decision") == "pending"
            and decision.get("approved_for_youtube_upload") is False
            and decision.get("reviewed_by") is None
            and decision.get("reviewed_at") is None
            and decision.get("replacement_required") is None,
            "decision_slots_are_unfilled_and_not_approved",
            {"decision": decision},
        )
    )

    checks.append(
        check(
            boundary.get("packet_only") is True
            and boundary.get("human_review_pending") is True
            and all(boundary.get(key) is False for key in FALSE_FLAGS),
            "boundary_preserves_pending_external_state",
            {"boundary": boundary},
        )
    )

    passed = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_icse_video_human_review_packet_verification",
        "status": "pass" if passed else "fail",
        "packet_path": rel(PACKET_PATH),
        "candidate_video_sha256": actual_video_hash,
        "checks": checks,
        "next_action": {
            "id": "human_review_video_candidate",
            "status": "pending_human_review",
            "input_packet": rel(PACKET_PATH),
        },
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "human_review_pending": True,
            "video_approved": False,
            "youtube_upload_performed": False,
            "hotcrp_submission_performed": False,
            "external_feedback_recorded": False,
            "route_complete": False,
        },
    }


def main() -> int:
    report = verify()
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
