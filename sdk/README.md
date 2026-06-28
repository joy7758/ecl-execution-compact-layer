# ECL SDK v0.1

## 1. 10-line Integration Example

```python
from sdk import ECL
trace = {"runtime": "openai", "trace": openai_trace}
ecl_object = ECL.from_trace(trace)
validation = ECL.validate(ecl_object)
replay = ECL.replay(ecl_object)
print(validation["valid"])
print(replay["artifact_hashes"]["execution_trace"])
print(replay["artifact_hashes"]["evidence_bundle"])
print(replay["artifact_hashes"]["replay_result"])
print(replay["verification_hash"])
```

## 2. OpenAI -> ECL Flow

```bash
python3 sdk/demo_openai.py
```

## 3. LangChain -> ECL Flow

```bash
python3 sdk/demo_langchain.py
```

## 4. Replay Example

```python
replay = ECL.replay(ecl_object)
```

## 5. Determinism Guarantee

The SDK uses fixed generation parameters, frozen schema validation, deterministic sorted-key compact JSON hashing, and local replay artifacts only.
