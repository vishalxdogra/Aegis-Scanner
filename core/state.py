# core/state.py
class ScanState:
    def __init__(self):
        self.defense_detected = False
        self.rate_limited = False
        self.scan_depth = "FULL"

    def downgrade(self):
        self.scan_depth = "SAFE"

    def __repr__(self):
        return f"<ScanState depth={self.scan_depth}>"