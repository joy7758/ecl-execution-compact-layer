from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ecl.adapters.langchain import adapt_trace as adapt_langchain_trace
from ecl.adapters.openai_agents import adapt_trace as adapt_openai_agents_trace
from ecl.adapters.openai_agents import adapt_trace_with_report as adapt_openai_trace_with_report
from ecl.validator import validate_record


FROZEN_SCHEMA_SHA256 = "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89"
EXTERNAL_INTERFACE_LOCK = {
    "README.md": "ee250ca25c2e2f5b9b10b06298c65bb25bed774deaeb17bd33ba081a38cc28df",
    "ecl/adapters/openai_agents.py": "6dd653924c97e4b746de72e35cf57a2d07f08898d0f65b9fb930cadac8ebdfc6",
    "demo/replay_demo.py": "14aba3613b6e2070c94191b73d686d94685fc314c34500bb03b185cb6399ebf1",
    "schemas/ecl-execution-compact-layer.schema.json": FROZEN_SCHEMA_SHA256,
}


class ECLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads((ROOT / "schemas" / "ecl-execution-compact-layer.schema.json").read_text())
        self.generated_at = "2026-06-28T00:00:00Z"

    def test_openai_agents_adapter_generates_valid_ecl(self) -> None:
        trace_path = ROOT / "tests" / "fixtures" / "openai_agents_trace.json"
        trace = json.loads(trace_path.read_text())
        payload = adapt_openai_trace_with_report(
            trace,
            source_trace_ref=str(trace_path),
            generated_at=self.generated_at,
            checkpoint_ref="state/ecl_goal_state.json",
        )
        record = payload["ecl"]
        report = validate_record(record, self.schema)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(record["lineage"]["source_adapter"], "openai_agents_trace")
        self.assertIn("loss_report", payload)
        loss_decisions = [
            item
            for item in record["evidence"]["policy_decisions"]
            if item["decision_ref"] == "adapter-loss-report"
        ]
        self.assertEqual(len(loss_decisions), 1)
        self.assertIn("loss_report", loss_decisions[0])

    def test_langchain_adapter_generates_valid_ecl(self) -> None:
        trace_path = ROOT / "tests" / "fixtures" / "langchain_trace.json"
        trace = json.loads(trace_path.read_text())
        record = adapt_langchain_trace(
            trace,
            source_trace_ref=str(trace_path),
            generated_at=self.generated_at,
            checkpoint_ref="state/ecl_goal_state.json",
        )
        report = validate_record(record, self.schema)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(record["lineage"]["source_adapter"], "langchain_trace")

    def test_build_artifacts_emits_required_outputs(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/build_artifacts.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        required = [
            "execution_trace.json",
            "decision_log.json",
            "schema_diff.json",
            "evidence_bundle.json",
            "validator_report.json",
            "ecl_from_openai_agents_trace.json",
            "ecl_from_langchain_trace.json",
        ]
        for name in required:
            self.assertTrue((ROOT / "out" / "ecl_artifacts" / name).exists(), name)
        report = json.loads((ROOT / "out" / "ecl_artifacts" / "validator_report.json").read_text())
        self.assertTrue(report["all_valid"], report)

        resume = subprocess.run(
            [
                sys.executable,
                "scripts/build_artifacts.py",
                "--resume-from",
                "latest",
                "--verify-state",
                "--continue-exact",
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(resume.returncode, 0, resume.stderr + resume.stdout)

    def test_freeze_snapshot_manifest(self) -> None:
        manifest_path = ROOT / "release" / "v0.1-local-freeze" / "hash_manifest.json"
        self.assertTrue(manifest_path.exists())
        manifest = json.loads(manifest_path.read_text())
        self.assertEqual(manifest["status"], "local_semantic_freeze")
        self.assertFalse(manifest["boundary"]["public_release"])
        self.assertFalse(manifest["boundary"]["external_validation"])
        freeze_paths = {entry["freeze_path"] for entry in manifest["entries"]}
        self.assertIn("release/v0.1-local-freeze/schema.json", freeze_paths)
        self.assertIn("release/v0.1-local-freeze/crosswalk.json", freeze_paths)
        self.assertIn("release/v0.1-local-freeze/validator.py", freeze_paths)
        self.assertIn("release/v0.1-local-freeze/evidence_bundle.json", freeze_paths)

    def test_replay_demo_is_deterministic(self) -> None:
        build = subprocess.run(
            [sys.executable, "scripts/build_artifacts.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(build.returncode, 0, build.stderr + build.stdout)
        first = subprocess.run(
            [sys.executable, "demo/replay_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        first_outputs = {
            path.name: path.read_text()
            for path in sorted((ROOT / "demo" / "out").glob("*.json"))
        }
        second = subprocess.run(
            [sys.executable, "demo/replay_demo.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        second_outputs = {
            path.name: path.read_text()
            for path in sorted((ROOT / "demo" / "out").glob("*.json"))
        }
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_outputs, second_outputs)
        self.assertEqual(
            sorted(first_outputs),
            ["evidence_bundle.json", "execution_trace.json", "replay_result.json"],
        )

    def test_schema_hash_is_unchanged(self) -> None:
        import hashlib

        schema_hash = hashlib.sha256((ROOT / "schemas" / "ecl-execution-compact-layer.schema.json").read_bytes()).hexdigest()
        self.assertEqual(schema_hash, FROZEN_SCHEMA_SHA256)

    def test_external_interface_files_are_locked(self) -> None:
        import hashlib

        for relative_path, expected_hash in EXTERNAL_INTERFACE_LOCK.items():
            actual_hash = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)


if __name__ == "__main__":
    unittest.main()
