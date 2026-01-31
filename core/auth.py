import re
from core.auth_profile import AuthProfile


class AuthManager:
    """
    Phase 18 – Unified Authentication Engine
    - No hardcoding
    - Profile-driven
    - Works for ANY form-based auth
    """

    def __init__(self, ctx):
        self.ctx = ctx

    def authenticate(self, profile: AuthProfile) -> bool:
        # -------- CSRF PREFETCH --------
        if profile.csrf_url and profile.csrf_field:
            r = self.ctx.get(profile.csrf_url)
            if not r:
                print("[-] Failed to fetch CSRF page")
                return False

            token = self._extract_csrf(r.text, profile.csrf_regex)
            if not token:
                print("[-] CSRF token not found")
                return False

            profile.fields[profile.csrf_field] = token

        # -------- AUTH REQUEST --------
        if profile.method.upper() == "POST":
            r = self.ctx.post(profile.login_url, data=profile.fields)
        else:
            r = self.ctx.get(profile.login_url, params=profile.fields)

        if not r:
            print("[-] Authentication request failed")
            return False

        # -------- SUCCESS VALIDATION --------
        if profile.success_check:
            if not profile.success_check(r.text):
                print("[-] Authentication failed (validation)")
                return False

        self.ctx.is_authenticated = True
        print("[+] Authentication successful")
        return True

    def _extract_csrf(self, html, regex):
        if not regex:
            return None
        m = re.search(regex, html)
        return m.group(1) if m else None