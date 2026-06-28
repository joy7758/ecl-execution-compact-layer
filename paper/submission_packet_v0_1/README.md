# ECL v0.1 Submission Packet

Status: human_review_packet_ready_not_submitted

Date prepared: 2026-06-28

Repository: https://github.com/joy7758/ecl-execution-compact-layer

Release: https://github.com/joy7758/ecl-execution-compact-layer/releases/tag/v0.1

## Purpose

This directory collects paper, release, experiment, metadata, GitHub review-surface, and hostile-readiness materials for human-controlled JOSS, arXiv, and Zenodo staging.

It does not perform submission, upload, deposit creation, DOI minting, or acceptance claim.

## JOSS State

```text
joss_content_package_ready=true
standard_joss_paper_path_ready=true
public_collaboration_surface_ready=true
joss_gate_verifier_ready=true
immediate_joss_submission_recommended=false
joss_submission_performed=false
public_repo_synced=true
public_development_history_ready=false
external_impact_signal_ready=false
```

Use `joss/JOSS_HOSTILE_READINESS_DECISION_v0_1.md` before deciding whether to submit.

## Validation Snapshot

```text
python3 -m unittest discover -s tests
Ran 75 tests
OK

python3 experiments/evaluate_trace_corpus.py
case_count=12
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974

python3 experiments/evaluate_validation_matrix.py
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

python3 scripts/joss_gate_verifier.py
status=joss_gate_failed_external_blockers
blocking_gates=["public_history", "external_impact"]
```

## Boundary

```text
automatic_submission_performed=false
external_publication_triggered=false
joss_submission_performed=false
arxiv_submission_performed=false
zenodo_deposit_created=false
doi_minted=false
third_party_validation=false
synthetic_corpus_only=true
public_repo_synced=true
```
