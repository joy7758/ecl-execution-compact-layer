# ECL State of the Field Final Matrix v0.1

Status: state_of_field_matrix_finalized

Date: 2026-06-28

Scope: This matrix compares ECL v0.1 against adjacent observability, tracing, provenance, and lineage systems. It does not claim ECL is a superset or replacement for any listed system.

## Comparison Matrix

| System | Execution representation | Replay invariance | IR abstraction level | Cross-runtime support | Loss-aware mapping |
| --- | --- | --- | --- | --- | --- |
| OpenTelemetry | Distributed telemetry traces and spans | Not a core requirement of the trace model | Telemetry data model, not an agent execution IR | Broad distributed systems instrumentation, not ECL-style agent semantic unification | Not the primary abstraction |
| LangSmith / LangChain tracing | Runtime-specific chains, runs, tools, callbacks, and trace views | Not a runtime-neutral replay artifact contract | Framework observability surface, not a compact IR | Strong inside LangChain/LangSmith ecosystem; not a neutral ECL object | Not mandatory as an IR-level preservation report |
| W3C PROV | General provenance entities, activities, and agents | Not defined as ECL-style replay artifact invariance | Provenance interchange model | Broad provenance interoperability, not agent-runtime execution normalization | Not focused on adapter-level trace loss |
| OpenLineage | Dataset/job lineage metadata and facets | Not an ECL-style replay contract | Lineage metadata model, not execution IR | Cross-system lineage exchange, not agent trace normalization | Not focused on runtime trace preservation loss |
| OpenAI Agents tracing | OpenAI Agents SDK workflow tracing | Not a cross-runtime replay artifact invariant | Runtime tracing surface | Strong for OpenAI-style traces; not a neutral IR across frameworks | Not a required cross-runtime adapter report |
| ECL v0.1 | Four execution surfaces: state, intent, action, evidence | Required for local replay artifacts and hashes | Minimal deterministic execution IR | Implemented for OpenAI-style and LangChain-style traces in v0.1 | Required in adapter layer when preservation is incomplete |

## Build-versus-Contribute Boundary

ECL is not a superset or wrapper of any listed system. Extending one adjacent system would not satisfy the v0.1 research goal because each adjacent system optimizes for a different primary abstraction:

- OpenTelemetry optimizes for telemetry spans and distributed tracing.
- LangSmith and LangChain tracing optimize for framework observability and debugging.
- W3C PROV optimizes for general provenance interchange.
- OpenLineage optimizes for dataset and job lineage.
- OpenAI Agents tracing optimizes for OpenAI Agents SDK workflow traces.

ECL instead optimizes for a small execution IR that can be validated, replayed, hashed, and compared locally across supported heterogeneous trace families.

## Non-Superset Rule

ECL does not claim to include all information from the listed systems. It deliberately keeps less information and records loss when source information is not preserved. This is a design constraint, not a missing feature.

```text
not_superset=true
not_wrapper=true
not_replacement=true
minimal_execution_ir=true
```

## Reviewer-Facing Summary

Adjacent systems can produce, observe, or exchange execution-related data. ECL defines a smaller target representation for deterministic local replay and loss-aware cross-runtime normalization. That is the abstraction boundary.

