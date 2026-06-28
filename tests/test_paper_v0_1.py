from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "ECL_PAPER_v0_1.md"
EVIDENCE = ROOT / "paper" / "ECL_PAPER_EVIDENCE_v0_1.json"

LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "sdk/ecl_dependency.py": "6e596c3f05208a0d1cd45b8da773a5a18abd52c347402be1ecfef41be250d343",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "mcp/ecl_tool_spec.json": "907a3ba39e1f64736c19c6a58a083e2361345c2a5ac80041e1044be546154688",
    "mcp/ecl_server_stub.py": "7d73e5159b78881bdd63fe0360251f07c1014477302e11f1d4bb77a88ad33d57",
}


class PaperV01Tests(unittest.TestCase):
    def test_paper_required_sections_exist(self) -> None:
        text = PAPER.read_text(encoding="utf-8")
        required_sections = [
            "## Abstract",
            "## 1. Introduction",
            "## 2. Problem Statement",
            "## 3. Related Work",
            "## 4. ECL Model",
            "## 5. Formal Execution Contract",
            "## 6. System Design",
            "## 7. Architecture",
            "## 8. Evaluation",
            "## 9. Discussion",
            "## 10. Limitations",
            "## 11. Conclusion",
            "## References",
        ]
        for section in required_sections:
            self.assertIn(section, text)

    def test_paper_contains_local_evidence_only(self) -> None:
        text = PAPER.read_text(encoding="utf-8")
        lower_text = text.lower()
        self.assertIn("Ran 77 tests", text)
        self.assertIn("case_count=12", text)
        self.assertIn('surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}', text)
        self.assertIn("total_source_fields=81", text)
        self.assertIn("direct_mapped_field_count=80", text)
        self.assertIn("sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a", text)
        self.assertIn("sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974", text)
        self.assertIn("sha256:8684fa8963ff9ad55c36eed6b89eb15992d1b05566aa1c79ced754fac67e1cdd", text)
        self.assertIn("not a published MCP server", text)
        self.assertIn("not an external adoption signal", text)
        self.assertIn("do not support claims of ecosystem adoption", lower_text)
        self.assertIn("third-party validation", lower_text)

    def test_evidence_manifest_boundaries(self) -> None:
        manifest = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(manifest["paper"]["status"], "draft_not_submitted")
        self.assertEqual(manifest["local_evidence"]["test_result"]["tests"], 77)
        self.assertEqual(manifest["local_evidence"]["trace_corpus_result"]["case_count"], 12)
        self.assertEqual(manifest["local_evidence"]["trace_corpus_result"]["loss_expectation_met_count"], 12)
        self.assertEqual(manifest["local_evidence"]["validation_matrix_result"]["case_count"], 8)
        self.assertEqual(manifest["local_evidence"]["validation_matrix_result"]["expectation_met_count"], 8)
        self.assertEqual(manifest["local_evidence"]["mapping_coverage_result"]["total_source_fields"], 81)
        self.assertEqual(manifest["local_evidence"]["mapping_coverage_result"]["direct_mapped_field_count"], 80)
        self.assertEqual(manifest["local_evidence"]["mapping_coverage_result"]["source_hash_only_field_count"], 1)
        self.assertTrue(manifest["boundary"]["public_release"])
        self.assertFalse(manifest["boundary"]["formal_submission"])
        self.assertFalse(manifest["boundary"]["third_party_validation"])
        self.assertFalse(manifest["boundary"]["benchmark_result"])
        self.assertFalse(manifest["boundary"]["schema_modified"])
        self.assertGreaterEqual(len(manifest["related_work_sources"]), 5)

    def test_no_core_drift(self) -> None:
        for relative_path, expected_hash in LOCKED_HASHES.items():
            actual_hash = sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)


if __name__ == "__main__":
    unittest.main()
