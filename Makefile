SHELL := /bin/bash
export PATH := .venv/bin:$(PATH)
include .env


deps:
	pip install -r requirements.txt

serve:
	gunicorn -c config/gunicorn.py app:application

serve-debug:
	python -m app

test:
	pytest -x --ff --nf


.PHONY: deps serve serve-debug test
