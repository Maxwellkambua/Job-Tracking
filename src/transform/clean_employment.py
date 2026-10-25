"""Clean and normalise raw parsed employment data."""
import re
import pandas as pd
from src.utils.logger import logger

# Canonical KNBS industry labels (adjust as new surveys appear)
CANONICAL_INDUSTRIES = {
    "agriculture, forestry and fishing": "Agriculture, forestry & fishing",
    "agriculture": "Agriculture, forestry & fishing",
    "mining and quarrying": "Mining & quarrying",
    "manufacturing": "Manufacturing",
    "electricity and water supply": "Electricity & water supply",
    "electricity, gas, steam and air conditioning supply": "Electricity & water supply",
    "construction": "Construction",
    "wholesale and retail trade": "Wholesale & retail trade",
    "wholesale and retail trade; repair of motor vehicles": "Wholesale & retail trade",
    "accommodation and food service activities": "Accommodation & food services",
    "accommodation and food services": "Accommodation & food services",
    "transportation and storage": "Transport & storage",
    "transport and storage": "Transport & storage",
    "information and communication": "Information & communication",
    "financial and insurance activities": "Financial & insurance",
    "financial and insurance": "Financial & insurance",
    "real estate activities": "Real estate",
    "real estate": "Real estate",
    "professional, scientific and technical activities": "Professional & technical",
    "administrative and support service activities": "Admin & support services",
    "public administration and defence": "Public administration & defence",
    "public administration": "Public administration & defence",
    "education": "Education",
    "human health and social work activities": "Health & social work",
    "human health and social work": "Health & social work",
    "arts, entertainment and recreation": "Arts & recreation",
    "other service activities": "Other services",
    "activities of households as employers": "Households as employers",
    "activities of extraterritorial organisations": "Extraterritorial orgs",
}

SECTOR_ALIASES = {
    "private": "Private", "priv": "Private",
    "public": "Public", "govt": "Public", "government": "Public",
    "total": "Total", "all": "Total",
}


def normalise_industry(name: str) -> str:
    key = re.sub(r"\s+", " ", str(name)).strip().lower()
    key = re.sub(r"[.;,]", "", key)
    return CANONICAL_INDUSTRIES.get(key, name.strip())


def normalise_sector(sector: str) -> str:
    return SECTOR_ALIASES.get(str(sector).strip().lower(), str(sector).strip())


def clean(df: pd.DataFrame, source_vintage: int) -> pd.DataFrame:
    out = df.copy()
    out["industry_name"] = out["industry_name"].map(normalise_industry)
    out["sector_group"] = out["sector_group"].map(normalise_sector)

    # Drop obvious non-industry rows
    drop_patterns = ("total", "all industries", "memorandum", "note")
    mask = out["industry_name"].str.lower().str.contains("|".join(drop_patterns))
    if mask.any():
        logger.info(f"Dropping {mask.sum()} non-industry rows: "
                    f"{out.loc[mask, 'industry_name'].unique().tolist()}")
    out = out[~mask].copy()

    # Coerce numbers
    out["employment_thousands"] = pd.to_numeric(out["employment_thousands"], errors="coerce")
    out = out.dropna(subset=["employment_thousands"])
    out = out[out["employment_thousands"] >= 0]

    # Add source vintage
    out["source_vintage"] = source_vintage

    logger.info(f"Cleaned to {len(out)} rows across "
                f"{out['industry_name'].nunique()} industries and "
                f"{out['year'].nunique()} years.")
    return out.reset_index(drop=True)