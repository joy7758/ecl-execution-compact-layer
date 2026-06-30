# ECL ICSE 2027 Video Human Review Packet v0.1

Status: pending_human_review_not_approved

Date checked: 2026-06-30

## Purpose

This packet is the bounded human-review surface for the local ICSE demo video candidate. It lets the human operator approve or reject the local candidate without implying that upload, HotCRP submission, external feedback, or peer review has occurred.

## Candidate Under Review

```text
video=paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.mp4
video_sha256=f349243a08f7230717e413ab7b19441c42a81b9a5addb08beacc23cedf59957a
caption=paper/workshop/video/ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.srt
caption_sha256=5e96ebcb1d7c07ac140d329fa664b9b88144dedb5017aafb9a9f5c9c7bdf929e
duration_seconds=239.160000
duration_human=3m59s
qa_report=paper/workshop/video/VIDEO_QA_REPORT_v0_1.md
asset_manifest=paper/workshop/video/VIDEO_ASSET_MANIFEST_v0_1.json
youtube_handoff=paper/workshop/YOUTUBE_UPLOAD_HANDOFF_v0_1.md
```

## Human Review Checklist

- Confirm the video opens and plays through locally.
- Confirm the voiceover is understandable enough for review use.
- Confirm the slides are readable at 720p.
- Confirm captions are bounded inside the video duration.
- Confirm the video states the Zenodo DOI as a software archive, not peer-review acceptance.
- Confirm the video does not claim external adoption, production deployment, benchmark superiority, public standard status, ICSE submission, or ICSE acceptance.
- Confirm the video avoids fixed test-count claims; current counts are left to live verifiers.
- Confirm the final video is suitable for unlisted YouTube upload during review.

## Decision Slots

```text
review_decision=pending
approved_for_youtube_upload=false
reviewed_by=<fill only after human review>
reviewed_at=<fill only after human review>
replacement_required=<fill only after human review>
notes=<fill only after human review>
```

## If Approved

Use `paper/workshop/YOUTUBE_UPLOAD_HANDOFF_v0_1.md` and upload the approved MP4 as an unlisted review video. Record the final YouTube URL through `post_pub/EXTERNAL_ACTION_EVIDENCE_INTAKE_TEMPLATE_v0_1.json`.

## If Rejected

Rebuild the candidate with:

```bash
python3 scripts/build_icse_video_candidate.py
python3 scripts/verify_video_human_review_packet.py
python3 scripts/verify_icse_tool_demo_package.py
```

Then repeat human review.

## Boundary

This packet is not a human approval, YouTube upload, HotCRP submission, external feedback record, external adoption signal, peer-review result, ICSE acceptance, JOSS readiness claim, or route completion proof.
