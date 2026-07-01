from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "post_pub" / "NEXT_HUMAN_ACTIONS_PACKET_v0_1.json"
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"


class NextHumanActionsPacketTests(unittest.TestCase):
    def load_packet(self) -> dict:
        return json.loads(PACKET_PATH.read_text(encoding="utf-8"))

    def test_packet_has_expected_ordered_human_actions(self) -> None:
        packet = self.load_packet()
        self.assertEqual(packet["status"], "human_actions_pending_not_executed")
        self.assertEqual(packet["source_status"], "actionable_local_gates_pass_future_external_steps_open")
        expected_ids = [
            "review_video_candidate",
            "upload_youtube_video",
            "record_youtube_url",
            "post_langchain_feedback_request",
            "post_mcp_feedback_request",
            "submit_icse_tool_demo",
            "record_third_party_feedback",
            "continue_monthly_maintenance",
        ]
        actions = packet["actions"]
        self.assertEqual([action["id"] for action in actions], expected_ids)
        self.assertEqual([action["order"] for action in actions], list(range(1, 9)))
        for action in actions:
            self.assertNotIn(action["status"], {"complete", "done", "posted", "submitted", "published"})

    def test_packet_actions_are_bounded_subset_of_external_queue(self) -> None:
        packet_ids = [action["id"] for action in self.load_packet()["actions"]]
        queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        queue_ids = [action["id"] for action in queue["actions"]]
        for action_id in packet_ids:
            self.assertIn(action_id, queue_ids)

    def test_packet_references_existing_input_packets(self) -> None:
        actions = self.load_packet()["actions"]
        self.assertEqual(
            actions[0]["input_packet"],
            "paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.md",
        )
        self.assertEqual(
            actions[0]["verification_command"],
            "python3 scripts/verify_video_human_review_packet.py",
        )
        self.assertEqual(
            actions[1]["input_packet"],
            "paper/workshop/YOUTUBE_UPLOAD_PREFLIGHT_v0_1.md",
        )
        for action in actions:
            input_packet = action["input_packet"]
            self.assertTrue((ROOT / input_packet).exists(), input_packet)

    def test_packet_preserves_external_boundary(self) -> None:
        boundary = self.load_packet()["boundary"]
        self.assertTrue(boundary["packet_only"])
        self.assertTrue(boundary["human_actions_pending"])
        for key in (
            "youtube_upload_performed",
            "forum_posts_published",
            "hotcrp_submission_performed",
            "external_feedback_recorded",
            "external_adoption_claim",
            "peer_review_claim",
            "icse_acceptance_claim",
            "joss_readiness_claim",
            "route_complete",
        ):
            self.assertFalse(boundary[key], key)

    def test_agent_index_exposes_next_human_actions_packet(self) -> None:
        index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["entrypoints"]["next_human_actions_packet"], "post_pub/NEXT_HUMAN_ACTIONS_PACKET_v0_1.md")
        self.assertEqual(
            index["entrypoints"]["next_human_actions_packet_verifier"],
            "python3 scripts/verify_next_human_actions_packet.py",
        )
        self.assertIn("post_pub/NEXT_HUMAN_ACTIONS_PACKET_v0_1.md", index["primary_artifacts"])
        self.assertIn("post_pub/NEXT_HUMAN_ACTIONS_PACKET_v0_1.json", index["primary_artifacts"])
        self.assertIn("scripts/verify_next_human_actions_packet.py", index["primary_artifacts"])

    def test_next_human_actions_verifier_reports_pass_without_external_writes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_next_human_actions_packet.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["next_action"]["id"], "review_video_candidate")
        self.assertTrue(report["boundary"]["verification_only"])
        self.assertTrue(report["boundary"]["human_actions_pending"])
        self.assertFalse(report["boundary"]["writes_external_state"])
        self.assertFalse(report["boundary"]["route_complete"])
        self.assertFalse(report["boundary"]["external_adoption_claim"])
        self.assertFalse(report["boundary"]["peer_review_claim"])


if __name__ == "__main__":
    unittest.main()
