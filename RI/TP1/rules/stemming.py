from Stemmer import Stemmer

class stemming:
    def __init__(self, language = 'english'):
        self.stemmer = Stemmer(language)

    def __call__(self, content):
        return [ self.stemmer.stemWord(word) for word in content ]