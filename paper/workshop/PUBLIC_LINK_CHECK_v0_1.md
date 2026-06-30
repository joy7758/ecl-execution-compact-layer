# ECL ICSE Public Link Check v0.1

Status: public_links_verified

Date checked: 2026-06-30

## Method

```bash
curl -L -sS -o /dev/null -w 'http_code=%{http_code}\nfinal_url=%{url_effective}\n' <url>
```

## Verified Links

| Link | HTTP | Final URL | Status |
| --- | ---: | --- | --- |
| ICSE 2027 Tool Demonstration and Data Showcase | 200 | `https://conf.researchr.org/track/icse-2027/icse-2027-demonstrations` | reachable |
| ECL repository | 200 | `https://github.com/joy7758/ecl-execution-compact-layer` | reachable |
| ECL GitHub release `v0.1` | 200 | `https://github.com/joy7758/ecl-execution-compact-layer/releases/tag/v0.1` | reachable |
| ECL Zenodo record | 200 | `https://zenodo.org/records/21003766` | reachable |
| ECL version DOI | 200 | `https://zenodo.org/records/21003766` | reachable |
| ICSE tool-demo tracking issue | 200 | `https://github.com/joy7758/ecl-execution-compact-layer/issues/7` | reachable |
| Public feedback request issue | 200 | `https://github.com/joy7758/ecl-execution-compact-layer/issues/8` | reachable |

## Official ICSE Facts Observed

- Track: ICSE 2027 Tool Demonstration and Data Showcase.
- Submission deadline: Friday 23-Oct-2026 AoE.
- Acceptance notification: Friday 11-Dec-2026 AoE.
- Camera ready: Wednesday 20-Jan-2027 AoE.
- Submission site: `https://icse27demos.hotcrp.com/`.
- Paper format: IEEE conference proceedings formatting, with LaTeX class options `\documentclass[10pt,conference]{IEEEtran}`.
- Page limit: not more than four pages for the main text, inclusive of references, figures, tables, appendices, and similar material.
- Video requirement: a short video between three and five minutes, online at submission time, with YouTube required during review.
- Tool distribution requirement: tool authors must distribute the tool in an easy-to-use form; reviewers should not have to build code.

## Boundary

This file records public-link and official-page verification only. It does not claim ICSE submission, video publication, ICSE acceptance, external adoption, production deployment, benchmark superiority, or peer-review validation.
