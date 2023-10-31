from edgar_db.parser import (
    EdgarParser,
    SubmissionParser,
    CoverPageParser,
    OtherManagerParser,
    SignatureParser,
    SummaryPageParser,
    # OtherManager2Parser,
    InfoTableParser,
)

edgar_file_parser: dict[str, type[EdgarParser]] = {
    "SUBMISSION.tsv": SubmissionParser,
    "COVERPAGE.tsv": CoverPageParser,
    "OTHERMANAGER.tsv": OtherManagerParser,
    "SIGNATURE.tsv": SignatureParser,
    "SUMMARYPAGE.tsv": SummaryPageParser,
    ## "OTHERMANAGER2.tsv": OtherManager2Parser,
    "INFOTABLE.tsv": InfoTableParser,
}
