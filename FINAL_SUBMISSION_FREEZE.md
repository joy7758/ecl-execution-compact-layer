# ECL v0.1 Final Submission Freeze

## Freeze State

```text
object_type=ecl_final_submission_freeze
version=0.1
date_checked=2026-06-28
primary_route=arxiv_plus_jss
system_frozen=true
schema_frozen=true
core_runtime_frozen=true
sdk_frozen=true
adapter_surface_frozen=true
submission_materials_frozen=true
no_further_engineering_changes_allowed_before_submission=true
only_external_submission_actions_remain=true
jss_submission_material_ready=true
arxiv_submission_material_ready=true
joss_route_deprioritized=true
joss_public_history_gate_status=fail_current_state
jss_public_history_gate_required=false
jss_submission_performed=false
arxiv_submission_performed=false
doi_minted=false
```

## Locked Submission Surfaces

- `paper/jss/JSS_ROUTE_LOCK_v0_1.md`
- `paper/jss/JSS_SUBMISSION_CHECKLIST.md`
- `paper/jss/JSS_SUBMISSION_MANIFEST_v0_1.json`
- `paper/jss/submission/ECL_JSS_submission_v0_1.zip`
- `paper/arxiv/ARXIV_FINAL_SUBMISSION_LOCK.md`
- `paper/arxiv/ARXIV_SUBMISSION_MANIFEST_v0_1.json`
- `paper/arxiv/submission/ECL_arxiv_v0_1.pdf`
- `paper/arxiv/submission/ECL_arxiv_v0_1_source.zip`
- `PUBLICATION_RISK_FINAL_REPORT.md`
- `ARXIV_JSS_SUBMISSION_STATUS.md`

## Boundary

No additional ECL engineering changes should be made before external submission actions unless a human reviewer explicitly reopens the freeze.

External actions still require human control:

- final arXiv category/PDF/upload review;
- final JSS portal metadata, article type, and file upload review;
- final JOSS timing decision only if the old JOSS route is reopened;
- Zenodo deposit and DOI minting if selected.
