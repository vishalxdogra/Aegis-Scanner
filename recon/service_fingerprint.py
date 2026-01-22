# recon/service_fingerprint.py
import requests
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ServiceFingerprinter:
    def __init__(self, host, ports, timeout=3):
        self.host = host
        self.ports = ports
        self.timeout = timeout
        self.services = {}  # port -> dict

    def fingerprint(self):
        for port in self.ports:
            info = self._probe_port(port)
            self.services[port] = info
        return self.services

    def _probe_port(self, port):
        # Try HTTP
        http_url = f"http://{self.host}:{port}"
        https_url = f"https://{self.host}:{port}"

        # HTTP first
        try:
            r = requests.get(http_url, timeout=self.timeout, allow_redirects=True)
            return {
                "type": "http",
                "url": r.url,
                "status": r.status_code,
                "server": r.headers.get("Server"),
                "content_type": r.headers.get("Content-Type")
            }
        except Exception:
            pass

        # HTTPS next
        try:
            r = requests.get(https_url, timeout=self.timeout, verify=False, allow_redirects=True)
            return {
                "type": "https",
                "url": r.url,
                "status": r.status_code,
                "server": r.headers.get("Server"),
                "content_type": r.headers.get("Content-Type")
            }
        except Exception:
            pass

        # Fallback: banner grab (non-web)
        try:
            sock = socket.socket()
            sock.settimeout(self.timeout)
            sock.connect((self.host, port))
            banner = sock.recv(1024).decode(errors="ignore").strip()
            sock.close()
            return {
                "type": "tcp",
                "banner": banner if banner else "unknown"
            }
        except Exception:
            return {
                "type": "unknown"
            }