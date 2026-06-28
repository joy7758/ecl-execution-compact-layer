# ECL v0.1

ECL is a deterministic execution IR for cross-runtime agent systems with replayable semantics and loss-aware mapping.

## Structure Overview

- SDK: `sdk/`
- MCP stub: `mcp/`
- replay system: `examples/`, `external/adoption/`, `demo/replay_demo.py`
- paper: `paper/`

## How To Use

```python
import ecl_dependency as ecl

ecl.wrap(trace)
ecl.verify(ecl_object)
```

## Non-goals

- not a framework
- not a runtime
- not a product
