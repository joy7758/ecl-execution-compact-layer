# arXiv Submission Package for ECL v0.1

Status: prepared_not_submitted

Date prepared: 2026-06-28

## 1. Title

ECL: A Deterministic Cross-Runtime Execution IR with Replayable Semantics

## 2. Abstract

Agent runtimes expose traces through framework-specific surfaces such as model inputs, tool calls, callbacks, spans, and event streams. These traces are useful locally but difficult to compare, replay, or cite across heterogeneous runtimes. This paper presents Execution Compact Layer (ECL), a deterministic execution intermediate representation for agent systems. ECL maps runtime traces into four replayable surfaces: `state`, `intent`, `action`, and `evidence`. The v0.1 artifact includes a frozen schema, deterministic validation and replay, OpenAI Agents SDK-style and LangChain-style trace adapters, an embeddable SDK, a dependency API, and a local compatibility stub. ECL is not a framework or public standard; it is a reproducible execution representation layer for cross-runtime agent traces.

## 3. Full System Description

ECL defines a minimal execution IR:

```text
E = (state, intent, action, evidence)
```

The IR records execution state, requested intent, performed action, and evidence references. It is validated against:

```text
schemas/ecl-execution-compact-layer.schema.json
```

The replay model is deterministic:

```text
input -> validate -> replay -> trace -> evidence -> hash
```

For unchanged input, schema, adapter, validator, and generation parameters, ECL preserves validation results and replay artifact hashes.

The SDK surface is:

```python
from ecl import ECL

record = ECL.create(state, intent, action)
ECL.validate(record)
ECL.replay(record)
```

The dependency surface is:

```python
import ecl_dependency as ecl

ecl_object = ecl.wrap(trace)
payload = ecl.emit(ecl_object)
result = ecl.verify(ecl_object)
```

The dependency interface lets an external system emit or verify ECL objects without modifying its host runtime.

## 4. Figure References

No new figures are introduced for this package.

Use existing architecture and flow references from:

```text
paper/arxiv/ARXIV_READY.md
paper/ECL_PAPER_v0_1.md
docs/ecl_external_architecture.md
```

## 5. BibTeX Entry

```bibtex
@software{ecl_v0_1,
  title = {ECL v0.1: Deterministic execution IR layer},
  author = {Zhang, Bin},
  year = {2026},
  version = {0.1},
  url = {https://github.com/joy7758/ecl-execution-compact-layer},
  note = {GitHub release: https://github.com/joy7758/ecl-execution-compact-layer/releases/tag/v0.1}
}
```

## 6. Submission Checklist

- Title finalized: yes.
- Abstract under 200 words: yes.
- Author recorded: Bin Zhang.
- Affiliation recorded: independent researcher.
- Repository URL recorded: https://github.com/joy7758/ecl-execution-compact-layer.
- GitHub release recorded: https://github.com/joy7758/ecl-execution-compact-layer/releases/tag/v0.1.
- License recorded: MIT.
- Tests passing locally: yes.
- External submission performed: no.
- DOI minted: no.

