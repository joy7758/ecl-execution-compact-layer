from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "experiments" / "out" / "mapping_coverage_evaluation.json"


class MappingCoverageEvaluationTests(unittest.TestCase):
    def test_mapping_coverage_is_deterministic(self) -> None:
        first = self._run_eval()
        first_payload = REPORT.read_text(encoding="utf-8")
        second = self._run_eval()
        second_payload = REPORT.read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_payload, second_payload)
        payload = json.loads(second_payload)
        summary = payload["summary"]
        self.assertEqual(summary["case_count"], 12)
        self.assertEqual(summary["by_runtime"], {"langchain": 6, "openai": 6})
        self.assertEqual(summary["total_source_fields"], 81)
        self.assertEqual(summary["direct_mapped_field_count"], 80)
        self.assertEqual(summary["source_hash_only_field_count"], 1)
        self.assertEqual(summary["loss_missing_field_count"], 4)
        self.assertEqual(summary["cases_with_loss"], 3)
        self.assertEqual(summary["surface_presence"]["state"], 12)
        self.assertEqual(summary["surface_presence"]["intent"], 12)
        self.assertEqual(summary["surface_presence"]["evidence"], 12)
        self.assertFalse(payload["boundary"]["third_party_validation"])
        self.assertFalse(payload["boundary"]["benchmark_result"])

    def test_source_hash_only_fields_are_explicit(self) -> None:
        self._run_eval()
        payload = json.loads(REPORT.read_text(encoding="utf-8"))
        hash_only = [
            (result["case_id"], field["field"])
            for result in payload["results"]
            for field in result["fields"]
            if field["retention"] == "source_hash_only"
        ]
        self.assertEqual(hash_only, [("openai_unknown_fields", "vendor_extra")])

    def _run_eval(self) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "experiments/evaluate_mapping_coverage.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result


if __name__ == "__main__":
    unittest.main()
