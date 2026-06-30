# ECL

ECL is a minimal deterministic execution IR for representing agent execution as state, intent, action, and evidence.

## What ECL Is NOT

- Not a public standard.
- Not a production audit control plane.
- Not a replacement for POP, AIP, or ARO.
- Not proof of external runtime adoption.

## Core Object Schema

- `state`: execution status, lifecycle phase, actor, persona, runtime, and correlation references.
- `intent`: requested operation, constraints, expected result, and evidence requirements.
- `action`: action name, execution mode, side effect class, tool reference, and parameter hash.
- `evidence`: result status, trace references, event chain, policy decisions, and hashes.

## Minimal Execution Flow

`runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes`

## Reproducibility

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
python3 experiments/evaluate_trace_corpus.py
```

## Documentation

- Reviewer quickstart: `docs/joss/REVIEWER_QUICKSTART_v0_1.md`
- API reference: `docs/api/ECL_API_REFERENCE_v0_1.md`
- SDK guide: `sdk/README.md`
- Dependency API guide: `sdk/DEPENDENCY_README.md`
- Research-use boundary: `docs/research_use/ECL_RESEARCH_USE_CASE_v0_1.md`
- One-command demo: `docs/demo/ONE_COMMAND_DEMO.md`
- Citation package: `citation/ECL_CITATION_PACKAGE_v0_1.md`
- Technical report: `paper/technical_report/ECL_TECHNICAL_REPORT_v0_1.md`
- Safe public announcement: `docs/dissemination/SAFE_PUBLIC_ANNOUNCEMENT_v0_1.md`

## Citation

ECL v0.1 is archived on Zenodo as a software record:

```text
Zhang, B. (2026). ECL v0.1 (0.1). Zenodo. https://doi.org/10.5281/zenodo.21003766
```

- Version DOI: `10.5281/zenodo.21003766`
- Concept DOI: `10.5281/zenodo.21003765`
- Record URL: `https://zenodo.org/records/21003766`

Use `CITATION.cff` for software citation metadata. Current boundaries are recorded in `CHANGELOG.md` and `paper/SUBMISSION_MATERIALS_INDEX.md`. The Zenodo archive is a software DOI record; it is not peer-review acceptance, external adoption, or a standardization claim.
