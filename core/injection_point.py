# core/injection_point.py
from copy import deepcopy

class InjectionPoint:
    def __init__(self, url, method, params, target_param):
        self.url = url
        self.method = method.upper()
        self.params = params
        self.target_param = target_param

    def clone(self):
        return InjectionPoint(
            self.url,
            self.method,
            deepcopy(self.params),
            self.target_param
        )

    def append(self, payload):
        p = self.clone()
        p.params[p.target_param] += payload
        return p

    def replace(self, payload):
        p = self.clone()
        p.params[p.target_param] = payload
        return p