CREATE INDEX IF NOT EXISTS idx_emp_fact_year
    ON employment_fact(year_key);

CREATE INDEX IF NOT EXISTS idx_emp_fact_industry_year
    ON employment_fact(industry_id, year_key);

CREATE INDEX IF NOT EXISTS idx_emp_fact_sector
    ON employment_fact(sector_group);