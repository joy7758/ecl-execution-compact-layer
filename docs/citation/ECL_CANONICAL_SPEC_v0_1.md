# ECL Canonical Citation Spec v0.1

## Definition

Execution Compact Layer (ECL) v0.1 is a deterministic execution representation stack that maps runtime traces into a replayable object with `state`, `intent`, `action`, and `evidence` surfaces.

## Scope

ECL v0.1 is intended to be cited as a local, reproducible execution representation surface. It is not a framework, not a public standard, not an ecosystem dependency signal, and not evidence of third-party use.

## Core Object

```json
{
  "state": {},
  "intent": {},
  "action": {},
  "evidence": {}
}
```

## Deterministic Contract

For identical input traces and frozen schema files, ECL v0.1 must produce identical sorted-key compact JSON hashes, replay artifacts, and validation results.

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

## Reference Surface

Agent-readable entrypoints:

- `schemas/ecl-execution-compact-layer.schema.json`
- `sdk/ecl.py`
- `sdk/ecl_dependency.py`
- `mcp/ecl_tool_spec.json`
- `mcp/ecl_server_stub.py` as an MCP-shaped local wrapper, not a conformant MCP server
- `examples/citation_repro_demo.py`

## Boundary Claims

This citation spec only supports the claim that ECL v0.1 is locally reproducible and internally verified. It does not claim public release, formal standard status, third-party validation, production deployment, or ecosystem adoption.
