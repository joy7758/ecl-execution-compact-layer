# ECL Demo Terminal Transcript v0.1

Status: make_demo_verified

Date: 2026-06-30

## Command

```bash
make demo
```

## Expected Command Expansion

```bash
python3 -m unittest discover -s tests
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
```

## Observed Output Summary

```text
Ran 78 tests
OK
{"all_deterministic": true, "all_valid": true, "result_hash": "sha256:e6decc8c2c4117011db44c6bcd62956b62344fe47871fc6564913cac2c156ac2"}
{"all_deterministic": true, "all_valid": true, "result_hash": "sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441"}
```

## Output Locations

```text
sdk/out/dependency_mode/
examples/out/external_recognition/
```

## Boundary

This is a local deterministic demo transcript. It is not external reviewer feedback, production deployment evidence, or third-party validation.
