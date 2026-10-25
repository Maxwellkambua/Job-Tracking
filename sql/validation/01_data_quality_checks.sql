-- 1. Row counts
SELECT 'employment_fact' AS table_name, COUNT(*) AS n FROM employment_fact
UNION ALL SELECT 'industry_dim', COUNT(*) FROM industry_dim
UNION ALL SELECT 'date_dim', COUNT(*) FROM date_dim
UNION ALL SELECT 'macro_context', COUNT(*) FROM macro_context;

-- 2. Year coverage
SELECT MIN(year_key) AS min_year, MAX(year_key) AS max_year,
       COUNT(DISTINCT year_key) AS distinct_years
FROM employment_fact;

-- 3. Orphan FKs
SELECT COUNT(*) AS orphan_industry_rows
FROM employment_fact f
LEFT JOIN industry_dim i ON f.industry_id = i.industry_id
WHERE i.industry_id IS NULL;

-- 4. Negative or extreme values
SELECT COUNT(*) AS bad_values
FROM employment_fact
WHERE employment_thousands < 0 OR employment_thousands > 100000;

-- 5. Duplicate rows
SELECT year_key, industry_id, sector_group, source_vintage, COUNT(*) AS n
FROM employment_fact
GROUP BY year_key, industry_id, sector_group, source_vintage
HAVING COUNT(*) > 1;