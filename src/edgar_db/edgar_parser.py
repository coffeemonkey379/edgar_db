from typing import Type

from edgar_db.orm_parser import (
    OrmParser,
    SubmissionOrmParser,
    CoverPageOrmParser,
    OtherManagerOrmParser,
    SignatureParser,
    SummaryPageOrmParser,
    # OtherManager2Parser,
    InfoTableParser,
)


edgar_file_parser: dict[str, Type[OrmParser]] = {
    "SUBMISSION.tsv": SubmissionOrmParser,
    "COVERPAGE.tsv": CoverPageOrmParser,
    "OTHERMANAGER.tsv": OtherManagerOrmParser,
    "SIGNATURE.tsv": SignatureParser,
    "SUMMARYPAGE.tsv": SummaryPageOrmParser,
    ## "OTHERMANAGER2.tsv": OtherManager2Parser,
    "INFOTABLE.tsv": InfoTableParser,
}
