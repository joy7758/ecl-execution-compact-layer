# Data Availability Statement

All data used in the evaluation are local fixtures, synthetic trace cases, and generated evidence artifacts included in the repository:

```text
https://github.com/joy7758/ecl-execution-compact-layer
```

No external production trace data are used. The evaluation can be reproduced with:

```bash
python3 -m unittest discover -s tests
python3 experiments/evaluate_trace_corpus.py
python3 experiments/evaluate_validation_matrix.py
python3 experiments/evaluate_mapping_coverage.py
python3 sdk/demo_dependency_mode.py
python3 examples/external_recognition_demo.py
```
