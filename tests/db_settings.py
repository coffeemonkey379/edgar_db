import os
from configparser import ConfigParser

from sqlalchemy import create_engine, text, URL
import pytest

from edgar_db import load_engine_url
from edgar_db.orm_db import Base

db_credentials = os.environ.get("LOCAL_DB")

if db_credentials is None:
    raise ValueError(
        "database credentials should be stored as environment variable "
        "in the format 'user;password'"
    )
username, password = db_credentials.split(";")
settings = ConfigParser()
settings.read("settings.cfg")


@pytest.fixture
def engine_url() -> URL:
    return load_engine_url(username, password)


@pytest.fixture
def engine_db_url() -> URL:
    return load_engine_url(
        username, password, database=settings.get("database", "db_name")
    )


def __build_database__() -> None:
    url = load_engine_url(username, password)
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text(f"COMMIT"))
        conn.execute(text(f"CREATE DATABASE {settings.get('database', 'db_name')}"))
    engine = create_engine(
        url._replace(**{"database": settings.get("database", "db_name")})
    )
    Base.metadata.create_all(engine)


def __delete_database__() -> None:
    url = load_engine_url(username, password)
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text(f"COMMIT"))
        conn.execute(
            text(f"DROP DATABASE {settings.get('database', 'db_name')} WITH (force)")
        )


temp_url_del_me = load_engine_url(
    username, password, database=settings.get("database", "db_name")
)
