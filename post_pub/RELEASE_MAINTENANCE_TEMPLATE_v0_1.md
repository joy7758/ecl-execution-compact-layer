# ECL Maintenance Release Template v0.1

Status: template_ready

Use this template for future maintenance releases `v0.1.1` through `v0.1.6`.

## Release Header

```text
version=
date=
commit=
release_url=
zenodo_action=none | new_version_candidate | new_version_published
```

## Required Checks

```bash
python3 -m unittest discover -s tests
make demo
git diff --check
```

## Required Evidence

- linked issue or maintenance note;
- changelog entry;
- release note;
- test result;
- any user/reviewer feedback, if real;
- explicit no-fabrication boundary.

## Boundary Sentence

This maintenance release does not claim external adoption, production deployment, benchmark superiority, peer-review acceptance, or public standard status unless independent evidence is linked.

