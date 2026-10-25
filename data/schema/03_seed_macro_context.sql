-- Seed date dimension
INSERT OR IGNORE INTO date_dim (year_key, decade, is_covid_period) VALUES
(2015, '2010s', 0), (2016, '2010s', 0), (2017, '2010s', 0),
(2018, '2010s', 0), (2019, '2010s', 0), (2020, '2020s', 1),
(2021, '2020s', 1), (2022, '2020s', 0), (2023, '2020s', 0),
(2024, '2020s', 0);

-- Seed macro context — UPDATE with verified KNBS figures before analysis
INSERT OR IGNORE INTO macro_context
    (year_key, overall_unemployment_rate, informal_sector_share_pct, total_wage_employment_k)
VALUES
(2019, 5.0, 83.0, 2900.0),
(2020, 5.7, 84.0, 2800.0),
(2021, 5.5, 84.5, 2850.0),
(2022, 5.3, 83.6, 3000.0),
(2023, 5.0, 83.0, 3150.0),
(2024, 5.0, 82.5, 3250.0);