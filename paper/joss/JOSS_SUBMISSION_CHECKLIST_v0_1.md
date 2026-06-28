# ECL JOSS Submission Checklist v0.1

Status: candidate_missing_human_metadata_not_submitted

Date checked: 2026-06-28

Scope: This checklist prepares a no-fee JOSS candidate package. It does not submit to JOSS, does not claim acceptance, and does not claim public release.

## Candidate Files

- `paper/joss/paper.md`
- `paper/joss/paper.bib`
- `paper/joss/JOSS_SUBMISSION_MANIFEST_v0_1.json`

## JOSS Fit

JOSS is the preferred no-paid-journal route because the JOSS documentation states that there are no fees for submitting or publishing in JOSS.

Source:

- https://joss.readthedocs.io/en/latest/submitting.html

## Current Local Readiness

Ready locally:

- JOSS-style `paper.md` exists.
- `paper.bib` exists.
- Summary section exists.
- Statement of need section exists.
- State of the field section exists.
- Software design section exists.
- Research impact statement exists.
- AI usage disclosure exists.
- Local test command is documented.
- No paid journal route is selected.

Still requires human confirmation before submission:

- Replace `<AUTHOR_NAME>`.
- Replace `<AFFILIATION_NAME>`.
- Confirm or remove `<ORCID_OPTIONAL>`.
- Complete `paper/joss/AUTHOR_METADATA_TEMPLATE_v0_1.json`.
- Confirm repository public release status.
- Confirm OSI-approved license file.
- Confirm long-term archive or DOI plan.
- Confirm final author approval.
- Pass `paper/joss/JOSS_PREFLIGHT_AUDIT_v0_1.json`.
- Confirm final JOSS metadata and repository URL.

## Boundary

- `joss_submission_performed=false`
- `formal_submission=false`
- `public_release=false`
- `paid_journal_selected=false`
- `acceptance_claim=false`
