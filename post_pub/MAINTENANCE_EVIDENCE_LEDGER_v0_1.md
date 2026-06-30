# ECL Maintenance Evidence Ledger v0.1

Status: initialized_no_external_feedback_recorded

Start date: 2026-06-30

## Purpose

This ledger records real maintenance signals for the six-month JOSS maturation route. It must not be used to fabricate public history, external users, citations, or adoption.

## Evidence Rules

- Record only real issues, commits, release notes, tests, documentation updates, and external feedback.
- Do not treat stars, forks, or casual mentions alone as adoption.
- Do not backdate entries.
- Do not mark JOSS-ready until the public-history window has actually elapsed and the JOSS gate passes.

## Current Baseline

```text
repository=https://github.com/joy7758/ecl-execution-compact-layer
zenodo_record=https://zenodo.org/records/21003766
version_doi=10.5281/zenodo.21003766
current_jss_state=JSSOFTWARE-D-26-01460 prescreen_reject rejected_and_closed
make_demo_verified=true
docker_demo_verified=true
external_feedback_recorded=false
public_maintenance_issues_created=true
public_feedback_request_issue_opened=true
```

## Maintenance Entries

| Date | Version/Commit | Evidence Type | Evidence | Status |
| --- | --- | --- | --- | --- |
| 2026-06-30 | `v0.1` / `1f22308026a66ebd7a762d5dac6111802f890fef` | public archive + demo baseline | Zenodo DOI, GitHub Release, `make demo` | baseline_recorded |
| 2026-06-30 | `443e73e68879e06ca3280cc08e02f53e3c8d783e` | public maintenance issue bootstrap | GitHub issues [#1](https://github.com/joy7758/ecl-execution-compact-layer/issues/1)-[#6](https://github.com/joy7758/ecl-execution-compact-layer/issues/6), labels `maintenance` and `joss-maturation` | maintainer_planning_issues_recorded |
| 2026-06-30 | `6dc23a92ed9d034076e147e7c0368e694d40ef6d` | ICSE tool-demo tracking issue | GitHub issue [#7](https://github.com/joy7758/ecl-execution-compact-layer/issues/7), label `tool-demo` | maintainer_tool_demo_tracking_recorded |
| 2026-06-30 | `2234fb6b7f8f854511605d2e782c43ebb7750bfa` | public feedback request issue | GitHub issue [#8](https://github.com/joy7758/ecl-execution-compact-layer/issues/8), labels `feedback` and `reproducibility` | maintainer_feedback_request_recorded |
| 2026-06-30 | `632d6441e09ffcd96ff707f816c588c8450d87bd` | Docker reviewer demo verification | `docker build -t ecl-demo .` and `docker run --rm ecl-demo`, image `sha256:740cc621c668a1608f9f897c0d53662a825cf706a42017d2b8f06c4038b29c3f` | docker_demo_verified |
| 2026-06-30 | `9b2d8a4134a2523a4434c7d0b217b932a2ff5728` | ICSE tool-demo PDF and link verification | IEEEtran PDF `sha256:7633104c76f499b6e3447da47c1e860f652782b870e1e98cef0e9d8e2ff2558e`, public link check all reachable | tool_demo_pdf_links_verified |
| 2026-06-30 | `ba7b4ae468d99096b049e30312fa84cc1b7613aa` | ICSE local video candidate | 3m45s MP4 `sha256:a9b1d130da66a38e408d5d51655678750354c62753ac7d7d33891dddec7927aa`, YouTube metadata draft, HotCRP field draft | local_video_candidate_generated |
| 2026-06-30 | `29d29912e634414a3aa4410821df1eb2b75ea0c3` | ICSE local video candidate timing repair and upload handoff | Rebuilt MP4 with aligned video/audio stream duration and bounded captions; new MP4 `sha256:70c31bc62f9c8855b0fa82c8bcef1092c260b9e3e65116d233af9355335f4e35`; YouTube upload still not performed | local_video_candidate_qa_repaired |
| 2026-06-30 | `7b93eb36256b95ba4786cd55291e7672932d9a80` | feedback issue expected-hash sync | Updated public feedback issue #8 and local dissemination surfaces to current `make demo` hashes: dependency `sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3`, external recognition `sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441` | feedback_issue_hashes_synced |
| 2026-06-30 | `a48937a6fe72b904f477403d566d8a3647a0cd73` | external forum posting handoff | Prepared LangChain Forum and MCP Discussions handoff copy with current `make demo` hashes and explicit not-posted boundaries | forum_posting_handoff_prepared |
| 2026-06-30 | `91bd0cce27039a5dd7424ad7f96a7f94ff839f68` | external action queue | Queued human-executed YouTube upload, forum posting, HotCRP submission, external feedback recording, and monthly maintenance steps with explicit evidence requirements | external_action_queue_initialized |
| 2026-06-30 | pending commit | external action queue test gate | Added unit tests for queue order, boundary flags, referenced packets, artifact hashes, and agent-index exposure | external_action_queue_test_gate_added |

## External Feedback Entries

No external reviewer/user feedback is recorded yet.

## Boundary

This ledger initializes the maintenance evidence structure. It is not proof of six months of public history, external adoption, independent validation, or JOSS readiness.
