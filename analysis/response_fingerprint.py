import re
import difflib
import json

# ==================================================
# GENERIC SQL ERROR PATTERNS (DB-AGNOSTIC)
# ==================================================

SQL_ERROR_PATTERN = re.compile(
    r"sql syntax|mysql_|mysqli_|sqlstate|ora-\d+|postgresql|sqlite|odbc|sql server",
    re.I
)


class ResponseFingerprint:
    """
    Production-grade HTTP response fingerprint.

    Supports:
    - HTML responses (templates, legacy apps)
    - JSON APIs (Node, Django, Flask, FastAPI)
    - Text fallbacks

    Used for semantic SQLi detection.
    """

    def __init__(self, response):
        self.response = response
        self.text = response.text if response else ""
        self.length = len(self.text)
        self.lines = self.text.count("\n")

        self.content_type = self._detect_content_type(response)
        self.normalized = self._normalize(self.text)
        self._data_sig = self._extract_data_signature()

    # ==================================================
    # CONTENT TYPE DETECTION
    # ==================================================

    def _detect_content_type(self, response):
        if not response:
            return "text"

        ct = response.headers.get("Content-Type", "").lower()

        if "application/json" in ct:
            return "json"
        if "text/html" in ct:
            return "html"

        if self.text.strip().startswith(("{", "[")):
            return "json"

        return "text"

    # ==================================================
    # NORMALIZATION
    # ==================================================

    def _normalize(self, text):
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[a-f0-9]{32}", "", text)
        return text.strip()

    # ==================================================
    # SEMANTIC SIGNATURE EXTRACTION
    # ==================================================

    def _extract_data_signature(self):
        if self.content_type == "json":
            return self._json_signature()
        if self.content_type == "html":
            return self._html_signature()
        return self._text_signature()

    # ---------------- JSON SIGNATURE ----------------

    def _json_signature(self):
        try:
            data = json.loads(self.text)
        except Exception:
            return ("invalid_json",)

        return self._flatten_json(data)

    def _flatten_json(self, obj):
        if isinstance(obj, dict):
            return tuple(
                sorted((k, self._flatten_json(v)) for k, v in obj.items())
            )
        if isinstance(obj, list):
            return tuple(self._flatten_json(v) for v in obj)
        return str(type(obj).__name__)

    # ---------------- HTML SIGNATURE ----------------

    def _html_signature(self):
        sig = []
        sig.append(len(re.findall(r"<tr\b", self.text, re.I)))
        sig.append(len(re.findall(r"<li\b", self.text, re.I)))
        sig.append(len(re.findall(r"<table\b", self.text, re.I)))
        sig.append(len(re.findall(r"\b(id|name|email|user|title)\b", self.text, re.I)))
        sig.append(len(re.findall(r"warning|error|exception", self.text, re.I)))
        return tuple(sig)

    # ---------------- TEXT FALLBACK ----------------

    def _text_signature(self):
        tokens = re.findall(r"[a-zA-Z0-9_]{3,}", self.text)
        return tuple(sorted(set(tokens[:50])))

    # ==================================================
    # PUBLIC API
    # ==================================================

    def data_signature(self):
        return self._data_sig

    def similarity(self, other):
        if not other:
            return 0.0

        return difflib.SequenceMatcher(
            None,
            self.normalized,
            other.normalized
        ).ratio()

    def has_sql_error(self):
        return bool(SQL_ERROR_PATTERN.search(self.text))

    def looks_empty(self):
        return self.length < 200 or self.lines < 5

    def significant_length_diff(self, other, ratio=0.30):
        if not other or not other.length:
            return False

        return abs(self.length - other.length) / other.length > ratio

    def has_visible_data(self):
        """
        Detects presence of actual data values (not labels).
        Works for HTML & JSON.
        """
        if self.content_type == "json":
            try:
                data = json.loads(self.text)
                return bool(data)
            except Exception:
                return False

        return bool(re.search(
            r"(id|name|email|user)\s*[:=]\s*[a-zA-Z0-9]",
            self.text,
            re.I
        ))