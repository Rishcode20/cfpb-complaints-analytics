EXPLAIN ANALYZE
SELECT COUNT(*)
FROM fact_complaints f
JOIN dim_company co USING (company_key)
WHERE co.company_name = 'CAPITAL ONE FINANCIAL CORPORATION'
  AND f.date_key BETWEEN '2026-01-01' AND '2026-03-31';
