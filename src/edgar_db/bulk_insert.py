from typing import Iterator, Optional, Any
import io

import psycopg2

from edgar_db.orm_parser import OrmParser


class StringIteratorIO(io.TextIOBase):
    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ""

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:n]
        self._buff = self._buff[len(ret) :]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                line.append(m)
        return "".join(line)


def bulk_upload(
    connection: psycopg2.extensions.connection,
    table: str,
    lines: Iterator[tuple[str]],
    parser: OrmParser,
    size: int = 8192,
) -> None:
    with connection.cursor() as cursor:
        string_iterator = StringIteratorIO(
            ("\t".join(parser.parse_table_args(*line)) + "\n" for line in lines)
        )
        cursor.copy_from(string_iterator, table, size=size, null="")
