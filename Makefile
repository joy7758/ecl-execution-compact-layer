.PHONY: demo test dependency-demo recognition-demo external-action-queue external-action-intake icse-package icse-video-candidate video-human-review youtube-upload-preflight post-jss-route next-human-actions

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

icse-video-candidate:
	$(PYTHON) scripts/build_icse_video_candidate.py

video-human-review:
	$(PYTHON) scripts/verify_video_human_review_packet.py

youtube-upload-preflight:
	$(PYTHON) scripts/verify_youtube_upload_preflight.py

post-jss-route:
	$(PYTHON) scripts/verify_post_jss_route.py

next-human-actions:
	$(PYTHON) scripts/verify_next_human_actions_packet.py

demo: test external-action-queue external-action-intake icse-package video-human-review youtube-upload-preflight post-jss-route next-human-actions dependency-demo recognition-demo
