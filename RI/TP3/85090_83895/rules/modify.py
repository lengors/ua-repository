import re

class modify:
    def __init__(self, regex, modification):
        self.regex = re.compile(regex)
        self.modification = modification

    def __call__(self, content):
        for match in re.finditer(self.regex, content):
            content = self.modification(content, match)
        return content