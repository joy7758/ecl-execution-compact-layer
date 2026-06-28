# ECL No-Paid-Journal Venue Screening v0.1

Status: screening_complete_no_submission_performed

Date checked: 2026-06-28

Scope: This screening identifies venues for the ECL paper while excluding paid-journal routes. It does not perform submission and does not claim acceptance, publication, or external validation.

## Screening Rule

Allowed:

- Diamond/no-fee journals or software-paper venues with no author-facing APC.
- Hybrid/subscription journals only when the non-open-access route does not require an author publication charge.
- Conferences and workshops as non-journal alternatives, with the caveat that accepted papers may require registration.
- Preprint or artifact archive routes as non-journal dissemination, not as peer-reviewed publication.

Excluded:

- Mandatory APC journals.
- Fully open-access paid journals.
- Optional paid Open Access routes when a no-fee subscription route exists.
- Venues whose fit depends on claims not supported by current local evidence.

## Recommended Route

### 1. Journal of Open Source Software (JOSS)

Classification: `eligible_zero_fee`

Fit: Strongest no-fee software-paper candidate if ECL is prepared as a public, installable, tested research software artifact.

Why it fits:

- ECL is a reproducible software artifact with tests, fixtures, deterministic replay, and a minimal API.
- JOSS is designed for short software papers rather than long theory papers.
- This avoids paid-journal routes.

Current readiness:

- Manuscript body exists, but a JOSS-specific short paper and public repository packaging still need final human metadata and release decisions.

Source evidence:

- JOSS site: https://joss.theoj.org/
- JOSS author documentation: https://joss.readthedocs.io/en/latest/submitting.html

### 2. Journal of Systems and Software (JSS)

Classification: `eligible_non_oa_route_only`

Fit: Strong software engineering system-paper target after strengthening evaluation beyond local fixtures.

Why it fits:

- ECL is a software engineering infrastructure artifact.
- The paper already has problem statement, method, system design, evaluation, and limitations.

Constraint:

- Use only a non-open-access/subscription route if available and confirm no author-side fee at submission time.
- Do not select an Open Access APC route.

Source evidence:

- Journal page: https://www.sciencedirect.com/journal/journal-of-systems-and-software
- Elsevier author publishing options: https://www.elsevier.com/researcher/author/publishing-options

### 3. Empirical Software Engineering (EMSE)

Classification: `eligible_non_oa_route_only`

Fit: Conditional. Better after expanding evaluation into an empirical study with multiple traces, failure cases, ablations, and reproducibility analysis.

Why it fits:

- EMSE can fit if ECL is framed as empirical evaluation of cross-runtime execution trace normalization.

Constraint:

- Current local fixture evaluation is too small for a strong empirical software engineering journal submission.
- Use only the no-fee/non-OA route if available; do not choose paid Open Access.

Source evidence:

- Journal page: https://link.springer.com/journal/10664
- Springer Open Choice information: https://www.springer.com/gp/open-access/springer-open-choice

### 4. Software and Systems Modeling (SoSyM)

Classification: `eligible_non_oa_route_only`

Fit: Conditional. Better if the paper emphasizes the formal execution model, IR semantics, determinism invariants, and model-to-runtime mapping.

Why it fits:

- ECL has a formal object model, replay invariants, and boundary rules.

Constraint:

- The current draft needs stronger formalization before this becomes the best target.
- Use only the no-fee/non-OA route if available; do not choose paid Open Access.

Source evidence:

- Journal page: https://link.springer.com/journal/10270
- Springer Open Choice information: https://www.springer.com/gp/open-access/springer-open-choice

## Non-Journal Dissemination Options

### arXiv

Classification: `preprint_not_journal`

Fit: Useful for timestamped visibility after the author confirms metadata and public release wording.

Boundary:

- arXiv is not peer review and not journal publication.

Source evidence:

- arXiv submission help: https://info.arxiv.org/help/submit/index.html

### Zenodo

Classification: `artifact_archive_not_journal`

Fit: Useful for artifact DOI after release packaging.

Boundary:

- Zenodo DOI is not peer review and not journal acceptance.

Source evidence:

- Zenodo: https://zenodo.org/

## Excluded or Not Recommended Now

### Mandatory or Paid Open Access Journal Routes

Classification: `excluded_paid_route`

Reason: The objective excludes paid journals. Any route requiring an article processing charge is excluded.

### ACM TOSEM

Classification: `exclude_for_now_fee_uncertain_or_apc_risk`

Reason: ACM publication models and institutional arrangements can affect author charges. Do not choose this venue unless a current institution-specific no-fee path is confirmed.

Source evidence:

- ACM Open: https://libraries.acm.org/subscriptions-access/acmopen

### IEEE Access

Classification: `excluded_paid_open_access`

Reason: Fully open-access APC route, not aligned with the no-paid-journal constraint.

Source evidence:

- IEEE Access author information: https://ieeeaccess.ieee.org/guide-for-authors/article-processing-charges/

## Final Recommendation

Primary no-fee route:

```text
JOSS after public software packaging and author metadata confirmation.
```

Primary full-paper route:

```text
Journal of Systems and Software via non-OA/subscription route only, after expanding evaluation.
```

Secondary full-paper route:

```text
EMSE or SoSyM via non-OA/subscription route only, depending on whether the paper is expanded empirically or formally.
```

No paid journal has been selected.

