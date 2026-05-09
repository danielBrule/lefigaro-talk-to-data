.PHONY: help venv install apply-sql-views start-backend tests

VENV := .venv
PYTHON := python
VENV_PYTHON := .venv\Scripts\python.exe

help:
	@echo Available targets:
	@echo   venv
	@echo   install
	@echo   start-backend
	@echo   apply-sql-views
	@echo   tests

venv:
	@if not exist ".venv\Scripts\python.exe" ($(PYTHON) -m venv .venv) else (echo Virtual environment already exists.)

install: venv
	".venv\Scripts\python.exe" -m pip --version
	@if exist "requirements.txt" (".venv\Scripts\python.exe" -m pip install --no-cache-dir -r "requirements.txt") else (echo No requirements.txt found.)

check: install
	@echo Running syntax checks...
	".venv\Scripts\python.exe" -c "import py_compile, pathlib; [py_compile.compile(str(p), doraise=True) for p in pathlib.Path('backend').rglob('*.py')]"

start-backend: install
	@echo Starting backend...
	".venv\Scripts\python.exe" -m backend.main

apply-sql-views: install
	@echo Deploying SQL views...
	".venv\Scripts\python.exe" backend\db\deploy_views.py

tests: install
	@echo Running tests...
	@set PYTHONPATH=%CD% && ".venv\Scripts\python.exe" -m pytest backend/tests/ -v