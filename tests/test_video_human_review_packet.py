from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "paper" / "workshop" / "video" / "VIDEO_HUMAN_REVIEW_PACKET_v0_1.json"
ICSE_MANIFEST_PATH = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"


class VideoHumanReviewPacketTests(unittest.TestCase):
    def load_packet(self) -> dict:
        return json.loads(PACKET_PATH.read_text(encoding="utf-8"))

    def test_packet_is_pending_and_not_approved(self) -> None:
        packet = self.load_packet()
        self.assertEqual(packet["status"], "pending_human_review_not_approved")
        self.assertEqual(packet["decision"]["review_decision"], "pending")
        self.assertFalse(packet["decision"]["approved_for_youtube_upload"])
        self.assertIsNone(packet["decision"]["reviewed_by"])
        self.assertIsNone(packet["decision"]["reviewed_at"])
        self.assertIsNone(packet["decision"]["replacement_required"])

    def test_packet_candidate_hash_matches_current_video_and_manifests(self) -> None:
        packet = self.load_packet()
        candidate = packet["candidate"]
        video_path = ROOT / candidate["video"]
        caption_path = ROOT / candidate["caption"]
        icse_manifest = json.loads(ICSE_MANIFEST_PATH.read_text(encoding="utf-8"))
        queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))

        actual_video_hash = sha256(video_path.read_bytes()).hexdigest()
        actual_caption_hash = sha256(caption_path.read_bytes()).hexdigest()
        self.assertEqual(actual_video_hash, candidate["video_sha256"])
        self.assertEqual(actual_caption_hash, candidate["caption_sha256"])
        self.assertEqual(actual_video_hash, icse_manifest["video"]["local_candidate_sha256"])
        self.assertEqual(actual_video_hash, queue["current_verified_inputs"]["video_candidate_sha256"])

    def test_packet_preserves_no_external_action_boundary(self) -> None:
        boundary = self.load_packet()["boundary"]
        self.assertTrue(boundary["packet_only"])
        self.assertTrue(boundary["human_review_pending"])
        for key in (
            "video_approved",
            "youtube_upload_performed",
            "hotcrp_submission_performed",
            "external_feedback_recorded",
            "external_adoption_claim",
            "peer_review_claim",
            "icse_acceptance_claim",
            "joss_readiness_claim",
            "route_complete",
        ):
            self.assertFalse(boundary[key], key)

    def test_video_human_review_verifier_reports_pending_without_writes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_video_human_review_packet.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["next_action"]["id"], "human_review_video_candidate")
        self.assertTrue(report["boundary"]["verification_only"])
        self.assertTrue(report["boundary"]["human_review_pending"])
        self.assertFalse(report["boundary"]["writes_external_state"])
        self.assertFalse(report["boundary"]["video_approved"])
        self.assertFalse(report["boundary"]["youtube_upload_performed"])
        self.assertFalse(report["boundary"]["hotcrp_submission_performed"])
        self.assertFalse(report["boundary"]["route_complete"])


if __name__ == "__main__":
    unittest.main()
