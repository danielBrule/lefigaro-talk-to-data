.PHONY: help venv install

VENV := .venv
PYTHON := python
PIP := $(VENV)/Scripts/pip

help:
	@echo "Available targets:"
	@echo "  venv      - create the local Python virtual environment"
	@echo "  install   - install dependencies into the virtual environment"

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created at $(VENV)"

install: venv
	$(PIP) install -U pip
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "No requirements.txt found. Add dependencies to requirements.txt or install manually."; \
	fi
