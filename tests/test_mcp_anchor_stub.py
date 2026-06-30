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
if str(ROOT) in sys.path:
    sys.path.remove(str(ROOT))
sys.path.insert(0, str(ROOT))

from mcp import ecl_server_stub as ecl_stub


LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "sdk/ecl_dependency.py": "6e596c3f05208a0d1cd45b8da773a5a18abd52c347402be1ecfef41be250d343",
    "sdk/ecl.py": "6862a865bd1057b0159c135a75ee8fa4492399794c063a21c02aa12e90f5ed04",
    "ecl/adapters/openai_agents.py": "6dd653924c97e4b746de72e35cf57a2d07f08898d0f65b9fb930cadac8ebdfc6",
    "ecl/adapters/langchain.py": "0dba4e6d7a8ed0ea63a466fec3e5bae7a7de0f6d39c57efd18f90b69d494eee5",
    "demo/replay_demo.py": "72f4da7d636ff8ad495cede4cf1e6f85b62f3da22568f5025c9f69282c1ea66d",
}


class MCPAnchorStubTests(unittest.TestCase):
    def _trace(self, runtime: str = "openai") -> dict:
        fixture_name = "openai_agents_trace.json" if runtime == "openai" else "langchain_trace.json"
        return {
            "runtime": runtime,
            "trace": json.loads((ROOT / "tests" / "fixtures" / fixture_name).read_text(encoding="utf-8")),
            "source_ref": f"tests/test_mcp_anchor_stub.py:{runtime}",
        }

    def test_tool_spec_is_local_safe_and_deterministic(self) -> None:
        spec_text = (ROOT / "mcp" / "ecl_tool_spec.json").read_text(encoding="utf-8")
        spec = json.loads(spec_text)
        tool_names = [tool["name"] for tool in spec["tools"]]
        self.assertEqual(tool_names, ["ecl.wrap", "ecl.emit", "ecl.verify"])
        self.assertTrue(all(tool["deterministic"] is True for tool in spec["tools"]))
        self.assertNotIn("registry", spec_text.lower())
        self.assertNotIn("external", spec_text.lower())
        self.assertFalse(spec["constraints"]["network"])
        self.assertFalse(spec["constraints"]["runtime_binding"])
        self.assertFalse(spec["constraints"]["schema_changes"])

    def test_public_surface_is_only_wrap_emit_verify(self) -> None:
        self.assertEqual(sorted(ecl_stub.__all__), ["emit", "verify", "wrap"])

    def test_wrap_emit_verify_are_stable(self) -> None:
        first_object = ecl_stub.wrap(self._trace("openai"))
        second_object = ecl_stub.wrap(self._trace("openai"))
        self.assertEqual(first_object, second_object)

        first_emit = ecl_stub.emit(first_object)
        second_emit = ecl_stub.emit(second_object)
        self.assertEqual(first_emit, second_emit)

        with self._dependency_output_dir():
            first_verify = ecl_stub.verify(first_object)
            second_verify = ecl_stub.verify(second_object)
        self.assertTrue(first_verify["valid"])
        self.assertTrue(first_verify["deterministic"])
        self.assertEqual(first_verify["replay"]["artifact_hashes"], second_verify["replay"]["artifact_hashes"])
        self.assertEqual(first_verify["replay"]["verification_hash"], second_verify["replay"]["verification_hash"])

    def test_cross_runtime_anchor_equivalence(self) -> None:
        records = [ecl_stub.wrap(self._trace(runtime)) for runtime in ("openai", "langchain")]
        with self._dependency_output_dir():
            for record in records:
                self.assertTrue(all(key in record for key in ("state", "intent", "action", "evidence")))
                result = ecl_stub.verify(record)
                self.assertTrue(result["valid"])
                self.assertTrue(result["deterministic"])

    def test_server_stub_script_is_deterministic(self) -> None:
        with self._dependency_output_dir() as output_dir:
            with tempfile.TemporaryDirectory() as mcp_output_dir:
                env = os.environ.copy()
                env["ECL_DEPENDENCY_OUTPUT_DIR"] = str(output_dir)
                env["ECL_MCP_STUB_OUTPUT_DIR"] = mcp_output_dir
                out_path = Path(mcp_output_dir) / "ecl_server_stub_result.json"
                first = subprocess.run(
                    [sys.executable, "mcp/ecl_server_stub.py"],
                    cwd=ROOT,
                    check=False,
                    text=True,
                    capture_output=True,
                    env=env,
                )
                self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
                first_file = out_path.read_text(encoding="utf-8")
                second = subprocess.run(
                    [sys.executable, "mcp/ecl_server_stub.py"],
                    cwd=ROOT,
                    check=False,
                    text=True,
                    capture_output=True,
                    env=env,
                )
                self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
                second_file = out_path.read_text(encoding="utf-8")

        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_file, second_file)
        result = json.loads(second_file)
        self.assertTrue(result["valid"])
        self.assertTrue(result["deterministic"])

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
