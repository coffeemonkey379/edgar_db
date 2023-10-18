import pytest

from edgar_db.urls import build_sec_url, collect_url_zip, HttpError
from zipfile import ZipFile


@pytest.fixture
def valid_url() -> str:
    url = "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/2013q2_form13f.zip"
    return url


def test_build_sec_url(valid_url) -> None:
    url = build_sec_url(2013, 2)

    assert valid_url == url


def test_collect_url_zip(valid_url) -> None:
    zip_file = collect_url_zip(valid_url)

    assert isinstance(zip_file, ZipFile)
