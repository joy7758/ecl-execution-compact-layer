# ECL Validation Matrix Evaluation v0.1

Status: synthetic_negative_validation_evaluated

Scope: This evaluation mutates one local synthetic ECL record to test validator rejection behavior. It is not production trace evidence, third-party validation, or benchmark evidence.

## Summary

- Baseline valid: true
- Mutation cases: 8
- Expected invalid cases: 8
- Invalid cases detected: 8
- Expectations met: 8/8
- Evaluation hash: sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0

## Case Results

| Case | Expected valid | Actual valid | Error count |
| --- | --- | --- | ---: |
| `missing_state` | false | false | 3 |
| `wrong_schema_version` | false | false | 3 |
| `tampered_canonical_hash` | false | false | 1 |
| `source_hash_mismatch` | false | false | 2 |
| `empty_event_chain` | false | false | 3 |
| `additional_root_property` | false | false | 2 |
| `invalid_action_mode` | false | false | 2 |
| `missing_evidence_hashes` | false | false | 3 |

## Boundary

```text
synthetic_mutation=true
external_api_calls=false
third_party_validation=false
benchmark_result=false
```
