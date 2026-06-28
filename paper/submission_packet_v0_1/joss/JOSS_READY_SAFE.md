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

# Engineering Process Model

ECL v0.1 follows a specification-first, single-phase design methodology:

```text
single_phase_design_methodology=true
spec_first_implementation_model=true
deterministic_architecture_predefined=true
iterative_refactoring_model=false
short_git_history_explained=true
reproducibility_depends_on_artifacts_not_commit_history=true
public_history_gate_status=fail_current_state
no_fake_history_added=true
no_commit_manipulation=true
schema_changes=false
```

The short public Git history is a publication-timing signal, not a claim that the project has already accumulated long-running public community development. ECL v0.1 was prepared as a frozen reference artifact whose reproducibility is evaluated through source files, schema, validator behavior, deterministic replay, examples, tests, experiment reports, and hash-stable outputs.

This narrative does not replace a true public-development-history signal. It only clarifies that the artifact's reviewable engineering evidence is specification-first and reproducibility-centered.

# Software Functionality

The ECL object model contains:

- `state`: execution lifecycle, actor, runtime, and correlation references.
- `intent`: requested operation, constraints, expected result, and evidence requirements.
- `action`: operation step, execution mode, side-effect class, tool reference, and parameter hash.
- `evidence`: result summary, trace references, event chain, policy decisions, and hashes.

The single authoritative execution flow is:

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

```bash
git clone https://github.com/joy7758/ecl-execution-compact-layer.git
cd ecl-execution-compact-layer
python3 -m pip install -e .
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
Ran 77 tests
OK
```

Additional deterministic checks are:

```bash
python3 experiments/evaluate_trace_corpus.py
python3 experiments/evaluate_validation_matrix.py
python3 experiments/evaluate_mapping_coverage.py
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
```

The demos and trace corpus are deterministic and use local fixtures or synthetic traces only.

# Boundary

ECL v0.1 is a software artifact for deterministic local execution representation. It does not claim external runtime validation, production deployment, benchmark superiority, formal standard status, JOSS acceptance, or a satisfied public-history gate.

```text
public_history_reviewer_concern_mitigated=true
public_history_gate_status=fail_current_state
joss_submission_performed=false
```
