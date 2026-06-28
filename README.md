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

`ECL -> validator -> trace -> evidence -> replay`

