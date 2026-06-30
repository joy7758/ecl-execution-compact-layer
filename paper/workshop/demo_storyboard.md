# ECL v0.1 Demo Storyboard

## Scene 1: Trace Fragmentation

Visual: split terminal or editor view with OpenAI-style and LangChain-style fixture files.

Message: different runtimes emit different trace shapes.

## Scene 2: ECL Four-Surface Object

Visual: `ecl_object.json` with `state`, `intent`, `action`, and `evidence` expanded.

Message: ECL provides a compact execution target.

## Scene 3: One-Command Demo

Visual: terminal running `make demo`.

Message: reviewer can run the tool without external services.

## Scene 4: Replay Outputs

Visual:

- `execution_trace.json`
- `evidence_bundle.json`
- `replay_result.json`

Message: replay artifacts are deterministic and hashable.

## Scene 5: Loss-Aware Mapping

Visual: `loss.json` or loss report field in generated output.

Message: ECL records incomplete preservation instead of claiming full-fidelity conversion.

## Scene 6: Archive and Boundary

Visual: Zenodo record `https://zenodo.org/records/21003766`.

Message: DOI-backed software artifact; no external adoption, production, standardization, or peer-review claim.
