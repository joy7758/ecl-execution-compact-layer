# ECL Docker Demo Status v0.1

Status: docker_demo_verified_after_daemon_start_and_dockerfile_fix

Date: 2026-06-30

## Command Verified

```bash
docker build -t ecl-demo .
docker run --rm ecl-demo
```

## Earlier Blockers

Initial daemon state:

```text
Docker version 29.5.2, build 79eb04c7d8
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

Initial start attempt:

```text
command=open -ga Docker
waiting_for_docker_daemon attempts=24
poll_interval_seconds=5
docker_daemon_ready=false
```

After a later start attempt, Docker became available:

```text
command=open -ga Docker
waiting_for_docker_daemon attempt=1
docker_daemon_ready=true
docker_context=desktop-linux
```

The default local Docker credential helper was unavailable from the shell:

```text
error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH
```

The verified build used a temporary Docker config that does not depend on the local credential helper:

```bash
tmpdockerconfig=$(mktemp -d)
printf '{"auths":{}}\n' > "$tmpdockerconfig/config.json"
DOCKER_CONFIG="$tmpdockerconfig" docker build -t ecl-demo .
docker run --rm ecl-demo
```

## Dockerfile Fix

The reviewer container requires `git` and `make` inside `python:3.11-slim`:

```text
apt-get install -y --no-install-recommends git make
```

`git` is required by the JOSS gate verifier tests. `make` is required by the container command.

## Verified Image

```text
image=ecl-demo:latest
image_id=sha256:740cc621c668a1608f9f897c0d53662a825cf706a42017d2b8f06c4038b29c3f
image_created=2026-06-30T09:32:42.241439138Z
image_size_bytes=90892094
```

## Verified Output

Host `make demo` and container `docker run --rm ecl-demo` now produce the same deterministic demo hashes:

```text
Ran 78 tests
OK
dependency_mode_result_hash=sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3
external_recognition_result_hash=sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441
```

## Boundary

This file claims only local Docker verification of the reviewer demo command. It does not claim ICSE submission, ICSE acceptance, external adoption, production deployment, benchmark superiority, or peer-review validation.
