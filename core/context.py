import requests
from datetime import datetime


class ScanContext:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ULTIMATE-Scanner/1.0"
        })

        self.findings = []
        self.is_authenticated = False
        self.stats = {"requests": 0, "errors": 0}
        self.started = datetime.utcnow()

    def get(self, url, **kwargs):
        if not self.target.in_scope(url):
            return None

        self.stats["requests"] += 1
        try:
            r = self.session.get(url, timeout=8, allow_redirects=True, **kwargs)
            return r
        except Exception:
            self.stats["errors"] += 1
            return None

    def post(self, url, data=None, **kwargs):
        if not self.target.in_scope(url):
            return None

        self.stats["requests"] += 1
        try:
            return self.session.post(url, data=data, timeout=8, allow_redirects=True, **kwargs)
        except Exception:
            self.stats["errors"] += 1
            return None

    def add_finding(self, finding):
        self.findings.append(finding)

    def summary(self):
        return {
            "target": str(self.target),
            "started": self.started.isoformat(),
            "requests": self.stats["requests"],
            "errors": self.stats["errors"],
            "findings": len(self.findings),
            "authenticated": self.is_authenticated
        }