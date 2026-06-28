# ECL vs Existing Systems

ECL does not compete with frameworks; it normalizes execution semantics.

| System | Execution Representation | Replayability | Loss Handling | Cross-runtime Support |
| --- | --- | --- | --- | --- |
| OpenAI Agents SDK trace | Runtime trace for OpenAI agent execution events and tool calls. | Runtime trace can be inspected, but deterministic ECL replay is outside the trace itself. | Missing or remapped fields require adapter-level loss reporting when converted to ECL. | Native to OpenAI runtime traces; cross-runtime normalization requires an IR such as ECL. |
| LangChain trace | Run tree representation with inputs, outputs, metadata, and child runs. | Run data can be replay-adjacent, but deterministic ECL replay is outside the trace itself. | Missing or remapped run fields require adapter-level loss reporting when converted to ECL. | Native to LangChain run structure; cross-runtime normalization requires an IR such as ECL. |
| MCP (Model Context Protocol) | Tool and context protocol messages rather than a single execution IR record. | Replay depends on captured calls and surrounding execution records. | Loss handling must be defined by the bridge that maps MCP interactions into ECL. | MCP can expose tools and context across systems; ECL normalizes execution semantics after capture. |
| ECL | Minimal execution IR with state, intent, action, and evidence. | Deterministic replay produces trace, evidence, and replay result artifacts. | Adapter-level loss reporting is required for incomplete mappings. | OpenAI and LangChain traces can be normalized through the external adoption hook. |

