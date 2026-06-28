# ECL Fork Analysis Model v0.1

Status: post-publication observation model

Scope: This document classifies external forks of ECL v0.1. It is documentation only. It does not implement monitoring, enforcement, repository scanning, or compatibility tooling.

## 1. Structural Fork

Definition:

A structural fork changes repository layout, packaging, documentation organization, examples, or distribution shape while preserving ECL semantics.

Example:

An external project keeps `state`, `intent`, `action`, and `evidence` unchanged but moves the SDK into a different package layout.

Risk level:

Low, if schema interpretation, validation, replay, hash behavior, and loss reporting remain unchanged.

## 2. Semantic Fork

Definition:

A semantic fork changes the meaning of an ECL field, adapter mapping, loss report, compatibility rule, or execution boundary.

Example:

An external project maps `reasoning` into `evidence` instead of `intent`, or treats `loss_report` as optional where an adapter contract requires it.

Risk level:

High, because two records may share ECL-like field names while no longer expressing the same execution semantics.

## 3. Execution Fork

Definition:

An execution fork changes deterministic replay, validation, canonicalization, artifact hashing, or evidence generation behavior.

Example:

An external project adds runtime timestamps, stochastic replay behavior, external API calls, or hidden mutable state to ECL replay.

Risk level:

Critical, because replay equivalence and artifact hash stability can no longer be assumed.

## 4. Classification Boundary

Fork classification is observational.

It does not claim:

- external misuse
- conformance failure
- legal interpretation
- official compatibility status
- governance authority over forked repositories

