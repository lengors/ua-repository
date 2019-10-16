from tokenization import tokenizer, simple_tokenizer
from corpus_reader import CorpusReader
from indexer import Indexer
import collections, rules
import sys, os, time

def write_file(filename, od):
    with open(filename, 'w') as file:
        file.write(''.join([ '{}{}\n'.format(key, ''.join([ ' , {} - {}'.format(k, len(v)) for k, v in sec_dic.items() ])) for key, sec_dic in od.items() ]))

def one_document(od):
    return list(od.keys())[:10]

def highest_frequency(od):
    return [ term for term, _ in sorted(od.items(), key = lambda x: len(x[1]), reverse = True)[:10] ]

def get_filenames(inputname):
    if os.path.isfile(inputname):
        return [ inputname ]
    elif os.path.isdir(inputname):
        return [ os.path.join(inputname, filename) for filename in os.listdir(inputname) if os.path.isfile(os.path.join(inputname, filename)) ]
    return [ ]

if __name__ == '__main__':
    #temp
    start = time.time()
    if len(sys.argv) > 3:
        stopwords_filename = 'stopwords.txt'
        inputname, output = sys.argv[1], sys.argv[2]
        token = sys.argv[3]
        filenames = get_filenames(inputname)
        if len(filenames) != 0 and os.path.isfile(stopwords_filename):
            start_t = time.time()
            indexer = Indexer()
            used_tokenizer = tokenizer if token == "tokenizer" else simple_tokenizer
            if used_tokenizer.has_rule(rules.stopping):
                used_tokenizer.make_rule(rules.stopping, stopwords_filename)
            for filename in filenames:
                corpus_reader = CorpusReader(filename)
                for pmid, document in corpus_reader.documents.items():
                    tokens = [ (i, token) for i, token in enumerate(used_tokenizer.tokenize(document)) ]
                    indexer.update(pmid, tokens)
            od = collections.OrderedDict(sorted(indexer.terms.items()))
            print(one_document(od))
            print("----")
            print(highest_frequency(od))
            end_t = time.time()
            print(end_t - start_t)
            write_file(output, od)
        else:
            if len(filenames) == 0:
                print('Error: File or directory (with files) don\'t exist!')
            if not os.path.isfile(stopwords_filename):
                print('Error: Stopwords\' file doesn\'t exist!')
    else:
        print('Usage: python engine.py [directiory|filename] [output_filename] [tokenizer_name]')
    end = time.time()
    print(end - start)