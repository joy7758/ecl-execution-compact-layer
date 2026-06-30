# ECL ICSE 2027 Tool Demo Submission Checklist

Status: pdf_and_links_verified_video_pending

Target: ICSE 2027 Tool Demonstration and Data Showcase

Official track page: https://conf.researchr.org/track/icse-2027/icse-2027-demonstrations

## Checked Facts

- Paper format observed on the official page: IEEE conference proceedings formatting with `\documentclass[10pt,conference]{IEEEtran}`.
- Paper length target observed on the official page: no more than 4 pages for main text, inclusive of references, figures, tables, appendices, etc.
- Video target observed on the official page: 3-5 minutes, uploaded to YouTube and available during review.
- Submission deadline shown on the official page: 2026-10-23 AoE.
- Notification shown on the official page: 2026-12-11 AoE.
- Camera-ready date shown on the official page: 2027-01-20 AoE.
- Tool should be easy to install and use; reviewers should not need complex manual setup.

## Required Local Materials

- Draft paper: `paper/workshop/ICSE_2027_TOOL_DEMO_DRAFT.md`
- IEEEtran source: `paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.tex`
- IEEEtran PDF: `paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.pdf`
- PDF build status: `paper/workshop/ICSE_2027_PDF_BUILD_STATUS_v0_1.md`
- Video script: `paper/workshop/demo_video_script.md`
- Storyboard: `paper/workshop/demo_storyboard.md`
- Video recording gate: `paper/workshop/VIDEO_RECORDING_GATE_v0_1.md`
- Demo manifest: `paper/workshop/ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json`
- Public link check: `paper/workshop/PUBLIC_LINK_CHECK_v0_1.md`
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
- [x] Render IEEEtran PDF in the required ICSE page limit.
- [x] Verify all public links resolve.
- [x] Confirm no claims of external adoption, production deployment, benchmark leadership, standards-body endorsement, or peer-reviewed acceptance.
- [x] Confirm JSS rejection is treated as routing feedback, not as reviewer validation.
- [ ] Record 3-5 minute demo video.
- [ ] Upload demo video to YouTube and record the URL.
- [ ] Append the video URL to the submission abstract before HotCRP upload.
- [ ] Perform human PDF review before any portal submission.

## Boundary

This checklist prepares an ICSE tool-demo feedback route. It is not a completed ICSE submission, accepted paper, camera-ready artifact, arXiv submission, or JSS resubmission.
