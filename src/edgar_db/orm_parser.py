from datetime import datetime, date
from abc import abstractmethod, ABC
from typing import Type, overload, Optional, Callable, Union, Literal, Any

from edgar_db.orm_db import (
    Base,
    SubmissionOrm,
    CoverPageOrm,
    OtherManagerOrm,
    SignatureOrm,
    SummaryPageOrm,
    OtherManager2Orm,
    InfoTableOrm,
)


class OrmParser(ABC):
    orm: Type[Base]

    @abstractmethod
    def parse_to_orm(cls, *args, **kwargs) -> Base:
        """_summary_

        Returns:
            Base: _description_
        """
        pass

    @classmethod
    def _orm_parse_attribute_args(cls, attribute: str) -> tuple[str, bool]:
        return (
            getattr(cls.orm, attribute).type.python_type.__name__,
            getattr(cls.orm, attribute).nullable,
        )

    @classmethod
    def _build_orm_init_args(
        cls, func_locals: dict[str, Any]
    ) -> tuple[Optional[Union[str, int, date]]]:
        vars = cls.orm.__init__.__code__.co_varnames[1:-1]
        return tuple(
            map(
                lambda var: cls.parse(
                    func_locals[var], *cls._orm_parse_attribute_args(var)
                ),
                vars,
            )
        )

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
        cls, str_: str, method: Literal["date", "int", "str"], nullable: bool = False
    ) -> Optional[Union[str, date, int]]:
        if (nullable) & (str_ == ""):
            return None
        func_map: dict[str, Callable] = {
            "date": cls.parse_date,
            "int": cls.parse_int,
            "str": lambda x: x,
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
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class CoverPageOrmParser(OrmParser):
    orm = CoverPageOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        reportcalendarorquarter: str,
        isamendment: str,
        amendmentno: str,
        amendmenttype: str,
        confdeniedexpired: str,
        datedeniedexpired: str,
        datereported: str,
        reasonfornonconfidentiality: str,
        filingmanager_name: str,
        filingmanager_street1: str,
        filingmanager_street2: str,
        filingmanager_city: str,
        filingmanager_stateorcountry: str,
        filingmanager_zipcode: str,
        reporttype: str,
        form13ffilenumber: str,
        provideinfoforinstruction5: str,
        additionalinformation: str,
    ) -> CoverPageOrm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class OtherManagerOrmParser(OrmParser):
    orm = OtherManagerOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        othermanager_sk: str,
        cik: str,
        form13ffilenumber: str,
        name: str,
    ) -> OtherManagerOrm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class SignatureParser(OrmParser):
    orm = SignatureOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        name: str,
        title: str,
        phone: str,
        signature: str,
        city: str,
        stateorcountry: str,
        signaturedate: str,
    ) -> SignatureOrm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class SummaryPageOrmParser(OrmParser):
    orm = SummaryPageOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        otherincludedmanagerscount: str,
        tableentrytotal: str,
        tablevaluetotal: str,
        isconfidentialomitted: str,
    ) -> SummaryPageOrm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class OtherManager2Parser(OrmParser):
    orm = OtherManager2Orm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        sequencenumber: str,
        cik: str,
        form13ffilenumber: str,
        name: str,
    ) -> OtherManager2Orm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)


class InfoTableParser(OrmParser):
    orm = InfoTableOrm

    @classmethod
    def parse_to_orm(
        cls,
        accession_number: str,
        infotable_sk: str,
        nameofissuer: str,
        titleofclass: str,
        cusip: str,
        value: str,
        sshprnamt: str,
        sshprnamttype: str,
        putcall: str,
        investmentdiscretion: str,
        othermanager: str,
        voting_auth_sole: str,
        voting_auth_shared: str,
        voting_auth_none: str,
    ) -> InfoTableOrm:
        func_locals = locals()
        args = cls._build_orm_init_args(func_locals)
        return cls.orm(*args)
