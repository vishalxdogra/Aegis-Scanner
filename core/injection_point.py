from copy import deepcopy


class InjectionPoint:
    """
    Represents a single injectable parameter.
    Supports multiple injection strategies.
    """

    def __init__(self, url, method, target_param, params, content_type):
        self.url = url
        self.method = method.upper()
        self.target_param = target_param
        self.params = params or {}
        self.content_type = content_type  # query | form | json

    # ---------------- STRATEGIES ----------------

    def inject_append(self, payload):
        new = deepcopy(self)
        new.params = dict(self.params)
        base = str(new.params.get(self.target_param, ""))
        new.params[self.target_param] = base + payload
        return new

    def inject_replace(self, payload):
        new = deepcopy(self)
        new.params = dict(self.params)
        new.params[self.target_param] = payload
        return new

    # ---------------- CONTEXT INSPECTION ----------------

    def base_value(self):
        return str(self.params.get(self.target_param, ""))

    def looks_numeric(self):
        v = self.base_value()
        return v.isdigit()

    def looks_quoted(self):
        v = self.base_value()
        return not v.isdigit()