# ECL v0.1 Submission Materials Index

Status: local_submission_packet_ready_not_submitted

Date prepared: 2026-06-28

Scope: This index organizes the local materials for human-controlled JOSS, arXiv, and Zenodo staging. It does not perform submission, DOI minting, upload, or acceptance claim.

## Primary Packet

```text
paper/submission_packet_v0_1/
paper/submission_packet_v0_1.zip
```

## JOSS Materials

Use for JOSS human submission:

```text
paper/joss/paper.md
paper/joss/paper.bib
paper/paper.md
paper/paper.bib
paper/joss/JOSS_SUBMISSION_CHECKLIST.md
paper/joss/JOSS_READY.md
paper/joss/JOSS_READY_SAFE.md
```

Support and audit:

```text
paper/joss/JOSS_PREFLIGHT_AUDIT_v0_1.md
paper/joss/JOSS_PREFLIGHT_AUDIT_v0_1.json
paper/joss/JOSS_HOSTILE_READINESS_DECISION_v0_1.md
paper/joss/JOSS_HOSTILE_READINESS_DECISION_v0_1.json
paper/joss/JOSS_GATE_VERIFICATION_v0_1.md
paper/joss/JOSS_GATE_VERIFICATION_v0_1.json
paper/joss/ENGINEERING_PROCESS_STATEMENT_v0_1.md
paper/NARRATIVE_UNIFICATION_v0_1.md
paper/joss/JOSS_FINAL_READINESS_REPORT_v0_1.md
paper/joss/JOSS_SUBMISSION_MANIFEST_v0_1.json
paper/joss/AUTHOR_METADATA_TEMPLATE_v0_1.json
```

## arXiv Materials

```text
paper/arxiv/ARXIV_READY.md
paper/arxiv/ARXIV_SUBMISSION_PACKAGE.md
paper/ECL_PAPER_v0_1.md
```

## Zenodo Metadata

```text
release/v0.1/zenodo_deposit_ready.json
release/v0.1/zenodo.json
```

Packet copies are under:

```text
paper/submission_packet_v0_1/zenodo/
```

## Evidence

```text
paper/ECL_PAPER_EVIDENCE_v0_1.json
experiments/TRACE_CORPUS_EVALUATION_v0_1.md
experiments/out/trace_corpus_evaluation.json
experiments/trace_corpus/corpus_manifest.json
experiments/VALIDATION_MATRIX_EVALUATION_v0_1.md
experiments/out/validation_matrix_evaluation.json
experiments/MAPPING_COVERAGE_EVALUATION_v0_1.md
experiments/out/mapping_coverage_evaluation.json
paper/PUBLICATION_READINESS_REPORT.md
PUBLICATION_ACTIVATION_FINAL_REPORT.md
CITATION.cff
CHANGELOG.md
CONTRIBUTING.md
SUPPORT.md
.github/workflows/tests.yml
.github/workflows/joss-paper.yml
.github/PULL_REQUEST_TEMPLATE.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/research_use_report.yml
.github/ISSUE_TEMPLATE/trace_mapping_case.yml
scripts/joss_gate_verifier.py
docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md
```

## Current Validation Snapshot

```text
python3 -m unittest discover -s tests
Ran 78 tests
OK

python3 experiments/evaluate_trace_corpus.py
case_count=12
valid_count=12
deterministic_count=12
loss_expectation_met_count=12
surface_coverage={"action": 12, "evidence": 12, "intent": 12, "state": 12}
evaluation_hash=sha256:f6afbe5e7cd63960f844c41bcb88438b3fa567e760504a61ad91ade245a7e8f9

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
```

## Upload Boundary

Do not upload internal repair notes unless explicitly needed for human review:

```text
paper/submission_packet_v0_1/reports/HOSTILE_REVIEW_REPAIR_REPORT.md
```

Boundary:

```text
joss_submission_performed=false
arxiv_submission_performed=false
zenodo_deposit_created=false
doi_minted=false
public_repo_synced=true
third_party_validation=false
synthetic_corpus_only=true
```
