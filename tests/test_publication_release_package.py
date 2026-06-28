from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "v0.1"
if not RELEASE.exists():
    RELEASE = ROOT


class PublicationReleasePackageTests(unittest.TestCase):
    def test_required_release_structure_exists(self) -> None:
        for relative_path in (
            "paper",
            "sdk",
            "mcp",
            "examples",
            "docs",
            "README.md",
            "LICENSE",
            "zenodo.json",
            "INTEGRITY_REPORT_v0_1.json",
        ):
            self.assertTrue((RELEASE / relative_path).exists(), relative_path)

    def test_public_readme_has_required_content_only(self) -> None:
        text = (RELEASE / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "ECL is a deterministic execution IR for cross-runtime agent systems with replayable semantics and loss-aware mapping.",
            text,
        )
        self.assertIn("import ecl_dependency as ecl", text)
        for item in ("not a framework", "not a runtime", "not a product"):
            self.assertIn(item, text)
        self.assertNotIn("benchmark", text.lower())
        self.assertNotIn("standard", text.lower())

    def test_zenodo_metadata_is_present_with_author_metadata(self) -> None:
        metadata = json.loads((RELEASE / "zenodo.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["title"], "ECL v0.1")
        self.assertEqual(metadata["description"], "deterministic execution IR layer")
        self.assertEqual(metadata["version"], "0.1")
        for keyword in ("execution IR", "agent systems", "determinism", "replay"):
            self.assertIn(keyword, metadata["keywords"])
        self.assertEqual(metadata["creators"][0]["name"], "Bin Zhang")
        self.assertEqual(metadata["creators"][0]["affiliation"], "independent researcher")
        self.assertEqual(metadata["license"], "MIT")

    def test_release_license_is_mit(self) -> None:
        text = (RELEASE / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", text)
        self.assertIn("Copyright (c) 2026 Bin Zhang", text)

    def test_packaged_core_hashes_match_source(self) -> None:
        pairs = {
            "schemas/ecl-execution-compact-layer.schema.json": "schemas/ecl-execution-compact-layer.schema.json",
            "sdk/ecl_dependency.py": "sdk/ecl_dependency.py",
            "sdk/ecl.py": "sdk/ecl.py",
            "mcp/ecl_tool_spec.json": "mcp/ecl_tool_spec.json",
            "mcp/ecl_server_stub.py": "mcp/ecl_server_stub.py",
        }
        for source_rel, release_rel in pairs.items():
            source_hash = sha256((ROOT / source_rel).read_bytes()).hexdigest()
            release_hash = sha256((RELEASE / release_rel).read_bytes()).hexdigest()
            self.assertEqual(source_hash, release_hash, source_rel)

    def test_release_manifest_preserves_publication_boundary(self) -> None:
        manifest = json.loads((RELEASE / "RELEASE_MANIFEST_v0_1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "github_release_ready_zenodo_pending")
        self.assertFalse(manifest["boundary"]["schema_modified"])
        self.assertFalse(manifest["boundary"]["feature_change"])
        self.assertFalse(manifest["boundary"]["doi_minted"])
        self.assertTrue(manifest["boundary"]["github_release_created"])
        self.assertTrue(manifest["boundary"]["public_release"])
        self.assertTrue(manifest["boundary"]["license_selected"])

    def test_integrity_report_records_required_validation(self) -> None:
        report = json.loads((RELEASE / "INTEGRITY_REPORT_v0_1.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "passed_local_release_package_validation_github_release_ready")
        commands = {item["command"]: item for item in report["commands"]}
        self.assertIn("python3 -m unittest discover -s tests", commands)
        self.assertIn("python3 sdk/demo_dependency_mode.py", commands)
        self.assertIn("python3 examples/external_recognition_demo.py", commands)
        self.assertTrue(report["boundary"]["deterministic"])
        self.assertTrue(report["boundary"]["schema_unchanged"])
        self.assertTrue(report["boundary"]["replay_stable"])
        self.assertTrue(report["boundary"]["cross_runtime_consistency_stable"])
        self.assertFalse(report["boundary"]["doi_minted"])
        self.assertTrue(report["boundary"]["github_release_created"])
        self.assertTrue(report["boundary"]["public_release"])
        self.assertTrue(report["boundary"]["license_selected"])

    def test_release_includes_reviewer_documentation(self) -> None:
        quickstart = RELEASE / "docs" / "joss" / "REVIEWER_QUICKSTART_v0_1.md"
        api_reference = RELEASE / "docs" / "api" / "ECL_API_REFERENCE_v0_1.md"
        self.assertTrue(quickstart.exists())
        self.assertTrue(api_reference.exists())
        self.assertIn("python3 -m unittest discover -s tests", quickstart.read_text(encoding="utf-8"))
        self.assertIn("ECL.validate(ecl_object)", api_reference.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
