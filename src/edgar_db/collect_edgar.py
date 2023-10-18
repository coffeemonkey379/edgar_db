from typing import Literal

from sqlalchemy import URL

from edgar_db.urls import build_sec_url, collect_url_zip
from edgar_db.edgar_parser import edgar_file_parser
from edgar_db.write import BuildZipOrm


def collect_edgar(year: int, quarter: Literal[1, 2, 3, 4], engine_str: URL) -> None:
    zip_file = collect_url_zip(build_sec_url(year, quarter))

    with BuildZipOrm(zip_file, edgar_file_parser, engine_str) as ZipOrm:
        ZipOrm.upload()
