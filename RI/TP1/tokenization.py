import rules

class Tokenizer:
    def __init__(self):
        self.rules = list()

    def add_rule(self, rule):
        self.rules.append(rule)
        return self

    def tokenize(self, content):
        for rule in self.rules:
            content = rule(content)
        return content

simple_tokenizer = Tokenizer()
simple_tokenizer.add_rule(rules.replace(r'[^a-zA-Z]+', ' '))
simple_tokenizer.add_rule(rules.apply(str.lower))
simple_tokenizer.add_rule(rules.apply(str.split, ' '))
simple_tokenizer.add_rule(rules.filter(rules.comparator(len) >= 3))

tokenizer = Tokenizer()
tokenizer.add_rule(rules.replace(r'(\n)+', ' '))
tokenizer.add_rule(rules.find(r'.*?([.,\-!?;*/=()\[\]:]* +|[.,\-!?;*/=()\[\]:]+ *)'))
tokenizer.add_rule(rules.map(lambda match: match.group(0)[:match.regs[1][0] - match.regs[0][0]]))
tokenizer.add_rule(rules.map(rules.apply(str.lower)))
tokenizer.add_rule(rules.filter(rules.comparator(len) > 0))