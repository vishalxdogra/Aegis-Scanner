from core.target import Target
from core.environment import EnvironmentProfile
from core.context import ScanContext

from recon.port_scanner import PortScanner
from recon.crawler import Crawler
from recon.service_fingerprint import ServiceFingerprinter

from analysis.attack_surface import AttackSurface
from analysis.forms import FormExtractor
# from attacks.sqli_engine import SQLiScanner
from analysis.parameters import ParameterDiscovery

from core.requester import Requester
from analysis.injection_factory import InjectionPointFactory
from attacks.sqli_engine import SQLiEngine



def main():
    url = input("Enter target URL: ").strip()

    # ---------------- TARGET & ENV ----------------
    target = Target(url)
    print(f"\n[*] Target: {target}")

    env = EnvironmentProfile(target)
    env.analyze()
    mode = env.scan_mode()

    print(f"[*] Scan mode: {mode}")

    ctx = ScanContext(target=target, mode=mode)

    # ---------------- PORT SCAN ----------------
    print("\n[*] Scanning ports...")
    ports = PortScanner(target.host).scan()

    if ports:
        print("[+] Open ports:")
        for p in ports:
            print(f"  - {p}")
    else:
        print("[-] No open ports found")

    # ---------------- SERVICE FINGERPRINT ----------------
    print("\n[*] Fingerprinting services...")
    services = ServiceFingerprinter(target.host, ports).fingerprint()

    web_targets = []
    for port, info in services.items():
        print(
            f"  - Port {port}: "
            f"{info['type'].upper()} | "
            f"Status={info['status']} | "
            f"Server={info['server']}"
        )
        web_targets.append(info["url"])

    # ---------------- CRAWLING ----------------
    print("\n[*] Crawling web applications...")
    urls = set()

    for base in web_targets:
        print(f"  [+] Crawling {base}")
        urls |= Crawler(base).crawl()

    print(f"\n[+] Total URLs discovered: {len(urls)}")

    for u in list(urls)[:20]:  # limit output
        print(f"  - {u}")

    if len(urls) > 20:
        print(f"  ... {len(urls) - 20} more URLs")

    form_extractor = FormExtractor(session=ctx.session)

    # ---------------- ATTACK SURFACE ----------------
    print("\n[*] Classifying attack surface...")
    surface = AttackSurface(urls).analyze()

    for category, items in surface.items():
        print(f"  - {category.upper()}: {len(items)} URLs")

    # ---- PARAMETER DISCOVERY ----
    print("\n[*] Discovering injectable parameters...")
    param_urls = ParameterDiscovery(urls).discover()
    print(f"[+] Generated {len(param_urls)} parameterized URLs")


    # ---------------- BUILD INJECTION POINTS ----------------
    print("\n[*] Building injection points...")

    points = []

    # From discovered URLs
    for url in urls:
        points.extend(InjectionPointFactory.from_url(url))

    # From discovered forms
    for url in urls:
        for form in form_extractor.extract_forms(url):
            points.extend(InjectionPointFactory.from_form(form))

    print(f"[+] Total injection points: {len(points)}")

    # ---------------- SQL INJECTION ----------------
    print("\n[*] Running unified SQL Injection engine...")

    engine = SQLiEngine(Requester(ctx))

    for point in points:
        finding = engine.test(point)
        if finding:
            ctx.add_finding(finding)
    

    # ---------------- RESULTS ----------------
    print("\n[SQLi Findings]")

    if not ctx.findings:
        print("[-] No SQL Injection detected")
    else:
        for f in ctx.findings:
            print(
                f"  - {f['method']} SQLi | {f['url']} | "
                f"param={f['parameter']} | "
                f"confidence={f['confidence']} | "
                f"technique={f['technique']}"
            )

if __name__ == "__main__":
    main()