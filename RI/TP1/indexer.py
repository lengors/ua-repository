from corpus_reader import CorpusReader
from tokenization import Tokenizer
import collections

class Indexer:
    def __init__(self, tokenizer : Tokenizer):
        self.terms = {} # {string : {doc_id : [index1, index2]}}
        self.tokenizer = tokenizer

    def index(self, corpus_reader : CorpusReader):
        for pmid, document in corpus_reader.documents.items():
            self.update(pmid, list(enumerate(self.tokenizer.tokenize(document))))

    def update(self, doc_id, terms): #terms = list
        for i, term in terms:
            term_docs = self.terms.setdefault(term, { })
            doc_occurrences = term_docs.setdefault(doc_id, [ ])
            doc_occurrences.append(i)

    def save(self, output_filename):
        with open(output_filename, 'w') as file:
            file.write(''.join([ '{}{}\n'.format(key, ''.join([ ',{}:{}'.format(k, len(v)) for k, v in sec_dic.items() ])) for key, sec_dic in self.terms.items() ]))

    def sort(self):
        self.terms = collections.OrderedDict(sorted(self.terms.items()))

    def __repr__(self):
        return str(self.terms)
