from datetime import datetime, date
from abc import abstractmethod, ABC
from typing import Type, overload, Optional, Callable, Union, Literal

from edgar_db.orm_db import SubmissionOrm, Base


class OrmParser(ABC):
    orm: Type[Base]

    @abstractmethod
    def parse_to_orm(cls, *args, **kwargs) -> Base:
        """_summary_

        Returns:
            Base: _description_
        """
        pass

    @overload
    @classmethod
    def parse(
        cls, str_: str, method: Literal["date"], nullable: Literal[False] = ...
    ) -> date:
        ...

    @overload
    @classmethod
    def parse(
        cls, str_: str, method: Literal["date"], nullable: Literal[True]
    ) -> Optional[date]:
        ...

    @overload
    @classmethod
    def parse(
        cls, str_: str, method: Literal["int"], nullable: Literal[False] = ...
    ) -> int:
        ...

    @overload
    @classmethod
    def parse(
        cls, str_: str, method: Literal["int"], nullable: Literal[True]
    ) -> Optional[int]:
        ...

    @classmethod
    def parse(
        cls, str_: str, method: Literal["date", "int"], nullable: bool = False
    ) -> Optional[Union[str, date, int]]:
        if (nullable) & (str_ == ""):
            return None
        func_map: dict[str, Callable] = {
            "date": cls.parse_date,
            "int": cls.parse_int,
        }
        res = func_map[method](str_)
        return res

    @classmethod
    def parse_date(cls, date_str: str) -> date:
        return datetime.strptime(date_str, "%d-%b-%Y").date()

    @classmethod
    def parse_int(cls, str_: str) -> int:
        return int(str_)


class SubmissionOrmParser(OrmParser):
    orm = SubmissionOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        filing_date: str,
        submissiontype: str,
        cik: str,
        periodofreport: str,
    ) -> SubmissionOrm:
        return cls.orm(
            accession_number,
            cls.parse(filing_date, "date", nullable=False),
            submissiontype,
            cik,
            cls.parse(periodofreport, "date"),
        )
