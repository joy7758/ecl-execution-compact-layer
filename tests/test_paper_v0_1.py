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
    "sdk/ecl_dependency.py": "b578b3fd326e046b43c67ed47fe7e83e8fb11d451301cd384659253b003d1f09",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "mcp/ecl_tool_spec.json": "907a3ba39e1f64736c19c6a58a083e2361345c2a5ac80041e1044be546154688",
    "mcp/ecl_server_stub.py": "1123685e770982965a356966a9e02e17f5795387f486649e33b0e798d40cc5a4",
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
        self.assertIn("Ran 65 tests", text)
        self.assertIn("sha256:358a039db2c737b8905d91e37e1ed8fc5ea4081dab8d25a0523b4958f7061651", text)
        self.assertIn("not a published MCP server", text)
        self.assertIn("not an external adoption signal", text)
        self.assertIn("do not support claims of public release", lower_text)

    def test_evidence_manifest_boundaries(self) -> None:
        manifest = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual(manifest["paper"]["status"], "draft_not_submitted")
        self.assertEqual(manifest["local_evidence"]["test_result"]["tests"], 65)
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
