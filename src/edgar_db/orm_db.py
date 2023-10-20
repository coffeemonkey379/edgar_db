from typing import TypeVar, Optional
from datetime import date
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    MappedAsDataclass,
    Mapped,
)
from sqlalchemy import VARCHAR, CHAR, Integer, BigInteger


class Base(MappedAsDataclass, DeclarativeBase):
    pass


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
    reportcalendarorquarter: Mapped[date]
    isamendment: Mapped[Optional[str]] = mapped_column(CHAR(1))
    amendmentno: Mapped[Optional[int]] = mapped_column(Integer)
    amendmenttype: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    confdeniedexpired: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datedeniedexpired: Mapped[Optional[date]]
    datereported: Mapped[Optional[date]]
    reasonfornonconfidentiality: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_name: Mapped[str] = mapped_column(VARCHAR(150))
    filingmanager_street1: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_street2: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    filingmanager_city: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    filingmanager_stateorcountry: Mapped[Optional[str]] = mapped_column(CHAR(2))
    filingmanager_zipcode: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    reporttype: Mapped[str] = mapped_column(VARCHAR(30))
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
    isconfidentialomitted: Mapped[str] = mapped_column(CHAR(1))


class OtherManager2Orm(Base):
    __tablename__ = "other_manager_2"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    sequencenumber: Mapped[int] = mapped_column(Integer)
    cik: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    form13ffilenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    name: Mapped[str] = mapped_column(VARCHAR(150))


class InfoTableOrm(Base):
    __tablename__ = "info_table"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
    infotable_sk: Mapped[int] = mapped_column(Integer, primary_key=True)
    nameofissuer: Mapped[str] = mapped_column(VARCHAR(200))
    titleofclass: Mapped[str] = mapped_column(VARCHAR(150))
    cusip: Mapped[str] = mapped_column(CHAR(9))
    value: Mapped[int]
    sshprnamt: Mapped[int] = mapped_column(BigInteger)
    sshprnamttype: Mapped[str] = mapped_column(VARCHAR(10))
    putcall: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    investmentdiscretion: Mapped[str] = mapped_column(VARCHAR(10))
    othermanager: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    voting_auth_sole: Mapped[int]
    voting_auth_shared: Mapped[int]
    voting_auth_none: Mapped[int]
