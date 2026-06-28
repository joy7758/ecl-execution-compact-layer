# First External Mention Strategy v0.1

## Goal

Create a clear first mention surface for ECL without claiming external adoption.

## Recommended Mention Order

1. Cite the canonical definition in `docs/citation/ECL_CANONICAL_SPEC_v0_1.md`.
2. Link to the local reproducibility demo in `examples/citation_repro_demo.py`.
3. Reference the MCP-shaped local wrapper in `mcp/ecl_tool_spec.json` and `mcp/ecl_server_stub.py`.
4. State that the current status is local, deterministic, and pre-adoption.

## Acceptable Claim

ECL v0.1 provides a locally reproducible execution representation surface with deterministic replay and evidence generation.

## Forbidden Claims

- ECL is an adopted ecosystem standard.
- ECL is a published or conformant MCP server.
- ECL has third-party production validation.
- ECL has benchmark leadership results.
- ECL is a replacement for OpenAI Agents SDK, LangChain, or MCP.

## First Mention Template

```text
We reference ECL v0.1 as a local deterministic execution representation stack:
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> artifact hashes.
Current status: pre-adoption, local verification only.
```
