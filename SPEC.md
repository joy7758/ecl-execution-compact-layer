# ECL v0.1 Local Semantic Freeze Specification

Status: local semantic freeze candidate

Scope: Execution Compact Layer (ECL) v0.1 defines a minimal deterministic execution intermediate representation for agent execution records. This specification is the single semantic source for the v0.1 freeze. It does not define adapter behavior, benchmark scoring, production governance, public release status, or external standard status.

## 1. Purpose

ECL v0.1 exists to lock the first executable semantics of an agent execution record.

An ECL record captures four execution surfaces:

- state: the execution lifecycle and identity references
- intent: the requested operation and constraints
- action: the executed or proposed operation step
- evidence: trace, result, hash, and audit references

ECL is an execution representation layer. It references source protocols and runtime traces, but it does not replace source protocols, runtime systems, audit systems, or evidence stores.

## 2. Normative Object Model

An ECL v0.1 record MUST be a JSON object with:

- `schema_version`
- `object_type`
- `ecl_id`
- `lineage`
- `state`
- `intent`
- `action`
- `evidence`
- `determinism`
- `audit`

The normative machine-readable binding for this object model is:

`schemas/ecl-execution-compact-layer.schema.json`

The schema is part of the local semantic freeze. A record that fails this schema is not an ECL v0.1 conforming record.

## 3. State Semantics

The `state` object describes the current execution lifecycle position and identity references.

Required semantics:

- `execution_status` MUST describe the execution outcome or current terminal state.
- `lifecycle_phase` MUST describe where the record sits in the lifecycle.
- `actor_ref` MUST identify the acting agent or agent-like entity by reference.
- `persona_ref` MUST identify the persona or identity-facing object by reference.
- `runtime_ref` MUST identify the runtime surface by reference.
- `correlation_id` MUST provide a stable join key across intent, action, result, trace, or receipt surfaces.

`state` is not an authority model. It records references and lifecycle state. It does not grant permissions.

## 4. Intent Semantics

The `intent` object describes the requested operation as a bounded execution input.

Required semantics:

- `summary` MUST be a human-readable compact statement of the requested execution.
- `operation` MUST be a stable operation label.
- `constraints` MUST preserve execution constraints as structured data.
- `evidence_requirements` MUST preserve requested evidence obligations as structured data.

Intent data MAY reference an external intent object. Such references do not import or redefine the external protocol.

## 5. Action Semantics

The `action` object describes the operation step selected or performed by the runtime.

Required semantics:

- `name` MUST identify the action.
- `execution_mode` MUST describe how execution was authorized or staged.
- `side_effect_class` MUST classify the expected side effect boundary.
- `parameters_hash`, when present, MUST be computed over canonical JSON for the parameters object.

Action semantics describe execution shape. They do not prove that a side effect occurred.

## 6. Evidence Semantics

The `evidence` object describes the reviewable execution record and integrity references.

Required semantics:

- `result_status` MUST describe the result state.
- `result_summary` MUST provide a compact result description.
- `trace_refs` MUST include at least one source trace reference.
- `event_chain` MUST include at least one hash-linked event.
- `policy_decisions` MUST be structured as decision records when available.
- `hashes` MUST include `canonical_hash` and `source_trace_hash`.

Evidence references MAY point to receipt, audit, trace, or result artifacts. ECL does not make those external artifacts authoritative by itself.

## 7. Determinism Rules

ECL v0.1 deterministic execution MUST use:

- canonicalization: `json-sort-keys-no-whitespace`
- hash algorithm: `sha256`
- timestamp policy: frozen snapshots SHOULD use a fixed generation timestamp
- record generation: repeated generation from the same source trace and same generation timestamp MUST produce the same ECL record hash

Canonical JSON means:

- object keys sorted lexicographically
- no insignificant whitespace
- ASCII-safe JSON serialization

## 8. Hash Model

ECL v0.1 uses hash references to make execution records reproducible and reviewable.

### 8.1 Source Trace Hash

`lineage.source_trace_hash` and `evidence.hashes.source_trace_hash` MUST match.

The source trace hash MUST be computed as:

`sha256(canonical_json(source_trace))`

### 8.2 Event Hash

Each event in `evidence.event_chain` MUST include:

- `event_hash`
- `chain_hash`

`event_hash` is the hash of the canonical event payload plus its deterministic index.

`chain_hash` is the hash of:

- previous chain hash
- current event hash

The first previous chain hash is `sha256:` followed by sixty-four `0` characters.

### 8.3 Canonical ECL Hash

`evidence.hashes.canonical_hash` MUST be computed over the full ECL record with `canonical_hash` temporarily set to:

`sha256:0000000000000000000000000000000000000000000000000000000000000000`

This avoids self-referential hash ambiguity.

### 8.4 State Hash

Checkpoint state files MUST include a `state_hash` computed over the checkpoint object with `state_hash` removed.

The state hash proves checkpoint integrity. It does not prove external runtime correctness.

## 9. Checkpoint Semantics

An ECL checkpoint is a deterministic state marker for local execution replay.

A checkpoint MUST include:

- goal or execution name
- current step
- status
- generation timestamp
- artifact references
- `state_hash`

A resume operation MUST verify `state_hash` before deterministic replay when `verify-state` behavior is requested.

Checkpoint replay is local reproducibility infrastructure. It is not a public release, external attestation, or production recovery guarantee.

## 10. Replay Invariants

For the same source inputs, same generation timestamp, same schema, same crosswalk, and same adapter implementation, replay MUST preserve:

- ECL object shape
- source trace hash
- event chain hash
- canonical ECL hash
- validator pass or fail result
- artifact manifest hash

Replay MAY rewrite output files. Rewriting output files is conforming when hashes remain stable under the same replay inputs.

## 11. Boundary Rules

ECL v0.1 MUST preserve these boundaries:

- local freeze is not public release
- schema validity is not external standard acceptance
- evidence bundle generation is not external validation
- runtime trace conversion is not ecosystem adoption
- protocol reference is not protocol replacement
- local replay is not production recovery

## 12. v0.1 Freeze Invariants

The v0.1 local semantic freeze locks:

- object model
- deterministic canonicalization rule
- hash model
- checkpoint state hash rule
- event chain rule
- replay invariants
- source protocol boundary rule

Changes to these invariants are breaking changes under `CHANGE_POLICY.md`.

