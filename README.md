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

## Citation

Use `CITATION.cff` for software citation metadata. Current boundaries are recorded in `CHANGELOG.md` and `paper/SUBMISSION_MATERIALS_INDEX.md`.
