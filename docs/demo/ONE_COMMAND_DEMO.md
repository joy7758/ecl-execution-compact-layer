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
docker build -t ecl-demo .
docker run --rm ecl-demo
```

If the local Docker credential helper is unavailable from the shell, use a temporary Docker config:

```bash
tmpdockerconfig=$(mktemp -d)
printf '{"auths":{}}\n' > "$tmpdockerconfig/config.json"
DOCKER_CONFIG="$tmpdockerconfig" docker build -t ecl-demo .
docker run --rm ecl-demo
```

Expected deterministic summary:

```text
Ran 78 tests
OK
dependency_mode_result_hash=sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3
external_recognition_result_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
```

## Boundary

The demo uses local fixtures and deterministic replay only. It performs no external API calls and does not prove external adoption, production deployment, standards-body endorsement, or peer-review acceptance.
