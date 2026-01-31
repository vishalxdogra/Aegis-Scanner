import re

DBMS_SIGNATURES = {
    "MySQL": [
        r"mysql", r"mysqli", r"you have an error in your sql syntax"
    ],
    "PostgreSQL": [
        r"postgresql", r"pg_query", r"pg_exec"
    ],
    "MSSQL": [
        r"sql server", r"unclosed quotation mark", r"microsoft ole db"
    ],
    "Oracle": [
        r"ora-\d+", r"oracle error"
    ]
}

class DBMSFingerprinter:
    @staticmethod
    def detect(text):
        if not text:
            return "Unknown"

        text = text.lower()
        for dbms, patterns in DBMS_SIGNATURES.items():
            for p in patterns:
                if re.search(p, text):
                    return dbms

        return "Unknown"