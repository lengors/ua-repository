import collections, math, pickle, os
from tokenization import Tokenizer

def body_ranked(value):
    idf, *docs = value[0].split(';')
    return (float(idf), { pmid : (float(weight), round(10 ** (float(weight) / float(idf) - 1))) for pmid, weight in [ doc.split(':') for doc in docs ] })

def body_ranked_positional(value):
    idf, *docs = value[0].split(';')
    return (float(idf), { pmid : (float(weight), [ int(position) for position in positions.split(',') ]) for pmid, weight, positions in [ doc.split(':') for doc in docs ] })

def body_unranked(docs):
    return { key : int(value) for key, value in [ doc.split(':') for doc in docs ] }

def body_unranked_positional(docs):
    return { pmid : [ int(position) for position in positions.split(',') ] for pmid, positions in [ doc.split(':') for doc in docs ] }

def count(value):
    return value

def count_positional(value):
    return len(value)

def header(line : str):
    return line.strip().split(';')

def header_ranked(line : str):
    return line.strip().split(':', 1)

def merge(docs0 : dict, docs1: dict):
    return { key : docs0.get(key, 0) + docs1.get(key, 0) for key in docs0.keys() | docs1.keys() }

def merge_positional(docs0 : dict, docs1 : dict):
    return { key : sorted(docs0.get(key, []) + docs1.get(key, [])) for key in docs0.keys() | docs1.keys() }

def parse_ranked(line : str):
    term, *value = header_ranked(line)
    return (term, body_ranked(value))

def parse_ranked_positional(line : str):
    term, *value = header_ranked(line)
    return (term, body_ranked_positional(value))

def parse_unranked(line : str):
    term, *docs = header(line)
    return (term, body_unranked(docs))

def parse_unranked_positional(line : str):
    term, *docs = header(line)
    return (term, body_unranked_positional(docs))

def write_ranked(line : tuple):
    return '{}:{};{}'.format(line[0], line[1][0], ';'.join([ '{}:{}'.format(pmid, weight) for pmid, (weight, count) in line[1][1].items() ]))

def write_ranked_positional(line : tuple):
    return '{}:{};{}'.format(line[0], line[1][0], ';'.join([ '{}:{}:{}'.format(pmid, weight, ','.join([ str(position) for position in positions ])) for pmid, (weight, positions) in line[1][1].items() ]))

def write_unranked(line : tuple):
    return '{};{}'.format(line[0], ';'.join([ '{}:{}'.format(pmid, count) for pmid, count in line[1].items() ]))

def write_unranked_positional(line : tuple):
    return '{};{}'.format(line[0], ';'.join([ '{}:{}'.format(pmid, ','.join([ str(position) for position in positions ])) for pmid, positions in line[1].items() ]))

class Index:
    def __init__(self, tokenizer : Tokenizer, positional: bool, ranked: bool = False):
        self.__terms = dict()
        self.__tokenizer = tokenizer
        if positional is not None and ranked is not None:
            self.__positional = positional
            self.__segments = list()
            self.__ranked = ranked
            self.__update_functions()

    def __get_segment(self, key):
            segment = [ filename for start, end, filename, _ in self.__segments if key >= start and key <= end ]
            return segment[0] if len(segment) > 0 else None

    def __load_segment(self, segment):
        with open(segment, 'r') as fin:
            self.__terms = collections.OrderedDict([ self.parse(line) for line in fin if len(line.strip()) > 0 ])
        return self.__terms

    def __save_segment(self, segment):
        with open(segment, 'w') as fout:
            fout.write(str(self))

    def __update(self, pmid, document):
        terms = self.__terms
        for term in self.__tokenizer.tokenize(document):
            documents = terms.setdefault(term, {})
            documents[pmid] = documents.get(pmid, 0) + 1

    def __update_functions(self):
        if self.__positional:
            self.count = count_positional
            self.merge = merge_positional
            if self.__ranked:
                self.body = body_ranked_positional
                self.header = header_ranked
                self.parse = parse_ranked_positional
                self.write = write_ranked_positional
            else:
                self.body = body_unranked_positional
                self.header = header
                self.parse = parse_unranked_positional
                self.write = write_unranked_positional
            self.update = self.__update_positional
            self.write_ranked = write_ranked_positional
        else:
            self.count = count
            self.merge = merge
            if self.__ranked:
                self.body = body_ranked
                self.header = header_ranked
                self.parse = parse_ranked
                self.write = write_ranked
            else:
                self.body = body_unranked
                self.header = header
                self.parse = parse_unranked
                self.write = write_unranked
            self.update = self.__update
            self.write_ranked = write_ranked

    def __update_positional(self, pmid, document):
        terms = self.__terms
        for i, term in enumerate(self.__tokenizer.tokenize(document)):
            documents = terms.setdefault(term, {})
            positions = documents.setdefault(pmid, [])
            positions.append(i)

    def __contains__(self, key):
        if key in self.__terms:
            return True
        segment = self.__get_segment(key)
        if segment is None:
            return False
        return key in self.__load_segment(segment)

    def __getitem__(self, key):
        value = self.__terms.get(key, None)
        if value is not None:
            return value
        segment = self.__get_segment(key)
        if segment is None:
            raise KeyError(key)
        return self.__load_segment(segment)[key]

    def __iter__(self):
        if self.segmented:
            for _, _, filename, _ in self.__segments:
                for value in iter(self.__load_segment(filename)):
                    yield value
        else:
            return iter(self.__terms)

    def __len__(self):
        if self.segmented:
            length = 0
            for _, _, filename, _ in self.__segments:
                length += len(self.__load_segment(filename))
            return length
        return len(self.__terms)

    def __repr__(self):
            return self.__str__()

    def __str__(self):
        return '{}\n'.format('\n'.join([ self.write(item) for item in self.__terms.items() ]))

    def get(self, key, default = None):
        value = self.__terms.get(key, None)
        if value is not None:
            return value
        segment = self.__get_segment(key)
        if segment is None:
            return default
        return self.__load_segment(segment).get(key, default)

    def items(self):
        if self.segmented:
            for _, _, filename, _ in self.__segments:
                for item in self.__load_segment(filename).items():
                    yield item
        else:
            return self.__terms.items()

    def keys(self):
        if self.segmented:
            for _, _, filename, _ in self.__segments:
                for key in self.__load_segment(filename).keys():
                    yield key
        else:
            return self.__terms.keys()

    def lazyget(self, key, default = None):
        value = self.__terms.get(key, None)
        if value is not None:
            return value
        segment = self.__get_segment(key)
        if segment is None:
            return default
        with open(segment, 'r') as fin:
            for line in fin:
                term, *body = self.header(line)
                if term == key:
                    return self.body(body)
        return default

    def normalize(self, documents):
        for document, length in documents.items():
            documents[document] = math.sqrt(length)

        for _, _, segment, _ in self.__segments:
            self.__load_segment(segment)
            for _, (_, docs) in self.terms.items():
                for pmid, (weight, extra) in docs.items():
                    docs[pmid] = (weight / documents[pmid], extra)
            self.__save_segment(segment)

    def reset(self):
        self.__terms = {}

    def save(self, *args):
        if len(args) == 1:
            filename = args[0]
            with open('{}.csv'.format(filename), 'w') as fout_data:
                with open('{}.idx'.format(filename), 'wb') as fout_state:
                    self.save(fout_data, fout_state)
        else:
            output_data, output_state = args
            if self.segmented:
                for _, _, filename, _ in self.__segments:
                    with open(filename, 'r') as fin:
                        output_data.write(fin.read())
            else:
                output_data.write(str(self))
            keys = [ 'positional', 'ranked', 'segments' ]
            state = { key : self.__dict__['_Index__{}'.format(key)] for key in keys }
            output_state.write(pickle.dumps(state))

    def sort(self):
        if not isinstance(self.__terms, collections.OrderedDict):
            self.__terms = collections.OrderedDict(sorted(self.__terms.items()))

    def values(self):
        if self.segmented:
            for _, _, filename, _ in self.__segments:
                for value in self.__load_segment(filename).values():
                    yield value
        else:
            return self.__terms.values()

    @property
    def positional(self):
        return self.__positional

    @property
    def ranked(self):
        return self.__ranked

    @property
    def segmented(self):
        return len(self.__segments) > 0

    @property
    def segments(self):
        return self.__segments

    @property
    def terms(self):
        return self.__terms

    @property
    def tokenizer(self):
        return self.__tokenizer

    @positional.setter
    def positional(self, positional : bool):
        self.__positional = positional
        self.__update_functions()

    @ranked.setter
    def ranked(self, ranked : bool):
        self.__ranked = ranked
        self.__update_functions()

    @staticmethod
    def load(*args):
        if len(args) == 1 or (len(args) == 2 and isinstance(args[1], Tokenizer)):
            input, *tokenizer = args
            with open('{}.csv'.format(input), 'r') as fin_data:
                with open('{}.idx'.format(input), 'rb') as fin_state:
                    return Index.load(fin_data, fin_state, *tokenizer)
        else:
            input_data, input_state, *tokenizer = args
            index = Index(tokenizer[0] if len(tokenizer) > 0 else None, None, None)
            state = pickle.loads(input_state.read())
            for key, value in state.items():
                index.__dict__['_Index__{}'.format(key)] = value
            index.__update_functions()

            for _, _, filename, size in index.__segments:
                pathname = os.path.dirname(filename)
                if not os.path.isdir(pathname):
                    os.makedirs(pathname)
                with open(filename, 'w') as fout:
                    fout.write(''.join([ next(input_data) for i in range(size) ]))

            return index

    @staticmethod
    def segment_on_load(output, segmentation = 10, folder = 'index\\segments', tokenizer = None):
        if type(output) == str:
            with open('{}.csv'.format(output), 'r') as fin_data:
                with open('{}.idx'.format(output), 'rb') as fin_state:
                    return Index.segment_on_load([ fin_data, fin_state ], segmentation, folder, tokenizer)
        else:
            fin_data, fin_state = output
            index = Index(tokenizer, None, None)
            state = pickle.loads(fin_state.read())
            index.__ranked = state['ranked']
            index.__positional = state['positional']
            index.__update_functions()

            if not os.path.isdir(folder):
                os.makedirs(folder)

            index.__segments = list()

            size = math.ceil(os.stat(fin_data.fileno()).st_size / segmentation)
            for i in range(segmentation):
                segment = fin_data.readlines(size)
                filename = os.path.join(folder, 'segment-{}'.format(len(os.listdir(folder))))
                with open(filename, 'w') as fout:
                    fout.write(''.join(segment))
                index.__segments.append((index.header(segment[0])[0], index.header(segment[-1])[0], filename, len(segment)))
            return index