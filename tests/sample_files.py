import pytest

from zipfile import ZipFile
from edgar_db.edgar_parser import edgar_file_parser
from edgar_db.upload import BuildZipOrm
from edgar_db.orm_parser import CoverPageEdgarParser
from db_settings import temp_url_del_me, __build_database__, __delete_database__
from edgar_db.bulk_insert import StringIteratorIO

__build_database__()

zip_file = ZipFile(r"2023q3_form13f.zip")

build_zip = BuildZipOrm(zip_file, edgar_file_parser, temp_url_del_me)

coverpage = zip_file.open("COVERPAGE.tsv")

header = build_zip._decode_line(coverpage.readline())

with build_zip.connection.cursor() as cursor:
    string_iterator = StringIteratorIO(
        (
            "\t".join(CoverPageEdgarParser.parse_table_args(*line)) + "\n"
            for line in map(build_zip._decode_line, coverpage)
        )
    )
    cursor.copy_from(
        string_iterator,
        CoverPageEdgarParser.orm.__tablename__,
        sep="\t",
        null="",
    )


coverpage = zip_file.open("COVERPAGE.tsv")
coverpage.readline()
test = StringIteratorIO(
    "\t".join(CoverPageEdgarParser.parse_table_args(*line)) + "\n"
    for line in map(build_zip._decode_line, coverpage)
)

result = test.read()

"\MO".replace("\\", "/")

result.split("\n")[816].split("\t").__len__()

test = list(map(lambda z: len(z.split("\t")), result.split("\n")[:-1]))
max(test)

result.split("\n")[816].split("\t").__len__()

result.split("\n")[test.index(max(test))]


__delete_database__()
