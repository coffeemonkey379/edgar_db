from typing import TypeVar, Optional
from datetime import date
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    MappedAsDataclass,
    Mapped,
)
from sqlalchemy import VARCHAR, CHAR, Integer


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
    amendmenttype: Mapped[Optional[str]] = mapped_column()
    datedeniedexpired: Mapped[Optional[date]]
    datereported: Mapped[Optional[date]]
    reasonfornonconfidentiality: Mapped[Optional[str]] = mapped_column(
        VARCHAR(40), primary_key=True
    )


class OtherManagerOrm(Base):
    __tablename__ = "other_manager"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)


class SignatureOrm(Base):
    __tablename__ = "signature"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)


class SummaryPageOrm(Base):
    __tablename__ = "summary_page"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)


class OtherManager2Orm(Base):
    __tablename__ = "other_manager_2"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)


class InfoTableOrm(Base):
    __tablename__ = "info_table"
    accession_number: Mapped[str] = mapped_column(VARCHAR(25), primary_key=True)
