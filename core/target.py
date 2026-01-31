from urllib.parse import urlparse
import ipaddress

class Target:
    def __init__(self, url):
        self.original = url
        self.parsed = urlparse(url if "://" in url else "http://" + url)

        self.scheme = self.parsed.scheme
        self.host = self.parsed.hostname
        self.port = self.parsed.port or (443 if self.scheme == "https" else 80)

    def base_url(self):
        return f"{self.scheme}://{self.host}:{self.port}"

    def in_scope(self, url):
        """
        Strict application scope:
        - same hostname
        - same scheme
        - same port
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.hostname == self.host
                and parsed.scheme == self.scheme
                and (parsed.port or (443 if parsed.scheme == "https" else 80)) == self.port
            )
        except Exception:
            return False

    def is_local(self):
        try:
            ip = ipaddress.ip_address(self.host)
            return ip.is_private or ip.is_loopback
        except ValueError:
            return self.host in ("localhost",)

    def __repr__(self):
        return f"<Target {self.base_url()}>"