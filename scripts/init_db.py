"""Create tables and run seed scripts."""
from config.settings import settings
from src.utils.db import execute_sql_file
from src.utils.logger import logger


def init():
    for sql_file in sorted(settings.schema_dir.glob("*.sql")):
        execute_sql_file(sql_file)


if __name__ == "__main__":
    init()
    logger.success("Database initialised.")