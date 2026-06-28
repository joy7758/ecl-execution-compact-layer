from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT_MD = ROOT / "paper" / "joss" / "JOSS_PREFLIGHT_AUDIT_v0_1.md"
PREFLIGHT_JSON = ROOT / "paper" / "joss" / "JOSS_PREFLIGHT_AUDIT_v0_1.json"
AUTHOR_TEMPLATE = ROOT / "paper" / "joss" / "AUTHOR_METADATA_TEMPLATE_v0_1.json"


class JOSSPreflightTests(unittest.TestCase):
    def test_preflight_artifacts_exist(self) -> None:
        self.assertTrue(PREFLIGHT_MD.exists())
        self.assertTrue(PREFLIGHT_JSON.exists())
        self.assertTrue(AUTHOR_TEMPLATE.exists())

    def test_preflight_marks_submission_not_ready(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "paper_content_ready_submission_preflight_not_passed")
        self.assertTrue(audit["summary"]["paper_content_ready"])
        self.assertFalse(audit["summary"]["submission_preflight_passed"])
        for key in (
            "license",
            "public-git-hosting",
            "public-url",
            "issue-tracker",
            "public-history",
            "author-metadata",
            "release-archive",
        ):
            self.assertIn(key, audit["summary"]["blocking_items"])

    def test_boundary_does_not_claim_submission_or_release(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        for value in audit["boundary"].values():
            self.assertFalse(value)
        text = PREFLIGHT_MD.read_text(encoding="utf-8")
        self.assertIn("joss_submission_performed=false", text)
        self.assertIn("paid_journal_selected=false", text)
        self.assertIn("license_selected=false", text)
        self.assertIn("github_release_created=false", text)

    def test_author_metadata_template_requires_human_completion(self) -> None:
        template = json.loads(AUTHOR_TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(template["status"], "requires_human_completion")
        self.assertFalse(template["boundary"]["human_verified"])
        self.assertFalse(template["boundary"]["submission_ready"])
        self.assertEqual(template["authors"][0]["name"], "<AUTHOR_NAME>")
        self.assertEqual(template["repository"]["license"], "<OSI_APPROVED_LICENSE>")

    def test_preflight_cites_official_joss_sources(self) -> None:
        audit = json.loads(PREFLIGHT_JSON.read_text(encoding="utf-8"))
        sources = set(audit["sources"])
        self.assertIn("https://joss.readthedocs.io/en/latest/submitting.html", sources)
        self.assertIn("https://joss.readthedocs.io/en/latest/review_criteria.html", sources)
        self.assertIn("https://joss.readthedocs.io/en/latest/paper.html", sources)


if __name__ == "__main__":
    unittest.main()
