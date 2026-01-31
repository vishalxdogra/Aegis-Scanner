class SQLiAuthority:
    """
    Tracks exploitation authority level for a single injection point
    """

    LEVELS = {
        "detect": 0,
        "boolean": 1,
        "union": 2,
        "metadata": 3
    }

    def __init__(self):
        self.level = 0

    def grant(self, name):
        self.level = max(self.level, self.LEVELS[name])

    def allows(self, name):
        return self.level >= self.LEVELS[name]