# ECL Gateway Spec v0.1

## 1. Scope

ECL is a deterministic execution IR gateway layer.

ECL standardizes agent execution expression across heterogeneous runtimes through a minimal, replayable, loss-aware interface.

ECL is NOT a framework.

ECL is NOT a runtime.

ECL is NOT a standard.

ECL is a gateway IR layer.

## 2. Core Object

The only core ECL object shape is:

```json
{
  "state": "...",
  "intent": "...",
  "action": "...",
  "evidence": "..."
}
```

## 3. Execution Contract

ECL execution is a pure deterministic function:

```text
runtime trace -> normalize/adapt -> ECL record -> validate -> replay -> {execution_trace, evidence_bundle, replay_result} -> artifact hashes
```

The runtime layer MUST be deterministic.

The runtime layer MUST NOT depend on hidden state.

The runtime layer MUST NOT use stochastic behavior.

Replay MUST produce an identical artifact hash for identical inputs, schema, adapter, validator, and generation parameters.

## 4. Gateway Boundary

Inbound boundary:

```text
OpenAI / LangChain / MCP-shaped local wrapper -> ECL
```

Inbound adapters map external runtime traces into ECL without changing ECL semantics.

Internal boundary:

```text
validator + deterministic execution
```

The internal boundary validates ECL objects and executes deterministic artifact generation only.

Outbound boundary:

```text
ECL -> execution_trace / evidence_bundle / replay_result
```

Outbound artifacts expose trace, evidence, and replay surfaces without claiming external validation or standard status.

## 5. Loss Model

ECL is a loss-aware IR mapping system.

Not all runtime information is preserved during mapping.

Mapping loss MUST be explicitly recorded.

`loss_report` is mandatory in the adapter layer.

A conforming adapter MUST report omitted, approximated, or structurally remapped source fields.
