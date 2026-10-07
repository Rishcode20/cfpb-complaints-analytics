DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date AS
SELECT d::DATE                          AS date_key,
       EXTRACT(YEAR FROM d)::INT        AS year,
       EXTRACT(QUARTER FROM d)::INT     AS quarter,
       EXTRACT(MONTH FROM d)::INT       AS month,
       TO_CHAR(d, 'Mon YYYY')           AS month_label,
       DATE_TRUNC('month', d)::DATE     AS month_start,
       TO_CHAR(d, 'Dy')                 AS weekday
FROM generate_series('2025-10-01'::DATE, '2026-10-31'::DATE, '1 day') AS d;

DROP TABLE IF EXISTS fact_complaints;
CREATE TABLE fact_complaints AS
SELECT c.complaint_id,
       c.date_received                  AS date_key,
       co.company_key,
       i.issue_key,
       c.state,
       c.zip3,
       c.submitted_via,
       c.company_response,
       c.is_timely,
       c.is_older_american,
       c.is_servicemember
FROM clean_complaints c
JOIN dim_company co ON co.company_name = c.company
JOIN dim_issue i    ON i.issue = c.issue
                   AND i.sub_issue = COALESCE(c.sub_issue, 'Not specified');
