# ECL Human Action Packet v0.1

Status: waiting_for_human_submission_inputs

Use this packet only after the human author decides to move from paper-and-screening completion to actual JOSS submission preparation.

## Human Inputs Needed

1. Author name.
2. Author affiliation.
3. ORCID or explicit decision to omit ORCID.
4. OSI-approved license choice.
5. Public repository URL.
6. Public issue tracker URL.
7. Release tag or archive DOI plan.
8. Final author approval.

## Files to Update After Human Inputs

- `paper/joss/paper.md`
- `paper/joss/AUTHOR_METADATA_TEMPLATE_v0_1.json`
- `paper/joss/JOSS_SUBMISSION_MANIFEST_v0_1.json`
- `paper/joss/JOSS_PREFLIGHT_AUDIT_v0_1.json`
- `paper/PAPER_COMPLETION_REPORT_v0_1.md`

## Verification Commands

```bash
python3 tests/test_joss_candidate.py
python3 tests/test_joss_preflight.py
python3 tests/test_venue_screening.py
python3 tests/test_paper_v0_1.py
python3 -m unittest discover -s tests
```

## Boundary

Do not submit until:

```text
joss_submission_ready=true
paid_journal_selected=false
formal_submission=false
```

The final submission click remains a separate human action.

