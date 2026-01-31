import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import warnings

warnings.filterwarnings("ignore")


class Crawler:
    """
    Crawl URLs AND extract HTML forms.
    Phase-11 compliant crawler.
    """

    def __init__(self, base_url, max_depth=2):
        self.base_url = base_url.rstrip("/")
        self.max_depth = max_depth
        self.visited = set()
        self.urls = set()
        self.forms = []

    def crawl(self):
        self._crawl(self.base_url, 0)

        # SAFETY NET
        if not self.urls:
            self.urls.add(self.base_url)

        return self.urls, self.forms

    def _crawl(self, url, depth):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            r = requests.get(url, timeout=6, verify=False)
        except Exception:
            return

        self.urls.add(url)

        if "text/html" not in r.headers.get("Content-Type", ""):
            return

        soup = BeautifulSoup(r.text, "html.parser")

        # ---------- LINK DISCOVERY ----------
        for a in soup.find_all("a", href=True):
            full = urljoin(url, a["href"])
            if self._in_scope(full):
                self._crawl(full, depth + 1)

        # ---------- FORM EXTRACTION ----------
        for form in soup.find_all("form"):
            action = form.get("action") or url
            method = form.get("method", "GET").upper()
            target = urljoin(url, action)

            params = {}
            for inp in form.find_all("input"):
                name = inp.get("name")
                if name:
                    params[name] = inp.get("value", "1")

            if params:
                self.forms.append({
                    "url": target,
                    "method": method,
                    "params": params
                })

    def _in_scope(self, url):
        try:
            return urlparse(url).hostname == urlparse(self.base_url).hostname
        except Exception:
            return False