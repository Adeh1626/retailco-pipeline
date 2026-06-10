# RetailCo Data Pipeline

## What This Project Is
A complete end-to-end data engineering pipeline built for learning purposes,
based on the HNG Stage 8 Data Engineering task brief.

The pipeline extracts retail data from an ERP API, loads it into a data lake,
moves it to a data warehouse, and models it into analytics-ready tables using
Kimball dimensional modelling principles.

## Note on the API
The original HNG Stage 8 ERP API is no longer available.
For this portfolio project, I built a fully functional mock ERP server (mock_api/)
using FastAPI that replicates all 9 entities, cursor pagination, incremental loading,
rate limiting, transient errors, soft deletes, and refund payments.

## Tools Used
- Apache Airflow 2.9 — pipeline orchestration
- Python 3.11 — data extraction
- PostgreSQL 18 — data lake and data warehouse
- dlt — loading from lake to warehouse
- dbt-core 1.5 — data transformation and modelling
- FastAPI — mock ERP API server

## Project Structure
- mock_api/ — fake ERP API server with all 9 entities
- extractor/ — Python extractor that pulls data from the API
- dlt_pipeline/ — moves data from lake to warehouse
- retailco/ — dbt project with staging and mart models
- airflow/ — Airflow DAG for scheduling
- design/ — bus matrix, ERD, architecture diagram

## How to Run

### Prerequisites
- Python 3.11
- PostgreSQL 18
- WSL/Ubuntu (for Airflow)

### Steps
1. Clone this repo
2. Create PostgreSQL databases: lake and warehouse
3. Start the mock API:
   cd mock_api
   pip install fastapi uvicorn faker
   uvicorn main:app --host 0.0.0.0 --port 8000
4. Run the extractor:
   python extractor/extractor.py
5. Run the dlt pipeline:
   python dlt_pipeline/load.py
6. Run dbt models:
   cd retailco
   dbt run --select staging
   dbt run --select marts
   dbt test
7. Start Airflow (in Ubuntu/WSL):
   airflow webserver --port 8080
   airflow scheduler

## Warehouse Tables
Dimensions: dim_date, dim_customer, dim_product, dim_store, dim_employee, dim_payment_method
Facts: fct_sales, fct_payments, fct_inventory_daily, fct_order_lifecycle
Data quality: flagged_payments

## Example Queries
Top selling products:
SELECT p.product_name, SUM(s.line_total) AS revenue
FROM dbt_marts.fct_sales s
JOIN dbt_marts.dim_product p ON s.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;