#!/usr/bin/env python3
"""Verify the local ICSE 2027 tool-demo package without submitting it."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"
INTAKE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json"


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


def resolve_manifest_path(argv: list[str]) -> Path:
    if len(argv) > 1:
        path = Path(argv[1])
        return path if path.is_absolute() else ROOT / path
    return DEFAULT_MANIFEST


def verify(manifest_path: Path) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    queue = load_json(QUEUE_PATH)
    intake = load_json(INTAKE_PATH)
    checks: list[dict[str, Any]] = []

    checks.append(
        check(
            manifest.get("object_type") == "ecl_icse_2027_tool_demo_manifest",
            "manifest_object_type",
            {"object_type": manifest.get("object_type")},
        )
    )

    local_files = manifest.get("local_files", {})
    missing_files = [
        path
        for path in local_files.values()
        if isinstance(path, str) and not (ROOT / path).exists()
    ]
    checks.append(check(not missing_files, "local_files_exist", {"missing_files": missing_files}))

    paper = manifest.get("paper", {})
    source_path = ROOT / local_files.get("ieee_source", "")
    pdf_path = ROOT / local_files.get("ieee_pdf", "")
    source_hash = file_sha256(source_path) if source_path.exists() else None
    pdf_hash = file_sha256(pdf_path) if pdf_path.exists() else None
    checks.append(
        check(
            paper.get("pdf_rendered") is True
            and source_hash == paper.get("source_sha256")
            and pdf_hash == paper.get("pdf_sha256")
            and int(paper.get("pages", 999)) <= int(paper.get("page_limit", 0))
            and paper.get("pdf_human_review_required") is True
            and paper.get("pdf_camera_ready") is False,
            "paper_pdf_and_source_match_manifest",
            {
                "source": rel(source_path),
                "source_sha256": source_hash,
                "expected_source_sha256": paper.get("source_sha256"),
                "pdf": rel(pdf_path),
                "pdf_sha256": pdf_hash,
                "expected_pdf_sha256": paper.get("pdf_sha256"),
                "pages": paper.get("pages"),
                "page_limit": paper.get("page_limit"),
                "pdf_camera_ready": paper.get("pdf_camera_ready"),
            },
        )
    )

    public_link_report = load_json(ROOT / manifest["public_link_check"]["path"])
    link_statuses = [link.get("status") for link in public_link_report.get("links", [])]
    checks.append(
        check(
            manifest["public_link_check"].get("performed") is True
            and manifest["public_link_check"].get("status") == "all_checked_links_reachable"
            and public_link_report.get("status") == "public_links_verified"
            and link_statuses
            and all(status == "reachable" for status in link_statuses),
            "public_link_check_report_is_green",
            {
                "path": manifest["public_link_check"].get("path"),
                "manifest_status": manifest["public_link_check"].get("status"),
                "report_status": public_link_report.get("status"),
                "link_statuses": link_statuses,
            },
        )
    )

    video = manifest.get("video", {})
    video_path = ROOT / video.get("local_candidate_path", "")
    video_hash = file_sha256(video_path) if video_path.exists() else None
    video_asset_manifest_md = ROOT / local_files.get("video_asset_manifest", "")
    video_asset_manifest_json = video_asset_manifest_md.with_suffix(".json")
    video_assets = load_json(video_asset_manifest_json) if video_asset_manifest_json.exists() else {}
    video_asset_text_paths = [
        ROOT / "paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.srt",
        ROOT / "paper/workshop/video/voiceover_text.txt",
        ROOT / "paper/workshop/video/make_demo_output.txt",
    ]
    stale_count_patterns = ["Ran 78 tests", "Ran 98 tests", "seventy eight tests", "ninety eight tests"]
    stale_count_hits = [
        {
            "path": rel(path),
            "pattern": pattern,
        }
        for path in video_asset_text_paths
        if path.exists()
        for pattern in stale_count_patterns
        if pattern in path.read_text(encoding="utf-8")
    ]
    checks.append(
        check(
            video.get("local_candidate_generated") is True
            and video_hash == video.get("local_candidate_sha256")
            and video.get("duration_between_three_and_five_minutes") is True
            and 180 <= float(video.get("duration_seconds", 0)) <= 300
            and video.get("video_audio_duration_aligned") is True
            and video.get("captions_bounded_inside_video_duration") is True
            and video.get("youtube_upload_performed") is False
            and video.get("youtube_url") is None
            and video.get("human_review_required") is True,
            "video_candidate_matches_manifest_and_upload_is_pending",
            {
                "path": rel(video_path),
                "sha256": video_hash,
                "expected_sha256": video.get("local_candidate_sha256"),
                "duration_seconds": video.get("duration_seconds"),
                "youtube_upload_performed": video.get("youtube_upload_performed"),
                "youtube_url": video.get("youtube_url"),
            },
        )
    )

    checks.append(
        check(
            video_assets.get("candidate_video", {}).get("sha256") == video.get("local_candidate_sha256")
            and video_assets.get("verified_requirements", {}).get("avoids_fixed_test_count_claim") is True
            and not stale_count_hits,
            "video_assets_avoid_fixed_test_count_claims",
            {
                "asset_manifest": rel(video_asset_manifest_json),
                "asset_manifest_video_sha256": video_assets.get("candidate_video", {}).get("sha256"),
                "manifest_video_sha256": video.get("local_candidate_sha256"),
                "stale_count_hits": stale_count_hits,
            },
        )
    )

    demo = manifest.get("demo", {})
    queue_inputs = queue.get("current_verified_inputs", {})
    checks.append(
        check(
            demo.get("make_demo_verified") is True
            and demo.get("docker_demo_verified") is True
            and demo.get("dependency_mode_result_hash")
            == queue_inputs.get("make_demo_dependency_hash")
            and demo.get("external_recognition_result_hash")
            == queue_inputs.get("make_demo_external_recognition_hash"),
            "demo_hashes_match_action_queue",
            {
                "make_demo_verified": demo.get("make_demo_verified"),
                "docker_demo_verified": demo.get("docker_demo_verified"),
                "dependency_hash": demo.get("dependency_mode_result_hash"),
                "queue_dependency_hash": queue_inputs.get("make_demo_dependency_hash"),
                "external_recognition_hash": demo.get("external_recognition_result_hash"),
                "queue_external_recognition_hash": queue_inputs.get("make_demo_external_recognition_hash"),
            },
        )
    )

    target = manifest.get("target", {})
    boundary = manifest.get("boundary", {})
    checks.append(
        check(
            target.get("submission_performed") is False
            and target.get("portal_upload_performed") is False
            and target.get("youtube_upload_performed") is False
            and boundary.get("no_icse_submission_claim") is True
            and boundary.get("final_video_upload_pending") is True
            and boundary.get("youtube_upload_pending") is True
            and boundary.get("no_external_adoption_claim") is True
            and boundary.get("no_production_deployment_claim") is True,
            "external_submission_boundaries_remain_false",
            {
                "submission_performed": target.get("submission_performed"),
                "portal_upload_performed": target.get("portal_upload_performed"),
                "youtube_upload_performed": target.get("youtube_upload_performed"),
                "boundary": boundary,
            },
        )
    )

    checks.append(
        check(
            intake.get("boundary", {}).get("external_action_recorded") is False
            and intake.get("boundary", {}).get("youtube_upload_performed") is False
            and intake.get("boundary", {}).get("hotcrp_submission_performed") is False
            and intake.get("boundary", {}).get("external_feedback_recorded") is False,
            "external_evidence_intake_is_still_empty",
            intake.get("boundary", {}),
        )
    )

    passed = all(item["status"] == "pass" for item in checks)
    return {
        "schema_version": "0.1.0",
        "object_type": "ecl_icse_tool_demo_package_verification",
        "status": "pass" if passed else "fail",
        "manifest_path": rel(manifest_path),
        "next_human_actions": [
            "review local video candidate",
            "upload final video to YouTube if approved",
            "record YouTube URL through the external action evidence intake gate",
            "submit through HotCRP only after human review",
        ],
        "checks": checks,
        "boundary": {
            "verification_only": True,
            "writes_external_state": False,
            "youtube_upload_performed": False,
            "hotcrp_submission_performed": False,
            "icse_acceptance_claim": False,
            "peer_review_claim": False,
            "external_adoption_claim": False,
        },
    }


def main(argv: list[str]) -> int:
    manifest_path = resolve_manifest_path(argv)
    report = verify(manifest_path)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
