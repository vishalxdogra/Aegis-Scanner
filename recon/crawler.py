# recon/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class Crawler:
    def __init__(self, base_url, max_depth=2):
        self.base_url = base_url.rstrip("/")
        self.visited = set()
        self.found_urls = set()
        self.max_depth = max_depth

    def crawl(self):
        self._crawl(self.base_url, 0)
        return self.found_urls

    def _crawl(self, url, depth):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            r = requests.get(url, timeout=5)
        except Exception:
            return

        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a["href"])
            if full_url.startswith(self.base_url):
                self.found_urls.add(full_url)
                self._crawl(full_url, depth + 1)