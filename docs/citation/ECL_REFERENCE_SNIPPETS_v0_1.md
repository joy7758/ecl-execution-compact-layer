# ECL Reference Snippets v0.1

## MCP-style Local Stub

```python
from mcp import ecl_server_stub as ecl

ecl_object = ecl.wrap(trace)
result = ecl.verify(ecl_object)
```

Boundary: this uses the local MCP-style stub only. It is not a published MCP server and does not imply registry integration.

## OpenAI Trace to ECL

```python
from sdk.ecl_dependency import wrap, verify

ecl_object = wrap({"runtime": "openai", "trace": openai_trace})
result = verify(ecl_object)
```

Boundary: this is a local trace conversion path. It does not call OpenAI APIs and does not modify any OpenAI runtime.

## Minimal Citation Sentence

ECL v0.1 is a deterministic execution representation stack that maps runtime traces into replayable `state`, `intent`, `action`, and `evidence` surfaces.

## Minimal Repository Reference

```json
{
  "name": "ecl-execution-compact-layer",
  "version": "0.1-local",
  "entrypoint": "sdk/ecl_dependency.py",
  "verification": "python3 -m unittest discover -s tests",
  "boundary": "local reproducibility only"
}
```
