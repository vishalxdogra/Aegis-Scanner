class ConfidenceEngine:
    """
    Correlates detection signals into confidence levels.

    This engine is intentionally conservative.
    It avoids false positives by requiring signal agreement.
    """

    WEIGHTS = {
        "error": 0.45,
        "boolean": 0.35,
        "union": 0.40,
        "time": 0.30,
    }

    @staticmethod
    def score(*signals):
        """
        Returns:
        - Very High
        - High
        - Medium
        - Low
        """
        signals = set(signals)

        score = sum(
            ConfidenceEngine.WEIGHTS.get(s, 0)
            for s in signals
        )

        if score >= 0.75:
            return "Very High"

        if score >= 0.50:
            return "High"

        if score >= 0.30:
            return "Medium"

        return "Low"