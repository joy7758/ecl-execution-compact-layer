from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "sdk/ecl_dependency.py": "b578b3fd326e046b43c67ed47fe7e83e8fb11d451301cd384659253b003d1f09",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "mcp/ecl_tool_spec.json": "907a3ba39e1f64736c19c6a58a083e2361345c2a5ac80041e1044be546154688",
    "mcp/ecl_server_stub.py": "1123685e770982965a356966a9e02e17f5795387f486649e33b0e798d40cc5a4",
}

DOCS = [
    "docs/citation/ECL_CANONICAL_SPEC_v0_1.md",
    "docs/citation/ECL_DEFINITION_NOTE_v0_1.md",
    "docs/citation/ECL_REFERENCE_SNIPPETS_v0_1.md",
    "docs/citation/FIRST_EXTERNAL_MENTION_STRATEGY_v0_1.md",
]


class ExternalCitationSeedPackTests(unittest.TestCase):
    def test_required_citation_docs_exist(self) -> None:
        for relative_path in DOCS:
            self.assertTrue((ROOT / relative_path).exists(), relative_path)

    def test_canonical_spec_contains_required_surfaces(self) -> None:
        text = (ROOT / "docs/citation/ECL_CANONICAL_SPEC_v0_1.md").read_text(encoding="utf-8")
        for token in (
            "state",
            "intent",
            "action",
            "evidence",
            "runtime trace -> normalize/adapt -> ECL record -> validate -> replay",
        ):
            self.assertIn(token, text)
        self.assertIn("does not claim public release", text)
        self.assertIn("ecosystem adoption", text)

    def test_docs_do_not_claim_status_upgrade(self) -> None:
        combined = "\n".join((ROOT / path).read_text(encoding="utf-8").lower() for path in DOCS)
        strategy = (ROOT / "docs/citation/FIRST_EXTERNAL_MENTION_STRATEGY_v0_1.md").read_text(encoding="utf-8").lower()
        forbidden = [
            "is an adopted ecosystem standard",
            "is a published or conformant mcp server",
            "has third-party production validation",
            "benchmark leadership",
        ]
        for phrase in forbidden:
            self.assertIn(phrase, strategy)
        self.assertIn("pre-adoption", combined)
        self.assertIn("## forbidden claims", strategy)
        self.assertIn("without claiming external adoption", strategy)

    def test_citation_repro_demo_is_deterministic(self) -> None:
        first = subprocess.run(
            [sys.executable, "examples/citation_repro_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        first_summary = (ROOT / "examples" / "out" / "citation_seed" / "citation_seed_result.json").read_text(encoding="utf-8")

        second = subprocess.run(
            [sys.executable, "examples/citation_repro_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        second_summary = (ROOT / "examples" / "out" / "citation_seed" / "citation_seed_result.json").read_text(encoding="utf-8")

        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_summary, second_summary)
        summary = json.loads(second_summary)
        self.assertTrue(summary["all_valid"])
        self.assertTrue(summary["all_deterministic"])
        self.assertFalse(summary["boundary"]["public_release"])
        self.assertFalse(summary["boundary"]["third_party_validation"])
        self.assertFalse(summary["boundary"]["ecosystem_adoption"])

    def test_no_core_drift(self) -> None:
        for relative_path, expected_hash in LOCKED_HASHES.items():
            actual_hash = sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)


if __name__ == "__main__":
    unittest.main()
