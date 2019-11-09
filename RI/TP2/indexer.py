from corpus_reader import CorpusReader
from tokenization import Tokenizer
import collections, math, psutil
import os, shutil, gc

class Indexer:
    class __InnerIndexer:
        def __init__(self, tokenizer : Tokenizer, index_folder : str, max_memory_usage : float = 20):
            self.terms = {}
            self.segments = []
            self.documents = set()
            self.tokenizer = tokenizer
            self.index_folder = index_folder
            self.max_memory_usage = max_memory_usage
            self.process = psutil.Process(os.getpid())
            self._write_function = self._write_unranked
            self._parse_function = self._parse_unranked
            self._merge_function = self._merge_unranked
            self.temp_index_folder = os.path.join(index_folder, 'blocks')
            self.segm_index_folder = os.path.join(index_folder, 'segments')
            if not os.path.isdir(index_folder):
                os.mkdir(index_folder)
            if not os.path.isdir(self.temp_index_folder):
                os.mkdir(self.temp_index_folder)
            if not os.path.isdir(self.segm_index_folder):
                os.mkdir(self.segm_index_folder)

        def __del__(self):
            shutil.rmtree(self.index_folder)

        def dispatch(self):
            if type(self.terms) != collections.OrderedDict:
                self.sort()
            filename = os.path.join(self.temp_index_folder, 'block-{}'.format(len(os.listdir(self.temp_index_folder))))
            with open(filename, 'w') as fout:
                fout.write(self.__str__())
            self.terms = {}
            gc.collect()

        def index(self, corpus_reader : CorpusReader):
            for pmid, document in corpus_reader.items():
                self.update(pmid, document)
                self.documents.add(pmid)
                if self.process.memory_percent() >= self.max_memory_usage:
                    self.dispatch()

        def merge(self, calculate_tfidf : bool = False):
            self.segments.clear()

            # select which function to use
            write_func = self.__write_forced_ranked if calculate_tfidf else self._write_function

            # sort in-memory terms if necessary
            if type(self.terms) != collections.OrderedDict:
                self.sort()

            # get in disk blocks
            filenames = [ filename for filename in [ os.path.join(self.temp_index_folder, filename) for filename in os.listdir(self.temp_index_folder) ] if os.path.isfile(filename) ]
            files = [ open(filename, 'r') for filename in filenames  ]

            # output file
            output_filename = os.path.join(self.segm_index_folder, 'segment-{}'.format(len(os.listdir(self.segm_index_folder))))
            output_file = open(output_filename, 'w')
            
            # current term for each sorted block
            lines = [ self._parse_function(line) for line in [ file.readline() for file in files ] if line and len(line.strip()) > 0 ]
            if len(self.terms) > 0:
                lines.append(self.terms.popitem(0))

            # temporary list to store terms before writing them to disk
            output = list()

            # gets first term (in order)
            cline = self.__get_line(lines, files, self._parse_function)

            # while terms to process are available
            while len(lines) > 0:

                # gets next term (in order)
                line = self.__get_line(lines, files, self._parse_function)

                # checks if current term and next term are mergable
                if line[0] == cline[0]:

                    # merges them
                    cline = (cline[0], self._merge_function(cline[1], line[1]))

                # else
                else:

                    # stores stringified version of term (and associated data)
                    output.append(write_func(cline))

                    # if too much memory in use then write to file stored terms
                    if self.process.memory_percent() >= self.max_memory_usage:
                        self.__flush(output, output_file, output_filename)
                        output_filename = os.path.join(self.segm_index_folder, 'segment-{}'.format(len(os.listdir(self.segm_index_folder))))
                        output_file = open(output_filename, 'w')
                        gc.collect()

                    # update current term
                    cline = line

            # stores stringified version of last term
            output.append(write_func(cline))

            self.__flush(output, output_file, output_filename)

            # deletes temporary blocks in disk
            shutil.rmtree(self.temp_index_folder)

            # sets if the data is ranked or not
            if calculate_tfidf:
                self._write_function = self._write_ranked
                self._parse_function = self._parse_ranked
                # self._merge_function = self._merge_ranked

        def sort(self):
            self.terms = collections.OrderedDict(sorted(self.terms.items()))

        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                documents[pmid] = documents.get(pmid, 0) + 1

        def _merge_unranked(self, docs0 : dict, docs1 : dict):
            return { key : docs0.get(key, 0) + docs1.get(key, 0) for key in docs0.keys() | docs1.keys() }

        def _parse_ranked(self, line : str):
            term, value = line.split(':', 1)
            idf, *docs = value.split(';')
            return (term, (float(idf), { pmid : (float(weight), round(10 ** (float(weight) / float(idf) - 1))) for pmid, weight in [ doc.split(':') for doc in docs ] }))

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
            return '\n'.join([ self._write_function(item) for item in self.terms.items() ])

        def __flush(self, output : list, output_file, output_filename : str):
            self.segments.append((output[0][0], output[-1][0], output_filename))
            output_file.write('\n'.join(output))
            output_file.close()
            output.clear()

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

        def __get_segment(self, key):
            segment = [ filename for start, end, filename in self.segments if key >= start and key <= end ]
            return segment[0] if len(segment) > 0 else None

        def __load_segment(self, segment):
            with open(segment, 'r') as fin:
                self.terms = collections.OrderedDict([ self._parse_function(line) for line in fin ])
            return self.terms

        def __write_forced_ranked(self, line : tuple):
            return self._write_ranked(self._rank(line))

        # useful functions to interact with the indexer
        def __contains__(self, key):
            if key in self.terms:
                return True
            segment = self.__get_segment(key)
            if segment is None:
                return False
            return key in self.__load_segment(segment)

        def __getitem__(self, key):
            value = self.terms.get(key, None)
            if value is not None:
                return value
            segment = self.__get_segment(key)
            if segment is None:
                raise KeyError(key)
            return self.__load_segment(segment)[key]

        def __iter__(self):
            for start, end, filename in self.segments:
                for value in iter(self.__load_segment(filename)):
                    yield value

        def __len__(self):
            length = 0
            for start, end, filename in self.segments:
                length += len(self.__load_segment(filename))
            return length

        def get(self, key, default = None):
            value = self.terms.get(key, None)
            if value is not None:
                return value
            segment = self.__get_segment(key)
            if segment is None:
                return default
            return self.__load_segment(segment).get(key, default)

        def items(self):
            for start, end, filename in self.segments:
                for item in self.__load_segment(filename).items():
                    yield item

        def keys(self):
            for start, end, filename in self.segments:
                for key in self.__load_segment(filename).keys():
                    yield key

        def save(self, output):
            if type(output) == str:
                with open(output, 'w') as fin:
                    self.save(fin)
            else:
                for start, end, filename in self.segments:
                    with open(filename, 'r') as fin:
                        output.write(fin.read())

        def values(self):
            for start, end, filename in self.segments:
                for value in self.__load_segment(filename).values():
                    yield value

    class __InnerPositionableIndexer(__InnerIndexer):
        def update(self, pmid, document):
            terms = self.terms
            for i, term in enumerate(self.tokenizer.tokenize(document)):
                documents = terms.setdefault(term, {})
                positions = documents.setdefault(pmid, [])
                positions.append(i)

        def _merge_unranked(self, docs0 : dict, docs1 : dict):
            return { key : sorted(docs0.get(key, []) + docs1.get(key, [])) for key in docs0.keys() | docs1.keys() }

        def _parse_ranked(self, line : str):
            term, value = line.split(':', 1)
            idf, *docs = value.split(';')
            return (term, (float(idf), { pmid : (float(weight), [ int(position) for position in positions.split(',') ]) for pmid, weight, positions in [ doc.split(':') for doc in docs ] }))

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
            return '{}:{};{}'.format(line[0], line[1][0], ';'.join([ '{}:{}:{}'.format(pmid, weight, ','.join([ str(position) for position in positions ])) for pmid, (weight, positions) in line[1][1].items() ]))

        def _write_unranked(self, line : tuple):   # line = (termo, {doc_id : [index1, index2]})
            return '{};{}'.format(line[0], ';'.join([ '{}:{}'.format(pmid, ','.join([ str(position) for position in positions ])) for pmid, positions in line[1].items() ]))

    def __init__(self, tokenizer : Tokenizer, index_folder : str, store_positions : bool = False):
        self.__indexer = self.__InnerPositionableIndexer(tokenizer, index_folder) if store_positions else self.__InnerIndexer(tokenizer, index_folder)

    def __getattr__(self, key):
        return getattr(self.__indexer, key)

    # explicit declaration of special methods required (not "intercepted" by __getattr__)
    def __contains__(self, key):
        return self.__indexer.__contains__(key)

    def __getitem__(self, key):
        return self.__indexer.__getitem__(key)

    def __iter__(self):
        return self.__indexer.__iter__()

    def __len__(self):
        return self.__indexer.__len__()