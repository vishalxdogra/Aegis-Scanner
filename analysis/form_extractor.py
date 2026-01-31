import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class FormExtractor:
    """
    Extracts HTML forms and converts them into POST InjectionPoints.
    """

    def __init__(self, session):
        self.session = session

    def extract(self, url):
        try:
            r = self.session.get(url, timeout=6)
        except Exception:
            return []

        if "text/html" not in r.headers.get("Content-Type", ""):
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        forms = []

        for form in soup.find_all("form"):
            action = form.get("action") or url
            method = form.get("method", "GET").upper()
            target_url = urljoin(url, action)

            params = {}
            for inp in form.find_all("input"):
                name = inp.get("name")
                if name:
                    params[name] = inp.get("value", "1")

            if params:
                forms.append((target_url, method, params))

        return forms