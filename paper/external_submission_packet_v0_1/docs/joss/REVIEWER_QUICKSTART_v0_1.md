# ECL JOSS Reviewer Quickstart v0.1

Status: joss_reviewer_quickstart

Scope: This document gives a reviewer a short, deterministic path to inspect and reproduce the ECL v0.1 software artifact. It uses only local commands and included fixtures.

## 1. Install

```bash
python3 -m pip install -e .
```

Expected package metadata:

```text
name=ecl-execution-compact-layer
version=0.1.0
license=MIT
python>=3.10
```

## 2. Run Tests

```bash
python3 -m unittest discover -s tests
```

Expected checked result:

```text
Ran 78 tests
OK
```

## 3. Reproduce Evaluations

```bash
python3 experiments/evaluate_trace_corpus.py
python3 experiments/evaluate_validation_matrix.py
python3 experiments/evaluate_mapping_coverage.py
```

Expected stable hashes:

```text
trace_corpus_evaluation_hash=sha256:2434da21056811e7eacf1ffac6944d5420ddeb2aa783f74423326a2b54a33974
validation_matrix_evaluation_hash=sha256:00fe0ee8952988f7460280b40554889a890c93f9d181a6c9d8ee8b0194b031c0
mapping_coverage_evaluation_hash=sha256:8a8b820ecbdd1b4e88a2d8e07b05be2d479add0f0c6c3265292cc5a86763e43a
```

## 4. Run Examples

```bash
python3 examples/citation_repro_demo.py
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
python3 mcp/ecl_server_stub.py
```

Expected stable result hashes:

```text
citation_repro_demo_hash=sha256:8684fa8963ff9ad55c36eed6b89eb15992d1b05566aa1c79ced754fac67e1cdd
dependency_mode_hash=sha256:e6decc8c2c4117011db44c6bcd62956b62344fe47871fc6564913cac2c156ac2
external_recognition_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
mcp_anchor_verification_hash=sha256:bdcf2ddb30a0e5975782f77fa86415226c46652bbd5490a667a2f2106dd65a5f
```

## 5. Inspect API Surface

Use:

```text
docs/api/ECL_API_REFERENCE_v0_1.md
sdk/README.md
sdk/DEPENDENCY_README.md
```

The main public Python surfaces are:

```text
sdk.ecl.ECL.create
sdk.ecl.ECL.validate
sdk.ecl.ECL.replay
sdk.ecl.ECL.to_trace
sdk.ecl.ECL.from_trace
sdk.ecl_dependency.wrap
sdk.ecl_dependency.emit
sdk.ecl_dependency.verify
```

## 6. Inspect JOSS Boundary

```bash
python3 scripts/joss_gate_verifier.py
```

Current expected gate state:

```text
content_package_ready=true
blocking_gates=["public_history"]
public_repo_sync=pass
public_history_maturation_plan=pass
immediate_joss_submission_recommended=false
```

## Boundary

```text
joss_submission_performed=false
third_party_validation=false
synthetic_corpus_only=true
public_history_gate_status=fail_current_state
```
