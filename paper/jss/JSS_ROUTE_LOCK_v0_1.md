# ECL JSS Route Lock v0.1

## Route Decision

```text
primary_publication_route=arxiv_plus_jss
jss_expansion=The Journal of Systems and Software
joss_deprioritized=true
joss_public_history_gate_avoided=true
schema_changes=false
core_modification=false
```

The JOSS package remains in the repository as a historical submission route, but it is no longer the primary target. The current target is:

```text
arXiv preprint -> Journal of Systems and Software submission package
```

## Why JSS

JSS is a better target for ECL because the contribution is a software systems artifact: deterministic execution representation, replay semantics, cross-runtime trace normalization, and reproducible validation. The route does not rely on the JOSS-specific six-month public-history gate.

## Residual Risks

- The evaluation is local and synthetic rather than third-party production evidence.
- The manuscript must avoid claiming standardization or ecosystem adoption.
- JSS reviewers may require a stronger comparison against tracing and observability systems.
- The paper should be submitted as a systems/software engineering contribution, not as a software note.
