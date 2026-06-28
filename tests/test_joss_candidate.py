from __future__ import annotations

from hashlib import sha256
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
JOSS_DIR = ROOT / "paper" / "joss"
PAPER = JOSS_DIR / "paper.md"
BIB = JOSS_DIR / "paper.bib"
STANDARD_PAPER = ROOT / "paper" / "paper.md"
STANDARD_BIB = ROOT / "paper" / "paper.bib"
CHECKLIST = JOSS_DIR / "JOSS_SUBMISSION_CHECKLIST_v0_1.md"
MANIFEST = JOSS_DIR / "JOSS_SUBMISSION_MANIFEST_v0_1.json"
CITATION = ROOT / "CITATION.cff"
CHANGELOG = ROOT / "CHANGELOG.md"

LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "sdk/ecl_dependency.py": "6e596c3f05208a0d1cd45b8da773a5a18abd52c347402be1ecfef41be250d343",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "mcp/ecl_tool_spec.json": "907a3ba39e1f64736c19c6a58a083e2361345c2a5ac80041e1044be546154688",
    "mcp/ecl_server_stub.py": "bd834ad160a05d97fe7a83ff44a42536491a58329212e6f8649ff03a8e60e001",
}


class JOSSCandidateTests(unittest.TestCase):
    def test_candidate_files_exist(self) -> None:
        for path in (PAPER, BIB, STANDARD_PAPER, STANDARD_BIB, CHECKLIST, MANIFEST):
            self.assertTrue(path.exists(), str(path))
        self.assertEqual(STANDARD_PAPER.read_text(encoding="utf-8"), PAPER.read_text(encoding="utf-8"))
        self.assertEqual(STANDARD_BIB.read_text(encoding="utf-8"), BIB.read_text(encoding="utf-8"))

    def test_paper_has_required_joss_sections(self) -> None:
        text = PAPER.read_text(encoding="utf-8")
        for section in (
            "# Summary",
            "# Statement of need",
            "# State of the field",
            "# Software design",
            "# Research impact statement",
            "# AI usage disclosure",
            "# References",
        ):
            self.assertIn(section, text)
        self.assertIn("bibliography: paper.bib", text)

    def test_paper_word_count_is_joss_candidate_size(self) -> None:
        text = PAPER.read_text(encoding="utf-8")
        body = re.sub(r"(?s)^---.*?---", "", text).replace("# References", "")
        words = re.findall(r"[A-Za-z0-9_]+", body)
        self.assertGreaterEqual(len(words), 750)
        self.assertLessEqual(len(words), 1750)

    def test_manifest_keeps_no_fee_and_not_submitted_boundary(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["target"]["short_name"], "JOSS")
        self.assertEqual(manifest["target"]["classification"], "eligible_zero_fee")
        self.assertEqual(manifest["status"], "candidate_metadata_applied_public_release_ready_not_submitted")
        self.assertFalse(manifest["boundary"]["joss_submission_performed"])
        self.assertFalse(manifest["boundary"]["formal_submission"])
        self.assertFalse(manifest["boundary"]["paid_journal_selected"])
        self.assertTrue(manifest["boundary"]["public_release"])
        self.assertTrue(manifest["boundary"]["license_selected"])
        self.assertTrue(manifest["boundary"]["github_release_created"])
        self.assertIn("final_joss_submission_approval", manifest["human_required_fields"])
        self.assertEqual(manifest["local_evidence"]["trace_corpus_result"]["surface_coverage"], {"action": 12, "evidence": 12, "intent": 12, "state": 12})

    def test_checklist_identifies_human_only_gaps(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("joss_submission_performed=false", text)
        self.assertIn("paid_journal_selected=false", text)
        self.assertIn("Author: Bin Zhang", text)
        self.assertIn("License: MIT", text)
        self.assertIn("Citation metadata: `CITATION.cff`", text)
        self.assertIn("CI workflow file: `.github/workflows/tests.yml`", text)

    def test_citation_and_changelog_are_agent_readable(self) -> None:
        citation = CITATION.read_text(encoding="utf-8")
        changelog = CHANGELOG.read_text(encoding="utf-8")
        self.assertIn("cff-version: 1.2.0", citation)
        self.assertIn("family-names: Zhang", citation)
        self.assertIn("version: \"0.1.0\"", citation)
        self.assertIn("## v0.1.0 - 2026-06-28", changelog)
        self.assertIn("synthetic_corpus_only=true", changelog)

    def test_bibliography_has_required_keys(self) -> None:
        text = BIB.read_text(encoding="utf-8")
        for key in (
            "openai_agents_tracing",
            "langchain_tracing",
            "mcp_spec",
            "opentelemetry_trace",
            "rfc8785",
        ):
            self.assertIn(key, text)

    def test_no_core_drift(self) -> None:
        for relative_path, expected_hash in LOCKED_HASHES.items():
            actual_hash = sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)


if __name__ == "__main__":
    unittest.main()
