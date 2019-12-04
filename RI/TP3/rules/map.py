class map:
    def __init__(self, function):
        self.function = function

    def __call__(self, content):
        return [ self.function(value) for value in content ]