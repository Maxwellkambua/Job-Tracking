#!/usr/bin/env bash
set -euo pipefail

echo "==> 1/4  Init DB"
python scripts/init_db.py

echo "==> 2/4  Download KNBS files"
python -m src.extract.download_knbs

echo "==> 3/4  Parse + clean + load"
python - <<'PY'
from pathlib import Path
import pandas as pd
from config.settings import settings
from src.extract.parse_excel import parse_employment_table
from src.transform.clean_employment import clean
from src.transform.build_dimensions import build_industry_dim, build_date_dim
from src.load.load_to_db import load_facts
from src.utils.logger import logger

all_cleaned = []
for f in sorted(settings.raw_dir.glob("*.xlsx")):
    vintage = int("".join(c for c in f.stem if c.isdigit())[-4:])
    logger.info(f"Parsing {f.name} (vintage {vintage})")
    try:
        parsed = parse_employment_table(f)
        all_cleaned.append(clean(parsed, source_vintage=vintage))
    except Exception as e:
        logger.warning(f"Skipping {f.name}: {e}")

if not all_cleaned:
    raise SystemExit("No data parsed. Check data/raw/ contents.")

df = pd.concat(all_cleaned, ignore_index=True)
# Keep the latest vintage per (year, industry, sector)
df = df.sort_values("source_vintage").drop_duplicates(
    subset=["year", "industry_name", "sector_group"], keep="last"
)

industry_dim = build_industry_dim(df)
date_dim = build_date_dim(df)
load_facts(df, industry_dim, date_dim)
PY

echo "==> 4/4  Done. Database ready at: $(python -c 'from config.settings import settings; print(settings.db_url)')"

echo "==> 5/5  Export JSON for web dashboard"
python -m src.export.export_to_json