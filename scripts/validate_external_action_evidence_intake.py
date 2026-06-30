#!/usr/bin/env python3
"""Validate external action evidence intake without performing external actions."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INTAKE = ROOT / "post_pub" / "EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json"

PENDING_STATUSES = {
    "pending_human_upload",
    "pending_human_post",
    "pending_human_submission",
    "waiting_on_external_response",
}

RECORDED_STATUSES = {
    "youtube_url_recorded",
    "forum_url_recorded",
    "discussion_url_recorded",
    "hotcrp_confirmation_recorded",
    "third_party_feedback_recorded",
}

FALSE_BY_DEFAULT_FLAGS = [
    "external_adoption_claim",
    "peer_review_claim",
    "joss_readiness_claim",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_url_like(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def validate_slot(slot: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = slot.get("status")
    source_url = slot.get("source_url")

    if status not in PENDING_STATUSES | RECORDED_STATUSES:
        errors.append(f"{slot.get('slot_id')}: unsupported status {status!r}")

    if status in PENDING_STATUSES:
        if source_url is not None:
            errors.append(f"{slot.get('slot_id')}: pending slot must not include source_url")
        for field in ("evidence_date", "recorded_by"):
            if slot.get(field) is not None:
                errors.append(f"{slot.get('slot_id')}: pending slot must not include {field}")

    if status in RECORDED_STATUSES:
        if not isinstance(source_url, str) or not is_url_like(source_url):
            errors.append(f"{slot.get('slot_id')}: recorded slot requires http(s) source_url")
        for field in ("evidence_date", "recorded_by", "claim_boundary"):
            if not slot.get(field):
                errors.append(f"{slot.get('slot_id')}: recorded slot requires {field}")

    if slot.get("slot_id") == "third_party_feedback" and status == "third_party_feedback_recorded":
        for field in ("reporting_party", "what_was_run", "observed_result"):
            if not slot.get(field):
                errors.append(f"third_party_feedback: recorded feedback requires {field}")

    return errors


def expected_boundary(payload: dict[str, Any]) -> dict[str, bool]:
    slots = {slot["slot_id"]: slot for slot in payload.get("evidence_slots", [])}
    return {
        "external_action_recorded": any(slot.get("status") in RECORDED_STATUSES for slot in slots.values()),
        "youtube_upload_performed": slots.get("youtube_video", {}).get("status") == "youtube_url_recorded",
        "forum_posts_published": any(
            slots.get(slot_id, {}).get("status") in {"forum_url_recorded", "discussion_url_recorded"}
            for slot_id in ("langchain_forum_post", "mcp_discussion_post")
        ),
        "hotcrp_submission_performed": slots.get("hotcrp_submission", {}).get("status")
        == "hotcrp_confirmation_recorded",
        "external_feedback_recorded": slots.get("third_party_feedback", {}).get("status")
        == "third_party_feedback_recorded",
        "external_reproduction_recorded": slots.get("third_party_feedback", {}).get("status")
        == "third_party_feedback_recorded"
        and bool(slots.get("third_party_feedback", {}).get("what_was_run")),
    }


def validate(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    errors: list[str] = []

    if payload.get("object_type") != "ecl_external_action_evidence_intake_template":
        errors.append("object_type must be ecl_external_action_evidence_intake_template")

    slots = payload.get("evidence_slots")
    if not isinstance(slots, list) or not slots:
        errors.append("evidence_slots must be a non-empty list")
        slots = []

    seen_slot_ids: set[str] = set()
    for slot in slots:
        slot_id = slot.get("slot_id")
        if not slot_id:
            errors.append("slot missing slot_id")
        elif slot_id in seen_slot_ids:
            errors.append(f"duplicate slot_id {slot_id}")
        else:
            seen_slot_ids.add(slot_id)
        errors.extend(validate_slot(slot))

    boundary = payload.get("boundary", {})
    expected = expected_boundary(payload)
    for key, expected_value in expected.items():
        if boundary.get(key) is not expected_value:
            errors.append(f"boundary.{key} expected {expected_value!r}, got {boundary.get(key)!r}")

    for key in FALSE_BY_DEFAULT_FLAGS:
        if boundary.get(key) is not False:
            errors.append(f"boundary.{key} must remain false")

    template_only_expected = not expected["external_action_recorded"]
    if boundary.get("template_only") is not template_only_expected:
        errors.append(
            f"boundary.template_only expected {template_only_expected!r}, got {boundary.get('template_only')!r}"
        )

    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_external_action_evidence_intake_validation",
        "status": "pass" if not errors else "fail",
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "slot_count": len(slots),
        "recorded_slot_count": sum(1 for slot in slots if slot.get("status") in RECORDED_STATUSES),
        "errors": errors,
        "boundary": {
            "validation_only": True,
            "writes_external_state": False,
            "external_adoption_claim": False,
            "peer_review_claim": False,
        },
    }


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_INTAKE
    if not path.is_absolute():
        path = ROOT / path
    report = validate(path)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
