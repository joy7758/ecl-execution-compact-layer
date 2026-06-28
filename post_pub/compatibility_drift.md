# ECL Compatibility Drift Model v0.1

Status: post-publication observation model

Scope: This document defines semantic drift after ECL v0.1 publication. It is documentation only. It does not add code, runtime hooks, telemetry, monitoring, or enforcement logic.

## 1. Semantic Drift

Semantic drift occurs when an external use of ECL preserves ECL-like names or structure but changes execution meaning, validation meaning, replay behavior, loss reporting, or compatibility interpretation.

Drift is measured against the ECL v0.1 reference model, not against popularity, implementation style, or repository activity.

## 2. Causes

External adaptation:

An external system adapts ECL to local runtime assumptions and changes field interpretation, adapter boundaries, or loss reporting rules.

Partial implementation:

An external system implements only part of ECL and omits required validation, replay, evidence, hash, or loss-aware behavior.

Runtime deviation:

An external runtime adds hidden state, nondeterministic behavior, external API calls, mutable execution context, or non-stable artifact generation.

## 3. Drift Detection Signals

Schema mismatch:

The external object adds, removes, renames, or reinterprets frozen ECL fields in a way that changes v0.1 meaning.

Loss model deviation:

The external adapter omits loss reporting, changes loss categories, hides lost fields, or reports incomplete mapping as full fidelity.

Replay inconsistency:

The same input, schema, adapter, validator, and generation parameters do not produce identical replay artifacts or artifact hashes.

## 4. Observation Boundary

This model identifies drift signals only.

It does not claim:

- automated drift detection
- external runtime enforcement
- official certification
- standard authority
- backward compatibility for forked semantics

