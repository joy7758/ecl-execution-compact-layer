# ECL External Action Queue v0.1

Status: external_actions_queued_not_executed

Date checked: 2026-06-30

## Purpose

This queue lists the remaining human-executed external actions for the post-JSS route. It is agent-readable coordination state only. It does not prove that any external action has been performed.

## Current Verified Inputs

```text
repository=https://github.com/joy7758/ecl-execution-compact-layer
zenodo_record=https://zenodo.org/records/21003766
version_doi=10.5281/zenodo.21003766
icse_tracking_issue=https://github.com/joy7758/ecl-execution-compact-layer/issues/7
feedback_issue=https://github.com/joy7758/ecl-execution-compact-layer/issues/8
make_demo_dependency_hash=sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3
make_demo_external_recognition_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
video_candidate=paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.mp4
video_candidate_sha256=70c31bc62f9c8855b0fa82c8bcef1092c260b9e3e65116d233af9355335f4e35
```

## Queue

| Order | Action | Target | Input Packet | Completion Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Human review of local video candidate | local file review | `paper/workshop/video/VIDEO_QA_REPORT_v0_1.md` | human decision to approve or replace candidate | pending_human_review |
| 2 | Upload final demo video | YouTube, unlisted during review | `paper/workshop/YOUTUBE_UPLOAD_HANDOFF_v0_1.md` | final YouTube URL | pending_human_upload |
| 3 | Record YouTube URL in repo | local repository | `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json`, `paper/workshop/HOTCRP_SUBMISSION_DRAFT_v0_1.md`, `paper/workshop/ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json`, `paper/workshop/TOOL_DEMO_SUBMISSION_CHECKLIST.md` | commit containing `youtube_upload_performed=true` and URL | waiting_on_youtube_url |
| 4 | Post feedback request | LangChain Forum | `docs/dissemination/EXTERNAL_FORUM_POSTING_HANDOFF_v0_1.md` | public forum URL | pending_human_post |
| 5 | Post feedback request | MCP GitHub Discussions | `docs/dissemination/EXTERNAL_FORUM_POSTING_HANDOFF_v0_1.md` | public discussion URL | pending_human_post |
| 6 | Record forum URLs in repo | local repository | `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json`, `post_pub/FEEDBACK_REQUEST_STATUS_v0_1.md`, `post_pub/MAINTENANCE_EVIDENCE_LEDGER_v0_1.md` | commit containing forum URLs and still `external_feedback_recorded=false` unless a third party replies | waiting_on_forum_urls |
| 7 | Submit ICSE tool demo | HotCRP `https://icse27demos.hotcrp.com/` | PDF, YouTube URL, HotCRP draft, public repo, DOI | HotCRP submission ID or confirmation page | pending_human_submission |
| 8 | Record ICSE submission evidence | local repository and issue #7 | `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json`, `paper/workshop/ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json`, `post_pub/MAINTENANCE_EVIDENCE_LEDGER_v0_1.md` | commit and public tracking comment | waiting_on_hotcrp_evidence |
| 9 | Record real third-party feedback | GitHub issue, forum reply, or reproducibility report | `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json`, `post_pub/FEEDBACK_INTAKE_PROTOCOL_v0_1.md` | attributable third-party URL and reported command/result | waiting_on_external_response |
| 10 | Continue monthly maintenance | GitHub issues #1-#6 | `post_pub/JOSS_SIX_MONTH_READINESS_PLAN.md` | monthly commits, tests, release notes, and issue updates | ongoing_time_dependent |

## After-Action Update Rules

- Do not mark `youtube_upload_performed=true` until a real YouTube URL exists.
- Do not mark `forum_posts_published=true` until a real public post URL exists.
- Do not mark `external_feedback_recorded=true` until a third party replies with attributable feedback or a reproducibility report.
- Do not mark `icse_submission_performed=true` until a real HotCRP submission confirmation exists.
- Do not mark `joss_readiness_claim=true` until the six-month public-history window has actually elapsed and the JOSS gate passes.
- Validate any filled evidence intake file with `python3 scripts/validate_external_action_evidence_intake.py <filled-intake-json>` before updating status files.

## Boundary

This queue is not a YouTube upload, forum post, HotCRP submission, ICSE acceptance, external feedback record, external adoption signal, peer-review result, or JOSS readiness claim.
