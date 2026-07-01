#!/usr/bin/env python3
"""Verify the local YouTube upload preflight packet without uploading."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_PATH = ROOT / "paper" / "workshop" / "YOUTUBE_UPLOAD_PREFLIGHT_v0_1.json"
METADATA_PATH = ROOT / "paper" / "workshop" / "YOUTUBE_METADATA_DRAFT_v0_1.md"
VIDEO_REVIEW_PATH = ROOT / "paper" / "workshop" / "video" / "VIDEO_HUMAN_REVIEW_PACKET_v0_1.json"
INTAKE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json"

FALSE_FLAGS = [
    "human_approval_recorded",
    "youtube_upload_performed",
    "youtube_url_recorded",
    "hotcrp_submission_performed",
    "external_feedback_recorded",
    "external_adoption_claim",
    "peer_review_claim",
    "icse_acceptance_claim",
    "joss_readiness_claim",
    "route_complete",
]

FORBIDDEN_METADATA_PHRASES = [
    "peer-review acceptance",
    "production deployment",
    "external adoption",
    "benchmark superiority",
    "standards-body endorsement",
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


def metadata_key(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}=(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def unsupported_positive_claims(text: str) -> list[str]:
    hits: list[str] = []
    lower_text = text.lower()
    for phrase in FORBIDDEN_METADATA_PHRASES:
        phrase_lower = phrase.lower()
        start = 0
        while True:
            index = lower_text.find(phrase_lower, start)
            if index == -1:
                break
            prefix = lower_text[max(0, index - 180) : index]
            if "not " not in prefix and "no " not in prefix:
                hits.append(phrase)
            start = index + len(phrase_lower)
    return hits


def verify() -> dict[str, Any]:
    preflight = load_json(PREFLIGHT_PATH)
    review = load_json(VIDEO_REVIEW_PATH)
    intake = load_json(INTAKE_PATH)
    inputs = preflight.get("upload_inputs", {})
    gate = preflight.get("current_gate", {})
    boundary = preflight.get("boundary", {})
    checks: list[dict[str, Any]] = []

    checks.append(
        check(
            preflight.get("object_type") == "ecl_youtube_upload_preflight"
            and preflight.get("status") == "preflight_inputs_ready_blocked_until_video_review_approved",
            "preflight_status_is_blocked_until_review_approved",
            {"object_type": preflight.get("object_type"), "status": preflight.get("status")},
        )
    )

    input_paths = [
        ROOT / inputs.get("video", ""),
        ROOT / inputs.get("caption", ""),
        ROOT / inputs.get("thumbnail", ""),
        ROOT / inputs.get("metadata", ""),
        ROOT / inputs.get("upload_handoff", ""),
        ROOT / inputs.get("video_review_packet", ""),
    ]
    missing_files = [rel(path) for path in input_paths if not path.exists()]
    checks.append(check(not missing_files, "upload_input_files_exist", {"missing_files": missing_files}))

    video_path = ROOT / inputs.get("video", "")
    caption_path = ROOT / inputs.get("caption", "")
    actual_video_hash = file_sha256(video_path) if video_path.exists() else None
    actual_caption_hash = file_sha256(caption_path) if caption_path.exists() else None
    review_candidate = review.get("candidate", {})
    checks.append(
        check(
            actual_video_hash == inputs.get("video_sha256")
            and actual_caption_hash == inputs.get("caption_sha256")
            and actual_video_hash == review_candidate.get("video_sha256")
            and actual_caption_hash == review_candidate.get("caption_sha256"),
            "upload_hashes_match_review_candidate",
            {
                "actual_video_sha256": actual_video_hash,
                "preflight_video_sha256": inputs.get("video_sha256"),
                "review_video_sha256": review_candidate.get("video_sha256"),
                "actual_caption_sha256": actual_caption_hash,
                "preflight_caption_sha256": inputs.get("caption_sha256"),
                "review_caption_sha256": review_candidate.get("caption_sha256"),
            },
        )
    )

    metadata_text = METADATA_PATH.read_text(encoding="utf-8")
    title = preflight.get("upload_metadata", {}).get("title")
    metadata_forbidden_hits = unsupported_positive_claims(metadata_text)
    checks.append(
        check(
            title in metadata_text
            and metadata_key(metadata_text, "video_sha256") == inputs.get("video_sha256")
            and metadata_key(metadata_text, "caption_sha256") == inputs.get("caption_sha256")
            and metadata_key(metadata_text, "youtube_upload_performed") == "false"
            and metadata_key(metadata_text, "youtube_url") == "<fill after human upload>"
            and not metadata_forbidden_hits,
            "metadata_draft_matches_inputs_and_boundary",
            {
                "title": title,
                "metadata_video_sha256": metadata_key(metadata_text, "video_sha256"),
                "metadata_caption_sha256": metadata_key(metadata_text, "caption_sha256"),
                "youtube_upload_performed": metadata_key(metadata_text, "youtube_upload_performed"),
                "youtube_url": metadata_key(metadata_text, "youtube_url"),
                "forbidden_hits": metadata_forbidden_hits,
            },
        )
    )

    checks.append(
        check(
            review.get("status") == "pending_human_review_not_approved"
            and review.get("decision", {}).get("approved_for_youtube_upload") is False
            and gate.get("video_review_status") == "pending_human_review_not_approved"
            and gate.get("approved_for_youtube_upload") is False
            and gate.get("youtube_upload_performed") is False
            and gate.get("youtube_url") is None,
            "upload_blocked_until_human_review_approval",
            {"review_status": review.get("status"), "review_decision": review.get("decision"), "gate": gate},
        )
    )

    slots = {slot.get("slot_id"): slot for slot in intake.get("evidence_slots", [])}
    youtube_slot = slots.get("youtube_video", {})
    checks.append(
        check(
            youtube_slot.get("status") == "pending_human_upload"
            and youtube_slot.get("source_url") is None
            and intake.get("boundary", {}).get("youtube_upload_performed") is False,
            "youtube_evidence_slot_is_empty",
            {"youtube_slot": youtube_slot, "intake_boundary": intake.get("boundary", {})},
        )
    )

    checks.append(
        check(
            boundary.get("preflight_only") is True
            and boundary.get("blocked_until_video_review_approved") is True
            and all(boundary.get(key) is False for key in FALSE_FLAGS),
            "boundary_preserves_no_external_upload_state",
            {"boundary": boundary},
        )
    )

    passed = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_youtube_upload_preflight_verification",
        "status": "pass" if passed else "fail",
        "preflight_path": rel(PREFLIGHT_PATH),
        "candidate_video_sha256": actual_video_hash,
        "checks": checks,
        "next_action": {
            "id": "approve_or_reject_video_candidate",
            "status": "pending_human_review",
            "blocked_upload": True,
        },
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "human_review_pending": True,
            "youtube_upload_performed": False,
            "youtube_url_recorded": False,
            "hotcrp_submission_performed": False,
            "route_complete": False,
        },
    }


def main() -> int:
    report = verify()
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
