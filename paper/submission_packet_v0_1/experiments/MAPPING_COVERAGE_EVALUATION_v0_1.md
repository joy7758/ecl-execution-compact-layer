# ECL Mapping Coverage Evaluation v0.1

Status: synthetic_mapping_coverage_evaluated

Scope: This evaluates field-level coverage over the local synthetic trace corpus. Direct mapping means a source top-level field maps to an ECL surface. Source-hash-only means the source field is not projected into a surface but remains covered by the raw trace hash. This is not production trace evidence, third-party validation, or benchmark evidence.

## Summary

- Cases: 12
- Runtimes: {'langchain': 6, 'openai': 6}
- Total source fields: 81
- Direct mapped source fields: 80
- Source-hash-only fields: 1
- Loss missing fields: 4
- Cases with source-hash-only fields: 1
- Cases with loss: 3
- Surface presence: {'state': 12, 'intent': 12, 'action': 10, 'evidence': 12}
- Surface presence by runtime: {'langchain': {'state': 6, 'intent': 6, 'action': 5, 'evidence': 6}, 'openai': {'state': 6, 'intent': 6, 'action': 5, 'evidence': 6}}
- Evaluation hash: sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a

## Case Results

| Case | Runtime | Fields | Direct mapped | Source hash only | Loss fields |
| --- | --- | ---: | ---: | ---: | --- |
| `openai_complete_multi_tool` | openai | 8 | 8 | 0 | none |
| `openai_missing_reasoning` | openai | 6 | 6 | 0 | reasoning |
| `openai_event_only_tool` | openai | 4 | 4 | 0 | reasoning |
| `openai_failed_result` | openai | 7 | 7 | 0 | none |
| `openai_unknown_fields` | openai | 8 | 7 | 1 | none |
| `openai_timestamp_drift` | openai | 7 | 7 | 0 | none |
| `langchain_complete_nested` | langchain | 7 | 7 | 0 | none |
| `langchain_missing_child_runs` | langchain | 6 | 6 | 0 | events,tool_call |
| `langchain_failed_tool` | langchain | 7 | 7 | 0 | none |
| `langchain_unknown_metadata` | langchain | 7 | 7 | 0 | none |
| `langchain_multi_step_tree` | langchain | 7 | 7 | 0 | none |
| `langchain_timestamp_drift` | langchain | 7 | 7 | 0 | none |

## Boundary

```text
synthetic_corpus=true
external_api_calls=false
third_party_validation=false
benchmark_result=false
```
