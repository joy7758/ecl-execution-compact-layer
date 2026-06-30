from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PostJSSRouteVerifierTests(unittest.TestCase):
    def test_post_jss_route_verifier_reports_local_gates_pass_and_open_external_steps(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_post_jss_route.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "actionable_local_gates_pass_future_external_steps_open")
        self.assertFalse(report["boundary"]["route_complete"])
        self.assertFalse(report["boundary"]["writes_external_state"])
        self.assertFalse(report["boundary"]["youtube_upload_performed"])
        self.assertFalse(report["boundary"]["hotcrp_submission_performed"])
        self.assertFalse(report["boundary"]["external_feedback_recorded"])
        self.assertGreaterEqual(len(report["open_external_steps"]), 5)

        check_statuses = {check["name"]: check["status"] for check in report["checks"]}
        self.assertEqual(check_statuses["zenodo_doi_and_citation_surfaces"], "pass")
        self.assertEqual(check_statuses["technical_report_surface"], "pass")
        self.assertEqual(check_statuses["jss_closed_and_joss_deferral_recorded"], "pass")
        self.assertEqual(check_statuses["icse_tool_demo_package_verifier"], "pass")
        self.assertEqual(check_statuses["external_actions_remain_pending_not_claimed"], "pass")

    def test_agent_index_exposes_post_jss_route_verifier(self) -> None:
        index = json.loads((ROOT / "agent-index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["entrypoints"]["post_jss_route_verifier"], "python3 scripts/verify_post_jss_route.py")
        self.assertIn("scripts/verify_post_jss_route.py", index["primary_artifacts"])


if __name__ == "__main__":
    unittest.main()
