class RiskEngine:
    def score(self, finding):
        score = 5

        if "UNION" in finding.technique:
            score = 9
        elif "Time" in finding.technique:
            score = 8
        elif "Error" in finding.technique:
            score = 7
        elif "Boolean" in finding.technique:
            score = 6

        if finding.authenticated:
            score += 1

        if finding.dbms and finding.dbms != "Unknown":
            score += 0.5

        score = min(score, 10)

        return {
            "score": round(score, 1),
            "severity": self._severity(score)
        }

    def _severity(self, score):
        if score >= 9:
            return "Critical"
        if score >= 7:
            return "High"
        if score >= 5:
            return "Medium"
        return "Low"