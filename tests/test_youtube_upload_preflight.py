from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_PATH = ROOT / "paper" / "workshop" / "YOUTUBE_UPLOAD_PREFLIGHT_v0_1.json"
VIDEO_REVIEW_PATH = ROOT / "paper" / "workshop" / "video" / "VIDEO_HUMAN_REVIEW_PACKET_v0_1.json"
INTAKE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json"


class YouTubeUploadPreflightTests(unittest.TestCase):
    def load_preflight(self) -> dict:
        return json.loads(PREFLIGHT_PATH.read_text(encoding="utf-8"))

    def test_preflight_is_blocked_until_review_approval(self) -> None:
        preflight = self.load_preflight()
        review = json.loads(VIDEO_REVIEW_PATH.read_text(encoding="utf-8"))
        self.assertEqual(preflight["status"], "preflight_inputs_ready_blocked_until_video_review_approved")
        self.assertEqual(review["status"], "pending_human_review_not_approved")
        self.assertFalse(preflight["current_gate"]["approved_for_youtube_upload"])
        self.assertFalse(preflight["current_gate"]["youtube_upload_performed"])
        self.assertIsNone(preflight["current_gate"]["youtube_url"])

    def test_upload_hashes_match_local_files_and_review_packet(self) -> None:
        preflight = self.load_preflight()
        review = json.loads(VIDEO_REVIEW_PATH.read_text(encoding="utf-8"))
        inputs = preflight["upload_inputs"]
        video_hash = sha256((ROOT / inputs["video"]).read_bytes()).hexdigest()
        caption_hash = sha256((ROOT / inputs["caption"]).read_bytes()).hexdigest()
        self.assertEqual(video_hash, inputs["video_sha256"])
        self.assertEqual(caption_hash, inputs["caption_sha256"])
        self.assertEqual(video_hash, review["candidate"]["video_sha256"])
        self.assertEqual(caption_hash, review["candidate"]["caption_sha256"])

    def test_youtube_evidence_slot_is_empty(self) -> None:
        intake = json.loads(INTAKE_PATH.read_text(encoding="utf-8"))
        slots = {slot["slot_id"]: slot for slot in intake["evidence_slots"]}
        youtube_slot = slots["youtube_video"]
        self.assertEqual(youtube_slot["status"], "pending_human_upload")
        self.assertIsNone(youtube_slot["source_url"])
        self.assertFalse(intake["boundary"]["youtube_upload_performed"])
        self.assertFalse(intake["boundary"]["external_action_recorded"])

    def test_preflight_boundary_preserves_no_external_upload(self) -> None:
        boundary = self.load_preflight()["boundary"]
        self.assertTrue(boundary["preflight_only"])
        self.assertTrue(boundary["blocked_until_video_review_approved"])
        for key in (
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
        ):
            self.assertFalse(boundary[key], key)

    def test_youtube_upload_preflight_verifier_reports_pass_without_writes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_youtube_upload_preflight.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["next_action"]["id"], "approve_or_reject_video_candidate")
        self.assertTrue(report["next_action"]["blocked_upload"])
        self.assertTrue(report["boundary"]["verification_only"])
        self.assertTrue(report["boundary"]["human_review_pending"])
        self.assertFalse(report["boundary"]["writes_external_state"])
        self.assertFalse(report["boundary"]["youtube_upload_performed"])
        self.assertFalse(report["boundary"]["youtube_url_recorded"])
        self.assertFalse(report["boundary"]["hotcrp_submission_performed"])
        self.assertFalse(report["boundary"]["route_complete"])


if __name__ == "__main__":
    unittest.main()
