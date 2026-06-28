from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments" / "trace_corpus" / "corpus_manifest.json"
REPORT = ROOT / "experiments" / "out" / "trace_corpus_evaluation.json"


class TraceCorpusEvaluationTests(unittest.TestCase):
    def test_corpus_manifest_has_required_coverage(self) -> None:
        manifest = json.loads(CORPUS.read_text(encoding="utf-8"))
        cases = manifest["cases"]
        self.assertGreaterEqual(len(cases), 12)
        runtimes = {case["runtime"] for case in cases}
        self.assertEqual(runtimes, {"openai", "langchain"})
        self.assertGreaterEqual(sum(1 for case in cases if case.get("expected_loss")), 3)
        tags = {tag for case in cases for tag in case.get("tags", [])}
        for tag in ("complete", "missing_field", "unknown_field", "failure_status", "timestamp"):
            self.assertIn(tag, tags)
        self.assertTrue(manifest["description"].startswith("Synthetic local trace corpus"))

    def test_evaluation_script_generates_deterministic_summary(self) -> None:
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
        self.assertEqual(summary["valid_count"], 12)
        self.assertEqual(summary["deterministic_count"], 12)
        self.assertEqual(summary["loss_expectation_met_count"], 12)
        self.assertEqual(summary["surface_coverage"], {"action": 12, "evidence": 12, "intent": 12, "state": 12})
        self.assertEqual(summary["surface_coverage_by_runtime"]["openai"], {"action": 6, "evidence": 6, "intent": 6, "state": 6})
        self.assertEqual(summary["surface_coverage_by_runtime"]["langchain"], {"action": 6, "evidence": 6, "intent": 6, "state": 6})
        self.assertFalse(payload["boundary"]["third_party_validation"])
        self.assertFalse(payload["boundary"]["benchmark_result"])

    def _run_eval(self) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, "experiments/evaluate_trace_corpus.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result


if __name__ == "__main__":
    unittest.main()
