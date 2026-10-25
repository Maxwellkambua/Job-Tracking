-- Total formal wage employment by industry (latest available year, "Total" sector)
SELECT
    i.industry_name,
    i.isic_code,
    f.employment_thousands
FROM employment_fact f
JOIN industry_dim i ON f.industry_id = i.industry_id
WHERE f.sector_group = 'Total'
  AND f.year_key = (SELECT MAX(year_key) FROM employment_fact)
ORDER BY f.employment_thousands DESC;