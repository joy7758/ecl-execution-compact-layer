# Compatibility Model v0.1

## 1. Supported Runtimes

ECL v0.1 compatibility may be evaluated for:

- OpenAI Agents SDK
- LangChain
- MCP-based agents

Supported runtime status means an ECL adapter contract can be evaluated. It does not mean ecosystem adoption, external certification, or standard status.

## 2. Compatibility Rule

ECL does not require full fidelity mapping, only semantic equivalence at execution level.

Semantic equivalence at execution level means:

- the execution state can be represented
- the intent can be represented or loss-reported
- the action can be represented or loss-reported
- the evidence surface can be represented through trace, hash, or loss report
- replay can reproduce the same ECL artifact hashes for identical inputs and parameters

When full fidelity is impossible, compatibility depends on explicit loss reporting.

## 3. Compatibility Level

Level 0 - no mapping:

No deterministic adapter exists, or the source runtime trace cannot be mapped into the ECL core object.

Level 1 - partial mapping, loss-aware:

A deterministic adapter maps the source runtime trace into ECL, but one or more source fields are omitted, approximated, or represented only through references or hashes. A `loss_report` is required.

Level 2 - full deterministic mapping:

A deterministic adapter maps the source runtime trace into ECL without semantic, structural, or temporal loss. Replay produces identical artifact hashes for identical inputs and parameters.

