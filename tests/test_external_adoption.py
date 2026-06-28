from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


trace_loader = load_module("trace_loader", ROOT / "external" / "adoption" / "trace_loader.py")
ecl_mapper = load_module("ecl_mapper", ROOT / "external" / "adoption" / "ecl_mapper.py")
replay_adapter = load_module("replay_adapter", ROOT / "external" / "adoption" / "replay_adapter.py")


class ExternalAdoptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.out_root = ROOT / "out" / "external_adoption"
        if cls.out_root.exists():
            shutil.rmtree(cls.out_root)

    def setUp(self) -> None:
        self.generated_at = "2026-06-28T00:00:00Z"

    def test_openai_trace_to_ecl_to_replay(self) -> None:
        self._assert_runtime_pipeline(
            runtime="openai",
            trace_path=ROOT / "tests" / "fixtures" / "openai_agents_trace.json",
        )

    def test_langchain_trace_to_ecl_to_replay(self) -> None:
        self._assert_runtime_pipeline(
            runtime="langchain",
            trace_path=ROOT / "tests" / "fixtures" / "langchain_trace.json",
        )

    def _assert_runtime_pipeline(self, *, runtime: str, trace_path: Path) -> None:
        envelope = trace_loader.load_trace(trace_path, runtime=runtime)
        self.assertEqual(envelope["runtime"], runtime)
        self.assertIn("raw_trace", envelope)
        self.assertIn("normalized_events", envelope)

        mapped = ecl_mapper.map_to_ecl(
            envelope,
            generated_at=self.generated_at,
            checkpoint_ref=f"out/external_adoption/{runtime}/checkpoint.json",
        )
        self.assertEqual(mapped["runtime"], runtime)
        self.assertTrue(mapped["deterministic"])
        self.assertIn("loss", mapped)
        self.assertIn("missing_fields", mapped["loss"])
        ecl_record = mapped["ecl"]
        for key in ("state", "intent", "action", "evidence"):
            self.assertIn(key, ecl_record)

        replay_dir = self.out_root / runtime
        first = replay_adapter.replay_ecl(ecl_record, out_dir=replay_dir)
        second = replay_adapter.replay_ecl(ecl_record, out_dir=replay_dir)
        self.assertTrue(first["valid"])
        self.assertTrue(first["deterministic"])
        self.assertEqual(first["artifact_hashes"], second["artifact_hashes"])
        self.assertEqual(first["verification_hash"], second["verification_hash"])
        for artifact in ("execution_trace.json", "evidence_bundle.json", "replay_result.json"):
            self.assertTrue((replay_dir / artifact).exists(), artifact)


if __name__ == "__main__":
    unittest.main()
