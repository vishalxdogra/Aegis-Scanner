import re
import requests

ENDPOINT_REGEX = re.compile(
    r"""["'](\/api\/[^"' ]+|\/v\d+\/[^"' ]+|\/[^"' ]+\.php[^"' ]*)["']"""
)

class JSEndpointExtractor:
    def extract(self, js_url):
        endpoints = set()

        try:
            r = requests.get(js_url, timeout=5)
            if r.status_code != 200:
                return endpoints
        except Exception:
            return endpoints

        for match in ENDPOINT_REGEX.findall(r.text):
            endpoints.add(match)

        return endpoints