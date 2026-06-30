# ECL v0.1

ECL is a deterministic execution IR for cross-runtime agent systems with replayable semantics and loss-aware mapping.

License: MIT.

## Archive DOI

- Version DOI: `10.5281/zenodo.21003766`
- Concept DOI: `10.5281/zenodo.21003765`
- Zenodo record: `https://zenodo.org/records/21003766`
- Citation: `Zhang, B. (2026). ECL v0.1 (0.1). Zenodo. https://doi.org/10.5281/zenodo.21003766`

This DOI records the ECL v0.1 software archive. It is not a peer-review acceptance, production deployment, external adoption signal, or formal endorsement.

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
