from datetime import datetime


class Finding:
    """
    Immutable detection result + controlled exploitation metadata
    """

    def __init__(
        self,
        vuln_type,
        url,
        parameter,
        method,
        technique,
        confidence,
        dbms=None,
        authenticated=False
    ):
        self.vuln_type = vuln_type
        self.url = url
        self.parameter = parameter
        self.method = method
        self.technique = technique
        self.confidence = confidence
        self.dbms = dbms
        self.authenticated = authenticated
        self.timestamp = datetime.utcnow()

        self.risk = None

        # -------- Phase 17 Fields --------
        self.point = None
        self.extraction_capable = False
        self.blind_capable = False
        self.extracted_data = None

    def key(self):
        return (self.vuln_type, self.url, self.parameter, self.method)