# ECL One-Command Demo

Status: local_offline_demo_ready

## Run

```bash
make demo
```

This runs:

```bash
python3 -m unittest discover -s tests
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
```

## Expected Outputs

- test suite result from `tests/`
- dependency-mode outputs under `sdk/out/dependency_mode/`
- external-recognition outputs under `examples/out/external_recognition/`

## Docker Option

```bash
docker build -t ecl-v0.1 .
docker run --rm ecl-v0.1
```

## Boundary

The demo uses local fixtures and deterministic replay only. It performs no external API calls and does not prove external adoption, production deployment, standards-body endorsement, or peer-review acceptance.
