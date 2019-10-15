SHELL := /bin/bash
export PATH := .venv/bin:$(PATH)
include .env


deps:
	pip install -r requirements.txt

serve:
	gunicorn --reload -w2 -b $(HOST):$(PORT) app:application

serve-debug:
	python -m app


.PHONY: deps serve serve-debug
