import re

SQL_ERRORS = re.compile(
    r"SQL syntax|mysql_|mysqli_|SQLSTATE|ORA-\d+|PostgreSQL|SQLite",
    re.IGNORECASE
)

class SQLiEngine:
    def __init__(self, requester):
        self.requester = requester

    def test(self, point):
        base = self.requester.send(point)
        if not base:
            return None

        base_len = len(base.text)

        strategies = [
            self._numeric,
            self._string_single,
            self._string_double
        ]

        for strat in strategies:
            finding = strat(point, base_len)
            if finding:
                return finding

        return None

    # ---------- STRATEGIES ----------

    def _numeric(self, point, base_len):
        t = self.requester.send(point.append(" AND 1=1"))
        f = self.requester.send(point.append(" AND 1=2"))

        if t and f and abs(len(t.text) - len(f.text)) > 80:
            return self._finding(point, "Boolean-based (numeric)")

        if t and SQL_ERRORS.search(t.text):
            return self._finding(point, "Error-based (numeric)")

        return None

    def _string_single(self, point, base_len):
        t = self.requester.send(point.replace("' AND '1'='1"))
        f = self.requester.send(point.replace("' AND '1'='2"))

        if t and f and abs(len(t.text) - len(f.text)) > 80:
            return self._finding(point, "Boolean-based (string)")

        if t and SQL_ERRORS.search(t.text):
            return self._finding(point, "Error-based (string)")

        return None

    def _string_double(self, point, base_len):
        t = self.requester.send(point.replace('" AND "1"="1'))
        f = self.requester.send(point.replace('" AND "1"="2'))

        if t and f and abs(len(t.text) - len(f.text)) > 80:
            return self._finding(point, "Boolean-based (double-quote)")

        if t and SQL_ERRORS.search(t.text):
            return self._finding(point, "Error-based (double-quote)")

        return None

    def _finding(self, point, technique):
        return {
            "type": "SQLi",
            "url": point.url,
            "parameter": point.target_param,
            "method": point.method.upper(),
            "confidence": "High",
            "technique": technique
        }