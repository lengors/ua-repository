class filter:
    def __init__(self, filter):
        self.filter = filter

    def __call__(self, content):
        return [ token for token in content if self.filter(token) ]