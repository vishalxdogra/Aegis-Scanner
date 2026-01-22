# core/environment.py
import requests

WAF_KEYWORDS = [
    "cloudflare",
    "akamai",
    "imperva",
    "aws",
    "azure",
    "fastly"
]

class EnvironmentProfile:
    def __init__(self, target):
        self.target = target
        self.headers = {}
        self.waf_detected = False
        self.latency = None

    def analyze(self):
        # Local targets never have WAF
        if self.target.is_local():
            self.waf_detected = False
            self.latency = 0
            return

        try:
            r = requests.get(self.target.base_url(), timeout=5)
            self.headers = r.headers
            self.latency = r.elapsed.total_seconds()

            header_blob = " ".join(
                [str(v).lower() for v in r.headers.values()]
            )

            for waf in WAF_KEYWORDS:
                if waf in header_blob:
                    self.waf_detected = True
                    break

        except Exception:
            # Treat unreachable public targets as restricted
            self.waf_detected = True

    def scan_mode(self):
        if self.target.is_local():
            return "FULL"
        if self.waf_detected:
            return "SAFE"
        return "CONTROLLED"