# CFPB Credit Card Complaints Analytics

SQL-first analytics project on 92,499 credit card complaints from the CFPB Consumer Complaint Database (Oct 5, 2025 to Oct 4, 2026).

**Live dashboard:** https://cfpb-complaints.streamlit.app

## What this project does

Loads raw complaint data into PostgreSQL, cleans it with SQL, models it as a star schema, answers business questions with window functions, and presents the results in a Streamlit dashboard.

## Tech stack

PostgreSQL 16, SQL (CTEs, window functions), Docker, Python, Pandas, Streamlit, Git/GitHub

## Pipeline

1. **Raw layer** (sql/01_create_raw.sql): 92,499 rows loaded as text, untouched.
2. **Clean layer** (sql/02_clean.sql): proper dates, "None" placeholders converted to NULL, ZIP codes reduced to 3 digits, tags turned into boolean flags.
3. **Star schema** (sql/03_dimensions.sql, sql/04_fact.sql): fact_complaints plus dim_company (543 companies), dim_issue (55 issue and sub-issue combinations) and dim_date.
4. **Analytics** (sql/05 to sql/07): month-over-month change with LAG, top issues per company with RANK, response rates by company.
5. **Performance** (sql/08, sql/09): primary keys and a composite index.
6. **Dashboard** (dashboard/): Streamlit app reading exported summary CSVs.

## Schema

    dim_company (company_key PK, company_name)
    dim_issue   (issue_key PK, issue, sub_issue)
    dim_date    (date_key PK, year, quarter, month, month_label, month_start, weekday)

    fact_complaints (complaint_id PK, date_key, company_key, issue_key,
                     state, zip3, submitted_via, company_response,
                     is_timely, is_older_american, is_servicemember)

## Findings

Company figures use complaints received through Sep 18, 2026.

- **Data lag:** daily counts hold at roughly 270 to 360 on weekdays until about Sep 18, 2026, then fade to single digits by Oct 4. This looks like complaints still being logged, so the analysis excludes everything after Sep 18.
- **Seasonality:** complaints peaked in January 2026 (9,516 that month, up 21.1% from December). Per-day averages are used for fair month-to-month comparison.
- **Volume is concentrated:** Capital One (12,915), Citibank (11,591) and Synchrony (8,744) lead in total complaints.
- **Relief rates vary widely** among companies with 1,000+ complaints, from 63.0% (TransUnion) to 3.3% (Experian). Citibank gives relief on 42.3% of complaints versus 21.0% for Capital One and 18.9% for Chase.
- **Timeliness:** nearly all companies respond on time 98.5% of the time or better. Synchrony is lowest at 95.71%.
- **Caveat:** relief rate is a rough measure. Companies receive different types of complaints, so it does not show which company is better.

## Query performance

A company and date-range query on fact_complaints went from sequential scans (about 5 ms) to an index-only scan using a composite index on (company_key, date_key) (about 0.5 ms), roughly 10x faster, verified with EXPLAIN ANALYZE. At 92K rows both are fast in absolute terms, and the gap would grow with larger data.

## Run it locally

Start the database:

    docker compose up -d

Download the data from the CFPB Consumer Complaint Database (credit card complaints, one year), save it as data/complaints_raw.csv, then run the files in sql/ in order.

Run the dashboard:

    pip install -r dashboard/requirements.txt
    streamlit run dashboard/app.py

## Data source

CFPB Consumer Complaint Database (public data).
