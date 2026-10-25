-- Absolute and percent change in employment, 2019 → 2021, by industry (Private only)
WITH base AS (
    SELECT i.industry_name,
           MAX(CASE WHEN f.year_key = 2019 THEN f.employment_thousands END) AS emp_2019,
           MAX(CASE WHEN f.year_key = 2021 THEN f.employment_thousands END) AS emp_2021
    FROM employment_fact f
    JOIN industry_dim i ON f.industry_id = i.industry_id
    WHERE f.sector_group = 'Private'
      AND f.year_key IN (2019, 2021)
    GROUP BY i.industry_name
)
SELECT industry_name,
       emp_2019,
       emp_2021,
       emp_2021 - emp_2019 AS abs_change,
       CASE WHEN emp_2019 > 0
            THEN ROUND((emp_2021 - emp_2019) * 100.0 / emp_2019, 1)
       END AS pct_change
FROM base
ORDER BY abs_change;