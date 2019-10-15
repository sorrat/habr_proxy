SHELL := /bin/bash
export PATH := .venv/bin:$(PATH)


deps:
	pip install -r requirements.txt


.PHONY: deps
