from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCREENING_MD = ROOT / "paper" / "venue_screening" / "NO_PAID_JOURNAL_SCREENING_v0_1.md"
SCREENING_JSON = ROOT / "paper" / "venue_screening" / "NO_PAID_JOURNAL_SCREENING_v0_1.json"
COMPLETION_REPORT = ROOT / "paper" / "PAPER_COMPLETION_REPORT_v0_1.md"


class VenueScreeningTests(unittest.TestCase):
    def test_screening_artifacts_exist(self) -> None:
        self.assertTrue(SCREENING_MD.exists())
        self.assertTrue(SCREENING_JSON.exists())
        self.assertTrue(COMPLETION_REPORT.exists())

    def test_no_paid_journal_selected(self) -> None:
        screening = json.loads(SCREENING_JSON.read_text(encoding="utf-8"))
        self.assertFalse(screening["selected_paid_journal"])
        self.assertFalse(screening["boundary"]["paid_journal_selected"])
        self.assertFalse(screening["boundary"]["formal_submission"])
        for venue in screening["venues"]:
            self.assertIn(
                venue["classification"],
                {"eligible_zero_fee", "eligible_non_oa_route_only"},
                venue["name"],
            )
            self.assertNotEqual(venue["classification"], "excluded_paid_route")

    def test_paid_routes_are_explicitly_excluded(self) -> None:
        screening = json.loads(SCREENING_JSON.read_text(encoding="utf-8"))
        excluded_classes = {item["classification"] for item in screening["excluded"]}
        self.assertIn("excluded_paid_route", excluded_classes)
        self.assertIn("excluded_paid_open_access", excluded_classes)
        text = SCREENING_MD.read_text(encoding="utf-8")
        self.assertIn("No paid journal has been selected.", text)
        self.assertIn("exclude_open_access_apc_route", SCREENING_JSON.read_text(encoding="utf-8"))

    def test_completion_report_keeps_submission_boundary(self) -> None:
        text = COMPLETION_REPORT.read_text(encoding="utf-8")
        self.assertIn("content_complete_public_release_ready_joss_not_submitted", text)
        self.assertIn("formal_submission=false", text)
        self.assertIn("joss_submission_performed=false", text)
        self.assertIn("paid_journal_route_selected=false", text)


if __name__ == "__main__":
    unittest.main()
