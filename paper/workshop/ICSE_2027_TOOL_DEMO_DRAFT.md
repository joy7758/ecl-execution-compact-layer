# ECL: A Deterministic Execution IR for Replayable Agent Runtime Traces

Status: ICSE 2027 Tool Demonstration draft

Target track: ICSE 2027 Tool Demonstration and Data Showcase

Repository: https://github.com/joy7758/ecl-execution-compact-layer

Software archive: https://zenodo.org/records/21003766

Version DOI: 10.5281/zenodo.21003766

## 1. Problem and Motivation

Agent frameworks emit execution traces through runtime-specific structures such as model inputs, tool calls, callbacks, spans, run trees, and event lists. These traces help developers inspect a run inside the source framework, but they are hard to compare, replay, or cite across runtimes.

ECL addresses a narrow tool problem: normalize supported agent-runtime traces into a deterministic execution representation that can be validated, replayed, hashed, and archived.

## 2. Tool Overview

ECL v0.1 provides:

- a JSON schema for the four ECL surfaces: `state`, `intent`, `action`, and `evidence`;
- local validators and deterministic hash utilities;
- OpenAI-style and LangChain-style trace mapping;
- replay artifact generation;
- an embeddable SDK;
- a dependency API with `wrap`, `emit`, and `verify`;
- an MCP-shaped local wrapper for protocol-surface simulation.

ECL is not a tracing backend, agent framework, production audit system, public standard, or external adoption claim.

## 3. Usage Workflow

The reviewer-facing workflow is:

```bash
make demo
```

The command runs:

```bash
python3 -m unittest discover -s tests
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
```

The dependency-mode API is:

```python
import ecl_dependency as ecl

ecl_object = ecl.wrap(trace)
result = ecl.verify(ecl_object)
```

The expected outputs are:

- ECL objects for OpenAI-style and LangChain-style fixtures;
- replay result JSON;
- evidence bundle JSON;
- deterministic hash summaries.

## 4. Demonstration Scenario

The demo uses two included local fixtures:

- `tests/fixtures/openai_agents_trace.json`
- `tests/fixtures/langchain_trace.json`

For each fixture, ECL:

1. loads the trace;
2. maps it into an ECL object;
3. records loss information when preservation is incomplete;
4. validates the ECL object;
5. generates replay artifacts;
6. computes stable hashes.

The demonstration focuses on workflow clarity and reproducibility, not production telemetry scale.

## 5. Validation and Reproducibility

The repository verification surface includes:

- unit tests for schema, adapters, SDK, dependency API, and local MCP-shaped wrapper;
- deterministic replay checks;
- synthetic cross-runtime trace-corpus evaluation;
- negative validation-matrix evaluation;
- mapping coverage evaluation.

The current local reviewer gate records:

```text
test_suite=pass
dependency_mode_result_hash=sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3
external_recognition_result_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
```

This evidence is local and repository-contained. It does not claim independent third-party validation.

## 6. Intended Users

The intended users are:

- researchers studying agent execution reproducibility;
- software-engineering reviewers who need a runnable trace-normalization artifact;
- developers who need a small local dependency for replayable execution records.

## 7. Limitations

- v0.1 supports only included OpenAI-style and LangChain-style trace families.
- Evaluations use synthetic local fixtures.
- The MCP-shaped wrapper is not a published MCP server.
- No external adoption, production deployment, benchmark superiority, or standards-body endorsement is claimed.
- JSS rejected the journal manuscript at pre-screening; the tool demo route is for community feedback.

## 8. Track Fit

ICSE 2027 Tool Demonstration and Data Showcase asks for tool demonstrations with clear software-engineering relevance, easy distribution, and a 3-5 minute video. ECL fits this route as a runnable research tool for deterministic replay of normalized agent-runtime traces.
