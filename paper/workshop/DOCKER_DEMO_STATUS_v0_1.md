# ECL Docker Demo Status v0.1

Status: docker_cli_present_daemon_unavailable

Date: 2026-06-30

## Command Attempted

```bash
docker build -t ecl-demo .
docker run --rm ecl-demo
```

## Observed Result

```text
Docker version 29.5.2, build 79eb04c7d8
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

## Interpretation

The Docker CLI is installed, but the Docker daemon was not running in the current environment. The container demo path is therefore prepared but not verified in this run.

## Verified Alternative

The reviewer-facing non-container command is verified:

```bash
make demo
```

Observed deterministic summary:

```text
Ran 78 tests
OK
dependency_mode_result_hash=sha256:e6decc8c2c4117011db44c6bcd62956b62344fe47871fc6564913cac2c156ac2
external_recognition_result_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
```

## Boundary

This file does not claim a working container image. It records a prepared Dockerfile and a blocked local Docker verification due to daemon availability.
