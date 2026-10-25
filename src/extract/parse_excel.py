"""
Parse KNBS Chapter 3 Excel to a tidy long-format DataFrame.

The KNBS table (Table 3.2: Wage Employment by Industry and Sector) is
typically published in a wide format, with year blocks as column groups
and Private / Public / Total as sub-columns. This module makes a best-
effort attempt to detect that structure and reshape it. If the layout
differs (KNBS does change it occasionally), we log a clear warning
and dump the sheet preview so the user can adjust.
"""
from pathlib import Path
import pandas as pd
from src.utils.logger import logger

TITLE_KEYWORDS = ("wage employment", "employment by industry")


def find_employment_sheet(xlsx_path: Path) -> str | None:
    """Scan sheet names to find the one containing employment-by-industry."""
    xls = pd.ExcelFile(xlsx_path)
    for name in xls.sheet_names:
        if any(kw in name.lower() for kw in ("3.2", "wage", "employment")):
            return name
    # fallback: inspect first rows of each sheet
    for name in xls.sheet_names:
        head = pd.read_excel(xls, sheet_name=name, header=None, nrows=10)
        flat = head.astype(str).agg(" ".join, axis=1).str.lower().str.cat(sep=" ")
        if any(kw in flat for kw in TITLE_KEYWORDS):
            return name
    return None


def parse_employment_table(
    xlsx_path: Path,
    industry_col: int = 0,
    year_col_start: int | None = None,
) -> pd.DataFrame:
    """
    Returns a long DataFrame with columns:
        industry_name, year, sector_group, employment_thousands
    """
    sheet = find_employment_sheet(xlsx_path)
    if sheet is None:
        raise ValueError(
            f"Could not locate an employment-by-industry sheet in {xlsx_path.name}. "
            "Open the file and verify sheet names."
        )
    logger.info(f"Reading sheet '{sheet}' from {xlsx_path.name}")

    raw = pd.read_excel(xlsx_path, sheet_name=sheet, header=None)
    logger.debug(f"Raw shape: {raw.shape}")

    # Detect header row: first row where >=3 cells look like year values
    header_row = None
    for i in range(min(30, len(raw))):
        vals = pd.to_numeric(raw.iloc[i], errors="coerce")
        if vals.between(2000, 2100).sum() >= 3:
            header_row = i
            break
    if header_row is None:
        logger.warning("Could not detect a year header row — dumping first 20 rows:")
        logger.warning(raw.head(20).to_string())
        raise ValueError("Year header not found — inspect the raw preview above.")

    years = pd.to_numeric(raw.iloc[header_row], errors="coerce")
    logger.info(f"Year header found at row {header_row}: {years.dropna().astype(int).tolist()}")

    # Body starts after the header row
    body = raw.iloc[header_row + 1 :].reset_index(drop=True)
    body = body.dropna(subset=[industry_col])

    # Column mapping: assume the block for each year has 3 sub-columns (Priv/Pub/Total)
    # unless the header row has one column per year.
    sub_groups = ["Private", "Public", "Total"]
    if year_col_start is None:
        # Find first column index where a year value appears in the header
        year_positions = [i for i, v in enumerate(years) if pd.notna(v)]
        if not year_positions:
            raise ValueError("No year positions in header.")
        year_col_start = year_positions[0]

    year_positions = sorted(i for i, v in enumerate(years) if pd.notna(v))
    block = year_positions[1] - year_positions[0] if len(year_positions) > 1 else 3

    records = []
    for _, row in body.iterrows():
        industry = str(row[industry_col]).strip()
        if not industry or industry.lower() in ("nan", "total", "total wage employment"):
            continue
        for ypos in year_positions:
            year = int(years[ypos])
            if block == 1:
                # single column per year = "Total"
                val = pd.to_numeric(row[ypos], errors="coerce")
                if pd.notna(val):
                    records.append(
                        {"industry_name": industry, "year": year,
                         "sector_group": "Total", "employment_thousands": float(val)}
                    )
            else:
                for offset, group in enumerate(sub_groups):
                    col = ypos + offset
                    if col >= len(row):
                        continue
                    val = pd.to_numeric(row[col], errors="coerce")
                    if pd.notna(val):
                        records.append(
                            {"industry_name": industry, "year": year,
                             "sector_group": group, "employment_thousands": float(val)}
                        )

    df = pd.DataFrame(records)
    logger.success(f"Parsed {len(df)} tidy records from {xlsx_path.name}")
    return df


if __name__ == "__main__":
    from config.settings import settings
    files = list(settings.raw_dir.glob("*.xlsx"))
    if not files:
        raise SystemExit("No .xlsx files in data/raw/. Run download_knbs.py first.")
    df = parse_employment_table(files[0])
    print(df.head(15))
    print(df.dtypes)