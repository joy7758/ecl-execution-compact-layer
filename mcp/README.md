# ECL MCP Anchor Stub v0.1

This directory is an MCP-shaped local wrapper ONLY.

It is NOT a registry plugin.
It is NOT external adoption.
It is NOT a published MCP server.
It is NOT ecosystem integration.

## Usage

```python
from mcp import ecl_server_stub as ecl
ecl_object = ecl.wrap(trace)
result = ecl.verify(ecl_object)
```

## Mapping

`mcp/ecl_server_stub.py` maps directly to `sdk/ecl_dependency.py`:

| MCP-shaped surface | Dependency SDK call |
| --- | --- |
| `ecl.wrap(trace)` | `sdk.ecl_dependency.wrap(trace)` |
| `ecl.emit(ecl_object)` | `sdk.ecl_dependency.emit(ecl_object)` |
| `ecl.verify(ecl_object)` | `sdk.ecl_dependency.verify(ecl_object)` |

## Determinism

The wrapper does not implement JSON-RPC transport, MCP host/client/server sessions, auth, registry integration, network services, or host runtime mutation. Its outputs are deterministic for identical inputs.
