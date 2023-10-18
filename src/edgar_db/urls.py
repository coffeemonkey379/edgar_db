from typing import Literal, Optional
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

from sqlalchemy import URL


def build_sec_url(year: int, quarter: Literal[1, 2, 3, 4]) -> str:
    """Builds URL for SEC 13-f zip file.

    Args:
        year (int): Year to collect zip file for.
        quarter (Literal[1, 2, 3,4]): Quarter to collect zip file for.

    Returns:
        str: URL for a zip file of SEC 13-f database for a specific year and quarter.
    """
    sec_url = "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/"
    return f"{sec_url}{year}q{quarter}_form13f.zip"


class HttpError(Exception):
    pass


def collect_url_zip(url: str) -> ZipFile:
    """Collects zip file from URL.

    Args:
        url (str): URL containing zip file.

    Raises:
        HttpError: URL response status not 200

    Returns:
        ZipFile: zip file from URL.
    """
    with urlopen(url) as response:
        content = response.read()
    return ZipFile(BytesIO(content))

def load_engine_url(
    user: str,
    password: str,
    ip: str = "localhost",
    port: Optional[int] = None,
    database: Optional[str] = None,
    driver: str = "postgresql"
) -> URL:
    return URL.create(driver, user, password, ip, port, database)
