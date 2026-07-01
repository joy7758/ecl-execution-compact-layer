# ECL ICSE 2027 YouTube Upload Preflight v0.1

Status: preflight_inputs_ready_blocked_until_video_review_approved

Date checked: 2026-07-01

## Purpose

This packet verifies that the local YouTube upload inputs are complete and hash-bound before any external upload occurs. It does not approve the video, upload the video, create a YouTube URL, update HotCRP, or record external feedback.

## Input Files

```text
video=paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.mp4
video_sha256=f349243a08f7230717e413ab7b19441c42a81b9a5addb08beacc23cedf59957a
caption=paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.srt
caption_sha256=5e96ebcb1d7c07ac140d329fa664b9b88144dedb5017aafb9a9f5c9c7bdf929e
thumbnail=paper/workshop/video/video_thumbnail.png
metadata=paper/workshop/YOUTUBE_METADATA_DRAFT_v0_1.md
upload_handoff=paper/workshop/YOUTUBE_UPLOAD_HANDOFF_v0_1.md
video_review_packet=paper/workshop/video/VIDEO_HUMAN_REVIEW_PACKET_v0_1.json
```

## Upload Metadata

```text
title=ECL v0.1: Deterministic Replay for Agent Runtime Traces
visibility=unlisted during review
audience=not made for kids
captions=upload SRT caption file
thumbnail=upload local thumbnail if YouTube accepts it
```

## Current Gate

```text
video_review_status=pending_human_review_not_approved
approved_for_youtube_upload=false
youtube_upload_performed=false
youtube_url=null
```

The upload must not be performed until the human review packet is updated with a real approval decision.

## Post-Upload Recording Rule

After a real YouTube URL exists, record it by filling only the `youtube_video` slot in a copy of:

```text
post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json
```

Then run:

```bash
python3 scripts/validate_external_action_evidence_intake.py <filled-intake-json>
```

## Boundary

This preflight packet is not human approval, YouTube upload, public video availability, HotCRP submission, external feedback, peer review, ICSE acceptance, JOSS readiness, or route completion.
