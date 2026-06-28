# ECL Narrative Unification v0.1

## Purpose

This file aligns the JOSS, arXiv, release, SDK, and reviewer surfaces around one execution narrative. It is documentation only and does not modify ECL behavior.

```text
single_authoritative_execution_flow=true
schema_changes=false
core_modification=false
public_history_gate_status=fail_current_state
joss_submission_performed=false
```

## Unified Definition

ECL is a deterministic execution representation layer for agent runtime traces. It maps framework-specific trace material into a minimal execution record with four surfaces: `state`, `intent`, `action`, and `evidence`.

## Unified Execution Flow

All publication surfaces should describe the same flow:

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

## Surface Alignment

Execution IR description:

- The core object remains `state`, `intent`, `action`, and `evidence`.
- No additional IR fields are introduced for JOSS, arXiv, SDK, or release packaging.

Replay semantics:

- Replay is deterministic and local.
- Replay produces stable artifacts that can be hashed and compared.
- Replay does not call external APIs.

Cross-runtime mapping:

- OpenAI-style traces and LangChain-style traces are mapped through deterministic adapters.
- Mapping loss is reported instead of inferred away.
- Cross-runtime support means semantic normalization, not complete preservation of every source-runtime field.

SDK description:

- `sdk/ecl.py` exposes the embeddable API.
- `sdk/ecl_dependency.py` exposes the non-intrusive dependency API.
- The MCP-style surface is a local stub, not a registry plugin or external adoption claim.

## Reviewer Boundary

The safe JOSS narrative and engineering process statement clarify why a short public Git history exists. They do not claim that public history has matured.

```text
public_history_reviewer_concern=mitigated_by_engineering_process_statement
public_history_gate_status=fail_current_state
no_fake_history_added=true
no_commit_manipulation=true
```

There is no conflicting pipeline: every surface should point back to the unified flow above.
