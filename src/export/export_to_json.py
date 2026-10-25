"""
Export analysis-ready JSON files consumed by the Next.js dashboard.

Output →  web/data/*.json  (committed to git; read at build time by Next.js)
"""
import json
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from config.settings import settings
from src.utils.db import get_engine
from src.utils.logger import logger

OUT_DIR = settings.base_dir / "web" / "data"


def _write(name: str, payload) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, separators=(",", ":"), default=str))
    logger.info(f"Wrote {name}  ({path.stat().st_size:,} bytes)")


def export_all() -> None:
    engine = get_engine()
    with engine.connect() as conn:
        # ── Full timeseries (fact grain) ──────────────────────────────
        ts = pd.read_sql(text("""
            SELECT f.year_key      AS year,
                   i.industry_name AS industry,
                   f.sector_group  AS sector,
                   f.employment_thousands AS value
            FROM employment_fact f
            JOIN industry_dim    i ON f.industry_id = i.industry_id
            ORDER BY year, industry
        """), conn)
        _write("timeseries.json", ts.to_dict(orient="records"))

        # ── KPI snapshot (latest year, sector = Total) ────────────────
        latest_year = int(ts["year"].max())
        latest = ts[(ts["year"] == latest_year) & (ts["sector"] == "Total")]
        prior  = ts[(ts["year"] == latest_year - 1) & (ts["sector"] == "Total")]

        total_now  = float(latest["value"].sum())
        total_prev = float(prior["value"].sum())
        yoy = (total_now - total_prev) / total_prev * 100 if total_prev else 0.0

        macro = conn.execute(text("""
            SELECT overall_unemployment_rate, informal_sector_share_pct
            FROM macro_context WHERE year_key = :y
        """), {"y": latest_year}).fetchone()
        unemp = float(macro[0]) if macro else None
        informal = float(macro[1]) if macro else None

        top_row = latest.sort_values("value", ascending=False).iloc[0]

        _write("kpis.json", {
            "latestYear": latest_year,
            "totalEmploymentThousands": round(total_now, 1),
            "yoyGrowthPct": round(yoy, 2),
            "unemploymentRate": unemp,
            "informalSharePct": informal,
            "topIndustry": top_row["industry"],
            "topIndustryValue": round(float(top_row["value"]), 1),
        })

        # ── Latest-year rankings ─────────────────────────────────────
        ranked = latest.sort_values("value", ascending=False).reset_index(drop=True)
        ranked["rank"] = ranked.index + 1
        ranked["sharePct"] = (ranked["value"] / ranked["value"].sum() * 100).round(2)
        _write("rankings.json", ranked[["rank", "industry", "value", "sharePct"]]
               .rename(columns={"value": "employmentThousands"})
               .to_dict(orient="records"))

        # ── COVID impact snapshot (Private sector) ───────────────────
        covid = pd.read_sql(text("""
            SELECT i.industry_name AS industry,
                   MAX(CASE WHEN f.year_key = 2019 THEN f.employment_thousands END) AS y2019,
                   MAX(CASE WHEN f.year_key = 2020 THEN f.employment_thousands END) AS y2020,
                   MAX(CASE WHEN f.year_key = 2021 THEN f.employment_thousands END) AS y2021,
                   MAX(CASE WHEN f.year_key = :latest THEN f.employment_thousands END) AS latest
            FROM employment_fact f
            JOIN industry_dim i ON f.industry_id = i.industry_id
            WHERE f.sector_group = 'Private'
              AND f.year_key IN (2019, 2020, 2021, :latest)
            GROUP BY i.industry_name
        """), conn, params={"latest": latest_year})

        covid["pctChange"] = (
            (covid["y2021"] - covid["y2019"]) / covid["y2019"] * 100
        ).round(1)

        _write("covid.json", {
            "latestYear": latest_year,
            "snapshot": covid.where(pd.notnull(covid), None).to_dict(orient="records"),
        })

    logger.success("Export complete → web/data/")


if __name__ == "__main__":
    export_all()