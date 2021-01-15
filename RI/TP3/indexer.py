from collections import defaultdict, Counter, OrderedDict
from CorpusReader import CorpusReader
import math
import sys
import psutil
import os
from Tokenizer import Tokenizer
from Index import Index


class Indexer:

    def __init__(self, writing_method: int = 0, positional: int = 0, output_path: str = 'index/',
                 block_max_size: float = 1000000, option: int = 2):
        self.index = Index(writing_method, positional, Tokenizer(option))
        self.writing_method = writing_method
        self.positional = positional
        self.parse = self.index.parse_line
        self.k = 1.2
        self.b = 0.75
        self.avdl = 0
        self.block_max_size = block_max_size
        self.docs_dl = OrderedDict()
        self.output_path = output_path
        self.size = 0
        self.temp_folder = 'index_blocks/'
        os.makedirs(self.temp_folder)
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

    # Creates index
    def create_index(self, corpus: CorpusReader):
        writing_method = self.writing_method
        update_index = self.index.update_index
        write_block_to_file = self.write_block_to_file
        clear_index = self.index.clear
        block_max_size = self.block_max_size
        self.size = len(corpus.doc_list)
        size = self.size
        numb_blocks = 0

        for doc in corpus.doc_list:

            update_index(doc.cord_uid, doc)

            if writing_method == 3:
                self.docs_dl[doc.cord_uid] = len(doc.list_tokens)

            if sys.getsizeof(self.index) > block_max_size or (self.index == size - 1):
                if writing_method == 3:
                    self.avdl = sum(self.docs_dl.values()) / len(self.docs_dl)
                write_block_to_file(numb_blocks)
                numb_blocks += 1
                clear_index()

        if writing_method == 3:
            self.avdl = sum(self.docs_dl.values()) / len(self.docs_dl)

    # Writes index to file
    def write_block_to_file(self, numb_blocks):
        file_path = os.path.join(self.temp_folder, 'block_{}'.format(numb_blocks))
        write_term = self.index.write_term_line
        with open(file_path, "w+", encoding='utf-8') as file:
            write = file.write
            for term in self.index.tokens:
                write(self.index.write_term_line(term))
        file.close()

    def get_term_line(self, tokens, lines, files):
        x, term_line = min(enumerate(lines), key=lambda l: l[1][0])
        if x >= len(files):
            if len(tokens) > 0:
                lines[x] = tokens.popitem(0)
            else:
                lines.pop(x)
        else:
            other_term_line = files[x].readline()
            if not other_term_line or len(other_term_line.strip()) == 0:
                lines.pop(x)
                files[x].close()
                files.pop(x)
            else:
                lines[x] = self.index.parse_line(other_term_line)
        return term_line

    def write_ranked(self, term):
        return self.index.write_term_line(self.rank_term(term))

    def rank_term(self, term: tuple):
        size = self.size
        k = self.k
        b = self.b
        avdl = self.avdl
        token, docs = term
        df = len(docs.keys())
        idf = math.log10(size / df)

        for cord_uid, positions in docs.items():
            if self.writing_method == 2:
                if self.positional == 0:
                    weight = (1 + math.log10(positions)) * idf
                else:
                    weight = (1 + math.log10(len(positions))) * idf

            else:
                if self.positional == 0:
                    weight = (math.log10(size / df) *
                              (((k + 1) * positions) /
                               (k * ((1 - b) + b * (self.docs_dl[cord_uid] / avdl)) + positions)))
                else:
                    weight = (math.log10(size / df) *
                              (((k + 1) * len(positions)) /
                               (k * ((1 - b) + b * (self.docs_dl[cord_uid] / avdl)) + len(positions))))
            docs[cord_uid] = (weight, positions)
        return term, (idf, docs)

    def merge_blocks(self):

        tokens = self.index.tokens
        parts = self.index.parts
        if self.writing_method == 2 or self.writing_method == 3:
            write = self.write_ranked
        else:
            write = self.index.write_term_line
        parts.clear()

        filenames = [filename for filename in [os.path.join(self.temp_folder, filename) for filename in
                                               os.listdir(self.temp_folder)] if os.path.isfile(filename)]
        files = [open(filename, 'r') for filename in filenames]

        output_filename = os.path.join(self.output_path, 'index_part{}'.format(len(os.listdir(self.output_path))))
        output_file = open(output_filename, 'w')

        lines = [parse(line) for line in [file.readline() for file in files] if line and len(line.strip()) > 0]

        if len(tokens) > 0:
            lines.append(tokens.popitem(0))

        output = list()

        term = self.get_term_line(tokens, lines, files)

        # while there are terms to process
        while len(lines) > 0:

            # next term
            next_term = self.get_term_line(tokens, lines, files)

            if next_term[0] == term[0]:

                # merges the terms
                if self.positional == 0:
                    merged = {k: term[1].get(k, 0) + next_term[1].get(k, 0) for k in term[1].keys() | next_term[1].keys()}
                else:
                    merged = {k: sorted(term[1].get(k, []) + next_term[1].get(k, [])) for k in
                              term[1].keys() | next_term[1].keys()}

                term = (term[0], merged)

            else:
                # stores string version of term
                output.append((term[0], write(term)))

                # if too much memory in use then write to file stored terms
                if self.__process.memory_percent() >= self.__max_memory_usage:
                    self.__flush(parts, output, output_file, output_filename)
                    output_filename = os.path.join(self.output_path,
                                                   'index_part-{}'.format(len(os.listdir(self.output_path))))
                    output_file = open(output_filename, 'w')
                    gc.collect()

                # update current term
                term = next_term

        # stores string version of last term
        output.append((term[0], write(term)))

        self.__flush(parts, output, output_file, output_filename)

        # deletes temporary blocks in disk
        shutil.rmtree(self.temp_folder)

        if self.writing_method == 2 or self.writing_method == 3:
            self.index.normalization(self.docs_dl)
