import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class FormExtractor:
    def __init__(self, session):
        self.session = session

    def extract_forms(self, url):
        forms = []
        try:
            r = self.session.get(url)
        except Exception:
            return forms

        soup = BeautifulSoup(r.text, "html.parser")

        for f in soup.find_all("form"):
            action = f.get("action") or url
            method = f.get("method", "get").lower()
            fields = {}

            for i in f.find_all("input"):
                name = i.get("name")
                if name:
                    fields[name] = "test"

            forms.append({
                "action": urljoin(url, action),
                "method": method,
                "fields": fields
            })

        return forms