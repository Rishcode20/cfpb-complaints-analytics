ALTER TABLE dim_company     ADD PRIMARY KEY (company_key);
ALTER TABLE dim_issue       ADD PRIMARY KEY (issue_key);
ALTER TABLE dim_date        ADD PRIMARY KEY (date_key);
ALTER TABLE fact_complaints ADD PRIMARY KEY (complaint_id);

CREATE INDEX idx_dim_company_name   ON dim_company (company_name);
CREATE INDEX idx_fact_company_date  ON fact_complaints (company_key, date_key);
CREATE INDEX idx_fact_issue         ON fact_complaints (issue_key);

VACUUM ANALYZE fact_complaints;
VACUUM ANALYZE dim_company;
