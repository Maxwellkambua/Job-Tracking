-- Dimension: industries (KNBS / ISIC categories)
CREATE TABLE IF NOT EXISTS industry_dim (
    industry_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_name   VARCHAR(150) NOT NULL UNIQUE,
    isic_code       VARCHAR(10),
    sector_group    VARCHAR(20)  -- 'Private' | 'Public' | 'Total'
);

-- Dimension: years
CREATE TABLE IF NOT EXISTS date_dim (
    year_key        INTEGER PRIMARY KEY,
    decade          VARCHAR(10),
    is_covid_period INTEGER DEFAULT 0  -- 1 for 2020-2021
);

-- Fact: annual wage employment (thousands of persons)
CREATE TABLE IF NOT EXISTS employment_fact (
    fact_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    year_key              INTEGER NOT NULL,
    industry_id           INTEGER NOT NULL,
    sector_group          VARCHAR(20) NOT NULL,
    employment_thousands  DECIMAL(10, 1),
    source_vintage        INTEGER,   -- publication year of the source survey
    FOREIGN KEY (year_key)    REFERENCES date_dim(year_key),
    FOREIGN KEY (industry_id) REFERENCES industry_dim(industry_id),
    UNIQUE (year_key, industry_id, sector_group, source_vintage)
);

-- Macro context: overall national indicators
CREATE TABLE IF NOT EXISTS macro_context (
    year_key                    INTEGER PRIMARY KEY,
    overall_unemployment_rate   DECIMAL(4, 1),
    informal_sector_share_pct   DECIMAL(4, 1),
    total_wage_employment_k     DECIMAL(10, 1),
    FOREIGN KEY (year_key) REFERENCES date_dim(year_key)
);