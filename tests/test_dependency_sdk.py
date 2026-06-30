from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SDK_DIR = ROOT / "sdk"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

import ecl_dependency as ecl


LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "ecl/adapters/openai_agents.py": "6dd653924c97e4b746de72e35cf57a2d07f08898d0f65b9fb930cadac8ebdfc6",
    "ecl/adapters/langchain.py": "0dba4e6d7a8ed0ea63a466fec3e5bae7a7de0f6d39c57efd18f90b69d494eee5",
    "demo/replay_demo.py": "72f4da7d636ff8ad495cede4cf1e6f85b62f3da22568f5025c9f69282c1ea66d",
}


class DependencySDKTests(unittest.TestCase):
    def _trace(self, runtime: str) -> dict:
        fixture = ROOT / "tests" / "fixtures" / ("openai_agents_trace.json" if runtime == "openai" else "langchain_trace.json")
        return {
            "runtime": runtime,
            "trace": json.loads(fixture.read_text(encoding="utf-8")),
            "source_ref": f"tests/test_dependency_sdk.py:{runtime}",
        }

    def test_import_entry_and_public_contract(self) -> None:
        self.assertEqual(sorted(ecl.__all__), ["emit", "verify", "wrap"])

    def test_wrap_consistency(self) -> None:
        first = ecl.wrap(self._trace("openai"))
        second = ecl.wrap(self._trace("openai"))
        self.assertEqual(first, second)

    def test_emit_verify_stability(self) -> None:
        ecl_object = ecl.wrap(self._trace("openai"))
        first_emit = ecl.emit(ecl_object)
        second_emit = ecl.emit(ecl_object)
        with self._dependency_output_dir():
            first_verify = ecl.verify(ecl_object)
            second_verify = ecl.verify(ecl_object)
        self.assertEqual(first_emit, second_emit)
        self.assertTrue(first_verify["valid"])
        self.assertEqual(first_verify["replay"]["artifact_hashes"], second_verify["replay"]["artifact_hashes"])
        self.assertEqual(first_verify["replay"]["verification_hash"], second_verify["replay"]["verification_hash"])

    def test_cross_runtime_equivalence(self) -> None:
        records = {runtime: ecl.wrap(self._trace(runtime)) for runtime in ("openai", "langchain")}
        checks = {}
        with self._dependency_output_dir():
            for runtime, record in records.items():
                checks[runtime] = {
                    "surfaces": all(key in record for key in ("state", "intent", "action", "evidence")),
                    "valid": ecl.verify(record)["valid"],
                    "deterministic": ecl.verify(record)["deterministic"],
                }
        self.assertTrue(all(item["surfaces"] and item["valid"] and item["deterministic"] for item in checks.values()))

    def test_dependency_mode_demo(self) -> None:
        first = subprocess.run(
            [sys.executable, "sdk/demo_dependency_mode.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        first_payload = (ROOT / "sdk" / "out" / "dependency_mode" / "dependency_mode_result.json").read_text(encoding="utf-8")
        second = subprocess.run(
            [sys.executable, "sdk/demo_dependency_mode.py"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        second_payload = (ROOT / "sdk" / "out" / "dependency_mode" / "dependency_mode_result.json").read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_payload, second_payload)
        summary = json.loads(second_payload)
        self.assertTrue(summary["all_valid"])
        self.assertTrue(summary["all_deterministic"])

    def test_no_schema_drift(self) -> None:
        for relative_path, expected_hash in LOCKED_HASHES.items():
            actual_hash = sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)

    def _dependency_output_dir(self):
        class TemporaryDependencyOutput:
            def __enter__(self_nonlocal):
                self_nonlocal.tmp = tempfile.TemporaryDirectory()
                self_nonlocal.previous = os.environ.get("ECL_DEPENDENCY_OUTPUT_DIR")
                os.environ["ECL_DEPENDENCY_OUTPUT_DIR"] = self_nonlocal.tmp.name
                return Path(self_nonlocal.tmp.name)

            def __exit__(self_nonlocal, exc_type, exc, traceback):
                if self_nonlocal.previous is None:
                    os.environ.pop("ECL_DEPENDENCY_OUTPUT_DIR", None)
                else:
                    os.environ["ECL_DEPENDENCY_OUTPUT_DIR"] = self_nonlocal.previous
                self_nonlocal.tmp.cleanup()

        return TemporaryDependencyOutput()


if __name__ == "__main__":
    unittest.main()
