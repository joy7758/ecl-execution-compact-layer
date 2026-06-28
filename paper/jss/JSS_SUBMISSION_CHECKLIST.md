# ECL JSS Submission Checklist v0.1

Target journal: The Journal of Systems and Software

Route: arXiv preprint plus JSS journal submission package.

## Source Requirements

```text
jss_source_docx_required=true
jss_pdf_preview_required=true
highlights_separate_editable_file=true
cover_letter_ready=true
declarations_ready=true
data_availability_statement_ready=true
```

## Manuscript Requirements

```text
title_page_ready=true
abstract_word_count_lte_250=true
keywords_count=6
highlights_count=4
highlights_each_lte_85_chars=true
credit_statement_ready=true
competing_interest_statement_ready=true
funding_statement_ready=true
generative_ai_statement_ready=true
data_availability_statement_ready=true
```

## Technical Validation

```text
unit_tests=78_ok
trace_corpus_cases=12
validation_matrix_cases=8
mapping_coverage_cases=12
sdk_demo_dependency_mode=deterministic_valid
external_recognition_demo=deterministic_valid
schema_changes=false
core_modification=false
```

## Boundary

```text
jss_submission_performed=false
arxiv_submission_performed=false
doi_minted=false
joss_route_deprioritized=true
public_history_gate_not_applicable_to_jss=true
```

## Human Actions Still Required

- Verify final author metadata and email address in the journal portal.
- Select the correct article type and classification in Editorial Manager.
- Confirm whether an arXiv preprint has already been submitted before journal submission.
- Upload the DOCX source, highlights file, cover letter, declarations, and PDF preview.
- Complete publisher declarations in the portal.
