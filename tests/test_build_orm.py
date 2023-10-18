from sqlalchemy import URL
import pytest

from sqlalchemy import inspect, create_engine

from edgar_db.build_orm import (
    database_exists,
    create_postgres_db,
    build_cache,
    NoCacheError,
)
from edgar_db.orm_db import Base

from db_settings import (
    engine_url,
    engine_db_url,
    __delete_database__,
    __build_database__,
)


def tables_built(url) -> bool:
    tables_in_db = inspect(create_engine(url)).get_table_names()
    tables_to_build = list(filter(lambda x: x, Base.metadata.tables.keys()))
    if tables_in_db == tables_to_build:
        return True
    return False


@pytest.mark.xfail(raises=ValueError)
def test_database_exists_db_not_set(engine_url):
    database_exists(engine_url)


def test_database_exists_false(engine_db_url):
    assert database_exists(engine_db_url) is False


@pytest.mark.xfail(raises=ValueError)
def test_create_postgres_db(engine_url):
    create_postgres_db(engine_url)


@pytest.mark.xfail(raises=ValueError)
def test_create_postgres_db_fail(engine_url):
    create_postgres_db(engine_url)


def test_create_postgres_db_success(engine_db_url):
    create_postgres_db(engine_db_url)
    assert tables_built(engine_db_url)
    delete_success = __delete_database__()
    assert delete_success is None


def test_build_cache_success(engine_db_url, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    url = build_cache(engine_db_url)
    assert tables_built(engine_db_url)
    assert isinstance(url, URL)
    delete_success = __delete_database__()
    assert delete_success is None


@pytest.mark.xfail(raises=NoCacheError)
def test_build_cache_fail(engine_db_url, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    build_cache(engine_db_url)


class TestDatabase:
    def setup_class(self):
        __build_database__()

    def test_database_exists_true(self, engine_db_url):
        assert database_exists(engine_db_url) is True

    def test_build_cache_prebuilt_true(self, engine_db_url):
        assert isinstance(build_cache(engine_db_url), URL)

    def teardown_class(self):
        __delete_database__()


@pytest.mark.xfail(raises=ValueError)
def test_build_cache_non_postgres(engine_db_url):
    engine_db_url = engine_db_url._replace(**{"drivername": "sqlite"})
