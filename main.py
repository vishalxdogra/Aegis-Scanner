from core.target import Target
from core.context import ScanContext
from core.auth import AuthManager
from core.auth_profile import AuthProfile
from core.requester import Requester

from recon.port_scanner import PortScanner
from recon.crawler import Crawler
from recon.service_fingerprint import ServiceFingerprinter

from analysis.injection_factory import InjectionPointFactory
from analysis.risk_engine import RiskEngine
from analysis.finding_deduplicator import FindingDeduplicator
from analysis.point_deduplicator import dedupe_points
from attacks.sqli_engine import SQLiEngine

import time


def main():
    url = input("Enter target URL: ").strip()
    target = Target(url)
    ctx = ScanContext(target)

    print(f"\n[*] Target: {target}")

    # ================= AUTH =================
    if input("Use authentication? (y/n): ").lower() == "y":
        print("[*] Configure authentication")

        login_url = input("Login URL: ").strip()
        method = input("Method (POST/GET) [POST]: ").strip() or "POST"

        fields = {}
        print("Enter login fields (blank key to stop)")
        while True:
            k = input("Field name: ").strip()
            if not k:
                break
            v = input("Field value: ").strip()
            fields[k] = v

        csrf = input("Use CSRF token? (y/n): ").lower() == "y"
        csrf_url = csrf_field = csrf_regex = None

        if csrf:
            csrf_url = input("CSRF page URL: ").strip()
            csrf_field = input("CSRF field name: ").strip()
            csrf_regex = input("CSRF regex (group 1): ").strip()

        profile = AuthProfile(
            login_url=login_url,
            method=method,
            fields=fields,
            csrf_url=csrf_url,
            csrf_field=csrf_field,
            csrf_regex=csrf_regex,
            success_check=lambda t: "logout" in t.lower() or "dashboard" in t.lower()
        )

        AuthManager(ctx).authenticate(profile)
    else:
        print("[*] Running unauthenticated scan")

    # ================= RECON =================
    print("\n[*] Scanning ports...")
    ports = PortScanner(target.host).scan()
    print("[+] Open ports:", ports)

    print("\n[*] Fingerprinting services...")
    services = ServiceFingerprinter(target.host, ports).fingerprint()

    web_targets = {target.base_url()}
    for s in services.values():
        if isinstance(s, dict) and "url" in s:
            web_targets.add(s["url"])

    # ================= CRAWL =================
    print("\n[*] Crawling...")
    urls, forms = set(), []

    for base in web_targets:
        u, f = Crawler(base).crawl()
        urls |= u
        forms.extend(f)

    urls.add(target.original)
    print(f"[+] URLs discovered: {len(urls)}")

    # ================= INJECTION POINTS =================
    print("\n[*] Building injection points...")
    points = []

    for u in urls:
        points.extend(InjectionPointFactory.from_url(u))

    for f in forms:
        points.extend(InjectionPointFactory.from_form(f))

    for u in urls:
        points.extend(InjectionPointFactory.from_json_endpoint(u))

    points = dedupe_points(points)

    # ================= SQLi =================
    print("\n[*] Running SQLi engine...")
    engine = SQLiEngine(Requester(ctx))
    risk_engine = RiskEngine()

    start = time.time()

    for i, p in enumerate(points, 1):
        print(f"[SQLi] {i}/{len(points)} | {p.method} {p.url} | param={p.target_param}")
        print("[DEBUG] InjectionPoint:",
            p.url,
            p.method,
            p.target_param,
            p.params,
            p.content_type)
        finding = engine.test(p)
        if finding:
            finding.risk = risk_engine.score(finding)
            ctx.add_finding(finding)

    findings = FindingDeduplicator.deduplicate(ctx.findings)
    print("\n[SQLi Findings]")
    for f in findings:
        print(
            f"- {f.method} {f.url} "
            f"param={f.parameter} "
            f"type={f.technique} "
            f"confidence={f.confidence}"
        )
    print(f"\n[*] SQLi scan completed in {round(time.time() - start, 2)}s")
    print("\n[*] Summary")
    print(ctx.summary())


if __name__ == "__main__":
    main()