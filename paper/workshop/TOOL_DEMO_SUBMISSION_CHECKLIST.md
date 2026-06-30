# ECL ICSE 2027 Tool Demo Submission Checklist

Status: draft_ready_for_human_review

Target: ICSE 2027 Tool Demonstration and Data Showcase

Official track page: https://conf.researchr.org/track/icse-2027/icse-2027-demonstrations

## Checked Facts

- Paper length target: 4 pages plus references.
- Video target: 3-5 minutes.
- Submission deadline shown on the official page: 2026-10-23 AoE.
- Notification shown on the official page: 2026-12-11 AoE.
- Tool should be easy to install and use; reviewers should not need complex manual setup.

## Required Local Materials

- Draft paper: `paper/workshop/ICSE_2027_TOOL_DEMO_DRAFT.md`
- Video script: `paper/workshop/demo_video_script.md`
- Storyboard: `paper/workshop/demo_storyboard.md`
- Demo manifest: `paper/workshop/ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json`
- Terminal transcript: `paper/workshop/demo_terminal_transcript_v0_1.md`
- Docker verification status: `paper/workshop/DOCKER_DEMO_STATUS_v0_1.md`
- One-command demo: `make demo`
- Repository: `https://github.com/joy7758/ecl-execution-compact-layer`
- Software archive DOI: `10.5281/zenodo.21003766`
- Tool-demo tracking issue: `https://github.com/joy7758/ecl-execution-compact-layer/issues/7`

## Pre-Submission Gates

- [x] Run `make demo`.
- [x] Start Docker daemon and rerun `docker build -t ecl-demo . && docker run --rm ecl-demo`.
- [x] Record current test count and output hashes.
- [ ] Render 4-page PDF in required ACM format.
- [ ] Record 3-5 minute demo video.
- [ ] Verify all public links resolve.
- [ ] Confirm no claims of external adoption, production deployment, benchmark leadership, standards-body endorsement, or peer-reviewed acceptance.
- [ ] Confirm JSS rejection is treated as routing feedback, not as reviewer validation.

## Boundary

This checklist prepares an ICSE tool-demo feedback route. It is not a completed ICSE submission, accepted paper, camera-ready artifact, arXiv submission, or JSS resubmission.
