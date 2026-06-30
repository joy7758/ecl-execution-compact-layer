# ECL Publication Risk Final Report

## Scope

```text
object_type=ecl_publication_risk_final_report
version=0.1
date_checked=2026-06-30
status=superseded_by_actual_jss_prescreen_decision
system_changes=false
new_features=false
joss_submission_performed=false
jss_submission_performed=true
jss_manuscript_number=JSSOFTWARE-D-26-01460
jss_decision=prescreen_reject
jss_rejected_and_closed=true
arxiv_submission_performed=false
doi_minted=true
zenodo_version_doi=10.5281/zenodo.21003766
```

This report is now a historical risk snapshot plus current route correction. The JSS risk estimate resolved as an actual pre-screen rejection before reviewer assignment. The current primary route is `zenodo_doi_plus_icse_tool_demo_feedback_route`; the old `arxiv_plus_jss` route is not active.

## Current Route

```text
primary_route=zenodo_doi_plus_icse_tool_demo_feedback_route
previous_primary_route=arxiv_plus_jss
jss_expansion=The Journal of Systems and Software
jss_current_state=prescreen_reject_rejected_and_closed
arxiv_current_state=endorsement_blocked_not_submitted
zenodo_current_state=published_doi_archive
joss_route_deprioritized=true
jss_public_history_gate_required_for_jss=false
```

## JSS Outcome

```text
jss_editorial_screening_outcome=reject
jss_sent_to_reviewers=false
jss_external_reviewer_reports=false
jss_revision_invited=false
jss_acceptance=false
```

Reason recorded from the decision email: the paper was judged not quite ready for publication in a leading journal, and the editor recommended feedback via workshops and/or conferences before submitting to JSS.

## JOSS Historical Risk

```text
immediate_joss_pre_review_pass_probability=very_low
immediate_joss_acceptance_probability=very_low
post_public_history_maturation_probability=moderate_if_external_use_or_research_impact_is_added
```

Reason: the software, paper, license, tests, documentation, and reproducibility surfaces are strong, but the current JOSS gate still records:

```text
public_history_gate_status=fail_current_state
external_impact_signal_ready=false
```

The engineering process statement mitigates a reviewer narrative concern. It does not satisfy the public-history gate.

## Top 5 JSS Prescreen Risk Factors Now Confirmed

1. `evaluation_scope`: The trace corpus is synthetic and local.
2. `comparison_depth`: Reviewers may ask for deeper comparison with tracing and observability systems.
3. `novelty_scope`: Reviewers may ask whether this is an IR contribution or adapter packaging.
4. `external_validity`: Only OpenAI-style and LangChain-style traces are evaluated.
5. `research_impact`: External research use or independent citation evidence is not verified.

## Top JOSS Reviewer Objections If Route Reopens

1. `public_history`: The repository does not yet show six months of public development history.
2. `research_impact`: External research use or independent citation evidence is not verified.
3. `synthetic_evaluation`: The trace corpus is synthetic and local.
4. `scope_vs_frameworks`: Reviewers may ask why ECL is software rather than documentation around adapters.
5. `maintenance_signal`: A single-author, newly public artifact may raise sustainability questions.

## arXiv Rejection Risk Factors

```text
arxiv_moderation_risk=moderate
arxiv_reviewer_risk=not_applicable_preprint_not_peer_review
```

Primary risks:

- category mismatch;
- perceived lack of scholarly novelty;
- manuscript reading as project documentation rather than a research paper;
- insufficient standalone explanation of evaluation limits;
- overclaiming if boundary statements are removed.

## Most Fragile Claims

- ECL as a cross-runtime execution IR: fragile if framed as a broad standard rather than a minimal local representation.
- Replayability: valid for deterministic local artifacts, not external side-effect verification.
- Loss-aware mapping: demonstrated on OpenAI-style and LangChain-style traces only.
- MCP surface: only a local tool-shaped stub, not protocol conformance.
- Publication readiness: content-ready does not mean submitted, accepted, DOI-minted, or externally adopted.

## Recommended Final Submission Timing

```text
arxiv_submission_timing=blocked_until_endorsement_or_alternative_preprint_route
jss_submission_timing=not_recommended_until_workshop_or_conference_feedback
joss_submission_timing=not_recommended_unless_route_reopens
joss_safe_reassessment_date=2026-12-29
```

Recommended path:

1. Use the Zenodo DOI as the stable public software archive.
2. Continue ICSE 2027 Tool Demonstration and Data Showcase preparation.
3. Collect real external feedback through GitHub issues, tool-demo review, and public forum posts if manually performed.
4. Reassess JSS/JOSS only after observable public maintenance history and external feedback evidence exist.

## Sources Checked

- JOSS submitting guide: https://joss.readthedocs.io/en/latest/submitting.html
- JOSS review checklist/editorial guidance: https://joss.readthedocs.io/en/latest/review_checklist.html
- Journal of Systems and Software guide for authors: https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors
- arXiv moderation guidance: https://info.arxiv.org/help/moderation/index.html
- arXiv short-works policy: https://blog.arxiv.org/2019/06/21/policy-on-short-works/
