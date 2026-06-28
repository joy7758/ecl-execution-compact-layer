## Summary

-

## ECL Boundary Check

- [ ] No schema change unless explicitly documented.
- [ ] No claim of JOSS submission, acceptance, DOI minting, third-party validation, or external adoption unless independently verified.
- [ ] Deterministic behavior preserved.

## Validation

```text
python3 -m unittest discover -s tests
python3 experiments/evaluate_trace_corpus.py
python3 experiments/evaluate_validation_matrix.py
```

## Notes for Reviewers

Describe any mapping, loss-reporting, replay, or paper-material changes in agent-readable terms.
