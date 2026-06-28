# Agent Instructions

This repository is an agent-readable implementation surface for Execution Compact Layer (ECL).

Rules:
- Keep protocol boundaries explicit. ECL references POP, AIP, and ARO artifacts; it does not replace them.
- Prefer structured JSON, JSON Schema, and deterministic Python entrypoints over prose-only documentation.
- Every generated artifact must be reproducible from `scripts/build_artifacts.py`.
- Every generated artifact must have an audit trail in `out/ecl_artifacts/evidence_bundle.json`.
- Do not claim public release, production audit control plane, external validation, or formal standard status from local artifacts.
- Keep adapters conservative. Unknown source trace fields may be copied only into hash-protected raw references or bounded metadata.

