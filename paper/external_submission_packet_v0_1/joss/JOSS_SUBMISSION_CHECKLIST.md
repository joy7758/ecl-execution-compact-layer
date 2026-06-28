# JOSS Submission Checklist for ECL v0.1

## 1. Required Metadata

- Author: Bin Zhang.
- Affiliation: independent researcher.
- ORCID: optional, not provided.

## 2. Repository Checklist

- Runnable examples: yes, `examples/external_recognition_demo.py` and `sdk/demo_dependency_mode.py`.
- Tests passing: yes, `python3 -m unittest discover -s tests`.
- License MIT confirmed: yes, root `LICENSE` and release license are MIT.
- Documentation completeness: yes, `README.md`, `paper/joss/JOSS_READY.md`, `sdk/README.md`, `CONTRIBUTING.md`, `SUPPORT.md`, `CHANGELOG.md`, `CITATION.cff`, and `release/v0.1/README.md` are present.
- Continuous integration workflow: yes, `.github/workflows/tests.yml` and `.github/workflows/joss-paper.yml` are present.
- Public collaboration templates: yes, `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` are present.
- Standard JOSS paper path: yes, `paper/paper.md` and `paper/paper.bib` mirror `paper/joss/paper.md` and `paper/joss/paper.bib`.

## 3. JOSS Requirements Mapping

- Software availability: public GitHub repository at `https://github.com/joy7758/ecl-execution-compact-layer`.
- Reproducibility: local tests and deterministic demos are documented and runnable.
- Synthetic trace-corpus evidence: `python3 experiments/evaluate_trace_corpus.py`.
- Installation instructions: repository clone, `python3 -m pip install -e .`, and Python test commands are included in `paper/joss/JOSS_READY.md`.

## 4. Human Action Steps

- Submit via the JOSS website.
- Link GitHub repo: `https://github.com/joy7758/ecl-execution-compact-layer`.
- Confirm final metadata in the JOSS form.
- Confirm that submission is a human action; no automated JOSS submission is performed by this package.
