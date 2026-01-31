class FindingDeduplicator:
    @staticmethod
    def deduplicate(findings):
        unique = {}
        for f in findings:
            unique[f.key()] = f
        return list(unique.values())