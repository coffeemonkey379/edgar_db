from typing import Literal

from sqlalchemy import URL

from edgar_db.urls import build_sec_13f_url, collect_url_zip
from edgar_db.edgar_parser import edgar_file_parser
from edgar_db.upload import ZipUploader
from edgar_db.logger import LOGGER


def collect_edgar(year: int, quarter: Literal[1, 2, 3, 4], engine: URL) -> None:
    LOGGER.info(
        f"Starting collecting for year - {year}, quarter - {quarter} to engine {engine}"
    )
    try:
        zip_file = collect_url_zip(build_sec_13f_url(year, quarter))

        build = ZipUploader(zip_file, edgar_file_parser, engine)
        build.upload()
        LOGGER.info(
            f"Successfully collected for year - {year}, quarter - {quarter} to engine {engine}"
        )
    except Exception:
        LOGGER.exception(
            f"Failed to collect for year - {year}, quarter - {quarter} to engine {engine}"
        )
