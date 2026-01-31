import time
from analysis.response_fingerprint import ResponseFingerprint
from analysis.finding_model import Finding
from analysis.dbms_fingerprint import DBMSFingerprinter
from analysis.confidence_engine import ConfidenceEngine

# ================= SAFE DEFAULTS =================

MAX_REQUESTS = 10
TIME_DELAY = 1.5

SIM_TRUE = 0.90
SIM_FALSE = 0.75
SIM_UNION = 0.70


class SQLiEngine:
    """
    Production-grade SQL Injection detection engine.

    Design principles:
    - Context-aware payload mutation
    - Boolean / Error / Union / Time detection
    - Semantic response analysis (not naive diffing)
    - Deterministic & safe-by-default
    - Framework-agnostic (HTML + JSON + APIs)
    """

    def __init__(self, requester):
        self.requester = requester

    # ==================================================
    # ENTRY POINT
    # ==================================================

    def test(self, point):
        """
        Tests a single InjectionPoint.
        Returns a Finding on confirmed SQLi, else None.
        """

        base = self.requester.send(point)
        if not base:
            return None

        base_fp = ResponseFingerprint(base)
        used = 1

        strategies = self._build_strategies(point)

        # ================= BOOLEAN / ERROR =================
        for strat in strategies:
            apply = strat["apply"]

            for true_p, false_p in strat["boolean"]:
                if used + 2 > MAX_REQUESTS:
                    break

                r_true = self.requester.send(apply(true_p))
                r_false = self.requester.send(apply(false_p))
                used += 2

                if not r_true or not r_false:
                    continue

                fp_t = ResponseFingerprint(r_true)
                fp_f = ResponseFingerprint(r_false)

                # ---------- ERROR BASED ----------
                if fp_t.has_sql_error():
                    return self._finalize(point, r_true.text, {"error"})

                # ---------- STRONG BOOLEAN (SEMANTIC) ----------
                if fp_t.has_visible_data() and not fp_f.has_visible_data():
                    return self._finalize(point, r_true.text, {"boolean"})

                if fp_t.looks_empty() != fp_f.looks_empty():
                    return self._finalize(point, r_true.text, {"boolean"})

                if fp_t.significant_length_diff(fp_f):
                    return self._finalize(point, r_true.text, {"boolean"})

                # ---------- FALLBACK SIMILARITY ----------
                if (
                    fp_t.similarity(base_fp) > SIM_TRUE
                    and fp_f.similarity(base_fp) < SIM_FALSE
                ):
                    return self._finalize(point, r_true.text, {"boolean"})

        # ================= UNION =================
        if used < MAX_REQUESTS and self._union_test(point, base_fp):
            return self._finalize(point, base.text, {"union"})

        # ================= TIME =================
        if used < MAX_REQUESTS and self._time_test(point):
            return self._finalize(point, base.text, {"time"})

        return None

    # ==================================================
    # STRATEGY BUILDER
    # ==================================================

    def _build_strategies(self, point):
        """
        Builds mutation strategies based on parameter context.
        Order matters.
        """
        strategies = []

        # ---------- NUMERIC PARAMETERS ----------
        if point.looks_numeric():
            strategies.append({
                "apply": lambda p: point.inject_append(" " + p),
                "boolean": [
                    ("AND 1=1", "AND 1=2"),
                    ("OR 1=1", "OR 1=2"),
                ],
            })

        # ---------- STRING / QUOTED PARAMETERS ----------
        strategies.append({
            "apply": lambda p: point.inject_replace(p),
            "boolean": [
                ("' OR '1'='1", "' OR '1'='2"),
                ('" OR "1"="1', '" OR "1"="2'),
            ],
        })

        # ---------- LEGACY FALLBACK ----------
        strategies.append({
            "apply": lambda p: point.inject_append(p),
            "boolean": [
                (" AND 1=1", " AND 1=2"),
            ],
        })

        return strategies

    # ==================================================
    # UNION TEST (SAFE, NO EXTRACTION)
    # ==================================================

    def _union_test(self, point, base_fp):
        for cols in range(1, 6):
            payload = f" UNION SELECT {','.join(['NULL'] * cols)}-- "
            r = self.requester.send(point.inject_append(payload))
            if not r:
                continue

            fp = ResponseFingerprint(r)
            if fp.similarity(base_fp) < SIM_UNION and not fp.has_sql_error():
                return True

        return False

    # ==================================================
    # TIME-BASED TEST
    # ==================================================

    def _time_test(self, point):
        start = time.time()
        r = self.requester.send(
            point.inject_append(f" AND SLEEP({TIME_DELAY})")
        )
        return r and (time.time() - start) > (TIME_DELAY + 0.4)

    # ==================================================
    # FINALIZE
    # ==================================================

    def _finalize(self, point, text, signals):
        finding = self._build_finding(point, text, signals)

        finding.point = point
        finding.extraction_capable = bool(signals & {"union", "error"})
        finding.blind_capable = bool(signals & {"boolean", "time"})

        return finding

    def _build_finding(self, point, text, signals):
        dbms = DBMSFingerprinter.detect(text)
        confidence = ConfidenceEngine.score(*signals)

        return Finding(
            vuln_type="SQLi",
            url=point.url,
            parameter=point.target_param,
            method=point.method,
            technique=" + ".join(sorted(signals)),
            confidence=confidence,
            dbms=dbms,
            authenticated=self.requester.ctx.is_authenticated
        )