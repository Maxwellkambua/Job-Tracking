"""Build the industry and date dimensions from cleaned fact data."""
import pandas as pd

# Simple mapping of KNBS industry → ISIC Rev.4 section letter (best effort)
ISIC_MAP = {
    "Agriculture, forestry & fishing": "A",
    "Mining & quarrying": "B",
    "Manufacturing": "C",
    "Electricity & water supply": "D+E",
    "Construction": "F",
    "Wholesale & retail trade": "G",
    "Transport & storage": "H",
    "Accommodation & food services": "I",
    "Information & communication": "J",
    "Financial & insurance": "K",
    "Real estate": "L",
    "Professional & technical": "M",
    "Admin & support services": "N",
    "Public administration & defence": "O",
    "Education": "P",
    "Health & social work": "Q",
    "Arts & recreation": "R",
    "Other services": "S",
    "Households as employers": "T",
    "Extraterritorial orgs": "U",
}


def build_industry_dim(clean_df: pd.DataFrame) -> pd.DataFrame:
    industries = clean_df["industry_name"].drop_duplicates().sort_values()
    dim = pd.DataFrame({"industry_name": industries})
    dim["isic_code"] = dim["industry_name"].map(ISIC_MAP)
    dim["sector_group"] = None  # sector is stored on the fact table
    dim = dim.reset_index(drop=True)
    dim.insert(0, "industry_id", range(1, len(dim) + 1))
    return dim


def build_date_dim(clean_df: pd.DataFrame) -> pd.DataFrame:
    years = sorted(clean_df["year"].dropna().astype(int).unique())
    dim = pd.DataFrame({"year_key": years})
    dim["decade"] = (dim["year_key"] // 10 * 10).astype(str) + "s"
    dim["is_covid_period"] = dim["year_key"].isin([2020, 2021]).astype(int)
    return dim