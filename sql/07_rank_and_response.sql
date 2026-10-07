-- Query 1: top 3 issues for each of the 5 biggest companies
WITH company_totals AS (
    SELECT company_key, COUNT(*) AS total
    FROM fact_complaints
    WHERE date_key <= '2026-09-18'
    GROUP BY company_key
    ORDER BY total DESC
    LIMIT 5
),
issue_counts AS (
    SELECT f.company_key, i.issue, COUNT(*) AS n
    FROM fact_complaints f
    JOIN dim_issue i USING (issue_key)
    WHERE f.date_key <= '2026-09-18'
      AND f.company_key IN (SELECT company_key FROM company_totals)
    GROUP BY f.company_key, i.issue
),
ranked AS (
    SELECT company_key, issue, n,
           RANK() OVER (PARTITION BY company_key ORDER BY n DESC) AS rnk
    FROM issue_counts
)
SELECT co.company_name, r.rnk, r.issue, r.n
FROM ranked r
JOIN dim_company co USING (company_key)
WHERE r.rnk <= 3
ORDER BY co.company_name, r.rnk;

-- Query 2: response rates for companies with 1,000+ complaints
SELECT co.company_name,
       COUNT(*) AS complaints,
       ROUND(100.0 * COUNT(*) FILTER (WHERE f.is_timely) / COUNT(*), 2) AS pct_timely,
       ROUND(100.0 * COUNT(*) FILTER (WHERE f.company_response LIKE '%relief') / COUNT(*), 1) AS pct_relief
FROM fact_complaints f
JOIN dim_company co USING (company_key)
WHERE f.date_key <= '2026-09-18'
GROUP BY co.company_name
HAVING COUNT(*) >= 1000
ORDER BY pct_relief DESC;
