# Changelog

All notable changes to ECL are recorded here for agent-readable release review.

## v0.1.0 - 2026-06-28

Status: public_release_and_zenodo_archive

- Added the ECL schema, validator, deterministic hash utilities, and replay artifacts.
- Added OpenAI-style and LangChain-style trace mapping surfaces.
- Added SDK and dependency APIs for local wrapping, emitting, and verifying ECL objects.
- Added an MCP-shaped local wrapper with explicit non-conformance boundaries.
- Added JOSS and arXiv submission-candidate paper materials.
- Added a 12-case synthetic trace-corpus evaluation covering OpenAI-style and LangChain-style traces.
- Added an 8-case negative validation-matrix evaluation for schema drift, hash tampering, missing fields, and invalid enum behavior.
- Added MIT license, contribution guidelines, support policy, citation metadata, and CI configuration.
- Published the ECL v0.1 software archive on Zenodo: `10.5281/zenodo.21003766`.
- Added technical-report and ICSE 2027 tool-demo preparation surfaces after JSS prescreen rejection.
- Added `make demo` as the one-command local reviewer entrypoint.
- Added citation package, safe public announcement copy, 90-day execution plan, and post-JSS route audit.
- Added ICSE demo manifest, local terminal transcript, Docker daemon status, and Zenodo technical-report new-version candidate package.
- Added maintenance evidence ledger, maintenance release template, and feedback intake protocol for the six-month JOSS maturation route.

Boundary:

```text
jss_submission_performed=true
jss_decision=prescreen_reject
jss_rejected_and_closed=true
arxiv_submission_performed=false
zenodo_deposit_created=true
zenodo_record_published=true
doi_minted=true
zenodo_version_doi=10.5281/zenodo.21003766
third_party_validation=false
synthetic_corpus_only=true
```
