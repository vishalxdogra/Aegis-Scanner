from urllib.parse import urlparse, parse_qs
from core.injection_point import InjectionPoint
import requests


class InjectionPointFactory:
    """
    Builds InjectionPoint objects while PRESERVING
    the full original request structure.
    """

    # ----------------------------------------
    # URL / QUERY BASED
    # ----------------------------------------
    @staticmethod
    def from_url(url):
        parsed = urlparse(url)
        base = parsed._replace(query="").geturl()
        params = parse_qs(parsed.query)

        points = []

        if not params:
            return points  # ❗ never invent params

        # Preserve ALL params, inject ONE at a time
        normalized = {
            k: v[0] if isinstance(v, list) else v
            for k, v in params.items()
        }

        for target in normalized:
            points.append(
                InjectionPoint(
                    url=base,
                    method="GET",
                    target_param=target,
                    params=normalized,
                    content_type="query"
                )
            )
        print("[DEBUG][IP]",
        base,
        "target=", target,
        "params=", normalized)
        return points
        
    # ----------------------------------------
    # HTML FORMS
    # ----------------------------------------
    @staticmethod
    def from_form(form):
        """
        form = {
            "url": str,
            "method": "GET" | "POST",
            "params": { name: value }
        }
        """
        points = []

        if not form.get("params"):
            return points

        for target in form["params"]:
            points.append(
                InjectionPoint(
                    url=form["url"],
                    method=form["method"],
                    target_param=target,
                    params=form["params"],  # FULL param set
                    content_type="form"
                )
            )

        return points

    # ----------------------------------------
    # JSON API
    # ----------------------------------------
    @staticmethod
    def from_json_endpoint(url):
        points = []

        try:
            r = requests.get(url, timeout=5)
            if "application/json" not in r.headers.get("Content-Type", ""):
                return points

            data = r.json()
            if not isinstance(data, dict):
                return points

            for key in data:
                points.append(
                    InjectionPoint(
                        url=url,
                        method="POST",
                        target_param=key,
                        params=data,  # FULL JSON BODY
                        content_type="json"
                    )
                )

        except Exception:
            pass

        return points