# recon/port_scanner.py
import socket
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, host, mode="SAFE"):
        self.host = host
        self.mode = mode
        self.open_ports = []

        self.ports = (
            range(1, 65536) if mode == "FULL"
            else [21, 22, 25, 80, 443, 3000, 3306, 5000, 5432, 8000, 8080, 9000]
        )

    def _scan_port(self, port):
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((self.host, port))
            sock.close()
            return port
        except Exception:
            return None

    def scan(self):
        workers = 200 if self.mode == "FULL" else 50

        with ThreadPoolExecutor(max_workers=workers) as executor:
            for result in executor.map(self._scan_port, self.ports):
                if result:
                    self.open_ports.append(result)

        return sorted(self.open_ports)