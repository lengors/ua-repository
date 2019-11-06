from corpus_reader import CorpusReader
from tokenization import Tokenizer
import collections, math, psutil
import os, shutil

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

        def dispatch(self):
            if type(self.terms) != collections.OrderedDict:
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
                if psutil.virtual_memory().percent >= 90:
                    self.dispatch()

        def merge(self, output_filename : str, calculate_tfidf : bool = False):
            # select which function to use
            write_func = self.__write_unranked_ranked if calculate_tfidf else self._write_unranked

            # sort in-memory terms if necessary
            if type(self.terms) != collections.OrderedDict:
                self.sort()

            # get in disk blocks
            filenames = [ filename for filename in [ os.path.join(self.index_folder, filename) for filename in os.listdir(self.index_folder) ] if os.path.isfile(filename) ]
            files = [ open(filename, 'r') for filename in filenames  ]

            # output file
            output_file = open(output_filename, 'w')
            
            # current term for each sorted block
            lines = [ self._parse_unranked(line) for line in [ file.readline() for file in files ] if line and len(line.strip()) > 0 ]
            if len(self.terms) > 0:
                lines.append(self.terms.popitem(0))

            # temporary list to store terms before writing them to disk
            output = list()

            # gets first term (in order)
            cline = self.__get_line(lines, files, self._parse_unranked)

            # while terms to process are available
            while len(lines) > 0:

                # gets next term (in order)
                line = self.__get_line(lines, files, self._parse_unranked)

                # checks if current term and next term are mergable
                if line[0] == cline[0]:

                    # merges them
                    cline = (cline[0], self._merge_unranked(cline[1], line[1]))

                # else
                else:

                    # stores stringified version of term (and associated data)
                    output.append(write_func(cline))

                    # if too much memory in use then write to file stored terms
                    if psutil.virtual_memory().percent >= 90:
                        output_file.write('{}\n'.format('\n'.join(output)))
                        output.clear()

                    # update current term
                    cline = line

            # stores stringified version of last term
            output.append(write_func(cline))

            # writes in-memory terms
            output_file.write('{}\n'.format('\n'.join(output)))

            # closes output file
            output_file.close()

            # deletes temporary blocks in disk
            shutil.rmtree(self.index_folder)

            # sets if the data is ranked or not
            self.ranked = calculate_tfidf

        def sort(self):
            self.terms = collections.OrderedDict(sorted(self.terms.items()))

        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                documents[pmid] = documents.get(pmid, 0) + 1

        def _merge_unranked(self, docs0 : dict, docs1 : dict):
            return { key : docs0.get(key, 0) + docs1.get(key, 0) for key in docs0.keys() | docs1.keys() }

        def _parse_unranked(self, line : str):
            term, *docs = line.split(';')
            return (term, { key : int(value) for key, value in [ doc.split(':') for doc in docs ] })

        def _rank(self, line : tuple):
            term, documents = line
            idf = math.log10(len(self.documents) / len(documents))
            for pmid, count in documents.items():
                documents[pmid] = ((1 + math.log10(count)) * idf, count)
            return (term, (idf, documents))

        def _write_ranked(self, line : tuple):
            return '{}:{};{}'.format(line[0], line[1][0], ';'.join([ '{}:{}'.format(pmid, weight) for pmid, (weight, count) in line[1][1].items() ]))

        def _write_unranked(self, line : tuple):
            return '{};{}'.format(line[0], ';'.join([ '{}:{}'.format(pmid, count) for pmid, count in line[1].items() ]))

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return '\n'.join([ self._write_ranked(item) for item in self.terms.items() ]) if self.ranked else '\n'.join([ self._write_unranked(item) for item in self.terms.items() ])

        def __get_line(self, lines, files, parse_func):
            i, line = min(enumerate(lines), key = lambda line: line[1][0])
            if i >= len(files):
                if len(self.terms) > 0:
                    lines[i] = self.terms.popitem(0)
                else:
                    lines.pop(i)
            else:
                new_line = files[i].readline()
                if not new_line or len(new_line.strip()) == 0:
                    lines.pop(i)
                    files[i].close()
                    files.pop(i)
                else:
                    lines[i] = parse_func(new_line)
            return line

        def __write_unranked_ranked(self, line : tuple):
            return self._write_ranked(self._rank(line))

    class __InnerPositionableIndexer(__InnerIndexer):
        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                positions = documents.setdefault(pmid, [])
                positions.append(i)

        def _merge_unranked(self, docs0 : dict, docs1 : dict):
            return { key : sorted(docs0.get(key, []) + docs1.get(key, [])) for key in docs0.keys() | docs1.keys() }

        def _parse_unranked(self, line : str):
            term, *docs = line.split(';')
            return (term, { pmid : [ int(position) for position in positions.split(',') ] for pmid, positions in [ doc.split(':') for doc in docs ] })

        def _rank(self, line : tuple):
            term, documents = line
            idf = math.log10(len(self.documents) / len(documents))
            for pmid, positions in documents.items():
                documents[pmid] = ((1 + math.log10(len(positions))) * idf, positions)
            return (term, (idf, documents))

        def _write_ranked(self, line : tuple):
            return '{}:{};{}'.format(line[0], line[1][0], ';'.join([ '{}:{}{}'.format(pmid, weight, '' if len(positions) == 0 else ':{}'.format(','.join([ str(position) for position in positions ]))) for pmid, (weight, positions) in line[1][1].items() ]))

        def _write_unranked(self, line : tuple):   # line = (termo, {doc_id : [index1, index2]})
            return '{};{}'.format(line[0], ';'.join([ '{}:{}'.format(pmid, ','.join([ str(position) for position in positions ])) for pmid, positions in line[1].items() ]))

    def __init__(self, tokenizer : Tokenizer, index_folder : str, store_positions : bool = False):
        self.__indexer = self.__InnerPositionableIndexer(tokenizer, index_folder) if store_positions else self.__InnerIndexer(tokenizer, index_folder)

    def __getattr__(self, key):
        return getattr(self.__indexer, key)
