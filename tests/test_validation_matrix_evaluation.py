from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "experiments" / "out" / "validation_matrix_evaluation.json"


class ValidationMatrixEvaluationTests(unittest.TestCase):
    def test_validation_matrix_is_deterministic(self) -> None:
        first = self._run_eval()
        first_payload = REPORT.read_text(encoding="utf-8")
        second = self._run_eval()
        second_payload = REPORT.read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_payload, second_payload)
        payload = json.loads(second_payload)
        summary = payload["summary"]
        self.assertTrue(summary["baseline_valid"])
        self.assertEqual(summary["case_count"], 8)
        self.assertEqual(summary["expected_invalid_count"], 8)
        self.assertEqual(summary["invalid_detected_count"], 8)
        self.assertEqual(summary["expectation_met_count"], 8)
        self.assertFalse(payload["boundary"]["third_party_validation"])
        self.assertFalse(payload["boundary"]["benchmark_result"])

    def test_validation_matrix_has_required_mutations(self) -> None:
        self._run_eval()
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        case_ids = {result["case_id"] for result in payload["results"]}
        self.assertEqual(
            case_ids,
            {
                "missing_state",
                "wrong_schema_version",
                "tampered_canonical_hash",
                "source_hash_mismatch",
                "empty_event_chain",
                "additional_root_property",
                "invalid_action_mode",
                "missing_evidence_hashes",
            },
        )
        self.assertTrue(all(result["error_count"] >= 1 for result in payload["results"]))

    def _run_eval(self) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "experiments/evaluate_validation_matrix.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result


if __name__ == "__main__":
    unittest.main()
