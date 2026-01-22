# analysis/parameters.py
from urllib.parse import urlparse

COMMON_PARAMS = [
    "id", "uid", "user", "userid", "page", "cat", "category",
    "item", "product", "pid", "ref", "doc", "file", "view"
]

class ParameterDiscovery:
    def __init__(self, urls):
        self.urls = urls

    def discover(self):
        discovered = set()

        for url in self.urls:
            if "?" in url:
                continue

            parsed = urlparse(url)
            if not parsed.path.endswith((".php", ".asp", ".aspx", ".jsp")):
                continue

            for p in COMMON_PARAMS:
                discovered.add(f"{url}?{p}=1")

        return discovered