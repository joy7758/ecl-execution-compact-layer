# ECL Next Human Actions Packet v0.1

Status: human_actions_pending_not_executed

Date checked: 2026-06-30

## Purpose

This packet is the current human-execution handoff for the post-JSS route. It turns the verified local state into the next bounded manual actions without claiming that any external action has occurred.

## Current Verified Route State

```text
post_jss_route_verifier=python3 scripts/verify_post_jss_route.py
post_jss_route_status=actionable_local_gates_pass_future_external_steps_open
zenodo_version_doi=10.5281/zenodo.21003766
jss_state=JSSOFTWARE-D-26-01460 prescreen_reject rejected_and_closed
icse_local_package_verified=true
external_action_queue_verified=true
external_action_evidence_intake_empty=true
```

## Human Actions

| Order | Human action | Input packet | Evidence to collect | Verification before recording |
| ---: | --- | --- | --- | --- |
| 1 | Review local ICSE demo video candidate | `paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.md` | human decision: approve or replace | `python3 scripts/verify_video_human_review_packet.py` |
| 2 | Upload approved video to YouTube | `paper/workshop/YOUTUBE_UPLOAD_PREFLIGHT_v0_1.md` | final YouTube URL | do not record until URL exists |
| 3 | Record YouTube URL | `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json` | filled `youtube_video` slot | `python3 scripts/validate_external_action_evidence_intake.py <filled-intake-json>` |
| 4 | Post LangChain feedback request | `docs/dissemination/EXTERNAL_FORUM_POSTING_HANDOFF_v0_1.md` | public LangChain Forum URL | record forum URL only, not feedback |
| 5 | Post MCP feedback request | `docs/dissemination/EXTERNAL_FORUM_POSTING_HANDOFF_v0_1.md` | public MCP Discussion URL | record discussion URL only, not feedback |
| 6 | Submit ICSE tool demo in HotCRP | `paper/workshop/HOTCRP_SUBMISSION_DRAFT_v0_1.md` | HotCRP submission ID or confirmation page | do not record until confirmation exists |
| 7 | Record real third-party feedback | `post_pub/FEEDBACK_INTAKE_PROTOCOL_v0_1.md` | attributable third-party URL and result | validate intake and update ledger only after reply exists |
| 8 | Continue monthly maintenance | `post_pub/JOSS_SIX_MONTH_READINESS_PLAN.md` | issue updates, tests, releases, fixes | do not reassess JOSS before 2026-12-29 |

## Recording Rule

Use this sequence for each external evidence item:

```bash
cp post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json /tmp/ecl-filled-intake.json
# edit only the relevant evidence slot
python3 scripts/validate_external_action_evidence_intake.py /tmp/ecl-filled-intake.json
python3 scripts/verify_post_jss_route.py
```

After validation passes, commit the filled status updates separately and comment on the relevant GitHub tracking issue.

## Boundary

This packet is not a YouTube upload, forum post, HotCRP submission, external feedback record, external adoption signal, peer-review result, ICSE acceptance, JOSS readiness claim, or route completion proof.
