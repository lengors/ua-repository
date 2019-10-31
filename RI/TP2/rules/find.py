import re

class find:
    def __init__(self, regex):
        self.regex = regex

    def __call__(self, content):
        return re.finditer(self.regex, content)