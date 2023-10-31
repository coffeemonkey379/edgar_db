from typing import Optional
from datetime import date

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    MappedAsDataclass,
    Mapped,
)
from sqlalchemy import VARCHAR, CHAR, Integer, BigInteger, URL, DATE, ForeignKey, Index
import psycopg2
from sqlalchemy import URL


def load_engine_url(
    user: str,
    password: str,
    ip: str = "localhost",
    port: Optional[int] = None,
    database: Optional[str] = None,
    driver: str = "postgresql",
) -> URL:
    return URL.create(driver, user, password, ip, port, database)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


def build_psycopg_conn(engine_str: URL) -> psycopg2.extensions.connection:
    kwargs = {}
    kwargs["host"] = engine_str.host
    kwargs["user"] = engine_str.username
    kwargs["password"] = engine_str.password
    kwargs["database"] = engine_str.database
    if engine_str.port:
        kwargs["port"] = str(engine_str.port)
    connection = psycopg2.connect(**kwargs)
    connection.autocommit = True

    return connection


class SubmissionOrm(Base):
    __tablename__ = "submission"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    filing_date: Mapped[date]
    submissiontype: Mapped[str] = mapped_column(VARCHAR(10))
    cik: Mapped[str] = mapped_column(VARCHAR(10))
    periodofreport: Mapped[date]


class CoverPageOrm(Base):
    __tablename__ = "cover_page"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    reportcalendarorquarter: Mapped[date] = mapped_column(DATE, index=True)
    isamendment: Mapped[Optional[str]] = mapped_column(CHAR(1))
    amendmentno: Mapped[Optional[int]] = mapped_column(Integer)
    amendmenttype: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    confdeniedexpired: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datedeniedexpired: Mapped[Optional[date]]
    datereported: Mapped[Optional[date]]
    reasonfornonconfidentiality: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_name: Mapped[str] = mapped_column(VARCHAR(150), index=True)
    filingmanager_street1: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_street2: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_city: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    filingmanager_stateorcountry: Mapped[Optional[str]] = mapped_column(CHAR(2))
    filingmanager_zipcode: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    reporttype: Mapped[str] = mapped_column(VARCHAR(30), index=True)
    form13ffilenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    provideinfoforinstruction5: Mapped[str] = mapped_column(VARCHAR(1))
    additionalinformation: Mapped[Optional[str]]


class OtherManagerOrm(Base):
    __tablename__ = "other_manager"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    othermanager_sk: Mapped[int] = mapped_column(Integer, primary_key=True)
    cik: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    form13ffilenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    name: Mapped[str] = mapped_column(VARCHAR(150))


class SignatureOrm(Base):
    __tablename__ = "signature"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(150))
    title: Mapped[str] = mapped_column(VARCHAR(60))
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    signature: Mapped[str] = mapped_column(VARCHAR(150))
    city: Mapped[str] = mapped_column(VARCHAR(30))
    stateorcountry: Mapped[str] = mapped_column(CHAR(2))
    signaturedate: Mapped[date]


class SummaryPageOrm(Base):
    __tablename__ = "summary_page"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    otherincludedmanagerscount: Mapped[Optional[int]]
    tableentrytotal: Mapped[Optional[int]]
    tablevaluetotal: Mapped[Optional[int]] = mapped_column(BigInteger)
    isconfidentialomitted: Mapped[Optional[str]] = mapped_column(CHAR(1))


class OtherManager2Orm(Base):
    __tablename__ = "other_manager_2"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    sequencenumber: Mapped[int] = mapped_column(Integer)
    cik: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    form13ffilenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    name: Mapped[str] = mapped_column(VARCHAR(150))


class InfoTableOrm(Base):
    __tablename__ = "info_table"
    accession_number: Mapped[str] = mapped_column(
        VARCHAR(25), ForeignKey(column="cover_page.accession_number"), primary_key=True
    )
    infotable_sk: Mapped[int] = mapped_column(Integer, primary_key=True)
    nameofissuer: Mapped[str] = mapped_column(VARCHAR(200), index=True)
    titleofclass: Mapped[str] = mapped_column(VARCHAR(150), index=True)
    cusip: Mapped[str] = mapped_column(CHAR(9), index=True)
    value: Mapped[int] = mapped_column(BigInteger)
    sshprnamt: Mapped[int] = mapped_column(BigInteger)
    sshprnamttype: Mapped[str] = mapped_column(VARCHAR(10))
    putcall: Mapped[Optional[str]] = mapped_column(VARCHAR(10), index=True)
    investmentdiscretion: Mapped[str] = mapped_column(VARCHAR(10))
    othermanager: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    voting_auth_sole: Mapped[int] = mapped_column(BigInteger)
    voting_auth_shared: Mapped[int] = mapped_column(BigInteger)
    voting_auth_none: Mapped[int] = mapped_column(BigInteger)

    __table_args__ = (
        Index(
            "accession_number",
            "infotable_sk",
            postgresql_using="BRIN",
        ),
    )
