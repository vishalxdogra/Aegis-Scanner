# core/requester.py
class Requester:
    def __init__(self, context):
        self.ctx = context

    def send(self, point):
        try:
            if point.method == "GET":
                return self.ctx.get(point.url, params=point.params)
            elif point.method == "POST":
                return self.ctx.post(point.url, data=point.params)
        except Exception:
            return None