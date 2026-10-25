"""Load cleaned data into the SQL warehouse."""
import pandas as pd
from sqlalchemy import text
from src.utils.db import get_engine, transaction
from src.utils.logger import logger


def _upsert_industry(conn, industry_dim: pd.DataFrame) -> dict[str, int]:
    conn.execute(text("DELETE FROM industry_dim"))
    industry_dim.to_sql("industry_dim", conn, if_exists="append", index=False)
    result = conn.execute(text("SELECT industry_name, industry_id FROM industry_dim"))
    return {name: iid for name, iid in result}


def _upsert_date(conn, date_dim: pd.DataFrame) -> None:
    conn.execute(text("DELETE FROM date_dim"))
    date_dim.to_sql("date_dim", conn, if_exists="append", index=False)


def load_facts(clean_df: pd.DataFrame, industry_dim: pd.DataFrame, date_dim: pd.DataFrame) -> None:
    engine = get_engine()
    with transaction() as conn:
        logger.info("Loading industry_dim...")
        mapping = _upsert_industry(conn, industry_dim)

        logger.info("Loading date_dim...")
        _upsert_date(conn, date_dim)

        logger.info("Loading employment_fact...")
        facts = clean_df.copy()
        facts["industry_id"] = facts["industry_name"].map(mapping)
        facts = facts.dropna(subset=["industry_id"])
        facts["industry_id"] = facts["industry_id"].astype(int)
        facts = facts.rename(columns={"year": "year_key"})
        cols = ["year_key", "industry_id", "sector_group",
                "employment_thousands", "source_vintage"]
        facts = facts[cols]

        # Idempotent load: delete+insert per (year, industry, sector, vintage)
        existing = conn.execute(text("SELECT COUNT(*) FROM employment_fact")).scalar()
        logger.info(f"Existing rows in employment_fact: {existing}")

        # Use temp table for safety
        facts.to_sql("_staging_fact", conn, if_exists="replace", index=False)
        conn.execute(text("""
            INSERT INTO employment_fact
                (year_key, industry_id, sector_group, employment_thousands, source_vintage)
            SELECT year_key, industry_id, sector_group, employment_thousands, source_vintage
            FROM _staging_fact
            WHERE NOT EXISTS (
                SELECT 1 FROM employment_fact f
                WHERE f.year_key = _staging_fact.year_key
                  AND f.industry_id = _staging_fact.industry_id
                  AND f.sector_group = _staging_fact.sector_group
                  AND f.source_vintage = _staging_fact.source_vintage
            )
        """))
        conn.execute(text("DROP TABLE _staging_fact"))
        total = conn.execute(text("SELECT COUNT(*) FROM employment_fact")).scalar()
        logger.success(f"employment_fact now has {total} rows.")