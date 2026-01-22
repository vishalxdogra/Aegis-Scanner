# core/context.py
import requests
from datetime import datetime
from urllib.parse import urlparse


class ScanContext:
    def __init__(
        self,
        target,
        mode="CONTROLLED",
        timeout=8,
        max_urls=150,
        max_depth=2
    ):
        self.target = target
        self.mode = mode
        self.timeout = timeout
        self.max_urls = max_urls
        self.max_depth = max_depth

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ULTIMATE-Scanner/1.0"
        })

        self.start_time = datetime.utcnow()

        self.findings = []
        self.stats = {
            "requests": 0,
            "urls_crawled": 0,
            "forms_tested": 0,
            "errors": 0
        }

    # -------------------------
    # Request wrappers
    # -------------------------
    def get(self, url, **kwargs):
        self._enforce_scope(url)
        self.stats["requests"] += 1
        try:
            return self.session.get(url, timeout=self.timeout, **kwargs)
        except Exception:
            self.stats["errors"] += 1
            return None

    def post(self, url, data=None, **kwargs):
        self._enforce_scope(url)
        self.stats["requests"] += 1
        try:
            return self.session.post(url, data=data, timeout=self.timeout, **kwargs)
        except Exception:
            self.stats["errors"] += 1
            return None

    # -------------------------
    # Scope enforcement
    # -------------------------
    def _enforce_scope(self, url):
        parsed = urlparse(url)
        if parsed.hostname and parsed.hostname != self.target.host:
            raise RuntimeError(f"Out-of-scope request blocked: {url}")

    # -------------------------
    # Findings
    # -------------------------
    def add_finding(self, finding):
        self.findings.append(finding)

    # -------------------------
    # Reporting
    # -------------------------
    def summary(self):
        return {
            "target": str(self.target),
            "mode": self.mode,
            "started": self.start_time.isoformat(),
            "stats": self.stats,
            "findings": len(self.findings)
        }