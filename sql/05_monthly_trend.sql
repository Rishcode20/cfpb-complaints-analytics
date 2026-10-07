WITH monthly AS (
    SELECT d.month_start,
           d.month_label,
           COUNT(*) AS complaints
    FROM fact_complaints f
    JOIN dim_date d ON d.date_key = f.date_key
    GROUP BY d.month_start, d.month_label
)
SELECT month_label,
       complaints,
       LAG(complaints) OVER (ORDER BY month_start) AS prev_month,
       ROUND(
         100.0 * (complaints - LAG(complaints) OVER (ORDER BY month_start))
         / LAG(complaints) OVER (ORDER BY month_start), 1
       ) AS pct_change
FROM monthly
ORDER BY month_start;
