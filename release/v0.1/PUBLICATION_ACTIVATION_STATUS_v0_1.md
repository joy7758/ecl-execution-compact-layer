# ECL Publication Activation Status v0.1

Status: publication_package_created_not_published

This package creates the local structure needed for external publication activation. It does not create a GitHub release, Zenodo deposit, DOI, public repository, or public license.

## Created

- `release/v0.1/README.md`
- `release/v0.1/LICENSE`
- `release/v0.1/zenodo.json`
- `release/v0.1/paper/`
- `release/v0.1/sdk/`
- `release/v0.1/mcp/`
- `release/v0.1/examples/`

## Still Requires Human Action

- Select and approve a real OSI-approved software license.
- Replace author placeholders in `zenodo.json`.
- Move the package into a public GitHub repository.
- Create a GitHub release.
- Create a Zenodo deposit and mint DOI.
- Confirm final distribution permission.

## Boundary

- `github_release_created=false`
- `zenodo_deposit_created=false`
- `doi_minted=false`
- `public_release=false`
- `license_selected=false`
