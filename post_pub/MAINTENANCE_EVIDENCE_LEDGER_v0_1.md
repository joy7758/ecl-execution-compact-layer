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
docker_demo_verified=false
external_feedback_recorded=false
public_maintenance_issues_created=true
```

## Maintenance Entries

| Date | Version/Commit | Evidence Type | Evidence | Status |
| --- | --- | --- | --- | --- |
| 2026-06-30 | `v0.1` / `1f22308026a66ebd7a762d5dac6111802f890fef` | public archive + demo baseline | Zenodo DOI, GitHub Release, `make demo` | baseline_recorded |
| 2026-06-30 | `443e73e68879e06ca3280cc08e02f53e3c8d783e` | public maintenance issue bootstrap | GitHub issues [#1](https://github.com/joy7758/ecl-execution-compact-layer/issues/1)-[#6](https://github.com/joy7758/ecl-execution-compact-layer/issues/6), labels `maintenance` and `joss-maturation` | maintainer_planning_issues_recorded |
| 2026-06-30 | `6dc23a92ed9d034076e147e7c0368e694d40ef6d` | ICSE tool-demo tracking issue | GitHub issue [#7](https://github.com/joy7758/ecl-execution-compact-layer/issues/7), label `tool-demo` | maintainer_tool_demo_tracking_recorded |

## External Feedback Entries

No external reviewer/user feedback is recorded yet.

## Boundary

This ledger initializes the maintenance evidence structure. It is not proof of six months of public history, external adoption, independent validation, or JOSS readiness.
