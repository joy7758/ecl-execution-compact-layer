# Adapter Contract v0.1

## 1. Input Contract

OpenAI trace format input MUST be a structured trace object that can expose:

- `model_input`
- `reasoning`
- `tool_call`
- `events` or `trace_events`

LangChain trace format input MUST be a structured run object that can expose:

- `inputs`
- `metadata`
- `child_runs`
- `outputs`

Adapters MUST treat unsupported or missing source fields as mapping loss, not as inferred facts.

## 2. Output Contract

Adapter output MUST include an ECL object.

The ECL object MUST preserve the core object surfaces:

- `state`
- `intent`
- `action`
- `evidence`

Adapter output MUST include a `loss_report` at the adapter layer.

Adapters MUST NOT modify ECL schema semantics.

## 3. Mapping Rule

| Source | ECL |
| --- | --- |
| `tool_call` | `action` |
| `model_input` | `intent` |
| `reasoning` | `intent` |
| runtime metadata / actor / correlation | `state` |
| `events` | `evidence` |
| outputs / result references | `evidence` |

Mappings MUST be deterministic.

Mappings MUST NOT use LLM inference.

Mappings MUST NOT depend on hidden state.

## 4. Loss Reporting

Loss reporting MUST use this structure:

```json
{
  "loss_type": "semantic | structural | temporal",
  "lost_fields": [],
  "preserved_fields": [],
  "confidence": 0.0
}
```

`loss_type` MUST classify the primary loss as semantic, structural, or temporal.

`lost_fields` MUST list source fields that were omitted, approximated, or not representable in ECL.

`preserved_fields` MUST list source fields preserved through direct mapping, reference, or hash.

`confidence` MUST be a number from `0.0` to `1.0`.
