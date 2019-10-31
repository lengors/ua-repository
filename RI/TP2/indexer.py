from corpus_reader import CorpusReader
from tokenization import Tokenizer
import collections
from math import log10



class Value: #idf, [Struct1, Struct2]

    def __init__(self):
        self.structs = list()

    def set_idf(self, idf):
        self.idf = idf

    def addStruct(self, struct):
        self.structs.append(struct)

    
class Struct:       # doc_id : term_weight : [pos1, pos2, pos3]

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.pos = list()
        
        


class Indexer:

    def __init__(self, tokenizer : Tokenizer):
        self.terms = {} # {string : idf; [doc_id : term_weight : [pos1, pos2, pos3]] }
        self.tokenizer = tokenizer

    def index(self, corpus_reader : CorpusReader):
        for pmid, document in corpus_reader.documents.items():
            termos = self.update(pmid, list(enumerate(self.tokenizer.tokenize(document))))
        
        num_docs = len(corpus_reader.documents.items())
        for term in self.terms:                                                 # calcula idfs
            idf = self.calc_idf(num_docs)
            self.terms[term].set_idf(idf)

    def update(self, doc_id, terms): #terms = list
        for i, term in terms:
            term_docs = self.terms.setdefault(term, Value())
            doc_occurrences = term_docs.setdefault(doc_id, Struct(doc_id))
            doc_occurrences.pos.append(i)


        for termo in terms:                        # calcula wtd
            weight = 1 + log10(len(self.terms[termo][doc_id]))
            

    def save(self, output_filename):
        with open(output_filename, 'w') as file:
            file.write(''.join([ '{}{}\n'.format(key, ''.join([ ',{}:{}'.format(k, len(v)) for k, v in sec_dic.items() ])) for key, sec_dic in self.terms.items() ]))

    def sort(self):
        self.terms = collections.OrderedDict(sorted(self.terms.items()))
            
    def calc_idf():
        return log10(num_docs / len(indexer.terms[term]))

    def __repr__(self):
        return str(self.terms)
