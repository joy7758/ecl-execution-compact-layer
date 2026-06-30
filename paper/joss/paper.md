---
title: 'ECL: A deterministic execution representation layer for agent runtime traces'
tags:
  - Python
  - agent systems
  - software engineering
  - reproducibility
  - trace analysis
authors:
  - name: Bin Zhang
    affiliation: 1
affiliations:
  - name: independent researcher
    index: 1
date: 28 June 2026
bibliography: paper.bib
---

# Summary

Execution Compact Layer (ECL) is a Python-based software artifact for representing agent runtime execution as deterministic, replayable records. Agent systems increasingly emit traces through runtime-specific objects such as model inputs, tool calls, callbacks, spans, run trees, and evidence logs. These records are useful inside their host frameworks, but they are difficult to compare or replay across runtimes without adopting the host runtime's full trace model. ECL addresses this problem by mapping runtime traces into four execution surfaces: `state`, `intent`, `action`, and `evidence`.

The current ECL v0.1 artifact contains a frozen JSON schema, validator, deterministic hash utilities, OpenAI Agents SDK-style and LangChain-style adapters, replay scripts, an embeddable SDK, a dependency API, local fixtures, and an MCP-shaped local wrapper. The implementation is intentionally conservative. It does not execute external agents, call network APIs, publish a protocol server, or claim ecosystem adoption. Its purpose is to make a runtime trace reproducible as a local execution representation that can be validated, replayed, hashed, and cited.

# Statement of need

Researchers and engineers who build agent systems often need to answer a practical question: what exactly happened during an agent run, and can that record be represented outside the runtime that produced it? Existing frameworks expose rich trace surfaces, including OpenAI Agents SDK tracing [@openai_agents_tracing], LangChain tracing [@langchain_tracing], and tool-oriented protocol surfaces such as MCP [@mcp_spec]. These systems solve important runtime and interoperability problems, but they do not by themselves define a minimal deterministic execution intermediate representation that is independent of any one host framework.

ECL is designed for work where execution records must be compared, archived, tested, or cited across framework boundaries. Typical users include researchers studying agent reliability, engineers building reproducibility pipelines, and developers who need a small dependency layer around runtime traces. ECL does not replace observability systems such as OpenTelemetry [@opentelemetry_trace]. Instead, it narrows the problem to a compact representation of agent execution semantics and a deterministic replay surface.

The artifact is useful when a team wants to preserve the shape of an agent execution without preserving every runtime-specific field. ECL's loss-aware adapters make this tradeoff explicit: some source information may be preserved only as raw trace references or recorded as mapping loss. This makes ECL closer to an execution representation layer than a tracing framework.

The ECL v0.1 software archive is available on Zenodo with version DOI `10.5281/zenodo.21003766` and concept DOI `10.5281/zenodo.21003765`. The DOI records the software artifact and does not imply journal acceptance, production deployment, external adoption, or standards-body endorsement.

# State of the field

Several adjacent systems motivate ECL. OpenAI Agents SDK and LangChain provide runtime-specific tracing and callback mechanisms [@openai_agents_tracing; @langchain_tracing]. MCP defines a tool and context exchange protocol surface [@mcp_spec]. OpenTelemetry defines a broad observability model for distributed traces [@opentelemetry_trace]. Compiler and execution environments use intermediate representations, including LLVM IR and WebAssembly, to separate source systems from execution or portability targets [@llvm_langref; @wasm_core].

ECL is narrower than these systems. It is not an OpenTelemetry semantic convention, a LangSmith replacement, a provenance exchange standard, or a lineage system. The build-versus-contribute decision is based on scope: ECL tests a small local representation for agent execution semantics, replay artifacts, and hash stability rather than extending a broader telemetry or provenance platform.

| System surface | Primary target | ECL distinction |
| --- | --- | --- |
| OpenAI Agents / LangChain tracing | Runtime-local execution traces | ECL maps selected trace fields into a shared local IR. |
| LangSmith-style observability | Hosted tracing, debugging, and evaluation workflows | ECL is a local representation layer and does not require hosted observability infrastructure. |
| OpenTelemetry | Distributed observability traces | ECL focuses on compact agent execution representation and replay artifacts. |
| MCP | Tool/context protocol surface | ECL only provides an MCP-shaped local wrapper, not protocol conformance. |
| PROV / OpenLineage | Provenance or data lineage interchange | ECL records deterministic execution evidence for agent traces rather than general provenance or dataset lineage. |

ECL borrows the separation principle from intermediate representations but applies it to agent execution records. It uses JSON schema, deterministic sorted-key compact JSON serialization, and SHA-256 hashes to make local records reproducible. This local serialization is not claimed to be a full RFC 8785/JCS implementation [@rfc8785]. The contribution is not a new agent runtime. The contribution is a small software layer that converts heterogeneous runtime traces into a validated execution object with stable replay artifacts.

# Software design

The ECL object model has four main surfaces:

1. `state`: lifecycle, actor, runtime, and correlation references.
2. `intent`: operation, constraints, expected result, and evidence requirements.
3. `action`: tool or operation step, execution mode, side-effect class, and parameters hash.
4. `evidence`: result summary, trace references, event chain, policy decisions, and hashes.

The implementation is organized around agent-readable entrypoints. The schema lives in `schemas/ecl-execution-compact-layer.schema.json`. Validation is implemented in `ecl/validator.py` and uses the declared `jsonschema` dependency. Runtime-specific adapters live in `ecl/adapters/` and `external/adoption/`. Replay is implemented by `demo/replay_demo.py` and `external/adoption/replay_adapter.py`. The embeddable SDK is exposed through `sdk/ecl.py`, and the minimal dependency interface is exposed through `sdk/ecl_dependency.py` with `wrap`, `emit`, and `verify`. The MCP-shaped local wrapper in `mcp/ecl_server_stub.py` delegates to the dependency interface without network calls or registry integration.

The deterministic replay contract is:

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

For unchanged input traces, schema, adapters, checkpoint references, and generation timestamp, ECL is expected to preserve the ECL object hash, replay artifact hashes, and validation result. The current local test suite verifies schema validation, adapter conversion, replay determinism, SDK stability, dependency API stability, MCP-shaped wrapper safety, citation-demo reproducibility, no paid-journal screening, paper-package boundaries, and deterministic evaluation over a synthetic cross-runtime trace corpus.

# Research impact statement

ECL supports research on agent reproducibility and execution semantics by providing a small, testable representation layer that can be inspected independently of any one runtime. Its current scope is intentionally limited to local verification over included fixtures. This makes it appropriate as a research-software artifact and as a foundation for later empirical studies, but it is not yet evidence of external adoption, production deployment, or benchmark superiority.

The artifact can help future work define execution equivalence classes for agent runs, compare trace-normalization strategies, and evaluate replay stability across larger trace corpora. It also provides a practical baseline for discussing how much information is lost when runtime-specific traces are mapped into a compact execution IR.

The current developer research workflow is documented in `docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md`. It uses a synthetic OpenAI-style and LangChain-style trace corpus to evaluate whether ECL preserves validation, replay determinism, four-surface mapping coverage, and explicit loss reporting. This is developer research use, not independent external use.

# Validation

The local verification command is:

```text
python3 -m unittest discover -s tests
```

The current checked result is:

```text
Ran 78 tests
OK
```

The trace-corpus evaluation command is:

```text
python3 experiments/evaluate_trace_corpus.py
```

The current synthetic-corpus result is:

```text
case_count=12
by_runtime={"langchain": 6, "openai": 6}
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
loss_type_counts={"semantic": 9, "structural": 3}
evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974
```

This corpus contains local synthetic traces only. It is included to stress adapter mapping, loss reporting, and replay determinism across OpenAI-style and LangChain-style trace shapes. It is not production trace evidence, third-party validation, or a benchmark result.

The validation-matrix evaluation is:

```text
python3 experiments/evaluate_validation_matrix.py
baseline_valid=true
case_count=8
expected_invalid_count=8
invalid_detected_count=8
expectation_met_count=8
evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0
```

This negative evaluation mutates a valid ECL record to check missing surfaces, schema-version drift, hash tampering, source-hash mismatch, empty event chains, additional root properties, invalid action modes, and missing evidence hashes.

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

This evaluation records whether each top-level source trace field is projected into an ECL surface or retained only through the source trace hash. It is included to make the loss-aware mapping claim auditable over the synthetic corpus.

The citation reproducibility demo is:

```text
python3 examples/citation_repro_demo.py
result_hash=sha256:8684fa8963ff9ad55c36eed6b89eb15992d1b05566aa1c79ced754fac67e1cdd
```

The MCP-shaped local wrapper self-check is:

```text
python3 mcp/ecl_server_stub.py
verification_hash=sha256:bdcf2ddb30a0e5975782f77fa86415226c46652bbd5490a667a2f2106dd65a5f
```

# AI usage disclosure

This draft and the surrounding submission-candidate artifacts were prepared with assistance from OpenAI Codex for repository inspection, deterministic test execution, artifact generation, and prose drafting. Human authors are responsible for verifying the final manuscript, authorship metadata, licensing, repository release state, and submission decision before any submission.

# Acknowledgements

No external funding was received for this work. Contributor acknowledgements remain empty unless additional human contributors are confirmed before submission.

# References
