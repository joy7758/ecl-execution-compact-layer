# ECL Definition Note v0.1

## Abstract

ECL v0.1 defines a deterministic execution representation stack for agent runtime traces. It compresses runtime-specific execution records into an ECL object whose replay and evidence surfaces are hash-stable under local deterministic execution.

## Definition

An ECL record is a deterministic representation of an execution event chain. The record preserves four surfaces:

- `state`: runtime and actor context required to interpret the execution.
- `intent`: normalized purpose, constraints, and expected result.
- `action`: normalized execution step, tool reference, and side-effect class.
- `evidence`: validation, event-chain, hash, and replay references.

## Invariants

- Determinism: identical input produces identical ECL and replay hashes.
- Replayability: each valid ECL record can produce execution trace, replay result, and evidence bundle artifacts.
- Loss awareness: adapter-level mapping may report semantic, structural, or temporal loss.
- Boundary preservation: ECL references source runtime traces without redefining the host runtime.

## Local Verification Surface

The local verification surface is:

```text
python3 -m unittest discover -s tests
python3 examples/citation_repro_demo.py
python3 mcp/ecl_server_stub.py
```

## Non-claims

This note is not a standard proposal, not a registry entry, not proof of external adoption, not a benchmark result, and not a production assurance claim.
