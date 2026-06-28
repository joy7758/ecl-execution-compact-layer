#!/usr/bin/env python3
"""OpenAI trace to ECL one-line SDK demo."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdk.ecl import ECL


def main() -> int:
    trace = json.loads((ROOT / "tests" / "fixtures" / "openai_agents_trace.json").read_text(encoding="utf-8"))
    ecl_object = ECL.from_trace({"runtime": "openai", "trace": trace, "source_ref": "sdk/demo_openai.py"})
    validation = ECL.validate(ecl_object)
    replay = ECL.replay(ecl_object)
    payload = {
        "runtime": "openai",
        "valid": validation["valid"],
        "ecl_object": ecl_object,
        "replay_result": replay,
        "evidence_bundle": replay["artifact_hashes"]["evidence_bundle"],
    }
    out = ROOT / "sdk" / "out" / "demo_openai.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"runtime": "openai", "valid": payload["valid"], "verification_hash": replay["verification_hash"]}, sort_keys=True))
    return 0 if payload["valid"] and replay["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

