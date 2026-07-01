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
- Added public maintainer-created maintenance issue bootstrap for `v0.1.1` through `v0.1.6`.
- Added external feedback request drafts and ICSE tool-demo tracking issue reference without posting or claiming feedback.
- Added public GitHub feedback request issue status while keeping external feedback and adoption claims false.
- Fixed the reviewer Docker demo path by installing `git` and `make`, and normalized replay artifact references for container/host-stable demo hashes.
- Added ICSE 2027 public-link verification and an IEEEtran draft PDF/source package for human review; video recording and ICSE submission remain pending.
- Added a local ICSE demo video candidate, captions, YouTube metadata draft, and HotCRP submission-field draft while keeping YouTube upload and ICSE submission false.
- Repaired the local ICSE demo video candidate timing so video/audio streams align and captions remain inside the 3m45s video duration; upload and submission remain false.
- Synchronized the public feedback request expected `make demo` hashes with the current deterministic demo outputs.
- Added an external forum posting handoff for LangChain Forum and MCP Discussions without marking any forum post as published.
- Added an external action queue for the remaining human-executed YouTube, forum, HotCRP, feedback, and maintenance steps.
- Added unit-test coverage for the external action queue boundaries, referenced packets, and cross-manifest hashes.
- Added a command-line external action queue verifier and wired it into `make demo` and CI without claiming any external action occurred.
- Added an external action evidence intake template and validator for future YouTube, forum, HotCRP, and third-party feedback URLs while keeping the default state empty.
- Added an ICSE tool-demo package verifier for local PDF, video, link, demo-hash, and external-submission boundary checks.
- Added an aggregate post-JSS route verifier that reports local gates passing while keeping future external steps open.
- Added a next-human-actions packet and verifier that converts the post-JSS route state into bounded manual actions without claiming upload, forum posting, HotCRP submission, external feedback, or route completion.
- Rebuilt the local ICSE video candidate without fixed test-count claims and added an agent-readable rebuild entrypoint plus verifier coverage for stale video count text.
- Added a pending human video-review packet and verifier that binds the next human action to the current local ICSE video candidate without approving, uploading, or submitting it.
- Added a YouTube upload preflight packet and verifier that confirms local upload inputs while keeping upload blocked until human video approval.

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
