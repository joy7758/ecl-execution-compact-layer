# ECL Zenodo Technical Report Attachment Decision v0.1

Status: github_release_uploaded_zenodo_new_version_required

Date: 2026-06-30

## Current State

Zenodo record `21003766` is already published:

```text
record_url=https://zenodo.org/records/21003766
version_doi=10.5281/zenodo.21003766
concept_doi=10.5281/zenodo.21003765
```

The technical report PDF exists in the repository and GitHub Release:

```text
paper/technical_report/ECL_TECHNICAL_REPORT_v0_1.pdf
github_release_asset=https://github.com/joy7758/ecl-execution-compact-layer/releases/download/v0.1/ECL_TECHNICAL_REPORT_v0_1.pdf
```

## Zenodo Attachment Boundary

The published Zenodo v0.1 file set cannot be silently modified. Adding the technical report PDF as a Zenodo file requires creating and publishing a new Zenodo version.

## Decision

No new Zenodo version has been published in this record.

The current safe state is:

```text
technical_report_uploaded_to_github_release=true
technical_report_uploaded_to_zenodo_record=false
zenodo_new_version_required=true
zenodo_new_version_published=false
```

## Next Action

If direct Zenodo attachment is required, create a new Zenodo version after human confirmation, attach:

- `ECL_v0.1_zenodo_deposit_package.zip`
- `paper/technical_report/ECL_TECHNICAL_REPORT_v0_1.pdf`
- citation metadata files

This would mint a new version DOI under the same concept DOI. Do not claim this has happened until a new public Zenodo version exists.
