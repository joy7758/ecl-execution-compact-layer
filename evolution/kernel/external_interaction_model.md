# ECL External Interaction Model v0.1

Status: theoretical formalization

Scope: This file defines external interaction signals for ECL evolution. It contains no code, SDK changes, runtime changes, monitoring, or system modification.

## 1. External Signals

`citations`:

Attributable references to ECL in papers, repositories, specifications, design documents, issues, or implementation notes.

`forks`:

External repository, packaging, documentation, implementation, or execution variants derived from or resembling ECL.

`runtime usage`:

External use of ECL object shape, adapter mapping, replay semantics, evidence generation, dependency interface, or trace normalization.

## 2. Mapping

```text
signal -> drift contribution
```

| Signal | Drift contribution |
| --- | --- |
| `citations` | May expose semantic interpretation drift when external descriptions reinterpret ECL concepts. |
| `forks` | May expose structural drift, semantic drift, or execution drift depending on what the fork changes. |
| `runtime usage` | May expose execution drift when replay, validation, hash, evidence, or loss behavior diverges. |

## 3. Constraint

External interaction is observational only.

No system modification is allowed by this model.

This model does not change ECL schema, SDK, runtime, adapters, release artifacts, or external systems.

