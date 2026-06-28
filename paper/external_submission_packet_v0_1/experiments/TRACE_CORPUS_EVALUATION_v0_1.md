# ECL Trace Corpus Evaluation v0.1

Status: synthetic_corpus_evaluated

Scope: This evaluation uses a local synthetic stress corpus. It is not production trace evidence, third-party validation, or benchmark evidence.

## Summary

- Cases: 12
- Runtimes: {'langchain': 6, 'openai': 6}
- Valid cases: 12/12
- Deterministic cases: 12/12
- Loss expectation met: 12/12
- Surface coverage: {'state': 12, 'intent': 12, 'action': 12, 'evidence': 12}
- Surface coverage by runtime: {'langchain': {'state': 6, 'intent': 6, 'action': 6, 'evidence': 6}, 'openai': {'state': 6, 'intent': 6, 'action': 6, 'evidence': 6}}
- Loss type counts: {'semantic': 9, 'structural': 3}
- Total normalized events: 23
- Tags: complete, failure_status, implicit_tool, loss_expected, missing_field, multi_event, nested_run, timestamp, unknown_field

## Case Results

| Case | Runtime | Category | Events | Loss | Valid | Deterministic |
| --- | --- | --- | ---: | --- | --- | --- |
| `openai_complete_multi_tool` | openai | complete | 3 | none | true | true |
| `openai_missing_reasoning` | openai | missing_reasoning | 1 | reasoning | true | true |
| `openai_event_only_tool` | openai | implicit_tool_call | 2 | reasoning | true | true |
| `openai_failed_result` | openai | failed_result | 1 | none | true | true |
| `openai_unknown_fields` | openai | unknown_fields | 1 | none | true | true |
| `openai_timestamp_drift` | openai | timestamp_drift | 1 | none | true | true |
| `langchain_complete_nested` | langchain | complete | 3 | none | true | true |
| `langchain_missing_child_runs` | langchain | missing_child_runs | 1 | events,tool_call | true | true |
| `langchain_failed_tool` | langchain | failed_result | 2 | none | true | true |
| `langchain_unknown_metadata` | langchain | unknown_fields | 2 | none | true | true |
| `langchain_multi_step_tree` | langchain | multi_step | 4 | none | true | true |
| `langchain_timestamp_drift` | langchain | timestamp_drift | 2 | none | true | true |

## Boundary

```text
synthetic_corpus=true
external_api_calls=false
third_party_validation=false
benchmark_result=false
```
