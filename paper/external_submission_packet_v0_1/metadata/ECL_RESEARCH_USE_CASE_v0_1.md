# ECL Research Use Case v0.1

Status: developer_research_workflow_documented

Date: 2026-06-28

Scope: This document records the current research workflow supported by ECL. It does not claim third-party adoption, production deployment, or benchmark superiority.

## Research Question

Can heterogeneous agent runtime traces be normalized into a deterministic execution representation that preserves replay stability and explicitly records mapping loss?

## Workflow

```text
runtime trace fixture
-> normalize trace
-> map to ECL object
-> validate schema and hash contract
-> replay artifacts
-> compare deterministic hashes
-> record loss expectation result
```

## Current Evidence

```text
python3 experiments/evaluate_trace_corpus.py
case_count=12
by_runtime={"langchain": 6, "openai": 6}
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974
```

Negative validation evidence:

```text
python3 experiments/evaluate_validation_matrix.py
baseline_valid=true
case_count=8
expected_invalid_count=8
invalid_detected_count=8
expectation_met_count=8
evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0
```

## Boundary

```text
developer_research_use=true
external_research_use=false
third_party_validation=false
benchmark_result=false
production_trace_evidence=false
```
