from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"
INTAKE_PATH = ROOT / "post_pub" / "EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json"


class ExternalActionQueueTests(unittest.TestCase):
    def load_queue(self) -> dict:
        return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))

    def test_queue_has_expected_ordered_actions(self) -> None:
        queue = self.load_queue()
        self.assertEqual(queue["status"], "external_actions_queued_not_executed")
        expected_ids = [
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
        actions = queue["actions"]
        self.assertEqual([action["id"] for action in actions], expected_ids)
        self.assertEqual([action["order"] for action in actions], list(range(1, 11)))
        for action in actions:
            self.assertNotIn(action["status"], {"complete", "done", "posted", "submitted"})

    def test_queue_preserves_external_action_boundaries(self) -> None:
        boundary = self.load_queue()["boundary"]
        self.assertTrue(boundary["queue_only"])
        for key in (
            "youtube_upload_performed",
            "forum_posts_published",
            "hotcrp_submission_performed",
            "external_feedback_recorded",
            "external_adoption_claim",
            "peer_review_claim",
            "joss_readiness_claim",
        ):
            self.assertFalse(boundary[key], key)

    def test_queue_references_existing_local_packets(self) -> None:
        queue = self.load_queue()
        packet_values: list[str] = []
        for action in queue["actions"]:
            input_packet = action["input_packet"]
            if isinstance(input_packet, str):
                packet_values.append(input_packet)
            else:
                packet_values.extend(input_packet)

        for packet in packet_values:
            self.assertTrue((ROOT / packet).exists(), packet)

    def test_queue_hashes_match_current_artifacts_and_manifests(self) -> None:
        queue = self.load_queue()
        inputs = queue["current_verified_inputs"]
        video_path = ROOT / inputs["video_candidate"]
        self.assertEqual(
            sha256(video_path.read_bytes()).hexdigest(),
            inputs["video_candidate_sha256"],
        )

        icse_manifest = json.loads(
            (ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            inputs["video_candidate_sha256"],
            icse_manifest["video"]["local_candidate_sha256"],
        )
        self.assertEqual(
            inputs["make_demo_dependency_hash"],
            icse_manifest["demo"]["dependency_mode_result_hash"],
        )
        self.assertEqual(
            inputs["make_demo_external_recognition_hash"],
            icse_manifest["demo"]["external_recognition_result_hash"],
        )

        feedback_status = json.loads(
            (ROOT / "post_pub" / "FEEDBACK_REQUEST_STATUS_v0_1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            inputs["make_demo_dependency_hash"],
            feedback_status["expected_make_demo_hashes"]["dependency_mode_result_hash"],
        )
        self.assertEqual(
            inputs["make_demo_external_recognition_hash"],
            feedback_status["expected_make_demo_hashes"]["external_recognition_result_hash"],
        )

    def test_agent_index_exposes_queue(self) -> None:
        index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["entrypoints"]["external_action_queue"], "post_pub/EXTERNAL_ACTION_QUEUE_v0_1.md")
        self.assertEqual(
            index["entrypoints"]["external_action_queue_verifier"],
            "python3 scripts/verify_external_action_queue.py",
        )
        self.assertIn("post_pub/EXTERNAL_ACTION_QUEUE_v0_1.md", index["primary_artifacts"])
        self.assertIn("post_pub/EXTERNAL_ACTION_QUEUE_v0_1.json", index["primary_artifacts"])
        self.assertIn("scripts/verify_external_action_queue.py", index["primary_artifacts"])
        self.assertEqual(
            index["entrypoints"]["external_action_evidence_intake"],
            "post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.md",
        )
        self.assertEqual(
            index["entrypoints"]["external_action_evidence_intake_validator"],
            "python3 scripts/validate_external_action_evidence_intake.py",
        )
        self.assertIn("post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.md", index["primary_artifacts"])
        self.assertIn("post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json", index["primary_artifacts"])
        self.assertIn("scripts/validate_external_action_evidence_intake.py", index["primary_artifacts"])

    def test_external_action_queue_verifier_reports_pass_without_writes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_external_action_queue.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertTrue(report["boundary"]["verification_only"])
        self.assertFalse(report["boundary"]["writes_external_state"])
        self.assertFalse(report["boundary"]["youtube_upload_performed"])
        self.assertFalse(report["boundary"]["external_feedback_recorded"])

    def test_external_action_evidence_intake_template_is_empty_and_valid(self) -> None:
        payload = json.loads(INTAKE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "template_pending_external_evidence")
        for slot in payload["evidence_slots"]:
            self.assertIsNone(slot["source_url"])
            self.assertIsNone(slot["evidence_date"])
            self.assertIsNone(slot["recorded_by"])

        result = subprocess.run(
            [sys.executable, "scripts/validate_external_action_evidence_intake.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["recorded_slot_count"], 0)
        self.assertFalse(report["boundary"]["writes_external_state"])

    def test_external_action_evidence_intake_rejects_unsupported_claim_boundary(self) -> None:
        payload = json.loads(INTAKE_PATH.read_text(encoding="utf-8"))
        payload["boundary"]["peer_review_claim"] = True
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            temp_path = handle.name
        try:
            result = subprocess.run(
                [sys.executable, "scripts/validate_external_action_evidence_intake.py", temp_path],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "fail")
            self.assertIn("boundary.peer_review_claim must remain false", report["errors"])
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_external_action_evidence_intake_accepts_bounded_youtube_url(self) -> None:
        payload = json.loads(INTAKE_PATH.read_text(encoding="utf-8"))
        payload["status"] = "youtube_url_recorded"
        payload["boundary"]["template_only"] = False
        payload["boundary"]["external_action_recorded"] = True
        payload["boundary"]["youtube_upload_performed"] = True
        for slot in payload["evidence_slots"]:
            if slot["slot_id"] == "youtube_video":
                slot["status"] = "youtube_url_recorded"
                slot["source_url"] = "https://youtu.be/example"
                slot["evidence_date"] = "2026-06-30"
                slot["recorded_by"] = "Bin Zhang"

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            temp_path = handle.name
        try:
            result = subprocess.run(
                [sys.executable, "scripts/validate_external_action_evidence_intake.py", temp_path],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["recorded_slot_count"], 1)
            self.assertFalse(report["boundary"]["peer_review_claim"])
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
