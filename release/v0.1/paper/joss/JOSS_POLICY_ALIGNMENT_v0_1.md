# ECL JOSS Policy Alignment v0.1

Status: local_policy_alignment

Date checked: 2026-06-28

Scope: This file maps the ECL v0.1 submission package to JOSS readiness concerns. It does not submit to JOSS, predict acceptance, or claim third-party adoption.

## JOSS-Facing Gates

| Gate | ECL Evidence | Status |
| --- | --- | --- |
| Software availability | Public GitHub repository and release package are present. | pass |
| Open-source license | MIT license is present. | pass |
| Installation and usage surface | README, SDK examples, MCP-shaped local stub, and reproducibility demos are present. | pass |
| Tests and reproducibility | `python3 -m unittest discover -s tests` plus deterministic experiment scripts are present. | pass |
| Paper structure | Standard JOSS paper mirror exists at `paper/paper.md` and `paper/paper.bib`. | pass |
| Statement of need | `paper/paper.md` includes a statement of need. | pass |
| Research impact statement | `paper/paper.md` includes a scoped research impact statement backed by local reproducibility experiments. | pass |
| Public development history | Current local git history is concentrated on 2026-06-28. | fail_current_state |

## Advisory Signals

| Signal | Meaning | Current Status |
| --- | --- | --- |
| External citation | Independent citation of ECL outside this repository. | unverified |
| Repository dependency | Another repository depending on ECL. | unverified |
| Independent user report | Third-party research use or issue report. | unverified |
| Production deployment | Operational use outside local examples. | unverified |

## Boundary

```text
external_impact_is_required_gate=false
external_impact_is_advisory_signal=true
research_impact_gate_uses_local_reproducibility_evidence=true
third_party_validation=false
joss_submission_performed=false
```

## Sources

- https://joss.readthedocs.io/en/latest/submitting.html
- https://joss.readthedocs.io/en/latest/review_criteria.html
- https://joss.readthedocs.io/en/latest/paper.html
