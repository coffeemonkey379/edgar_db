from typing import Generator, Type, Iterable
from zipfile import ZipFile

from sqlalchemy import URL
import psycopg2

from edgar_db.logger import LOGGER
from edgar_db.orm_parser import OrmParser
from edgar_db.bulk_insert import bulk_upload


class MissingFileError(Exception):
    pass


class OrmOrderError(Exception):
    pass


class BuildZipOrm:
    """

    Args:
        zip_file (ZipFile): _description_
        file_orm_map (dict[str, OrmParser]): _description_

    Raises:
        MissingFileError: _description_
    """

    def __init__(
        self,
        zip_file: ZipFile,
        file_orm_map: dict[str, OrmParser],
        engine_str: URL,
    ):
        self.self = self
        self.zip_file = zip_file
        self.file_orm_map = file_orm_map
        self.connection = self._build_psycopg_conn(engine_str)

        file_names = list(map(lambda x: x.filename, self.zip_file.infolist()))

        if not all(key in file_names for key in file_orm_map.keys()):
            missing = set(file_orm_map.keys()) - set(file_names)
            raise MissingFileError(
                f"The following files are missing {', '.join(missing)} from zip file {file_names}"
            )

    def upload(self):
        for file, orm_map in self.file_orm_map.items():
            LOGGER.info(f"Starting upload on {file}")
            self._upload(file, orm_map)
            LOGGER.info(f"Finished upload on {file}")

    def _insert(self, values, parser: OrmParser) -> None:
        bulk_upload(
            self.connection,
            parser.orm.__tablename__,
            map(self._decode_line, values),
            parser,
        )

    def _build_psycopg_conn(self, engine_str: URL) -> psycopg2.extensions.connection:
        kwargs = {}
        kwargs["host"] = engine_str.host
        kwargs["user"] = engine_str.username
        kwargs["password"] = engine_str.password
        kwargs["database"] = engine_str.database
        if engine_str.port:
            kwargs["port"] = engine_str.port
        connection = psycopg2.connect(**kwargs)
        connection.autocommit = True

        return connection

    def _upload(self, file: str, orm_parser: OrmParser) -> None:
        file_value = self.zip_file.open(file)
        headers = self._decode_line(file_value.readline(), lower=True)
        table_args_order = list(orm_parser.parse_table_args.__code__.co_varnames[1:-1])
        if table_args_order != headers:
            args_order = "\n".join(table_args_order)
            header_order = "\n".join(headers)
            raise OrmOrderError(
                f"\n\nOrder of the ORM {orm_parser.orm} initialisation parameters: \n\n{args_order}\n\n\n"
                f"is not equal to file {file} header order: \n\n{header_order}"
            )
        self._insert(file_value, orm_parser)

    def _decode_line(self, line: bytes, lower: bool = False) -> list[str]:
        decoded = line.decode()
        if lower:
            decoded = decoded.lower()
        line_str = decoded.replace("\n", "").split("\t")
        return line_str
