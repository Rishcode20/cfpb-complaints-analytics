DROP TABLE IF EXISTS dim_company;
CREATE TABLE dim_company AS
SELECT ROW_NUMBER() OVER (ORDER BY company) AS company_key,
       company AS company_name
FROM (SELECT DISTINCT company FROM clean_complaints) c;

DROP TABLE IF EXISTS dim_issue;
CREATE TABLE dim_issue AS
SELECT ROW_NUMBER() OVER (ORDER BY issue, sub_issue) AS issue_key,
       issue,
       sub_issue
FROM (
    SELECT DISTINCT issue,
           COALESCE(sub_issue, 'Not specified') AS sub_issue
    FROM clean_complaints
) i;
