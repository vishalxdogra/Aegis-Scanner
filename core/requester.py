class Requester:
    """
    Dispatches HTTP requests for InjectionPoints.

    Centralized request handling ensures:
    - Consistent cookies
    - Authentication persistence
    - Safe retries
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def send(self, point):
        print("[DEBUG][REQ]",
        point.method,
        point.url,
        point.params)
        if not point or not point.url:
            return None

        try:
            if point.method == "GET":
                return self.ctx.get(
                    point.url,
                    params=point.params
                )

            if point.method == "POST":
                if point.content_type == "json":
                    return self.ctx.post(
                        point.url,
                        json=point.params
                    )
                return self.ctx.post(
                    point.url,
                    data=point.params
                )

        except Exception:
            return None

        return None