# ECL: A Deterministic Cross-Runtime Execution IR with Replayable Semantics

Status: arXiv-ready system paper draft

Date: 2026-06-28

Author: Bin Zhang

Affiliation: independent researcher

## Abstract

Agent runtimes expose traces through framework-specific surfaces such as model inputs, tool calls, callbacks, spans, and event streams. These traces are useful locally but difficult to compare, replay, or cite across heterogeneous runtimes. This paper presents Execution Compact Layer (ECL), a deterministic execution intermediate representation for agent systems. ECL maps runtime traces into four replayable surfaces: `state`, `intent`, `action`, and `evidence`. The v0.1 artifact includes a frozen schema, deterministic validation and replay, OpenAI Agents SDK-style and LangChain-style trace adapters, an embeddable SDK, a dependency API, and a local MCP-style compatibility stub. ECL is not a framework or public standard; it is a reproducible execution representation layer for cross-runtime agent traces.

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
input -> validate -> replay -> trace -> evidence -> hash
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
| model input | `state` |
| reasoning or requested operation | `intent` |
| tool call or run step | `action` |
| events and result references | `evidence` |

Mapping is loss-aware. When source information is omitted, approximated, or structurally remapped, the adapter records a loss report instead of claiming full-fidelity preservation.

## 4. SDK and Dependency Layer

The SDK exposes a compact local API:

```python
from ecl import ECL

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

## 5. MCP Compatibility Stub

ECL v0.1 includes a local MCP-style compatibility surface:

```text
mcp/ecl_tool_spec.json
mcp/ecl_server_stub.py
```

The stub exposes:

- `ecl.wrap`
- `ecl.emit`
- `ecl.verify`

The stub is local only. It is not a published MCP server, registry plugin, or external adoption signal.

## 6. Replay Semantics

Let:

- `T_r` be a trace from runtime `r`
- `M_r` be a deterministic adapter for runtime `r`
- `E` be an ECL object
- `L` be a loss report
- `P` be the validator
- `R` be the replay function
- `H` be SHA-256 over canonical JSON

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
- MCP-style local stub safety
- cross-runtime fixture conversion
- replay artifact determinism

The local verification command is:

```text
python3 -m unittest discover -s tests
```

The current checked result is:

```text
Ran 65 tests
OK
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

