# analysis/attack_surface.py
from urllib.parse import urlparse, parse_qs, urlunparse

SQLI_PARAMS = {"id", "uid", "user", "userid", "item", "product"}
LFI_PARAMS  = {"file", "page", "path", "include", "template"}
XSS_PARAMS  = {"q", "search", "query", "msg", "comment", "name"}

SENSITIVE_PATHS = {
    "admin", "login", "console", "setup", "security",
    "phpinfo.php", "config", "dashboard"
}

IGNORE_PATHS = {
    "logout", "delete", "reset", "remove"
}


class AttackSurface:
    def __init__(self, urls):
        self.raw_urls = urls
        self.surface = {
            "sqli": set(),
            "lfi": set(),
            "xss": set(),
            "admin": set(),
            "info": set(),
            "other": set()
        }

    def analyze(self):
        for url in self.raw_urls:
            clean = self._normalize(url)
            parsed = urlparse(clean)
            params = parse_qs(parsed.query)

            # Ignore destructive endpoints
            if any(p in parsed.path.lower() for p in IGNORE_PATHS):
                continue

            # Sensitive paths
            if any(p in parsed.path.lower() for p in SENSITIVE_PATHS):
                self.surface["admin"].add(clean)

            # Parameter-based classification
            for param in params.keys():
                p = param.lower()

                if p in SQLI_PARAMS:
                    self.surface["sqli"].add(clean)
                elif p in LFI_PARAMS:
                    self.surface["lfi"].add(clean)
                elif p in XSS_PARAMS:
                    self.surface["xss"].add(clean)

            # Info disclosure
            if clean.endswith((".md", ".yml", ".yaml")) or "phpinfo.php" in clean:
                self.surface["info"].add(clean)

            # Fallback
            if clean not in self._flatten():
                self.surface["other"].add(clean)

        return self.surface

    def _normalize(self, url):
        parsed = urlparse(url)
        # remove fragment (#...)
        parsed = parsed._replace(fragment="")
        # normalize trailing slash
        path = parsed.path.rstrip("/") or "/"
        parsed = parsed._replace(path=path)
        return urlunparse(parsed)

    def _flatten(self):
        flat = set()
        for group in self.surface.values():
            flat.update(group)
        return flat