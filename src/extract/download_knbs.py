"""Download KNBS Economic Survey chapter files."""
from pathlib import Path
import requests
from config.settings import settings
from src.utils.logger import logger


def download_file(url: str, dest: Path, timeout: int = 60) -> Path:
    if dest.exists():
        logger.info(f"Already downloaded: {dest.name} ({dest.stat().st_size:,} bytes)")
        return dest
    logger.info(f"Downloading {url}")
    resp = requests.get(url, timeout=timeout, stream=True,
                        headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    logger.success(f"Saved {dest.name} ({dest.stat().st_size:,} bytes)")
    return dest


def download_all() -> dict[int, Path]:
    """Download every survey URL configured in settings. Returns {year: path}."""
    results: dict[int, Path] = {}
    for year, url in settings.survey_urls.items():
        suffix = Path(url).suffix or ".bin"
        dest = settings.raw_dir / f"economic_survey_{year}{suffix}"
        try:
            results[year] = download_file(url, dest)
        except Exception as e:
            logger.error(f"Failed to download {year}: {e}")
    return results


if __name__ == "__main__":
    out = download_all()
    logger.info(f"Downloaded {len(out)} files")