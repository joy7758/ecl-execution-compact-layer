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

Execution Compact Layer (ECL) is a Python software artifact for converting agent runtime traces into deterministic, replayable execution records. ECL represents execution through four surfaces: `state`, `intent`, `action`, and `evidence`. The artifact includes a JSON schema, validator, OpenAI Agents SDK-style and LangChain-style trace adapters, deterministic replay scripts, an embeddable SDK, examples, fixtures, and tests.

ECL does not execute agents, call external APIs, or replace agent frameworks. Its purpose is to make runtime traces reproducible as local execution records that can be validated, replayed, hashed, and cited.

# Statement of Need

Agent frameworks expose useful runtime traces, but those traces are usually tied to framework-specific structures such as model inputs, tool calls, callbacks, spans, run trees, or event logs. Researchers and engineers who compare agent behavior across frameworks need a small reproducible representation that can be inspected outside the host runtime.

ECL addresses this need by mapping heterogeneous runtime traces into a minimal execution IR. The mapping is intentionally loss-aware: source information that cannot be represented directly is recorded as mapping loss instead of being silently treated as preserved.

# Software Functionality

The ECL object model contains:

- `state`: execution lifecycle, actor, runtime, and correlation references.
- `intent`: requested operation, constraints, expected result, and evidence requirements.
- `action`: operation step, execution mode, side-effect class, tool reference, and parameter hash.
- `evidence`: result summary, trace references, event chain, policy decisions, and hashes.

The deterministic execution flow is:

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

The main software surfaces are:

- schema: `schemas/ecl-execution-compact-layer.schema.json`
- validator: `ecl/validator.py`
- adapters: `ecl/adapters/` and `external/adoption/`
- replay: `demo/replay_demo.py` and `external/adoption/replay_adapter.py`
- SDK: `sdk/ecl.py`
- dependency API: `sdk/ecl_dependency.py`
- examples: `examples/`
- tests: `tests/`

# Installation

ECL v0.1 uses Python and declares its schema-validation dependency in `pyproject.toml`.

Clone the repository:

```bash
git clone https://github.com/joy7758/ecl-execution-compact-layer.git
cd ecl-execution-compact-layer
python3 -m pip install -e .
```

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

# Minimal Example

```python
from sdk import ECL

trace = {
    "runtime": "openai",
    "trace": {
        "model_input": "Summarize a trace",
        "reasoning": "Need a deterministic record",
        "tool_call": {"name": "summarize", "arguments": {"format": "short"}},
        "events": [{"type": "tool_call"}],
    },
    "source_ref": "joss-ready-example",
}

ecl_object = ECL.from_trace(trace)
validation = ECL.validate(ecl_object)

assert validation["valid"]
```

# Reproducibility

The required verification command is:

```bash
python3 -m unittest discover -s tests
```

The current local result is:

```text
Ran 75 tests
OK
```

The synthetic trace-corpus evaluation is:

```bash
python3 experiments/evaluate_trace_corpus.py
```

Current local result:

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

The dependency-mode demo is:

```bash
python3 sdk/demo_dependency_mode.py
```

The external recognition demo is:

```bash
python3 examples/external_recognition_demo.py
```

The demos and trace corpus are deterministic and use local fixtures or synthetic traces only.

The negative validation-matrix evaluation is:

```bash
python3 experiments/evaluate_validation_matrix.py
```

Current local result:

```text
baseline_valid=true
case_count=8
expected_invalid_count=8
invalid_detected_count=8
expectation_met_count=8
evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0
```

The field-level mapping coverage evaluation is:

```bash
python3 experiments/evaluate_mapping_coverage.py
```

Current local result:

```text
case_count=12
total_source_fields=81
direct_mapped_field_count=80
source_hash_only_field_count=1
loss_missing_field_count=4
evaluation_hash=sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a
```

The developer research-use workflow is documented in:

```text
docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md
```

# Boundary

ECL v0.1 is a software artifact for deterministic local execution representation. It does not claim external runtime validation, production deployment, benchmark superiority, formal standard status, or JOSS acceptance.
