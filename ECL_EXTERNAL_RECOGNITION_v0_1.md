# ECL External Recognition v0.1

## 1. Definition

ECL is a minimal deterministic execution IR for recognizing agent execution as state, intent, action, and evidence across OpenAI and LangChain traces.

## 2. Non-goals

- ECL is not a public standard.
- ECL is not an agent framework.
- ECL is not a production audit control plane.
- ECL is not a benchmark layer.
- ECL is not a replacement for runtime traces.

## 3. Core Object

```json
{
  "state": "...",
  "intent": "...",
  "action": "...",
  "evidence": "..."
}
```

## 4. Why It Exists

- It gives external runtimes one deterministic execution representation.
- It preserves replay and evidence outputs from the same execution record.
- It records mapping loss when runtime traces cannot be represented fully.

## 5. Minimal Adoption Flow

```text
OpenAI / LangChain -> ECL -> replay -> evidence
```

