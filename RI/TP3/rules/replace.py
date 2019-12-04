import re

class replace:
    def __init__(self, regex, by):
        self.regex, self.by = re.compile(regex), by

    def __call__(self, content):
        return re.sub(self.regex, self.by, content)