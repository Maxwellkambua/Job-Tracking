"""Central configuration. Loads values from environment."""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_url: str = Field(default="sqlite:///data/kenya_employment.db", alias="DB_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    base_dir: Path = Path(__file__).resolve().parent.parent
    raw_dir: Path = base_dir / "data" / "raw"
    processed_dir: Path = base_dir / "data" / "processed"
    schema_dir: Path = base_dir / "data" / "schema"

    # Known local filenames → year mapping used by downloader
    # Keys are the *Economic Survey year* (i.e., the publication year)
    survey_urls: dict[int, str] = {
        2023: "https://www.knbs.or.ke/wp-content/uploads/2023/05/2023-Economic-Survey-1.pdf",
        2024: "https://www.knbs.or.ke/wp-content/uploads/2024/05/2024-Economic-Survey.pdf",
        2025: "https://www.knbs.or.ke/wp-content/uploads/2025/05/Chapter-3-Employment-Earnings-and-Consumer-Price-Indices.xlsx",
    }


settings = Settings()

# Ensure directories exist
for d in (settings.raw_dir, settings.processed_dir, settings.schema_dir):
    d.mkdir(parents=True, exist_ok=True)