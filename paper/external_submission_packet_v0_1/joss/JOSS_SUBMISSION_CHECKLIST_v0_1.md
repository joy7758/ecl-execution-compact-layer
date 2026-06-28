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

Confirmed for publication activation:

- Author: Bin Zhang.
- Affiliation: independent researcher.
- ORCID: omitted.
- License: MIT.
- Repository target: `https://github.com/joy7758/ecl-execution-compact-layer`.
- Community guidelines: `CONTRIBUTING.md` and `SUPPORT.md`.
- Citation metadata: `CITATION.cff`.
- Changelog: `CHANGELOG.md`.
- CI workflow file: `.github/workflows/tests.yml`.
- JOSS paper draft workflow: `.github/workflows/joss-paper.yml`.
- Issue templates: `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/research_use_report.yml`, and `.github/ISSUE_TEMPLATE/trace_mapping_case.yml`.
- Pull request template: `.github/PULL_REQUEST_TEMPLATE.md`.
- Standard JOSS paper mirror: `paper/paper.md` and `paper/paper.bib`.
- Developer research-use note: `docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md`.

Still requires human confirmation before JOSS submission:

- Confirm public development history expectation.
- Confirm Zenodo DOI or archive plan if required.
- Confirm final JOSS submission approval.
- Pass `paper/joss/JOSS_PREFLIGHT_AUDIT_v0_1.json`.
- Confirm final JOSS metadata and repository URL.

## Boundary

- `joss_submission_performed=false`
- `formal_submission=false`
- `public_release=true`
- `paid_journal_selected=false`
- `acceptance_claim=false`
