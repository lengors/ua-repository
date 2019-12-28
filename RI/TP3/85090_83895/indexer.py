from corpus_reader import CorpusReader
from index import Index

# python modules
import psutil, os, gc, shutil, math

class Indexer:
    def __init__(self, index : Index, index_folder : str, max_memory_usage : float = 20):
        self.__index = index
        self.__documents = dict()
        self.__max_memory_usage = max_memory_usage
        self.__process = psutil.Process(os.getpid())
        self.__temp_index_folder = os.path.join(index_folder, 'blocks')
        self.__segm_index_folder = os.path.join(index_folder, 'segments')

    def __dispatch(self):
        self.__index.sort()
        self.__ensure_folders()
        filename = os.path.join(self.__temp_index_folder, 'block-{}'.format(len(os.listdir(self.__temp_index_folder))))
        with open(filename, 'w') as fout:
            fout.write(str(self.__index))
        self.__index.reset()
        gc.collect()

    def __ensure_folders(self):
        if not os.path.isdir(self.__temp_index_folder):
            os.makedirs(self.__temp_index_folder)
        if not os.path.isdir(self.__segm_index_folder):
            os.makedirs(self.__segm_index_folder)

    def __flush(self, segments, output : list, output_file, output_filename : str):
        segments.append((output[0][0], output[-1][0], output_filename, len(output)))
        output_file.write('{}\n'.format('\n'.join([ line for _, line in output ])))
        output_file.close()
        output.clear()

    def __get_line(self, terms, lines, files, parse_func):
        i, line = min(enumerate(lines), key = lambda line: line[1][0])
        if i >= len(files):
            if len(terms) > 0:
                lines[i] = terms.popitem(0)
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

    def __rank(self, line : tuple):
        term, documents = line
        count = self.__index.count
        idf = math.log10(len(self.__documents) / len(documents))
        for pmid, extra in documents.items():
            weight = 1 + math.log10(count(extra))
            self.__documents[pmid] += weight * weight
            documents[pmid] = (weight, extra)
        return (term, (idf, documents))

    def __write_forced_ranked(self, line : tuple):
        return self.__index.write_ranked(self.__rank(line))

    def index(self, corpus_reader : CorpusReader):
        update = self.__index.update
        for pmid, document in corpus_reader.items():
            update(pmid, document)
            self.__documents.setdefault(pmid, 0)
            if self.__process.memory_percent() >= self.__max_memory_usage:
                self.__dispatch()

    def merge(self, calculate_tfidf : bool = False):
        # select which function to use
        write = self.__write_forced_ranked if calculate_tfidf else self.__index.write
        parse = self.__index.parse
        merge = self.__index.merge

        # sort in-memory terms if necessary
        self.__index.sort()

        terms = self.__index.terms
        segments = self.__index.segments

        # clear segments
        segments.clear()

        # ensures folders exist
        self.__ensure_folders()

        # get in disk blocks
        filenames = [ filename for filename in [ os.path.join(self.__temp_index_folder, filename) for filename in os.listdir(self.__temp_index_folder) ] if os.path.isfile(filename) ]
        files = [ open(filename, 'r') for filename in filenames  ]

        # output file
        output_filename = os.path.join(self.__segm_index_folder, 'segment-{}'.format(len(os.listdir(self.__segm_index_folder))))
        output_file = open(output_filename, 'w')
            
        # current term for each sorted block
        lines = [ parse(line) for line in [ file.readline() for file in files ] if line and len(line.strip()) > 0 ]
        if len(terms) > 0:
            lines.append(terms.popitem(0))

        # temporary list to store terms before writing them to disk
        output = list()

        # gets first term (in order)
        cline = self.__get_line(terms, lines, files, parse)

        # while terms to process are available
        while len(lines) > 0:

            # gets next term (in order)
            line = self.__get_line(terms, lines, files, parse)

            # checks if current term and next term are mergable
            if line[0] == cline[0]:

                # merges them
                cline = (cline[0], merge(cline[1], line[1]))

            # else
            else:
                # stores stringified version of term (and associated data)
                output.append((cline[0], write(cline)))

                # if too much memory in use then write to file stored terms
                if self.__process.memory_percent() >= self.__max_memory_usage:
                    self.__flush(segments, output, output_file, output_filename)
                    output_filename = os.path.join(self.__segm_index_folder, 'segment-{}'.format(len(os.listdir(self.__segm_index_folder))))
                    output_file = open(output_filename, 'w')
                    gc.collect()

                # update current term
                cline = line

        # stores stringified version of last term
        output.append((cline[0], write(cline)))

        self.__flush(segments, output, output_file, output_filename)

        # deletes temporary blocks in disk
        shutil.rmtree(self.__temp_index_folder)

        # sets if the data is ranked or not
        if calculate_tfidf:
            self.__index.ranked = True
            self.__index.normalize(self.__documents)