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
            "final_joss_submission_approval",
        ):
            self.assertIn(key, audit["summary"]["blocking_items"])
        self.assertNotIn("external-impact", audit["summary"]["blocking_items"])
        self.assertIn("external-impact", audit["summary"]["advisory_items"])

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
            "docs/joss/REVIEWER_QUICKSTART_v0_1.md",
            "docs/api/ECL_API_REFERENCE_v0_1.md",
            "docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md",
            "paper/joss/ECL_DEVELOPMENT_EVIDENCE_LAYER_v0_1.md",
            "paper/joss/JOSS_PUBLIC_HISTORY_MATURATION_PLAN_v0_1.md",
            "paper/joss/JOSS_PUBLIC_HISTORY_MATURATION_PLAN_v0_1.json",
        ):
            self.assertTrue((ROOT / relative_path).exists(), relative_path)
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        ids = {check["id"]: check for check in audit["checks"]}
        self.assertEqual(ids["open-source-metadata"]["status"], "pass")
        self.assertEqual(ids["reviewer-documentation"]["status"], "pass")
        self.assertEqual(ids["development-evidence"]["status"], "pass")
        self.assertEqual(ids["public-history-maturation-plan"]["status"], "pass")
        self.assertFalse(ids["public-history-maturation-plan"]["blocking"])
        self.assertEqual(ids["external-impact"]["status"], "advisory_unverified")
        self.assertFalse(ids["external-impact"]["blocking"])

    def test_hostile_readiness_decision_keeps_submission_blocked(self) -> None:
        decision = json.loads(HOSTILE_DECISION_JSON.read_text(encoding="utf-8"))
        self.assertEqual(decision["status"], "not_ready_for_immediate_joss_submission")
        self.assertFalse(decision["decision"]["immediate_joss_submission_recommended"])
        self.assertTrue(decision["decision"]["synthetic_experiment_evidence_ready"])
        self.assertTrue(decision["decision"]["standard_joss_paper_path_ready"])
        self.assertTrue(decision["decision"]["public_collaboration_surface_ready"])
        self.assertTrue(decision["decision"]["development_evidence_ready"])
        self.assertTrue(decision["decision"]["public_history_maturation_plan_ready"])
        self.assertFalse(decision["decision"]["public_development_history_ready"])
        self.assertFalse(decision["decision"]["external_impact_signal_ready"])
        self.assertFalse(decision["evidence"]["development_evidence"]["satisfies_public_history_gate"])
        self.assertFalse(decision["evidence"]["public_history_maturation_plan"]["satisfies_public_history_gate"])
        self.assertEqual(
            decision["evidence"]["public_history_maturation_plan"]["earliest_safe_review_date_utc"],
            "2026-12-29",
        )
        blocker_ids = {blocker["id"] for blocker in decision["remaining_blockers"]}
        self.assertIn("public-development-history", blocker_ids)
        self.assertNotIn("external-impact", blocker_ids)
        advisory_ids = {signal["id"] for signal in decision["advisory_signals"]}
        self.assertIn("external-impact-signal", advisory_ids)
        self.assertFalse(decision["boundary"]["joss_submission_performed"])

    def test_reviewer_documentation_is_agent_readable(self) -> None:
        quickstart = (ROOT / "docs" / "joss" / "REVIEWER_QUICKSTART_v0_1.md").read_text(encoding="utf-8")
        api_reference = (ROOT / "docs" / "api" / "ECL_API_REFERENCE_v0_1.md").read_text(encoding="utf-8")
        for token in (
            "python3 -m pip install -e .",
            "python3 -m unittest discover -s tests",
            "trace_corpus_evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974",
            "blocking_gates=[\"public_history\"]",
        ):
            self.assertIn(token, quickstart)
        for token in (
            "ECL.create(state, intent, action)",
            "ECL.validate(ecl_object)",
            "ECL.replay(ecl_object)",
            "sdk.ecl_dependency",
            "no_external_api_calls=true",
        ):
            self.assertIn(token, api_reference)


if __name__ == "__main__":
    unittest.main()
