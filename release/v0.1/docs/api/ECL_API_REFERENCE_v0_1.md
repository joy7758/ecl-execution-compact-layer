# ECL API Reference v0.1

Status: joss_api_reference

Scope: This document is the public, agent-readable API reference for the ECL v0.1 software artifact. It documents existing import surfaces only. It does not define new schema fields, runtime hooks, or external service behavior.

## Install

```bash
python3 -m pip install -e .
```

## Python SDK: `sdk.ecl.ECL`

| Method | Input | Output | Deterministic behavior |
| --- | --- | --- | --- |
| `ECL.create(state, intent, action)` | Three dictionaries describing the four ECL surfaces. | ECL execution record. | Uses fixed `generated_at`, checkpoint reference, sorted JSON hashing, and frozen schema conventions. |
| `ECL.validate(ecl_object)` | ECL execution record. | Validation report with `valid`, `errors`, and recomputed hash fields. | Reads `schemas/ecl-execution-compact-layer.schema.json` and recomputes deterministic hashes. |
| `ECL.replay(ecl_object)` | ECL execution record. | Replay verification plus `execution_trace`, `evidence_bundle`, and `replay_result` artifact hashes. | Writes local artifacts under `sdk/out/replay` with deterministic hash outputs. |
| `ECL.to_trace(runtime_output)` | Runtime output or `{"runtime": ..., "trace": ...}` envelope. | Normalized trace envelope. | Performs structural normalization only; no inference, no network calls. |
| `ECL.from_trace(trace)` | Normalized trace envelope or runtime output. | ECL execution record. | Uses deterministic OpenAI-style or LangChain-style mapping. |

Minimal usage:

```python
from sdk import ECL

trace = {"runtime": "openai", "trace": openai_trace}
ecl_object = ECL.from_trace(trace)
validation = ECL.validate(ecl_object)
replay = ECL.replay(ecl_object)

assert validation["valid"]
assert replay["deterministic"]
```

## Dependency API: `sdk.ecl_dependency`

| Function | Input | Output | Boundary |
| --- | --- | --- | --- |
| `wrap(trace)` | OpenAI-style trace, LangChain-style trace, or existing ECL record. | ECL execution record. | Does not mutate host runtime state. |
| `emit(ecl_object)` | ECL execution record. | Dependency payload containing canonical hash and emitted object. | Does not publish externally. |
| `verify(ecl_object)` | ECL execution record. | Validation and replay report with local artifact paths. | Writes local deterministic artifacts only. |

Minimal dependency mode:

```python
from sdk import ecl_dependency as ecl

ecl_object = ecl.wrap(trace)
payload = ecl.emit(ecl_object)
verification = ecl.verify(ecl_object)

assert verification["valid"]
assert verification["deterministic"]
```

## CLI Entrypoints

| Command | Purpose |
| --- | --- |
| `python3 -m unittest discover -s tests` | Run the full local test suite. |
| `python3 experiments/evaluate_trace_corpus.py` | Evaluate the 12-case synthetic trace corpus. |
| `python3 experiments/evaluate_validation_matrix.py` | Evaluate negative validation mutations. |
| `python3 experiments/evaluate_mapping_coverage.py` | Evaluate field-level mapping coverage. |
| `python3 examples/citation_repro_demo.py` | Run the citation reproducibility demo. |
| `python3 mcp/ecl_server_stub.py` | Run local MCP-shaped wrapper self-check. |
| `python3 scripts/joss_gate_verifier.py` | Generate machine-readable JOSS readiness gate output. |

## Output Artifacts

| Artifact | Producer |
| --- | --- |
| `execution_trace.json` | replay adapters and demos |
| `evidence_bundle.json` | replay adapters and demos |
| `replay_result.json` | replay adapters and demos |
| `experiments/out/trace_corpus_evaluation.json` | trace-corpus evaluation |
| `experiments/out/validation_matrix_evaluation.json` | validation-matrix evaluation |
| `experiments/out/mapping_coverage_evaluation.json` | mapping-coverage evaluation |
| `paper/joss/JOSS_GATE_VERIFICATION_v0_1.json` | JOSS gate verifier |

## Determinism Boundary

```text
no_external_api_calls=true
no_runtime_mutation=true
schema_modified=false
deterministic_sorted_json_hashing=true
local_artifacts_only=true
```

## Non-Goals

- This API does not execute external agents.
- This API does not publish MCP tools or register a server.
- This API does not certify OpenAI, LangChain, or MCP conformance.
- This API does not satisfy the JOSS public-history gate.
