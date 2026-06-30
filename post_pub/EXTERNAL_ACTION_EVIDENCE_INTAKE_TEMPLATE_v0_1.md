# ECL External Action Evidence Intake Template v0.1

Status: template_pending_external_evidence

Date checked: 2026-06-30

## Purpose

This template is the bounded intake surface for future human-provided external URLs and evidence. It is intentionally empty at v0.1 because no YouTube upload, forum post, HotCRP submission, or third-party feedback has been recorded yet.

## How To Use

When an external action is performed by a human, copy the JSON template and fill only the matching evidence slot:

- `youtube_video` after the final demo video is uploaded.
- `langchain_forum_post` after a public LangChain Forum post exists.
- `mcp_discussion_post` after a public MCP GitHub Discussion exists.
- `hotcrp_submission` after a HotCRP submission confirmation exists.
- `third_party_feedback` after an attributable third party reports feedback or reproduction results.

Then run:

```bash
python3 scripts/validate_external_action_evidence_intake.py <filled-intake-json>
```

## Required Evidence Fields

```text
evidence_id=
external_action_id=
evidence_kind=
source_url=
evidence_date=
recorded_by=
claim_boundary=
```

## Current Empty-State Boundary

```text
youtube_upload_performed=false
forum_posts_published=false
hotcrp_submission_performed=false
external_feedback_recorded=false
external_reproduction_recorded=false
external_adoption_claim=false
peer_review_claim=false
joss_readiness_claim=false
```

## Boundary

This template is not an external action, not evidence that an action occurred, not a YouTube upload, not a forum post, not a HotCRP submission, not third-party feedback, not external adoption, and not peer review.
