# ECL: A Deterministic Cross-Runtime Execution IR with Replayable Semantics

Status: arXiv-ready system paper draft

Date: 2026-06-28

Author: Bin Zhang

Affiliation: independent researcher

## Abstract

Agent runtimes expose traces through framework-specific surfaces such as model inputs, tool calls, callbacks, spans, and event streams. These traces are useful locally but difficult to compare, replay, or cite across heterogeneous runtimes. This paper presents Execution Compact Layer (ECL), a deterministic execution intermediate representation for agent systems. ECL maps runtime traces into four replayable surfaces: `state`, `intent`, `action`, and `evidence`. The v0.1 artifact includes a frozen schema, deterministic validation and replay, OpenAI Agents SDK-style and LangChain-style trace adapters, an embeddable SDK, a dependency API, and an MCP-shaped local wrapper. ECL is not a framework or public standard; it is a reproducible execution representation layer for cross-runtime agent traces.

## 1. Execution IR Definition

An ECL record is an execution object:

```text
E = (state, intent, action, evidence)
```

where:

- `state` records execution lifecycle, runtime identity, actor, and correlation references.
- `intent` records requested operation, constraints, expected result, and evidence requirements.
- `action` records tool or operation step, execution mode, side-effect class, and parameter hash.
- `evidence` records result status, trace references, event chain, policy decisions, and artifact hashes.

The machine-readable schema is:

```text
schemas/ecl-execution-compact-layer.schema.json
```

The IR is minimal by design. It captures execution semantics needed for validation and replay, not full runtime state preservation.

## 2. Deterministic Execution Model

ECL execution is defined as a deterministic local transformation:

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

For unchanged input, schema, adapter, validator, checkpoint reference, and generation parameters, ECL preserves:

- ECL object hash
- validation result
- execution trace hash
- evidence bundle hash
- replay result hash

The deterministic contract excludes hidden mutable state, stochastic behavior, network calls, and external runtime execution.

## 3. Cross-Runtime Abstraction

ECL maps heterogeneous runtime traces into a common execution representation.

The v0.1 mapping covers:

- OpenAI Agents SDK-style traces
- LangChain-style traces

The adapter rule is:

| Runtime source | ECL surface |
| --- | --- |
| runtime metadata, actor, correlation | `state` |
| model input, reasoning, requested operation | `intent` |
| tool call or run step | `action` |
| events, outputs, result references | `evidence` |

Mapping is loss-aware. When source information is omitted, approximated, or structurally remapped, the adapter records a loss report instead of claiming full-fidelity preservation.

## 4. SDK and Dependency Layer

The SDK exposes a compact local API:

```python
from sdk import ECL

record = ECL.create(state, intent, action)
ECL.validate(record)
ECL.replay(record)
```

The dependency layer exposes a non-invasive interface:

```python
import ecl_dependency as ecl

ecl_object = ecl.wrap(trace)
payload = ecl.emit(ecl_object)
result = ecl.verify(ecl_object)
```

This layer allows an external system to produce or verify ECL objects without modifying the host runtime.

## 5. MCP-Shaped Local Wrapper

ECL v0.1 includes an MCP-shaped local tool surface:

```text
mcp/ecl_tool_spec.json
mcp/ecl_server_stub.py
```

The stub exposes:

- `ecl.wrap`
- `ecl.emit`
- `ecl.verify`

The wrapper is local only. It is not a conformant MCP implementation, JSON-RPC transport, host-client-server session model, registry plugin, or external adoption signal.

## 6. Replay Semantics

Let:

- `T_r` be a trace from runtime `r`
- `M_r` be a deterministic adapter for runtime `r`
- `E` be an ECL object
- `L` be a loss report
- `P` be the validator
- `R` be the replay function
- `H` be SHA-256 over deterministic sorted-key compact JSON

The adapter contract is:

```text
M_r(T_r) -> (E, L)
```

The validation contract is:

```text
P(E, schema) -> valid | invalid
```

The replay contract is:

```text
R(E) -> (execution_trace.json, evidence_bundle.json, replay_result.json)
```

The replay invariant is:

```text
If E, schema, validator, replay function, and generation parameters are unchanged,
then H(R(E)) is unchanged.
```

ECL replay verifies representational stability. It does not prove that an external side effect occurred.

## 7. Evaluation Surface

The v0.1 repository verifies:

- schema validation
- adapter determinism
- SDK stability
- dependency API stability
- MCP-shaped local wrapper safety
- cross-runtime fixture conversion
- replay artifact determinism
- synthetic trace-corpus conversion, loss reporting, and replay stability

The local verification command is:

```text
python3 -m unittest discover -s tests
```

The current checked result is:

```text
Ran 77 tests
OK
```

The synthetic trace-corpus evaluation is:

```text
python3 experiments/evaluate_trace_corpus.py
case_count=12
by_runtime={"langchain": 6, "openai": 6}
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
loss_type_counts={"semantic": 9, "structural": 3}
evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974
```

The corpus is local and synthetic. It is not production trace evidence, third-party validation, or a benchmark result.

The negative validation-matrix evaluation is:

```text
python3 experiments/evaluate_validation_matrix.py
baseline_valid=true
case_count=8
expected_invalid_count=8
invalid_detected_count=8
expectation_met_count=8
evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0
```

The field-level mapping coverage evaluation is:

```text
python3 experiments/evaluate_mapping_coverage.py
case_count=12
total_source_fields=81
direct_mapped_field_count=80
source_hash_only_field_count=1
loss_missing_field_count=4
evaluation_hash=sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a
```

## 8. Boundary

ECL does not compete with agent frameworks. It normalizes execution semantics into a replayable local representation.

ECL v0.1 does not claim:

- external adoption
- formal standard status
- production audit control
- benchmark leadership
- full-fidelity runtime preservation

## References

References are maintained in:

```text
paper/joss/paper.bib
```
