# ECL Hostile Review Remediation v0.1

Status: current-route remediation applied

Date: 2026-06-28

Scope: This note applies the actionable parts of the hostile review to the current arXiv + JSS route. It does not reopen the JOSS submission route and does not claim external submission.

## Current Route

```text
primary_route=arxiv_plus_jss
joss_route=deprioritized
schema_changes=false
core_runtime_changes=false
sdk_changes=false
adapter_changes=false
external_submission_performed=false
```

## Review Finding Disposition

| Finding | Current disposition | Action |
| --- | --- | --- |
| JOSS `public_history` gate | Not applicable to the active JSS route; still fails if the JOSS route is reopened. | Keep JOSS blocked/deprioritized language. |
| State-of-field comparison too thin | Still relevant to arXiv and JSS. | Added explicit comparison with tracing, observability, provenance, lineage, and IR systems. |
| MCP compatibility ambiguity | Still relevant. | Strengthened non-conformance boundary: no JSON-RPC, session model, stateful connection, capability negotiation, auth layer, registry integration, or side-effect proof. |
| Evaluation metric ambiguity | Still relevant. | Added case-level, field-level, and label-level unit definitions for the trace-corpus and mapping-coverage counters. |
| Stale 65-test packet values | Historical JOSS packet issue; current arXiv + JSS manifests report 78 tests. | No active-package change required. |
| Research impact overclaim risk | Still relevant. | Active manuscripts keep claims local and do not claim adoption, production reliability, benchmark leadership, or third-party validation. |

## Authoritative Submission Surfaces

```text
paper/arxiv/submission/ECL_arxiv_v0_1.md
paper/arxiv/submission/ECL_arxiv_v0_1.pdf
paper/arxiv/submission/ECL_arxiv_v0_1_source.zip
paper/jss/JSS_READY.md
paper/jss/submission/ECL_JSS_manuscript_v0_1.docx
paper/jss/submission/ECL_JSS_submission_v0_1.zip
```

## Remaining Boundaries

- No arXiv upload has been performed.
- No JSS portal submission has been performed.
- No DOI has been minted.
- No external adoption signal is claimed.
- No JOSS submission should be attempted until its public-history condition is actually satisfied.
