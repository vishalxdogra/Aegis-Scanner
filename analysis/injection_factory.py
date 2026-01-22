# analysis/injection_factory.py
from urllib.parse import urlparse, parse_qs
from core.injection_point import InjectionPoint

class InjectionPointFactory:

    @staticmethod
    def from_url(url):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        points = []
        for p in params:
            clean_url = parsed._replace(query="").geturl()
            points.append(
                InjectionPoint(
                    url=clean_url,
                    method="GET",
                    params={k: v[0] for k, v in params.items()},
                    target_param=p
                )
            )
        return points

    @staticmethod
    def from_form(form):
        points = []
        for field in form["fields"]:
            points.append(
                InjectionPoint(
                    url=form["action"],
                    method=form["method"],
                    params=form["fields"].copy(),
                    target_param=field
                )
            )
        return points