# Changelog

All notable changes to ECL are recorded here for agent-readable release review.

## v0.1.0 - 2026-06-28

Status: public_release_ready_local_submission_staging

- Added the ECL schema, validator, deterministic hash utilities, and replay artifacts.
- Added OpenAI-style and LangChain-style trace mapping surfaces.
- Added SDK and dependency APIs for local wrapping, emitting, and verifying ECL objects.
- Added an MCP-shaped local wrapper with explicit non-conformance boundaries.
- Added JOSS and arXiv submission-candidate paper materials.
- Added a 12-case synthetic trace-corpus evaluation covering OpenAI-style and LangChain-style traces.
- Added an 8-case negative validation-matrix evaluation for schema drift, hash tampering, missing fields, and invalid enum behavior.
- Added MIT license, contribution guidelines, support policy, citation metadata, and CI configuration.

Boundary:

```text
joss_submission_performed=false
arxiv_submission_performed=false
zenodo_deposit_created=false
doi_minted=false
third_party_validation=false
synthetic_corpus_only=true
```
