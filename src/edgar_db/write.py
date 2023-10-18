from typing import Generator, Type
from zipfile import ZipFile

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from edgar_db.orm_parser import OrmParser
from edgar_db.orm_db import Base


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
        file_orm_map: dict[str, Type[OrmParser]],
        engine_str: URL,
    ):
        self.self = self
        self.zip_file = zip_file
        self.file_orm_map = file_orm_map
        self.engine = create_engine(engine_str)
        self.session = sessionmaker(bind=self.engine)

        file_names = list(map(lambda x: x.filename, self.zip_file.infolist()))

        if not all(key in file_names for key in file_orm_map.keys()):
            missing = set(file_orm_map.keys()) - set(file_names)
            raise MissingFileError(
                f"The following files are missing {', '.join(missing)} from zip file {file_names}"
            )

    def __enter__(self):
        self.session = self.session()
        self.session.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.__exit__(exc_type, exc_value, exc_traceback)

    def upload(self):
        for file, orm_map in self.file_orm_map.items():
            for orm in self._construct_orms(file, orm_map):
                self.session.add(orm)
            self.session.flush()
        self.session.commit()

    def _construct_orms(
        self, file: str, orm_parser: OrmParser
    ) -> Generator[Base, None, None]:
        file_value = self.zip_file.open(file)
        headers = self._decode_line(file_value.readline(), lower=True)
        orm_init_order = list(orm_parser.orm.__init__.__code__.co_varnames[1:-1])
        if orm_init_order != headers:
            orm_order = "\n".join(orm_init_order)
            header_order = "\n".join(headers)
            raise OrmOrderError(
                f"\n\nOrder of the ORM {orm_parser.orm} initialisation parameters: \n\n{orm_order}\n\n\n"
                f"is not equal to file {file} header order: \n\n{header_order}"
            )
        for line in file_value.readlines():
            decoded = self._decode_line(line)
            yield orm_parser.parse_to_orm(*decoded)

    def _decode_line(self, line: bytes, lower: bool = False) -> list[str]:
        decoded = line.decode()
        if lower:
            decoded = decoded.lower()
        line_str = decoded.replace("\n", "").split("\t")
        return line_str
