-- Share of private formal employment by industry in the latest year
SELECT
    i.industry_name,
    f.employment_thousands,
    ROUND(
        100.0 * f.employment_thousands /
        SUM(f.employment_thousands) OVER (), 2
    ) AS share_pct
FROM employment_fact f
JOIN industry_dim i ON f.industry_id = i.industry_id
WHERE f.sector_group = 'Private'
  AND f.year_key = (SELECT MAX(year_key) FROM employment_fact)
ORDER BY share_pct DESC;