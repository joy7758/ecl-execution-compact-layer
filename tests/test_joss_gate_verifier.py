from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]

class JOSSGateVerifierTests(unittest.TestCase):
    def test_gate_verifier_records_joss_blockers_and_advisory_signals(self) -> None:
        with tempfile.TemporaryDirectory() as output_dir:
            env = os.environ.copy()
            env["ECL_JOSS_GATE_OUTPUT_DIR"] = output_dir
            result = subprocess.run(
                [sys.executable, "scripts/joss_gate_verifier.py"],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = Path(output_dir) / "JOSS_GATE_VERIFICATION_v0_1.json"
            payload = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], "joss_gate_failed_blockers")
        self.assertTrue(payload["decision"]["content_package_ready"])
        self.assertFalse(payload["decision"]["immediate_joss_submission_recommended"])
        self.assertEqual(payload["gates"]["required_files"]["status"], "pass")
        self.assertEqual(payload["gates"]["standard_paper_mirror"]["status"], "pass")
        self.assertEqual(payload["gates"]["experiment_reports"]["status"], "pass")
        self.assertEqual(payload["gates"]["research_impact"]["status"], "pass")
        self.assertTrue(payload["gates"]["research_impact"]["evidence"]["statement_of_need_present"])
        self.assertTrue(payload["gates"]["research_impact"]["evidence"]["research_impact_statement_present"])
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["total_source_fields"], 81)
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["direct_mapped_field_count"], 80)
        self.assertEqual(payload["gates"]["experiment_reports"]["mapping_coverage"]["source_hash_only_field_count"], 1)
        self.assertIn(payload["gates"]["public_repo_sync"]["status"], {"pass", "fail_uncommitted_changes"})
        self.assertEqual(payload["gates"]["public_history"]["status"], "fail_current_state")
        self.assertEqual(payload["advisory_signals"]["external_impact"]["status"], "unverified")
        self.assertFalse(payload["advisory_signals"]["external_impact"]["blocking"])
        if payload["gates"]["public_repo_sync"]["status"] == "pass":
            self.assertNotIn("public_repo_sync", payload["blocking_gates"])
            self.assertTrue(payload["boundary"]["public_repo_synced"])
        else:
            self.assertIn("public_repo_sync", payload["blocking_gates"])
            self.assertFalse(payload["boundary"]["public_repo_synced"])
        self.assertIn("public_history", payload["blocking_gates"])
        self.assertNotIn("external_impact", payload["blocking_gates"])
        self.assertTrue(payload["boundary"]["research_impact_verified"])
        self.assertFalse(payload["boundary"]["joss_submission_performed"])


if __name__ == "__main__":
    unittest.main()
