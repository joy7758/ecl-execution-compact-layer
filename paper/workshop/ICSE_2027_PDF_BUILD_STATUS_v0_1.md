# ECL ICSE 2027 PDF Build Status v0.1

Status: ieeetran_pdf_rendered_for_human_review

Date checked: 2026-06-30

## Format

The official ICSE 2027 Tool Demonstration and Data Showcase page was checked on 2026-06-30. The observed requirement is IEEE conference proceedings formatting, not ACM formatting:

```tex
\documentclass[10pt,conference]{IEEEtran}
```

## Build

Source:

```text
paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.tex
sha256=5d30fa2d2d34fcb82e7f31ccadccdc9adeaeb0cb99e1c36bfed20a1a75e00d85
```

PDF:

```text
paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.pdf
sha256=7633104c76f499b6e3447da47c1e860f652782b870e1e98cef0e9d8e2ff2558e
pages=2
page_limit=4
page_size=letter
```

Compile command:

```bash
SOURCE_DATE_EPOCH=1782777600 FORCE_SOURCE_DATE=1 \
python3 /Users/zhangbin/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
  /Users/zhangbin/GitHub/ecl-execution-compact-layer/paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.tex \
  --compiler texlive \
  --output-directory /Users/zhangbin/GitHub/ecl-execution-compact-layer/paper/workshop/ieee/build \
  --json
```

Result:

```text
exit_code=0
rebuild_hash_stable=true
visual_render_checked=true
visual_render_status=no_overlap_or_clipping_observed
```

## Remaining Human Gate

The PDF is a draft rendered for human review. Before an actual ICSE submission, the author still needs to:

- review the PDF content and author metadata;
- record and upload a 3-5 minute YouTube demo video;
- append the video URL to the submission abstract as required by the track page;
- perform the actual HotCRP submission action.

## Boundary

This status file does not claim ICSE submission, ICSE acceptance, camera-ready completion, video publication, external adoption, production deployment, benchmark superiority, or peer-review validation.
