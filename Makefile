.PHONY: demo test dependency-demo recognition-demo external-action-queue external-action-intake icse-package

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests

dependency-demo:
	$(PYTHON) sdk/demo_dependency_mode.py

recognition-demo:
	$(PYTHON) examples/external_recognition_demo.py

external-action-queue:
	$(PYTHON) scripts/verify_external_action_queue.py

external-action-intake:
	$(PYTHON) scripts/validate_external_action_evidence_intake.py

icse-package:
	$(PYTHON) scripts/verify_icse_tool_demo_package.py

demo: test external-action-queue external-action-intake icse-package dependency-demo recognition-demo
