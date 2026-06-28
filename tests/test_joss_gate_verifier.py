from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "paper" / "joss" / "JOSS_GATE_VERIFICATION_v0_1.json"


class JOSSGateVerifierTests(unittest.TestCase):
    def test_gate_verifier_records_external_blockers(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/joss_gate_verifier.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "joss_gate_failed_external_blockers")
        self.assertTrue(payload["decision"]["content_package_ready"])
        self.assertFalse(payload["decision"]["immediate_joss_submission_recommended"])
        self.assertEqual(payload["gates"]["required_files"]["status"], "pass")
        self.assertEqual(payload["gates"]["standard_paper_mirror"]["status"], "pass")
        self.assertEqual(payload["gates"]["experiment_reports"]["status"], "pass")
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["total_source_fields"], 81)
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["direct_mapped_field_count"], 80)
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["source_hash_only_field_count"], 1)
        self.assertEqual(payload["gates"]["public_repo_sync"]["status"], "fail_uncommitted_changes")
        self.assertEqual(payload["gates"]["public_history"]["status"], "fail_current_state")
        self.assertEqual(payload["gates"]["external_impact"]["status"], "unverified")
        self.assertIn("public_repo_sync", payload["blocking_gates"])
        self.assertIn("public_history", payload["blocking_gates"])
        self.assertIn("external_impact", payload["blocking_gates"])
        self.assertFalse(payload["boundary"]["public_repo_synced"])
        self.assertFalse(payload["boundary"]["joss_submission_performed"])


if __name__ == "__main__":
    unittest.main()
