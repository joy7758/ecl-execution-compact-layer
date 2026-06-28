# ECL v0.1

ECL is a deterministic execution IR for cross-runtime agent systems with replayable semantics and loss-aware mapping.

License: MIT.

## Structure Overview

- SDK: `sdk/`
- MCP stub: `mcp/`
- replay system: `examples/`, `external/adoption/`, `demo/replay_demo.py`
- paper: `paper/`
- reviewer quickstart: `docs/joss/REVIEWER_QUICKSTART_v0_1.md`
- API reference: `docs/api/ECL_API_REFERENCE_v0_1.md`

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
