.PHONY: help venv install apply-sql-views

VENV := .venv
PYTHON := python
PIP := $(VENV)/Scripts/pip

help:
	@echo "Available targets:"
	@echo "  venv             - create the local Python virtual environment"
	@echo "  install          - install dependencies into the virtual environment"
	@echo "  apply-sql-views  - apply SQL view files to Azure SQL (requires connection vars)"

venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created at $(VENV)"

install: venv
	$(PIP) install -U pip
	$(PYTHON) -c "import pathlib, subprocess; p=pathlib.Path('requirements.txt'); print('No requirements.txt found. Add dependencies to requirements.txt or install manually.') if not p.exists() else subprocess.check_call([r'$(PIP)', 'install', '-r', str(p)])"

apply-sql-views: install
	@echo "Deploying SQL views..."
	$(VENV)/Scripts/python.exe backend/db/deploy_views.py
