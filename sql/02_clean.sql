DROP TABLE IF EXISTS clean_complaints;

CREATE TABLE clean_complaints AS
SELECT
    complaint_id::BIGINT                              AS complaint_id,
    LEFT(date_received, 10)::DATE                     AS date_received,
    LEFT(date_sent_to_company, 10)::DATE              AS date_sent_to_company,
    product,
    NULLIF(sub_product, 'None')                       AS sub_product,
    issue,
    NULLIF(sub_issue, 'None')                         AS sub_issue,
    company,
    NULLIF(state, 'None')                             AS state,
    CASE WHEN zip_code ~ '^[0-9]{3}'
         THEN LEFT(zip_code, 3) END                   AS zip3,
    (tags LIKE '%Older American%')                    AS is_older_american,
    (tags LIKE '%Servicemember%')                     AS is_servicemember,
    submitted_via,
    NULLIF(company_public_response, 'None')           AS company_public_response,
    company_response,
    (timely_response = 'Yes')                         AS is_timely
FROM raw_complaints;
