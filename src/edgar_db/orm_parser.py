from datetime import datetime, date
from abc import abstractmethod, ABC
from typing import Type, overload, Optional, Callable, Literal, Callable, Protocol
from collections import defaultdict


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
    def parse_table_args(cls, *args, **kwargs) -> tuple[str]:
        """_summary_

        Returns:
            Base: _description_
        """
        pass

    @classmethod
    def _parse_attribute_args(cls, attribute: str) -> tuple[str, bool]:
        return (
            getattr(cls.orm, attribute).type.python_type.__name__,
            getattr(cls.orm, attribute).nullable,
        )

    @classmethod
    def _build_table_args(cls, func_locals: dict[str, str]) -> tuple[str]:
        vars: tuple[str] = cls.orm.__init__.__code__.co_varnames[1:-1]
        parse_func: Callable[[str], str] = lambda var: cls._parse(
            func_locals[var], *cls._parse_attribute_args(var)
        )
        table_args = tuple(map(parse_func, vars))
        return table_args

    @classmethod
    def _parse(cls, str_: str, method: str, nullable: bool = False) -> str:
        if (nullable) & (str_ == ""):
            return str_
        func_map: defaultdict[str, Callable[[str], str]] = defaultdict(
            lambda: lambda x: x.replace("\\", "/")
        )
        func_map["date"] = cls.parse_date
        res = func_map[method](str_)
        return res

    @classmethod
    def parse_date(cls, date_str: str) -> str:
        return datetime.strptime(date_str, "%d-%b-%Y").date().isoformat()


class SubmissionOrmParser(OrmParser):
    orm = SubmissionOrm

    @classmethod
    def parse_table_args(
        cls,
        accession_number: str,
        filing_date: str,
        submissiontype: str,
        cik: str,
        periodofreport: str,
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class CoverPageOrmParser(OrmParser):
    orm = CoverPageOrm

    @classmethod
    def parse_table_args(
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
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class OtherManagerOrmParser(OrmParser):
    orm = OtherManagerOrm

    @classmethod
    def parse_table_args(
        cls,
        accession_number: str,
        othermanager_sk: str,
        cik: str,
        form13ffilenumber: str,
        name: str,
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class SignatureParser(OrmParser):
    orm = SignatureOrm

    @classmethod
    def parse_table_args(
        cls,
        accession_number: str,
        name: str,
        title: str,
        phone: str,
        signature: str,
        city: str,
        stateorcountry: str,
        signaturedate: str,
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class SummaryPageOrmParser(OrmParser):
    orm = SummaryPageOrm

    @classmethod
    def parse_table_args(
        cls,
        accession_number: str,
        otherincludedmanagerscount: str,
        tableentrytotal: str,
        tablevaluetotal: str,
        isconfidentialomitted: str,
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class OtherManager2Parser(OrmParser):
    orm = OtherManager2Orm

    @classmethod
    def parse_table_args(
        cls,
        accession_number: str,
        sequencenumber: str,
        cik: str,
        form13ffilenumber: str,
        name: str,
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)


class InfoTableParser(OrmParser):
    orm = InfoTableOrm

    @classmethod
    def parse_table_args(
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
    ) -> tuple[str]:
        func_locals = locals()
        return cls._build_table_args(func_locals)
