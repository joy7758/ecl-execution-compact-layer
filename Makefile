.PHONY: demo test dependency-demo recognition-demo

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests

dependency-demo:
	$(PYTHON) sdk/demo_dependency_mode.py

recognition-demo:
	$(PYTHON) examples/external_recognition_demo.py

demo: test dependency-demo recognition-demo
