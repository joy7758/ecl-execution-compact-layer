# Contributing to ECL

ECL is a deterministic local execution representation artifact. Contributions should preserve protocol boundaries, deterministic replay, and explicit claim boundaries.

## Development Setup

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```

## Contribution Rules

- Do not change the frozen schema without a new version and migration note.
- Do not claim external adoption, standard status, DOI minting, or formal submission from local artifacts.
- Keep runtime mappings loss-aware.
- Keep examples deterministic and offline.
- Update tests when changing adapters, replay, SDK behavior, or publication packet structure.

## Pull Request Checklist

- Tests pass with `python3 -m unittest discover -s tests`.
- No schema drift unless the PR explicitly changes schema version.
- No network calls are added to replay or examples.
- New documentation uses the authoritative pipeline:
  `runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes`.
