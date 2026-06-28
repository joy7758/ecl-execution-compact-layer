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

The current ECL v0.1 artifact contains a frozen JSON schema, validator, deterministic hash utilities, OpenAI Agents SDK-style and LangChain-style adapters, replay scripts, an embeddable SDK, a dependency API, local fixtures, and a local MCP-style anchor stub. The implementation is intentionally conservative. It does not execute external agents, call network APIs, publish a protocol server, or claim ecosystem adoption. Its purpose is to make a runtime trace reproducible as a local execution representation that can be validated, replayed, hashed, and cited.

# Statement of need

Researchers and engineers who build agent systems often need to answer a practical question: what exactly happened during an agent run, and can that record be represented outside the runtime that produced it? Existing frameworks expose rich trace surfaces, including OpenAI Agents SDK tracing [@openai_agents_tracing], LangChain tracing [@langchain_tracing], and tool-oriented protocol surfaces such as MCP [@mcp_spec]. These systems solve important runtime and interoperability problems, but they do not by themselves define a minimal deterministic execution intermediate representation that is independent of any one host framework.

ECL is designed for work where execution records must be compared, archived, tested, or cited across framework boundaries. Typical users include researchers studying agent reliability, engineers building reproducibility pipelines, and developers who need a small dependency layer around runtime traces. ECL does not replace observability systems such as OpenTelemetry [@opentelemetry_trace]. Instead, it narrows the problem to a compact representation of agent execution semantics and a deterministic replay surface.

The artifact is useful when a team wants to preserve the shape of an agent execution without preserving every runtime-specific field. ECL's loss-aware adapters make this tradeoff explicit: some source information may be preserved only as raw trace references or recorded as mapping loss. This makes ECL closer to an execution representation layer than a tracing framework.

# State of the field

Several adjacent systems motivate ECL. OpenAI Agents SDK and LangChain provide runtime-specific tracing and callback mechanisms [@openai_agents_tracing; @langchain_tracing]. MCP defines a tool and context exchange protocol surface [@mcp_spec]. OpenTelemetry defines a broad observability model for distributed traces [@opentelemetry_trace]. Compiler and execution environments use intermediate representations, including LLVM IR and WebAssembly, to separate source systems from execution or portability targets [@llvm_langref; @wasm_core].

ECL borrows the separation principle from intermediate representations but applies it to agent execution records. It uses JSON schema, canonical JSON, and SHA-256 hashes to make local records reproducible [@rfc8785]. The contribution is not a new agent runtime. The contribution is a small software layer that converts heterogeneous runtime traces into a validated execution object with stable replay artifacts.

# Software design

The ECL object model has four main surfaces:

1. `state`: lifecycle, actor, runtime, and correlation references.
2. `intent`: operation, constraints, expected result, and evidence requirements.
3. `action`: tool or operation step, execution mode, side-effect class, and parameters hash.
4. `evidence`: result summary, trace references, event chain, policy decisions, and hashes.

The implementation is organized around agent-readable entrypoints. The schema lives in `schemas/ecl-execution-compact-layer.schema.json`. Validation is implemented in `ecl/validator.py`. Runtime-specific adapters live in `ecl/adapters/` and `external/adoption/`. Replay is implemented by `demo/replay_demo.py` and `external/adoption/replay_adapter.py`. The embeddable SDK is exposed through `sdk/ecl.py`, and the minimal dependency interface is exposed through `sdk/ecl_dependency.py` with `wrap`, `emit`, and `verify`. The local MCP-style anchor in `mcp/ecl_server_stub.py` delegates to the dependency interface without network calls or registry integration.

The deterministic replay contract is:

```text
trace -> ECL object -> validate -> replay -> evidence -> hash
```

For unchanged input traces, schema, adapters, checkpoint references, and generation timestamp, ECL is expected to preserve the ECL object hash, replay artifact hashes, and validation result. The current local test suite verifies schema validation, adapter conversion, replay determinism, SDK stability, dependency API stability, MCP-style anchor safety, citation-demo reproducibility, no paid-journal screening, and paper-package boundaries.

# Research impact statement

ECL supports research on agent reproducibility and execution semantics by providing a small, testable representation layer that can be inspected independently of any one runtime. Its current scope is intentionally limited to local verification over included fixtures. This makes it appropriate as a research-software artifact and as a foundation for later empirical studies, but it is not yet evidence of external adoption, production deployment, or benchmark superiority.

The artifact can help future work define execution equivalence classes for agent runs, compare trace-normalization strategies, and evaluate replay stability across larger trace corpora. It also provides a practical baseline for discussing how much information is lost when runtime-specific traces are mapped into a compact execution IR.

# Validation

The local verification command is:

```text
python3 -m unittest discover -s tests
```

The current checked result is:

```text
Ran 65 tests
OK
```

The citation reproducibility demo is:

```text
python3 examples/citation_repro_demo.py
result_hash=sha256:358a039db2c737b8905d91e37e1ed8fc5ea4081dab8d25a0523b4958f7061651
```

The MCP-style local anchor self-check is:

```text
python3 mcp/ecl_server_stub.py
verification_hash=sha256:3770d486d473720ae7d84546906e24214ee156ad458bee8fec3c59873ea153b8
```

# AI usage disclosure

This draft and the surrounding submission-candidate artifacts were prepared with assistance from OpenAI Codex for repository inspection, deterministic test execution, artifact generation, and prose drafting. Human authors are responsible for verifying the final manuscript, authorship metadata, licensing, repository release state, and submission decision before any submission.

# Acknowledgements

Author acknowledgements are intentionally left blank until the human author confirms funding, institutional support, and contributor attribution.

# References
