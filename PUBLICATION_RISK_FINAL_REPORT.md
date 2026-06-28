# ECL Publication Risk Final Report

## Scope

```text
object_type=ecl_publication_risk_final_report
version=0.1
date_checked=2026-06-28
system_changes=false
new_features=false
joss_submission_performed=false
jss_submission_performed=false
arxiv_submission_performed=false
doi_minted=false
```

This report estimates submission risk for the frozen ECL v0.1 package. The estimates are qualitative risk bands, not statistical predictions. The current primary route is `arxiv_plus_jss`; the previous JOSS route is deprioritized because of its public-history gate.

## Current Route

```text
primary_route=arxiv_plus_jss
jss_expansion=The Journal of Systems and Software
joss_route_deprioritized=true
jss_public_history_gate_required=false
```

## JSS Acceptance Probability Estimate

```text
immediate_jss_editorial_screening_probability=moderate
jss_major_revision_probability=high
jss_acceptance_without_revision_probability=low
```

Reason: the JSS route does not depend on the JOSS public-history gate, but reviewers are likely to challenge evaluation scope, comparison depth, and the absence of external user evidence.

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

## Top 5 JSS Reviewer Objections

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
arxiv_submission_timing=acceptable_after_human_pdf_and_category_review
jss_submission_timing=acceptable_after_human_metadata_and_file_review
joss_submission_timing=not_recommended_unless_route_reopens
joss_safe_reassessment_date=2026-12-29
```

Recommended path:

1. Submit arXiv only after final PDF/category/human metadata review.
2. Submit JSS only after human portal metadata review and file classification.
3. Treat JSS as the primary journal route because it does not use the JOSS public-history gate.
4. Keep JOSS deprioritized unless the public-history risk is later acceptable or resolved.

## Sources Checked

- JOSS submitting guide: https://joss.readthedocs.io/en/latest/submitting.html
- JOSS review checklist/editorial guidance: https://joss.readthedocs.io/en/latest/review_checklist.html
- Journal of Systems and Software guide for authors: https://www.sciencedirect.com/journal/journal-of-systems-and-software/publish/guide-for-authors
- arXiv moderation guidance: https://info.arxiv.org/help/moderation/index.html
- arXiv short-works policy: https://blog.arxiv.org/2019/06/21/policy-on-short-works/
