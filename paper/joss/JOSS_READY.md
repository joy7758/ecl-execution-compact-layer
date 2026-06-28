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
trace -> ECL object -> validate -> replay -> evidence -> hash
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

ECL v0.1 uses the Python standard library for its core local examples and tests.

Clone the repository:

```bash
git clone https://github.com/joy7758/ecl-execution-compact-layer.git
cd ecl-execution-compact-layer
```

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

# Minimal Example

```python
import sys
from pathlib import Path

ROOT = Path("ecl-execution-compact-layer").resolve()
sys.path.insert(0, str(ROOT / "sdk"))

import ecl_dependency as ecl

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

ecl_object = ecl.wrap(trace)
result = ecl.verify(ecl_object)

assert result["valid"]
assert result["deterministic"]
```

# Reproducibility

The required verification command is:

```bash
python3 -m unittest discover -s tests
```

The current local result is:

```text
Ran 65 tests
OK
```

The dependency-mode demo is:

```bash
python3 sdk/demo_dependency_mode.py
```

The external recognition demo is:

```bash
python3 examples/external_recognition_demo.py
```

Both demos are deterministic and use local fixtures only.

# Boundary

ECL v0.1 is a software artifact for deterministic local execution representation. It does not claim external runtime validation, production deployment, benchmark superiority, formal standard status, or JOSS acceptance.

