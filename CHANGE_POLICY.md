# ECL v0.1 Change Policy

Status: local semantic freeze policy

Scope: This policy controls schema evolution and semantic drift for the ECL v0.1 local semantic freeze. It is not a public governance process, standards process, or release process.

## 1. Version Meaning

ECL uses an ECL-specific version policy, not generic semantic versioning.

Version shape:

`MAJOR.MINOR.PATCH[-stage]`

For v0.1, the frozen schema version is:

`0.1.0-draft`

Meaning:

- `0`: pre-standard, local candidate maturity
- `1`: first frozen semantic profile
- `0`: no patch-level compatibility fix applied
- `draft`: no public standard claim

## 2. Freeze Level

The current freeze is:

`Level 0 - Local Semantic Freeze`

Level definitions:

| Level | Name | Meaning |
| --- | --- | --- |
| 0 | Local Semantic Freeze | Internal reproducibility only. No external claims. |
| 1 | Executable Prototype | Runnable adapters and replayable traces. Still non-standard. |
| 2 | External Integration Candidate | Multiple runtime integrations and published reproducibility package. Still not a standard. |
| 3 | Standard Candidate | Community adoption, cross-project dependency, and explicit governance process. |

The current repository is at the Level 0 to Level 1 transition boundary.

## 3. Breaking Change Definition

A change is breaking when it changes how an ECL v0.1 record is interpreted, hashed, validated, replayed, or migrated.

Breaking changes include:

- adding a required top-level field
- removing a required top-level field
- renaming any frozen field
- changing the meaning of any frozen field
- changing `schema_version`
- changing `object_type`
- changing canonical JSON rules
- changing hash algorithm
- changing canonical ECL hash blanking behavior
- changing source trace hash behavior
- changing event chain behavior
- changing checkpoint state hash behavior
- changing replay invariants
- changing protocol boundary rules
- changing validation from structural validation into external authority

Breaking changes MUST NOT be applied inside the v0.1 local freeze snapshot.

## 4. Non-Breaking Change Definition

A change is non-breaking only when it preserves v0.1 interpretation, hash behavior, validation behavior, replay behavior, and migration behavior.

Allowed non-breaking changes outside the frozen snapshot include:

- adding explanatory documentation that does not redefine semantics
- adding examples that validate against the frozen schema
- adding tests that confirm existing invariants
- improving error messages without changing pass or fail semantics
- adding optional metadata only when it is already allowed by the frozen schema

Non-breaking does not mean risk-free. Every non-breaking change SHOULD include a validator run and artifact hash comparison when it touches execution code.

## 5. Compatibility Boundary

An ECL v0.1 consumer MAY rely on:

- the schema path named in `SPEC.md`
- required object model fields
- canonicalization value
- hash algorithm value
- canonical hash blanking rule
- source trace hash match rule
- event chain shape
- checkpoint state hash verification
- replay invariants

An ECL v0.1 consumer MUST NOT rely on:

- undocumented source trace fields
- adapter implementation internals
- filesystem layout outside declared artifact paths
- external protocol acceptance
- public release state
- benchmark authority
- production recovery behavior

## 6. Migration Rule

Migration is allowed only as transform.

Allowed:

- read a valid v0.1 object
- produce a new object under a new schema version
- record source hash, migration tool hash, and decision log
- preserve the original v0.1 artifact unchanged

Forbidden:

- reinterpret a v0.1 field in place
- silently change a field meaning
- mutate a frozen v0.1 snapshot and keep the same version
- claim that a migrated object is still byte-equivalent to the original

Rule:

`transform, do not reinterpret`

## 7. Snapshot Immutability

`release/v0.1-local-freeze/` is an execution snapshot artifact.

After freeze creation, files inside that directory SHOULD be treated as immutable evidence. Corrections require a new freeze directory or a clearly marked repair snapshot. Do not overwrite a frozen artifact while preserving the same freeze identity.

## 8. Claim Boundary

The following statements are forbidden for v0.1 local freeze:

- ECL is a public standard
- ECL has external standard acceptance
- ECL has ecosystem adoption
- ECL is a production audit control plane
- ECL benchmark results are leaderboard results
- ECL adapter demos prove external runtime conformance

Allowed statement:

`ECL v0.1 is a local semantic freeze candidate for a minimal deterministic execution IR and replayable artifact surface.`

