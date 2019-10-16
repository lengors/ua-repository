import rules, collections

class Tokenizer:
    def __init__(self, *rules):
        self.__rules = collections.OrderedDict()
        for rule in rules:
            self.add_rule(rule)

    def __len__(self):
        return len(self.__rules)

    def add_rule(self, rule):
        self.set_rule(len(self), rule)

    def del_rule(self, key):
        return self.__rules.pop(key)

    def has_rule(self, key):
        return key in self.__rules

    def make_rule(self, key, *args, **kwargs):
        self.__rules[key] = key(*args, **kwargs)

    def set_rule(self, key, rule = None):
        self.__rules[key] = rule

    def tokenize(self, content):
        for key, rule in self.__rules.items():
            content = rule(content)
        return content

def __normalize(content, match):
    return content[:match.regs[1][0]] + match.group(1).replace('.', '') + content[match.regs[1][1]:]

simple_tokenizer = Tokenizer()
simple_tokenizer.add_rule(rules.replace(r'[^a-zA-Z]+', ' '))
simple_tokenizer.add_rule(rules.apply(str.lower))
simple_tokenizer.add_rule(rules.apply(str.split, ' '))
simple_tokenizer.add_rule(rules.filter(rules.comparator(len) >= 3))

tokenizer = Tokenizer()
tokenizer.add_rule(rules.replace(r'(\n)+', ' '))
tokenizer.add_rule(rules.apply(str.lower))
tokenizer.add_rule(rules.modify(r'(?:[^a-z]|^)([a-z](?:\.[a-z])+\.?)(?:[^a-z]|$)', __normalize))
tokenizer.add_rule(rules.find(r'([a-z]+(?:-[a-z]+)+)|(?:.*?([.,\-!?;*/=()\[\]:"\'\\]* +|[.,\-!?;*/=()\[\]:"\'\\]+ *))|(.+)'))
tokenizer.add_rule(rules.map(lambda match: match.group(0)[:match.regs[2][0] - match.regs[0][0]] if match.groups()[0] is None and match.groups()[2] is None else match.group(0)))
tokenizer.add_rule(rules.filter(rules.comparator(len) >= 2))
tokenizer.set_rule(rules.stopping)
tokenizer.make_rule(rules.stemming)