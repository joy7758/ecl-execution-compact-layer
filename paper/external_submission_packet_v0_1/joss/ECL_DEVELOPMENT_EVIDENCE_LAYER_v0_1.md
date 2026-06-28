# ECL Development Evidence Layer v0.1

Status: engineering_evolution_narrative

Date checked: 2026-06-28

Scope: This document records engineering evolution evidence for ECL v0.1. It is not a fabricated git history, not a substitute for JOSS public-history requirements, and not evidence of external adoption.

## Purpose

JOSS reviewers can reasonably ask whether ECL is a single repository dump or the result of iterative engineering. The public git history for this repository is currently concentrated on 2026-06-28, so this document makes the internal design evolution explicit without rewriting history.

## Decision Timeline

| Stage | Decision | Evidence Surface | Outcome |
| --- | --- | --- | --- |
| Object model selection | Keep the ECL record limited to `state`, `intent`, `action`, and `evidence`. | `schemas/ecl-execution-compact-layer.schema.json`, `SPEC.md`, `paper/paper.md` | Prevented schema expansion into a general trace framework. |
| Determinism contract | Use sorted JSON serialization and SHA-256 artifact hashes for local replay stability. | `ecl/canonical.py`, `demo/replay_demo.py`, `external/adoption/replay_adapter.py` | Enabled repeatable replay artifacts and hash checks. |
| Adapter boundary | Treat OpenAI-style and LangChain-style traces as input formats, not runtime dependencies. | `ecl/adapters/`, `external/adoption/`, `tests/fixtures/` | Avoided external API calls and runtime mutation. |
| Loss handling | Record loss explicitly rather than hiding incomplete mappings. | `external/adoption/ecl_mapper.py`, `experiments/MAPPING_COVERAGE_EVALUATION_v0_1.md` | Made incomplete field preservation auditable. |
| SDK surface | Limit dependency mode to `wrap`, `emit`, and `verify`. | `sdk/ecl_dependency.py`, `tests/test_dependency_sdk.py` | Preserved a small adoption surface. |
| MCP-shaped surface | Keep MCP support local and non-registrable. | `mcp/ecl_server_stub.py`, `mcp/ecl_tool_spec.json`, `tests/test_mcp_anchor_stub.py` | Avoided claiming public MCP server status. |
| JOSS repair | Add pyproject metadata, paper mirror, CI surfaces, synthetic corpus, validation matrix, mapping coverage, and gate verifier. | `pyproject.toml`, `.github/`, `paper/joss/`, `experiments/`, `scripts/joss_gate_verifier.py` | Converted a concept-heavy artifact into a reproducible software submission package. |

## Rejected Alternatives

| Alternative | Reason Rejected |
| --- | --- |
| Treat ECL as a full agent runtime. | This would compete with host frameworks and expand scope beyond execution representation. |
| Preserve every runtime-specific trace field as first-class schema fields. | This would make the schema runtime-dependent and unstable. |
| Claim MCP conformance or registry integration. | The repository only provides a local MCP-shaped wrapper. |
| Treat external impact as a hard JOSS gate. | External adoption is a strong signal but not the sole evidence of research impact. |
| Treat a development narrative as public history. | That would misrepresent JOSS public-history expectations. |
| Backfill or rewrite git history. | That would create invalid credibility evidence. |

## Stabilization Evidence

| Stabilization Area | Current Evidence |
| --- | --- |
| Unit tests | `python3 -m unittest discover -s tests` runs 75 tests. |
| Trace corpus | 12 synthetic OpenAI-style and LangChain-style cases validate and replay deterministically. |
| Negative validation | 8 invalid-record mutations are detected. |
| Mapping coverage | 80 direct source-field mappings, 1 source-hash-only field, and 4 loss-missing fields are recorded over 12 cases. |
| Replay artifacts | `examples/citation_repro_demo.py`, `sdk/demo_dependency_mode.py`, and `mcp/ecl_server_stub.py` produce deterministic hashes. |
| Submission boundary | JOSS submission, DOI minting, and third-party validation are explicitly false unless externally performed. |

## Remaining Risk

```text
public_git_history_span_days=1
public_history_gate_status=fail_current_state
development_evidence_layer_status=pass
does_not_satisfy_public_history_gate=true
non_fake_history=true
```

## Interpretation

This evidence layer mitigates the reviewer concern that the repository lacks an engineering story. It does not satisfy the JOSS public-history gate by itself. The correct submission interpretation is:

```text
technical_submission_package_ready=true
development_evidence_documented=true
joss_public_history_gate=false
immediate_joss_submission_recommended=false
```
