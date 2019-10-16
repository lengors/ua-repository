from tokenization import tokenizer, simple_tokenizer, Tokenizer
from corpus_reader import CorpusReader
from indexer import Indexer
import argparse, rules
import os, time

def one_document(od):
    return [ term for term, docs in sorted(od.items()) if len(docs) == 1 ][:10]

def highest_frequency(od):
    return [ term for term, _ in sorted(od.items(), key = lambda x: len(x[1]), reverse = True)[:10] ]

def get_filenames(inputname):
    if os.path.isfile(inputname):
        return [ inputname ]
    elif os.path.isdir(inputname):
        return [ os.path.join(inputname, filename) for filename in os.listdir(inputname) if os.path.isfile(os.path.join(inputname, filename)) ]
    return [ ]

def timeit(function, *args, **kwargs):
    start = time.time()
    result = function(*args, **kwargs)
    end = time.time()
    return result, end - start

def indexit(tokenizer, filenames):
    indexer = Indexer(used_tokenizer)
    for filename in filenames:
        corpus_reader = CorpusReader(filename)
        indexer.index(corpus_reader)
    return indexer

if __name__ == '__main__':
    tokenizers = { key : value for key, value in globals().items() if type(value) == Tokenizer }
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type = str, help = 'Filename or directory with files to index')
    parser.add_argument('output', type = str, help = 'Filename of the file with the indexer result')
    parser.add_argument('tokenizer', choices = list(tokenizers.keys()), type = str, help = 'Indicates which tokenizer the indexer must use')
    parser.add_argument('-s', '--stopwords', type = str, help = 'Filename of the stopwords list (ignored if tokenizer is "simple_tokenizer")', default = 'stopwords.txt')
    args = parser.parse_args()
    filenames = get_filenames(args.input)
    files_exist = len(filenames) != 0
    stopwords_exist = os.path.isfile(args.stopwords)
    if files_exist and stopwords_exist:
        used_tokenizer = tokenizers[args.tokenizer]
        if used_tokenizer.has_rule(rules.stopping):
            used_tokenizer.make_rule(rules.stopping, args.stopwords)
        indexer, interval = timeit(indexit, used_tokenizer, filenames)
        indexer.save(args.output)
        print('Answers:')
        print(' a) Time taken: {:.2f}s; Disk size: {:.1f}kB.'.format(interval, os.path.getsize(args.output) / 1000))
        print(' b) Vocabulary size: {}.'.format(len(indexer.terms)))
        print(' c) {}.'.format(one_document(indexer.terms)))
        print(' d) {}.'.format(highest_frequency(indexer.terms)))
    else:
        if not files_exist:
            print('Error: File or directory (with files) to index doesn\'t exist!')
        if not stopwords_exist:
            print('Error: Stopwords\' file doesn\'t exist!')