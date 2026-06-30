# ECL v0.1 Demo Video Script

Target length: 3-5 minutes

## 0:00-0:30 Problem

Agent runtimes produce traces in different shapes. An OpenAI-style trace and a LangChain-style trace can both describe tool-using agent execution, but their native structures are not directly comparable.

ECL v0.1 provides a small deterministic execution IR for replayable trace records.

## 0:30-1:10 Repository and Archive

Show:

- repository: https://github.com/joy7758/ecl-execution-compact-layer
- Zenodo record: https://zenodo.org/records/21003766
- version DOI: `10.5281/zenodo.21003766`

State clearly: the DOI is a software archive, not peer-review acceptance or external adoption.

## 1:10-2:00 One-Command Demo

Run:

```bash
make demo
```

Explain that the command runs the unit tests, dependency-mode demo, and external-recognition demo without external API calls.

## 2:00-3:00 OpenAI and LangChain Trace Mapping

Open the generated outputs:

- `sdk/out/dependency_mode/openai/ecl_object.json`
- `sdk/out/dependency_mode/langchain/ecl_object.json`
- `examples/out/external_recognition/recognition_demo_result.json`

Point to the four ECL surfaces:

- `state`
- `intent`
- `action`
- `evidence`

## 3:00-4:00 Replay and Hash Stability

Show replay outputs:

- execution trace
- evidence bundle
- replay result
- verification hash

Explain that deterministic replay means unchanged input and code produce stable artifact hashes.

## 4:00-4:40 Boundary and Limitations

State:

- ECL is not a framework.
- ECL is not a tracing backend.
- ECL is not a public standard.
- ECL v0.1 uses local synthetic fixtures.
- The MCP-shaped wrapper is local only.

## 4:40-5:00 Closing

Summarize the tool contribution:

ECL normalizes supported agent-runtime traces into a small, replayable execution representation with explicit loss reporting and local hash-based verification.
