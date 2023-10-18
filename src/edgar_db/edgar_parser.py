from typing import Type

from edgar_db.orm_parser import SubmissionOrmParser, OrmParser

edgar_file_parser: dict[str, Type[OrmParser]] = {"SUBMISSION.tsv": SubmissionOrmParser}
