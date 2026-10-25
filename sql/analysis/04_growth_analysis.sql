-- CAGR of private wage employment per industry, 2015 → latest year
WITH bounds AS (
    SELECT MIN(year_key) AS y0, MAX(year_key) AS y1 FROM employment_fact
),
base AS (
    SELECT i.industry_name,
           MAX(CASE WHEN f.year_key = (SELECT y0 FROM bounds) THEN f.employment_thousands END) AS emp_start,
           MAX(CASE WHEN f.year_key = (SELECT y1 FROM bounds) THEN f.employment_thousands END) AS emp_end
    FROM employment_fact f
    JOIN industry_dim i ON f.industry_id = i.industry_id
    WHERE f.sector_group = 'Private'
    GROUP BY i.industry_name
)
SELECT industry_name,
       emp_start,
       emp_end,
       ROUND(
           (POWER(emp_end * 1.0 / NULLIF(emp_start, 0),
                  1.0 / NULLIF((SELECT y1 - y0 FROM bounds), 0)) - 1) * 100,
           2
       ) AS cagr_pct
FROM base
WHERE emp_start IS NOT NULL AND emp_end IS NOT NULL AND emp_start > 0
ORDER BY cagr_pct DESC;