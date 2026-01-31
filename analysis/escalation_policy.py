class EscalationPolicy:
    """
    Governs what extraction actions are allowed.
    Prevents unsafe or automatic data leakage.
    """

    ALLOWED_TECHNIQUES = {"union", "error"}

    @staticmethod
    def allow_extraction(finding, requested_action):
        # Must be confirmed SQLi
        if finding.vuln_type != "SQLi":
            return False

        # Technique must support extraction
        techniques = set(finding.technique.split(" + "))
        if not techniques & EscalationPolicy.ALLOWED_TECHNIQUES:
            return False

        # Allowed actions
        if requested_action not in {
            "version",
            "db_name",
            "current_user",
            "current_db"
        }:
            return False

        return True