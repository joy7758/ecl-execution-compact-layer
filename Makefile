.PHONY: demo test dependency-demo recognition-demo external-action-queue external-action-intake

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

demo: test external-action-queue external-action-intake dependency-demo recognition-demo
