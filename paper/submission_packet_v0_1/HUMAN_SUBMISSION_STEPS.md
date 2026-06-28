# Human Submission Steps

Status: manual_action_required

## JOSS

Use:

- `standard-paper/paper.md`
- `standard-paper/paper.bib`
- `joss/JOSS_SUBMISSION_CHECKLIST.md`
- `joss/JOSS_HOSTILE_READINESS_DECISION_v0_1.md`
- `joss/JOSS_GATE_VERIFICATION_v0_1.md`

Current recommendation:

```text
immediate_joss_submission_recommended=false
```

Human actions:

1. Review the hostile readiness decision.
2. Review the gate verification output.
3. Commit and push the repaired worktree before using the public repository URL.
4. Confirm whether to accept the public-history blocker and the external-impact advisory risk.
5. If still proceeding, open the JOSS submission website and enter final metadata manually.

## arXiv

Use:

- `arxiv/ARXIV_SUBMISSION_PACKAGE.md`
- `arxiv/ARXIV_READY.md`
- `arxiv/ECL_PAPER_v0_1.md`

## Zenodo

Use:

- `zenodo/zenodo_deposit_ready.json`
- `zenodo/zenodo.json`

Boundary:

```text
joss_submission_performed=false
arxiv_submission_performed=false
zenodo_deposit_created=false
doi_minted=false
```
