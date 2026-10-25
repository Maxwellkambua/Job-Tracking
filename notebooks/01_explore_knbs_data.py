"""
Interactive explorer (run as a script for reproducibility, or convert to
Jupyter cells by pasting between the `# %%` markers).
"""
# %% imports
from pathlib import Path
import pandas as pd
from config.settings import settings
from src.extract.parse_excel import parse_employment_table, find_employment_sheet

# %% list raw files
files = sorted(settings.raw_dir.glob("*.xlsx"))
print("Available Excel files:")
for f in files:
    print(" ", f.name, f"({f.stat().st_size:,} bytes)")

# %% inspect sheets in the latest file
if files:
    xls = pd.ExcelFile(files[-1])
    print("\nSheet names in", files[-1].name)
    for s in xls.sheet_names:
        print("  -", s)
    print("\nDetected employment sheet:", find_employment_sheet(files[-1]))

# %% parse and preview
if files:
    df = parse_employment_table(files[-1])
    print("\nShape:", df.shape)
    print("\nSample:")
    print(df.sample(min(10, len(df))).to_string())
    print("\nIndustry names:")
    print(sorted(df["industry_name"].unique()))
    print("\nYears:", sorted(df["year"].unique()))
    print("\nSectors:", df["sector_group"].unique().tolist())