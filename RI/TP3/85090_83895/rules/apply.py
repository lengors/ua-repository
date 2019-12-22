class apply:
    def __init__(self, function, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.function = function

    def __call__(self, content):
        return self.function(content, *self.args, **self.kwargs)