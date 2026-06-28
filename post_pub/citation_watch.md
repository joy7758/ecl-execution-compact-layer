# ECL Citation Watch Model v0.1

Status: post-publication observation model

Scope: This document defines citation signals for the published ECL v0.1 artifact. It is documentation only. It does not implement telemetry, monitoring, repository scanning, or citation indexing.

## 1. Citation Signal

A citation signal is an external, attributable reference that uses ECL as a scientific, engineering, or implementation dependency surface.

A valid citation signal MUST identify at least one of:

- the ECL repository
- the ECL v0.1 release
- the ECL paper or specification
- the ECL object model
- an ECL implementation surface such as SDK, adapter, replay, or dependency API

The signal MUST be externally attributable. Local notes, private drafts, and unpublished internal references do not count.

## 2. Non-Signals

The following do NOT count as citation signals by themselves:

- GitHub stars
- GitHub forks
- social mentions without reference details
- unlinked name mentions
- private bookmarks
- automated package mirrors
- crawler or indexer references

A star, fork, or mention MAY become supporting evidence only when paired with an attributable citation type listed below.

## 3. Citation Types

| Type | Definition | Minimum evidence |
| --- | --- | --- |
| Academic citation | A paper, preprint, thesis, technical report, or formal bibliography entry cites ECL. | Public document URL or DOI plus cited ECL target. |
| Repository dependency | An external repository imports, vendors, or declares ECL as a dependency. | Public repository URL plus dependency reference. |
| Specification reference | An external specification, design note, issue, ADR, or protocol document references ECL semantics. | Public document URL plus referenced ECL section or release. |
| Implementation reuse | External code reuses ECL object shape, adapter rules, replay behavior, or dependency interface. | Public code URL plus reused ECL surface. |

## 4. Observation Boundary

This model records citation evidence only.

It does not claim:

- external validation
- standard adoption
- runtime conformance
- implementation correctness
- ecosystem dependency

