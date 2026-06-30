from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"


class ICSEToolDemoPackageTests(unittest.TestCase):
    def test_icse_tool_demo_package_verifier_reports_pass_without_writes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_icse_tool_demo_package.py"],
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
        self.assertFalse(report["boundary"]["hotcrp_submission_performed"])
        self.assertFalse(report["boundary"]["peer_review_claim"])

        check_names = {check["name"] for check in report["checks"]}
        self.assertIn("paper_pdf_and_source_match_manifest", check_names)
        self.assertIn("video_candidate_matches_manifest_and_upload_is_pending", check_names)
        self.assertIn("video_assets_avoid_fixed_test_count_claims", check_names)
        self.assertIn("video_human_review_packet_is_pending_and_bound_to_candidate", check_names)
        self.assertIn("external_submission_boundaries_remain_false", check_names)

    def test_agent_index_exposes_icse_tool_demo_package_verifier(self) -> None:
        index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
        self.assertEqual(
            index["entrypoints"]["icse_video_candidate_builder"],
            "python3 scripts/build_icse_video_candidate.py",
        )
        self.assertEqual(
            index["entrypoints"]["icse_video_human_review_packet"],
            "paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.md",
        )
        self.assertEqual(
            index["entrypoints"]["icse_video_human_review_packet_verifier"],
            "python3 scripts/verify_video_human_review_packet.py",
        )
        self.assertEqual(
            index["entrypoints"]["icse_tool_demo_package_verifier"],
            "python3 scripts/verify_icse_tool_demo_package.py",
        )
        self.assertIn("scripts/build_icse_video_candidate.py", index["primary_artifacts"])
        self.assertIn("scripts/verify_video_human_review_packet.py", index["primary_artifacts"])
        self.assertIn("paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.md", index["primary_artifacts"])
        self.assertIn("paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.json", index["primary_artifacts"])
        self.assertIn("scripts/verify_icse_tool_demo_package.py", index["primary_artifacts"])

    def test_icse_tool_demo_package_verifier_rejects_unsupported_submission_claim(self) -> None:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        payload["target"]["submission_performed"] = True
        payload["boundary"]["no_icse_submission_claim"] = False

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            temp_path = handle.name
        try:
            result = subprocess.run(
                [sys.executable, "scripts/verify_icse_tool_demo_package.py", temp_path],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "fail")
            failed = {check["name"] for check in report["checks"] if check["status"] == "fail"}
            self.assertIn("external_submission_boundaries_remain_false", failed)
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
