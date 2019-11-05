"""from corpus_reader import CorpusReader
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
            
    def calc_idf(self, num_docs):
        return log10(num_docs / len(indexer.terms[term]))

    def __repr__(self):
        return str(self.terms)
"""

from corpus_reader import CorpusReader
from tokenization import Tokenizer
import collections, math, psutil
import os, shutil

def get_line(lines, files, parse_func):
    i, line = min(enumerate(lines), key = lambda line: line[1][0])
    new_line = files[i].readline()
    if not new_line or len(new_line.strip()) == 0:
        lines.pop(i)
        files[i].close()
        files.pop(i)
    else:
        lines[i] = parse_func(new_line)
    return line

class Indexer:
    class __InnerIndexer:
        def __init__(self, tokenizer : Tokenizer, index_folder : str):
            self.terms = {}
            self.ranked = False
            self.documents = set()
            self.tokenizer = tokenizer
            self.index_folder = index_folder
            if not os.path.isdir(self.index_folder):
                os.mkdir(self.index_folder)

        def __del__(self):
            # shutil.rmtree(self.index_folder)
            pass

        def dispatch(self):
            self.sort()
            filename = os.path.join(self.index_folder, 'block-{}'.format(len(os.listdir(self.index_folder))))
            with open(filename, 'w') as fout:
                fout.write(self.__str__())
            del self.terms
            self.terms = {}

        def index(self, corpus_reader : CorpusReader):
            for pmid, document in corpus_reader.documents.items():
                self.update(pmid, document)
                self.documents.add(pmid)
                if psutil.virtual_memory().percent >= 66:
                    self.dispatch()

        def merge(self):
            self.dispatch()
            if self.ranked:
                self.__merge_ranked()
            else:
                self.__merge_unranked()

        def rank(self):
            if not self.ranked:
                self._rank()
                self.ranked = True

        def save(self, output_filename):
            with open(output_filename, 'w') as fout:
                fout.write(self.__str__())

        def sort(self):
            self.terms = collections.OrderedDict(sorted(self.terms.items()))

        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                documents[pmid] = documents.get(pmid, 0) + 1

        def _merge_ranked(self, docs0 : dict, docs1 : dict):
            pass

        def _merge_unranked(self, docs0 : dict, docs1 : dict):
            return { key : docs0.get(key, 0) + docs1.get(key, 0) for key in docs0.keys() | docs1.keys() }

        def _parse_ranked(self, line : str):
            pass

        def _parse_unranked(self, line : str):
            term, *docs = line.split(',')
            return (term, { key : int(value) for key, value in [ doc.split(':') for doc in docs ] })

        def _rank(self):
            for term, documents in self.terms.items():
                idf = math.log10(len(self.documents) / len(documents))
                for pmid in self.documents:
                    count = documents.get(pmid, 0)
                    documents[pmid] = (0 if count == 0 else (1 + math.log10(count)) * idf, count)
                self.terms[term] = (idf, documents)

        def _write_ranked(self, output_file, line : tuple):
            pass

        def _write_unranked(self, line : tuple):
            return '{},{}\n'.format(line[0], ','.join([ '{}:{}'.format(pmid, count) for pmid, count in line[1].items() ]))

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return '\n'.join([ '{}:{};{}'.format(term, idf, ';'.join([ '{}:{}'.format(pmid, weight) for pmid, (weight, count) in documents.items() ])) for term, (idf, documents) in self.terms.items() ]) if self.ranked else '\n'.join([ '{},{}'.format(term, ','.join([ '{}:{}'.format(pmid, count) for pmid, count in documents.items() ])) for term, documents in self.terms.items() ])

        def __merge_ranked(self):
            filenames = [ filename for filename in [ os.path.join(self.index_folder, filename) for filename in os.listdir(self.index_folder) ] if os.path.isfile(filename) ]
            files = [ open(filename, 'r') for filename in filenames  ]
            output_file = open(os.path.join(self.index_folder, 'blocks-merged'), 'w')
            lines = [ self._parse_ranked(line) for line in [ file.readline() for file in files ] if line and len(line.strip()) > 0 ]
            cline = get_line(lines, files, self._parse_ranked)
            while len(lines) > 0:
                line = get_line(lines, files, self._parse_ranked)
                if line[0] == cline[0]:
                    cline = (cline[0], self._merge_unranked(cline[1], line[1]))
                else:
                    output_file.write(self._write_ranked(cline))
                    cline = line
            output_file.write(self._write_ranked(cline))
            for filename in filenames:
                os.remove(filename)
            output_file.close()

        def __merge_unranked(self):
            filenames = [ filename for filename in [ os.path.join(self.index_folder, filename) for filename in os.listdir(self.index_folder) ] if os.path.isfile(filename) ]
            files = [ open(filename, 'r') for filename in filenames  ]
            output_file = open(os.path.join(self.index_folder, 'blocks-merged'), 'w')
            lines = [ self._parse_unranked(line) for line in [ file.readline() for file in files ] if line and len(line.strip()) > 0 ]
            cline = get_line(lines, files, self._parse_unranked)
            while len(lines) > 0:
                line = get_line(lines, files, self._parse_unranked)
                if line[0] == cline[0]:
                    cline = (cline[0], self._merge_unranked(cline[1], line[1]))
                else:
                    output_file.write(self._write_unranked(cline))
                    cline = line
            output_file.write(self._write_unranked(cline))
            for filename in filenames:
                os.remove(filename)
            output_file.close()

    class __InnerPositionableIndexer(__InnerIndexer):
        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                positions = documents.setdefault(pmid, [])
                positions.append(i)

        def _rank(self):
            for term, documents in self.terms.items():
                idf = math.log10(len(self.documents) / len(documents))
                for pmid in self.documents:
                    positions = documents.get(pmid, [])
                    documents[pmid] = (0 if len(positions) == 0 else (1 + math.log10(len(positions))) * idf, positions)
                self.terms[term] = (idf, documents)
        
        def __str__(self):
            return '\n'.join([ '{}:{};{}'.format(term, idf, ';'.join([ '{}:{}{}'.format(pmid, weight, '' if len(positions) == 0 else ':{}'.format(','.join([ str(position) for position in positions ]))) for pmid, (weight, positions) in documents.items() ])) for term, (idf, documents) in self.terms.items() ]) if self.ranked else '\n'.join([ '{},{}'.format(term, ','.join([ '{}:{}'.format(pmid, len(positions)) for pmid, positions in documents.items() ])) for term, documents in self.terms.items() ])

    def __init__(self, tokenizer : Tokenizer, index_folder : str, store_positions : bool = False):
        self.__indexer = self.__InnerPositionableIndexer(tokenizer, index_folder) if store_positions else self.__InnerIndexer(tokenizer, index_folder)

    def __getattr__(self, key):
        return getattr(self.__indexer, key)
