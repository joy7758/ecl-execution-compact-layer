# ECL Abstraction Boundary v0.1

Status: abstraction_boundary_defined

Date: 2026-06-28

Scope: This document defines the narrow abstraction boundary for ECL v0.1. It is a reviewer-facing argument and does not change the schema, implementation, SDK, adapters, tests, or submission status.

```text
schema_changes=false
core_modification=false
sdk_changes=false
adapter_changes=false
external_adoption_claim=false
joss_submission_performed=false
```

## Minimal Claim

ECL is the smallest deterministic execution IR in this repository that preserves replay semantics across heterogeneous agent-runtime traces through four execution surfaces:

```text
state / intent / action / evidence
```

The claim is intentionally narrow. ECL is not a framework, runtime, public standard, benchmark, audit authority, production deployment, or proof of external side effects.

## Not Reducible To OpenTelemetry

OpenTelemetry provides telemetry concepts for distributed tracing and observability. ECL is not a telemetry convention or span schema.

Reduction to OpenTelemetry fails because ECL requires:

- loss-aware adapter mapping from runtime trace structures into a compact execution object;
- replay invariance over local ECL artifacts;
- a cross-runtime semantic surface independent of any span model or telemetry backend.

OpenTelemetry can describe traces. ECL defines a compact execution representation that can be validated, replayed, and hashed locally.

## Not Reducible To LangSmith / LangChain Tracing

LangSmith and LangChain tracing expose runtime-specific observability for chains, tools, callbacks, and runs. ECL is not a hosted tracing workflow or a replacement for LangChain observability.

Reduction to LangSmith or LangChain tracing fails because ECL requires:

- a runtime-neutral representation rather than one framework's run tree;
- explicit loss reports when a source trace cannot be fully preserved;
- stable replay artifacts independent of the original runtime service.

LangChain-style traces can be input to ECL. They are not the ECL abstraction itself.

## Not Reducible To W3C PROV / OpenLineage

W3C PROV and OpenLineage define broader provenance and lineage exchange structures. ECL is not a general provenance model and not a dataset lineage standard.

Reduction to PROV or OpenLineage fails because ECL requires:

- agent-execution-specific surfaces for state, intent, action, and evidence;
- deterministic local replay artifacts as part of the representation contract;
- adapter-level loss reporting for runtime-specific trace preservation.

PROV and OpenLineage can represent provenance or lineage. ECL represents local execution semantics for agent traces.

## Not Reducible To JSON Schema + Hashes

ECL uses JSON schema and SHA-256 hashing, but those mechanisms are not the abstraction.

Reduction to "JSON schema plus hash" fails because ECL requires:

- a fixed execution-surface model;
- deterministic adapter contracts;
- replay artifact generation;
- loss-aware mapping semantics;
- explicit boundaries around side effects, external adoption, and host-runtime authority.

A schema can validate shape. A hash can verify bytes. ECL adds execution meaning, replay invariance, and loss-aware cross-runtime mapping.

## Irreducible Core

The irreducible ECL v0.1 core is:

```text
runtime trace
  -> deterministic adapter
  -> ECL object: state / intent / action / evidence
  -> validation
  -> replay artifacts
  -> stable hashes
  -> explicit loss report when preservation is incomplete
```

If any of these elements is removed, the artifact collapses into an adjacent but different system:

- without cross-runtime mapping, it is just a single-runtime trace representation;
- without loss reporting, it can silently overclaim preservation;
- without replay invariance, it is not a deterministic execution IR;
- without the four execution surfaces, it is only generic structured data;
- without local validation and hashes, it is not reproducible as an execution artifact.

## Reviewer-Safe Boundary Sentence

ECL v0.1 is best described as a minimal deterministic execution IR for agent-runtime traces: it does not replace tracing, provenance, lineage, or observability systems, but it defines a small replayable representation that those systems do not provide as a single combined abstraction.

