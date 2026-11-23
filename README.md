# Marketing Data Pipeline (Python + SQLite)

A complete local learning project. SQLite is included with Python, so no database server installation is needed.

## Setup on Windows

Open this folder in VS Code, then choose Terminal > New Terminal.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run the project

1. Generate sample CSV and JSON files:

```powershell
py generate_data.py
```

2. Start the mock advertising API in terminal 1:

```powershell
py mock_api.py
```

Leave it running.

3. Open terminal 2, activate `.venv`, and run:

```powershell
py etl.py
```

4. Display loaded records:

```powershell
py main.py
```

5. Run tests:

```powershell
py -m pytest -q
```

The database file `marketing.db` is created automatically. SQL reporting examples are in `sql/analytics.sql`; data-quality checks are in `sql/audit.sql`.

## Files

- `database.py`: creates tables and opens the SQLite connection.
- `generate_data.py`: creates sample CSV/JSON source files.
- `mock_api.py`: serves paginated advertising data using Flask.
- `etl.py`: extracts, cleans, validates and loads records.
- `main.py`: displays table counts and sample rows.
- `sql/`: reporting and audit queries.
- `tests/`: cleaning-function tests.
- `case_study.md`: ROAS discrepancy walkthrough.

This is a learning project, not a production deployment. SQLite is used to avoid a separate database installation. MySQL can be introduced later.
