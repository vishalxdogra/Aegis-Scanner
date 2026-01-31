class Explainer:
    def explain(self, finding):
        return (
            f"The parameter '{finding.parameter}' in '{finding.url}' is vulnerable to "
            f"{finding.technique}. The application responds differently to crafted SQL "
            f"inputs, indicating unsanitized database queries. "
            f"This vulnerability may allow attackers to manipulate backend SQL queries."
        )