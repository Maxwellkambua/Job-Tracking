"""SQLAlchemy engine + helpers."""
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from config.settings import settings

_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        connect_args = {}
        if settings.db_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        _engine = create_engine(settings.db_url, future=True, connect_args=connect_args)
    return _engine


@contextmanager
def transaction():
    engine = get_engine()
    with engine.begin() as conn:
        yield conn


def execute_sql_file(path):
    """Execute a .sql file against the database."""
    from pathlib import Path
    from src.utils.logger import logger

    path = Path(path)
    logger.info(f"Executing SQL file: {path}")
    sql = path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    with transaction() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
    logger.success(f"Executed {len(statements)} statements from {path.name}")