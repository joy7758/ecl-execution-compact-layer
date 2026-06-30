from __future__ import annotations

from pathlib import Path
from hashlib import sha256
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdk.ecl import ECL


LOCKED_HASHES = {
    "schemas/ecl-execution-compact-layer.schema.json": "15d089eaee07ec27d1fc69b5418e5dc5f1b1fa55f2c9395c03cde0ad6773cf89",
    "ecl/adapters/openai_agents.py": "6dd653924c97e4b746de72e35cf57a2d07f08898d0f65b9fb930cadac8ebdfc6",
    "ecl/adapters/langchain.py": "0dba4e6d7a8ed0ea63a466fec3e5bae7a7de0f6d39c57efd18f90b69d494eee5",
    "demo/replay_demo.py": "72f4da7d636ff8ad495cede4cf1e6f85b62f3da22568f5025c9f69282c1ea66d",
}


class SDKTests(unittest.TestCase):
    def test_sdk_surface_has_only_required_methods(self) -> None:
        public = sorted(name for name in dir(ECL) if not name.startswith("_") and callable(getattr(ECL, name)))
        self.assertEqual(public, ["create", "from_trace", "replay", "to_trace", "validate"])

    def test_create_validate_replay(self) -> None:
        ecl_object = ECL.create(
            {"actor_ref": "agent:sdk-test", "persona_ref": "persona:sdk-test", "runtime_ref": "sdk", "correlation_id": "sdk-test-001"},
            {"summary": "Validate SDK create path", "operation": "sdk_create"},
            {"name": "sdk_action", "execution_mode": "direct", "side_effect_class": "read_only", "tool_ref": "tool:sdk"},
        )
        validation = ECL.validate(ecl_object)
        self.assertTrue(validation["valid"], validation)
        replay = ECL.replay(ecl_object)
        self.assertTrue(replay["valid"], replay)

    def test_openai_demo_is_deterministic(self) -> None:
        first = self._run_demo("sdk/demo_openai.py")
        first_payload = (ROOT / "sdk" / "out" / "demo_openai.json").read_text(encoding="utf-8")
        second = self._run_demo("sdk/demo_openai.py")
        second_payload = (ROOT / "sdk" / "out" / "demo_openai.json").read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_payload, second_payload)
        self.assertTrue(json.loads(second_payload)["valid"])

    def test_langchain_demo_is_deterministic(self) -> None:
        first = self._run_demo("sdk/demo_langchain.py")
        first_payload = (ROOT / "sdk" / "out" / "demo_langchain.json").read_text(encoding="utf-8")
        second = self._run_demo("sdk/demo_langchain.py")
        second_payload = (ROOT / "sdk" / "out" / "demo_langchain.json").read_text(encoding="utf-8")
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first_payload, second_payload)
        self.assertTrue(json.loads(second_payload)["valid"])

    def test_no_core_hash_changes(self) -> None:
        for relative_path, expected_hash in LOCKED_HASHES.items():
            actual_hash = sha256((ROOT / relative_path).read_bytes()).hexdigest()
            self.assertEqual(actual_hash, expected_hash, relative_path)

    def _run_demo(self, path: str) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, path],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result


if __name__ == "__main__":
    unittest.main()
