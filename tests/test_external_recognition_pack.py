from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExternalRecognitionPackTests(unittest.TestCase):
    def test_one_page_spec_has_only_required_sections(self) -> None:
        text = (ROOT / "ECL_EXTERNAL_RECOGNITION_v0_1.md").read_text(encoding="utf-8")
        sections = [line.strip() for line in text.splitlines() if line.startswith("## ")]
        self.assertEqual(
            sections,
            [
                "## 1. Definition",
                "## 2. Non-goals",
                "## 3. Core Object",
                "## 4. Why It Exists",
                "## 5. Minimal Adoption Flow",
            ],
        )
        non_goal_lines = [
            line for line in text.splitlines()
            if line.startswith("- ECL is not") or line.startswith("- ECL is not")
        ]
        self.assertLessEqual(len(non_goal_lines), 5)

    def test_external_recognition_demo_is_deterministic(self) -> None:
        first = subprocess.run(
            [sys.executable, "examples/external_recognition_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        first_summary = (ROOT / "examples" / "out" / "external_recognition" / "recognition_demo_result.json").read_text(encoding="utf-8")
        second = subprocess.run(
            [sys.executable, "examples/external_recognition_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        second_summary = (ROOT / "examples" / "out" / "external_recognition" / "recognition_demo_result.json").read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_summary, second_summary)
        summary = json.loads(second_summary)
        self.assertTrue(summary["all_valid"])
        self.assertTrue(summary["all_deterministic"])
        for runtime in ("openai", "langchain"):
            runtime_dir = ROOT / "examples" / "out" / "external_recognition" / runtime
            for artifact in ("ecl_object.json", "replay_result.json", "evidence_bundle.json"):
                self.assertTrue((runtime_dir / artifact).exists(), f"{runtime}/{artifact}")


if __name__ == "__main__":
    unittest.main()

