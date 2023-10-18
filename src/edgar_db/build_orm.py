from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import OperationalError

from edgar_db.orm_db import Base


def database_exists(url: URL) -> bool:
    """Finds if database

    Args:
        eng_str (str): _description_

    Returns:
        bool: _description_
    """
    db_name = url.database
    if db_name is None:
        raise ValueError(f"url database name must be set!")
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            conn.execute(text(f"COMMIT"))
    except OperationalError:
        return False
    return True


def create_postgres_db(url: URL) -> None:
    db_name = url.database
    if db_name is None:
        raise ValueError(f"url database name must be set!")
    engine = create_engine(url._replace(**{"database": None}))
    with engine.connect() as conn:
        conn.execute(text(f"COMMIT"))
        conn.execute(text(f"CREATE DATABASE {db_name}"))
    Base.metadata.create_all(create_engine(url))


class NoCacheError(Exception):
    pass


def build_cache(url: URL) -> URL:
    if url.get_backend_name() != "postgresql":
        raise ValueError(
            f"eng_str should be a sqlalchemy compliant for postgresql i.e.\n\n"
            f"For postgresql - ' postgresql://user:password@ip:port/database ' \n\n"
        )
    if database_exists(url):
        return url
    msg = "Are you sure you'd like to build a new cache? If so press y, then enter\n"
    if input(msg).lower() == "y":
        create_postgres_db(url)
        return url
    raise NoCacheError("No cache created!")
