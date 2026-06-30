# ECL JOSS Six-Month Readiness Plan

Status: post_jss_rejection_maturation_plan

Start date: 2026-06-30

Current JSS state: `JSSOFTWARE-D-26-01460` prescreen reject / rejected and closed

## Purpose

Build observable engineering maturity before any future JOSS resubmission. This plan does not claim current JOSS readiness.

## Month 1: Public Artifact Stabilization

Target maintenance release: `v0.1.1`

- Keep Zenodo DOI and GitHub Release links visible.
- Maintain `make demo` as the reviewer entrypoint.
- Record issue templates and contribution rules.
- Fix documentation errors without changing v0.1 semantics.

## Month 2: User-Readable Workflow

Target maintenance release: `v0.1.2`

- Improve one-command demo clarity.
- Add screenshots or terminal transcript if needed.
- Keep examples deterministic and offline.
- Avoid adding unsupported runtime claims.

## Month 3: Feedback Collection

Target maintenance release: `v0.1.3`

- Seek workshop, tool-demo, or repository issue feedback.
- Record external comments as comments or issues only when they really exist.
- Do not convert casual mentions into adoption claims.

## Month 4: Evaluation Hardening

Target maintenance release: `v0.1.4`

- Expand local fixtures only if they are reproducible and license-safe.
- Keep production trace claims blocked unless real public traces are available.
- Track deterministic hashes after each release.

## Month 5: Maintenance Release Candidate

Target maintenance release: `v0.1.5`

- Prepare a maintenance release if defects are found.
- Record schema migration only if schema changes.
- Keep v0.1 DOI immutable; use a new version for payload changes.

## Month 6: Resubmission Gate

Target maintenance release: `v0.1.6`

Before any JOSS resubmission, verify:

- public issue / maintenance history exists;
- `make demo` passes from a clean checkout;
- documentation matches current behavior;
- citation metadata is current;
- no unsupported adoption, production, or standardization claims are present.

## Evidence Ledgers

- Maintenance evidence ledger: `post_pub/MAINTENANCE_EVIDENCE_LEDGER_v0_1.md`
- Maintenance release template: `post_pub/RELEASE_MAINTENANCE_TEMPLATE_v0_1.md`
- Feedback intake protocol: `post_pub/FEEDBACK_INTAKE_PROTOCOL_v0_1.md`

## Boundary

This is a readiness plan, not a JOSS acceptance signal, revision invitation, community adoption record, or peer-reviewed result.
