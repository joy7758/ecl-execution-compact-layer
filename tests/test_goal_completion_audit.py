from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "paper" / "final_audit" / "GOAL_COMPLETION_AUDIT_v0_1.md"
AUDIT_JSON = ROOT / "paper" / "final_audit" / "GOAL_COMPLETION_AUDIT_v0_1.json"
HUMAN_PACKET = ROOT / "paper" / "final_audit" / "HUMAN_ACTION_PACKET_v0_1.md"


class GoalCompletionAuditTests(unittest.TestCase):
    def test_final_audit_artifacts_exist(self) -> None:
        self.assertTrue(AUDIT_MD.exists())
        self.assertTrue(AUDIT_JSON.exists())
        self.assertTrue(HUMAN_PACKET.exists())

    def test_paper_and_screening_marked_complete(self) -> None:
        audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
        self.assertTrue(audit["complete_surfaces"]["paper_creation_complete"])
        self.assertTrue(audit["complete_surfaces"]["venue_screening_complete"])
        self.assertFalse(audit["complete_surfaces"]["paid_journal_selected"])
        complete_ids = {
            item["id"]
            for item in audit["requirements"]
            if item["status"] == "complete"
        }
        self.assertIn("general-paper", complete_ids)
        self.assertIn("joss-paper", complete_ids)
        self.assertIn("venue-screening", complete_ids)
        self.assertIn("paid-journal-excluded", complete_ids)

    def test_submission_boundaries_remain_false(self) -> None:
        audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8"))
        incomplete = audit["incomplete_surfaces"]
        self.assertFalse(incomplete["formal_submission"])
        self.assertFalse(incomplete["joss_submission_ready"])
        self.assertFalse(incomplete["joss_submission_performed"])
        self.assertFalse(incomplete["public_release"])
        self.assertFalse(incomplete["github_release_created"])
        self.assertFalse(incomplete["license_selected"])
        for value in audit["boundary"].values():
            self.assertFalse(value)

    def test_human_action_packet_lists_required_inputs(self) -> None:
        text = HUMAN_PACKET.read_text(encoding="utf-8")
        for phrase in (
            "Author name",
            "Author affiliation",
            "OSI-approved license choice",
            "Public repository URL",
            "Final author approval",
        ):
            self.assertIn(phrase, text)
        self.assertIn("The final submission click remains a separate human action.", text)

    def test_no_paid_journal_screening_is_still_false(self) -> None:
        screening = json.loads((ROOT / "paper" / "venue_screening" / "NO_PAID_JOURNAL_SCREENING_v0_1.json").read_text(encoding="utf-8"))
        self.assertFalse(screening["selected_paid_journal"])
        self.assertEqual(screening["preferred_no_fee_candidate"], "JOSS")


if __name__ == "__main__":
    unittest.main()
