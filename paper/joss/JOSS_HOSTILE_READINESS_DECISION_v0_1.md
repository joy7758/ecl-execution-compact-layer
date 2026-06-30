# ECL JOSS Hostile Readiness Decision v0.1

Status: not_ready_for_immediate_joss_submission

Date checked: 2026-06-28

Scope: This is a hostile pre-submission decision for JOSS readiness. It does not submit to JOSS and does not claim acceptance.

## Decision

```text
immediate_joss_submission_recommended=false
joss_content_package_ready=true
software_install_test_ready=true
synthetic_experiment_evidence_ready=true
standard_joss_paper_path_ready=true
public_collaboration_surface_ready=true
joss_gate_verifier_ready=true
reviewer_narrative_alignment_ready=true
public_repo_synced=true
public_development_history_ready=false
external_impact_signal_ready=false
```

## Fixed Since Hostile Review

- `jsonschema>=4.0` is declared in `pyproject.toml`.
- `pyproject.toml` includes package metadata, project URLs, authorship, README, and keywords.
- `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SUPPORT.md`, and `.github/workflows/tests.yml` are present.
- OpenAI-style mapping now records `model_input -> intent`, `runtime_metadata -> state`, `tool_call -> action`, and `events/outputs -> evidence`.
- MCP language is restricted to "MCP-shaped local wrapper" and does not claim protocol conformance.
- The local evaluation now includes a 12-case synthetic trace corpus with all four ECL surfaces covered.
- The negative validation matrix now tests eight invalid-record mutations.
- Field-level mapping coverage now reports 80 directly mapped source fields, 1 source-hash-only field, and 4 loss-missing fields over 12 synthetic cases.
- Standard JOSS paper mirror files are present at `paper/paper.md` and `paper/paper.bib`.
- Public collaboration surfaces are present through issue templates, pull request template, test CI, and JOSS paper draft workflow.
- `scripts/joss_gate_verifier.py` records the remaining JOSS blocker and advisory external-impact signal as machine-readable gate evidence.
- The short-history reviewer narrative is explicitly handled through `paper/joss/ENGINEERING_PROCESS_STATEMENT_v0_1.md`, `paper/joss/JOSS_READY_SAFE.md`, `paper/NARRATIVE_UNIFICATION_v0_1.md`, and `paper/joss/JOSS_FINAL_READINESS_REPORT_v0_1.md`.

## Current Evidence

```text
python3 -m unittest discover -s tests
Ran 78 tests
OK

python3 experiments/evaluate_trace_corpus.py
case_count=12
by_runtime={"langchain": 6, "openai": 6}
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
evaluation_hash=sha256:f6afbe5e7cd63960f844c41bcb88438b3fa567e760504a61ad91ade245a7e8f9

python3 experiments/evaluate_validation_matrix.py
baseline_valid=true
case_count=8
expected_invalid_count=8
invalid_detected_count=8
expectation_met_count=8
evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0

python3 experiments/evaluate_mapping_coverage.py
case_count=12
total_source_fields=81
direct_mapped_field_count=80
source_hash_only_field_count=1
loss_missing_field_count=4
evaluation_hash=sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a
```

## Remaining Hostile-Reviewer Blockers

| Gate | Status | Evidence |
| --- | --- | --- |
| Public development history over time | fail_current_state | Local git history is concentrated on 2026-06-28. |
| Reviewer narrative alignment | pass_not_gate_satisfying | The package explains the spec-first, single-phase design model without fabricating commit history. |
| Public-history maturation plan | pass_not_gate_satisfying | `paper/joss/JOSS_PUBLIC_HISTORY_MATURATION_PLAN_v0_1.md` records a non-fabricated maturation path with earliest safe reassessment on 2026-12-29. |
| External impact or independent use | advisory_unverified | No external citation, third-party dependency, or independent user signal is verified; this is advisory rather than the sole impact gate. |
| JOSS final human submission approval | not_done | No JOSS portal action has been performed. |

## Recommendation

Do not submit to JOSS immediately unless the author accepts a residual public-history risk. The reviewer-perception risk from short history is mitigated by the engineering process statement, but the actual public-history gate remains unsatisfied. The technically repaired package is suitable for continued public development, arXiv/Zenodo staging, and external feedback gathering. Re-run this decision no earlier than the public-history maturation checkpoint unless JOSS policy or verified external evidence changes; external-use evidence remains a positive advisory signal but is not treated as the sole JOSS impact gate.

## Sources

- https://joss.readthedocs.io/en/latest/submitting.html
- https://joss.readthedocs.io/en/latest/review_criteria.html
- https://joss.readthedocs.io/en/latest/paper.html

## Boundary

```text
joss_submission_performed=false
acceptance_claim=false
third_party_validation=false
external_adoption=false
public_repo_synced=true
reviewer_narrative_alignment_ready=true
synthetic_corpus_only=true
```
