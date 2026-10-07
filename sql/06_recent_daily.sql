SELECT date_key,
       COUNT(*) AS complaints
FROM fact_complaints
WHERE date_key >= '2026-09-10'
GROUP BY date_key
ORDER BY date_key;
