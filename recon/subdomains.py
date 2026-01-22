import requests

COMMON_SUBDOMAINS = [
    "www", "admin", "api", "dev", "test", "staging", "dashboard"
]

class SubdomainScanner:
    def __init__(self, domain, scheme="http"):
        self.domain = domain
        self.scheme = scheme
        self.found = []

    def scan(self):
        for sub in COMMON_SUBDOMAINS:
            url = f"{self.scheme}://{sub}.{self.domain}"
            try:
                r = requests.get(url, timeout=3)
                if r.status_code < 500:
                    self.found.append(url)
            except Exception:
                continue
        return self.found