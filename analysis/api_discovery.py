import requests

COMMON_API_PATHS = [
    "/api",
    "/api/v1",
    "/api/v2",
    "/graphql",
    "/auth",
    "/search"
]

class APIDiscovery:
    def discover(self, base_url):
        apis = set()

        for path in COMMON_API_PATHS:
            url = base_url.rstrip("/") + path
            try:
                r = requests.get(url, timeout=4)
                if r.status_code in (200, 401, 403):
                    apis.add(url)
            except Exception:
                continue

        return apis