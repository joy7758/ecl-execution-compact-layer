from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_MD = ROOT / "paper" / "joss" / "JOSS_PREFLIGHT_AUDIT_v0_1.md"
PREFLIGHT_JSON = ROOT / "paper" / "joss" / "JOSS_PREFLIGHT_AUDIT_v0_1.json"
AUTHOR_TEMPLATE = ROOT / "paper" / "joss" / "AUTHOR_METADATA_TEMPLATE_v0_1.json"
HOSTILE_DECISION_JSON = ROOT / "paper" / "joss" / "JOSS_HOSTILE_READINESS_DECISION_v0_1.json"


class JOSSPreflightTests(unittest.TestCase):
    def test_preflight_artifacts_exist(self) -> None:
        self.assertTrue(PREFLIGHT_MD.exists())
        self.assertTrue(PREFLIGHT_JSON.exists())
        self.assertTrue(AUTHOR_TEMPLATE.exists())
        self.assertTrue(HOSTILE_DECISION_JSON.exists())

    def test_preflight_marks_submission_not_ready(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "public_release_ready_joss_submission_preflight_not_passed")
        self.assertTrue(audit["summary"]["paper_content_ready"])
        self.assertFalse(audit["summary"]["submission_preflight_passed"])
        for key in (
            "public-history",
            "external-impact",
            "final_joss_submission_approval",
        ):
            self.assertIn(key, audit["summary"]["blocking_items"])

    def test_boundary_does_not_claim_submission_or_release(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        self.assertFalse(audit["boundary"]["formal_submission"])
        self.assertFalse(audit["boundary"]["joss_submission_performed"])
        self.assertFalse(audit["boundary"]["paid_journal_selected"])
        self.assertFalse(audit["boundary"]["acceptance_claim"])
        self.assertTrue(audit["boundary"]["public_release"])
        self.assertTrue(audit["boundary"]["github_release_created"])
        self.assertTrue(audit["boundary"]["license_selected"])
        text = PREFLIGHT_MD.read_text(encoding="utf-8")
        self.assertIn("joss_submission_performed=false", text)
        self.assertIn("paid_journal_selected=false", text)
        self.assertIn("license_selected=true", text)
        self.assertIn("github_release_created=true", text)
        self.assertIn("external user, citation, dependency, or third-party research-impact signal", text)

    def test_author_metadata_template_requires_human_completion(self) -> None:
        template = json.loads(AUTHOR_TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(template["status"], "human_metadata_applied")
        self.assertTrue(template["boundary"]["human_verified"])
        self.assertFalse(template["boundary"]["submission_ready"])
        self.assertEqual(template["authors"][0]["name"], "Bin Zhang")
        self.assertEqual(template["affiliations"][0]["name"], "independent researcher")
        self.assertEqual(template["repository"]["license"], "MIT")

    def test_preflight_cites_official_joss_sources(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        sources = set(audit["sources"])
        self.assertIn("https://joss.readthedocs.io/en/latest/submitting.html", sources)
        self.assertIn("https://joss.readthedocs.io/en/latest/review_criteria.html", sources)
        self.assertIn("https://joss.readthedocs.io/en/latest/paper.html", sources)

    def test_open_source_metadata_surface_exists(self) -> None:
        for relative_path in (
            "CITATION.cff",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SUPPORT.md",
            ".github/workflows/tests.yml",
            ".github/workflows/joss-paper.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/research_use_report.yml",
            ".github/ISSUE_TEMPLATE/trace_mapping_case.yml",
            "docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md",
        ):
            self.assertTrue((ROOT / relative_path).exists(), relative_path)
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        ids = {check["id"]: check for check in audit["checks"]}
        self.assertEqual(ids["open-source-metadata"]["status"], "pass")
        self.assertEqual(ids["external-impact"]["status"], "unverified")

    def test_hostile_readiness_decision_keeps_submission_blocked(self) -> None:
        decision = json.loads(HOSTILE_DECISION_JSON.read_text(encoding="utf-8"))
        self.assertEqual(decision["status"], "not_ready_for_immediate_joss_submission")
        self.assertFalse(decision["decision"]["immediate_joss_submission_recommended"])
        self.assertTrue(decision["decision"]["synthetic_experiment_evidence_ready"])
        self.assertTrue(decision["decision"]["standard_joss_paper_path_ready"])
        self.assertTrue(decision["decision"]["public_collaboration_surface_ready"])
        self.assertFalse(decision["decision"]["public_development_history_ready"])
        self.assertFalse(decision["decision"]["external_impact_signal_ready"])
        blocker_ids = {blocker["id"] for blocker in decision["remaining_blockers"]}
        self.assertIn("public-development-history", blocker_ids)
        self.assertIn("external-impact", blocker_ids)
        self.assertFalse(decision["boundary"]["joss_submission_performed"])


if __name__ == "__main__":
    unittest.main()
