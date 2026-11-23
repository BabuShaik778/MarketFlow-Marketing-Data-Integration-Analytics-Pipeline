# Marketing Data Engineering Pipeline

An end-to-end data engineering project that integrates advertising, CRM, and store data using Python, REST APIs, and SQLite. The project demonstrates data extraction, transformation, validation, relational data modelling, and SQL-based marketing analytics.

## Project Overview

Marketing data is often spread across multiple sources, making it difficult to generate consistent business insights.

This project demonstrates a pipeline that:
- Extracts data from CSV and JSON files.
- Retrieves paginated data through a Flask REST API.
- Cleans and transforms incoming records.
- Validates records before database loading.
- Stores structured data in a relational SQLite database.
- Supports marketing analytics and data quality auditing through SQL.

## Architecture

```text
CSV Files       JSON Files       Flask REST API
    |               |                  |
    +---------------+------------------+
                    |
                    v
             Python ETL Pipeline
                    |
          +---------+----------+
          |                    |
      Extraction          Transformation
                               |
                     Cleaning & Validation
                               |
                               v
                         SQLite Database
                          marketing.db
                               |
                    +----------+----------+
                    |                     |
               Analytics SQL          Audit SQL
                    |                     |
                    +----------+----------+
                               |
                       Marketing Insights
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL and data processing |
| Flask | Mock REST API |
| Requests | API integration |
| CSV / JSON | Source data formats |
| SQLite | Relational database |
| SQL | Analytics and auditing |
| Pytest | Automated testing |
| VS Code | Development environment |

## Project Structure

```text
marketing_data_project/
│
├── data/
│   ├── customers.csv
│   └── other generated source files
│
├── sql/
│   ├── analytics.sql
│   └── audit.sql
│
├── tests/
│   └── test_etl.py
│
├── database.py
├── generate_data.py
├── mock_api.py
├── etl.py
├── main.py
├── marketing.db
├── requirements.txt
├── case_study.md
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd marketing_data_project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Project

### Step 1: Generate sample data

```bash
python generate_data.py
```

This generates synthetic CSV and JSON source files.

### Step 2: Start the mock API

```bash
python mock_api.py
```

API endpoint:

`http://127.0.0.1:5000/ads`

Keep this terminal running.

### Step 3: Run the ETL pipeline

Open a second terminal in the project directory:

```bash
python etl.py
```

The pipeline extracts, transforms, validates, and loads the data into SQLite.

### Step 4: View database results

```bash
python main.py
```

This displays database table counts and sample records.

## Database Design

### Dimension Tables

| Table | Description |
|---|---|
| dim_customer | Customer information |
| dim_campaign | Campaign information |
| dim_product | Product information |

### Fact Tables

| Table | Description |
|---|---|
| fact_ad_spend_daily | Daily advertising spend |
| fact_lead | Marketing lead records |
| fact_order | Customer order transactions |
| fact_order_item | Order-level product details |

### Monitoring Tables

| Table | Description |
|---|---|
| rejected_rows | Records rejected during ETL |
| pipeline_runs | Pipeline execution history |

## SQL Analytics and Auditing

The `sql/analytics.sql` file contains queries for exploring marketing performance and business metrics.

The `sql/audit.sql` file contains queries for inspecting data quality and database consistency.

Execute these files against `marketing.db` using a SQLite-compatible SQL client.

## Initial Execution Results

The first successful pipeline execution produced:

| Metric | Records |
|---|---:|
| Processed records | 176 |
| Customers | 40 |
| Campaigns | 3 |
| Daily advertising spend | 6 |
| Leads | 70 |
| Orders | 30 |
| Products | 4 |
| Order items | 30 |
| Rejected records | 0 |

These figures represent the initial execution only.

## Running Tests

Run the automated tests with:

```bash
python -m pytest -q
```

## Design Decisions

- **Python:** Used for data extraction, transformation, and validation.
- **Flask:** Used to simulate an external paginated advertising API.
- **SQLite:** Selected for a lightweight local database without requiring a separate database server.
- **CSV and JSON:** Used to represent different source-system formats.
- **SQL:** Used for analytical queries and data quality checks.

## Assumptions and Limitations

- The project uses synthetic marketing data.
- The Flask API simulates an external data provider.
- SQLite is used instead of PostgreSQL.
- The pipeline is designed as a learning implementation.
- The initial execution results do not establish rerun safety or production readiness.
- Real advertising platform integrations and production monitoring are outside the current scope.

## Future Improvements

- Migrate the database to PostgreSQL.
- Integrate real advertising and CRM APIs.
- Implement incremental ETL processing.
- Add stronger data reconciliation and validation.
- Improve logging and monitoring.
- Add query execution plan analysis.
- Build a marketing performance dashboard.

## Learning Outcomes

This project demonstrates practical concepts in:

- ETL pipeline development
- Python data processing
- REST API integration
- CSV and JSON processing
- Data cleaning and validation
- Relational database design
- SQL analytics
- Data quality auditing
- Automated testing
