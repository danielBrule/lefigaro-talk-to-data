# Newspaper Talk to Data

A scaffold for a "talk to data" solution focused on newspaper analytics.
The repository includes a backend API, frontend shell, SQL artifacts, metadata, evaluation assets, and infrastructure scaffolding.

## Python Environment Setup

A project-specific Python environment is created in `.venv`.

### Create the virtual environment

```powershell
cd newspaper-talk-to-data
python -m venv .venv
```

### Activate the environment (PowerShell)

```powershell
cd newspaper-talk-to-data
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

Once dependencies are added, install them from `pyproject.toml` or a requirements file.

```powershell
pip install -U pip
pip install -r requirements.txt
```

## Repository Layout

- `backend/` - backend API, core logic, services, prompts, validation, and database code
- `frontend/` - frontend source code
- `sql/` - SQL views, security scripts, and tests
- `metadata/` - glossary, metrics, schema descriptions, and example questions
- `evaluations/` - benchmark questions and expected SQL/results
- `infra/` - infrastructure definitions, including Terraform
- `docs/` - documentation

## Azure SQL View Deployment

SQL view definitions are stored in `sql/views/` and use the `analytics` schema.

### Local development

1. Copy `.env.example` to `.env` and fill in your Azure SQL connection details:

   ```powershell
   copy .env.example .env
   # Edit .env with your Azure SQL server, database, username, password
   ```

2. Deploy views:

   ```powershell
   cd newspaper-talk-to-data
   make apply-sql-views
   ```

### Run the backend locally

Start the backend API once your dependencies are installed and `.env` is configured:

```powershell
cd newspaper-talk-to-data
make start-backend
```

Alternatively:

```powershell
cd newspaper-talk-to-data
.\.venv\Scripts\python.exe backend/main.py
```

Then open FastAPI docs in your browser:

- `http://localhost:8000/docs` — interactive Swagger UI
- `http://localhost:8000/redoc` — ReDoc API docs
- `http://localhost:8000/openapi.json` — raw OpenAPI schema

Example endpoints to test in the browser:

- `http://localhost:8000/api/articles`
- `http://localhost:8000/api/keywords`
- `http://localhost:8000/api/contributors`
- `http://localhost:8000/api/errors`

### GitHub Actions / CI-CD

Add the following secrets to your GitHub repository settings:
- `AZURE_SQL_SERVER`
- `AZURE_SQL_DATABASE`
- `AZURE_SQL_USERNAME`
- `AZURE_SQL_PASSWORD`

### Local development now, online later

For local development, keep working from the `newspaper-talk-to-data` folder and use the local `.venv`.
When you are ready to run online, ensure the same SQL migration files in `sql/views/` are deployed to the Azure SQL instance using the GitHub Action or `make apply-sql-views`.
