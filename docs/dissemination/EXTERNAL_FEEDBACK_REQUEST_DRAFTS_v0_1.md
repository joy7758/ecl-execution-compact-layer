# ECL External Feedback Request Drafts v0.1

Status: drafts_ready_not_posted

Date: 2026-06-30

## Purpose

These drafts support the 90-day feedback-intake route after the Zenodo DOI archive. They are not evidence that feedback has been requested, received, or independently validated.

## LangChain Forum Draft

```text
Title: Feedback request: deterministic execution IR for replayable agent runtime traces

ECL v0.1 is a DOI-archived prototype for representing agent runtime traces as a small deterministic execution IR.

It maps OpenAI-style and LangChain-style traces into four replayable surfaces: state, intent, action, and evidence. The repository includes an offline one-command demo:

make demo

I am looking for bounded feedback on the trace mapping surface:

- whether the state / intent / action / evidence split is clear;
- whether the loss-reporting boundary is understandable;
- whether the one-command demo is reproducible from a clean checkout;
- whether the limitations are stated narrowly enough.

Repository: https://github.com/joy7758/ecl-execution-compact-layer
Archive: https://doi.org/10.5281/zenodo.21003766

Boundary: this is a prototype and citation-ready software artifact. It is not a framework, benchmark, production deployment, standard, or adoption claim.
```

## MCP Discussion Draft

```text
Title: Feedback request: MCP-shaped local wrapper boundary for ECL

ECL v0.1 is a small deterministic execution IR prototype for replayable agent runtime traces. It includes a local MCP-shaped wrapper stub so that ECL wrap / emit / verify can be inspected as a protocol-shaped surface.

I am looking for feedback on the boundary wording:

- the local wrapper is not a published MCP server;
- it is not a registry plugin;
- it does not claim MCP compliance;
- it only demonstrates how ECL could be exposed as wrap / emit / verify semantics.

Repository: https://github.com/joy7758/ecl-execution-compact-layer
Archive: https://doi.org/10.5281/zenodo.21003766

Boundary: no production integration, external adoption, or standards-body claim is made.
```

## GitHub Feedback Issue Prompt

```text
Please run:

make demo

Then report:

- operating system;
- Python version;
- whether all tests passed;
- dependency_mode_result_hash;
- external_recognition_result_hash;
- any confusing documentation or trace-mapping boundary.

Do not include private traces, credentials, personal data, or production logs.
```

## Boundary

```text
drafts_prepared=true
posts_published=false
external_feedback_recorded=false
external_adoption_claim=false
peer_review_claim=false
production_deployment_claim=false
```
