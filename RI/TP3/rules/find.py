import re

class find:
    def __init__(self, regex):
        self.regex = re.compile(regex)

    def __call__(self, content):
        return re.finditer(self.regex, content)