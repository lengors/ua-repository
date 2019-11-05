class comparator:
    def __init__(self, *rules):
        self.rules = rules

    def __eq__(self, other):
        return lambda token: self.prepare(token) == other

    def __ne__(self, other):
        return lambda token: self.prepare(token) != other

    def __le__(self, other):
        return lambda token: self.prepare(token) <= other

    def __ge__(self, other):
        return lambda token: self.prepare(token) >= other

    def __lt__(self, other):
        return lambda token: self.prepare(token) < other

    def __gt__(self, other):
        return lambda token: self.prepare(token) > other

    def prepare(self, token):
        for rule in self.rules:
            token = rule(token)
        return token