# ECL ICSE 2027 HotCRP Submission Draft v0.1

Status: draft_only_not_submitted

## Track

ICSE 2027 Tool Demonstration and Data Showcase

## Title

ECL: A Deterministic Execution IR for Replayable Agent Runtime Traces

## Authors

Bin Zhang, Independent Researcher

## Abstract Draft

ECL is a small deterministic execution intermediate representation for replayable agent-runtime traces. The tool maps supported OpenAI-style and LangChain-style local fixtures into four ECL surfaces: state, intent, action, and evidence. It validates normalized records, emits deterministic replay artifacts, records mapping loss when source information is not fully preserved, and computes stable hashes. The reviewer workflow is a one-command local demo, `make demo`, with an optional Docker path. ECL v0.1 is archived as a Zenodo software record and is intentionally narrow: it is not an agent framework, tracing backend, benchmark, public standard, production deployment, or external adoption claim.

Video: `<YOUTUBE_URL_TO_BE_FILLED_AFTER_HUMAN_UPLOAD>`

## Public Tool URL

https://github.com/joy7758/ecl-execution-compact-layer

## Archive URL

https://doi.org/10.5281/zenodo.21003766

## Artifact / Usage Instructions

```bash
git clone https://github.com/joy7758/ecl-execution-compact-layer.git
cd ecl-execution-compact-layer
make demo
```

Optional Docker path:

```bash
docker build -t ecl-demo .
docker run --rm ecl-demo
```

## Keywords

```text
agent systems; execution traces; deterministic replay; intermediate representation; reproducibility; tool demonstration
```

## Checklist Before Human Submission

- [ ] Review `paper/workshop/ieee/ECL_ICSE_2027_TOOL_DEMO_DRAFT.pdf`.
- [ ] Review or replace the local video candidate.
- [ ] Upload final video to YouTube.
- [ ] Replace `<YOUTUBE_URL_TO_BE_FILLED_AFTER_HUMAN_UPLOAD>` in the abstract.
- [ ] Verify all public links again.
- [ ] Submit through `https://icse27demos.hotcrp.com/`.

## Boundary

This is a local HotCRP field draft only. It is not a portal upload, not an ICSE submission, not an acceptance, not a video publication, and not external validation.
