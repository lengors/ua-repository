from tokenization import tokenizer, simple_tokenizer, Tokenizer
from corpus_reader import CorpusReader
from indexer import Indexer
from index import Index
import argparse, rules
import os, time, utils
import shutil

'''
    Trabalho realizado por : 
        - Lucas Barros, nmec : 83895;
        - Pedro Cavadas, nmec : 85090;
'''

# idf = log10(N / dft), N = nº total de documentos, dft n º de documentos em que o termo aparece

def one_document(od):
    return [ term for term, (idf, docs) in od.items() if len(docs) == 1 ][:10]

def highest_frequency(od):
    return [ term for term, _ in sorted(od.items(), key = lambda x: len(x[1][1]), reverse = True)[:10] ]

def indexit(tokenizer, filenames, store_positions = False, calculate_tfidf = False, memory_usage = 20):
    index = Index(tokenizer, store_positions)
    indexer = Indexer(index, 'index', max_memory_usage = memory_usage)
    for filename in filenames:
        indexer.index(CorpusReader(filename))
    indexer.merge(calculate_tfidf)
    return index

def main():
    parser.add_argument('--store_positions', action='store_true', help = 'Indicates if indexer stores positions of terms or not')
    parser.add_argument('--tfidf', action='store_true', help = 'Indicates if program calculates tfidf or not')
    args = parser.parse_args()
    filenames = utils.get_filenames(args.input)
    files_exist = len(filenames) != 0
    stopwords_exist = os.path.isfile(args.stopwords)
    if files_exist and stopwords_exist:
        used_tokenizer = tokenizers[args.tokenizer]
        if used_tokenizer.has_rule(rules.stopping):
            used_tokenizer.make_rule(rules.stopping, args.stopwords)
        (index, max_memory) , interval = utils.timeit(utils.profileit,
            indexit, used_tokenizer, filenames, store_positions = args.store_positions, calculate_tfidf = args.tfidf, memory_usage = args.memory)
        index.save(args.output)
        print('Answers:')
        print('Time taken: {}s'.format(interval))
        print('Max memory usage: {}'.format(utils.sizeof_fmt(max_memory)))
        print('Disk size: {}'.format(utils.sizeof_fmt(os.path.getsize('{}.csv'.format(args.output)))))
        shutil.rmtree('index')
    else:
        if not files_exist:
            print('Error: File or directory (with files) to index doesn\'t exist!')
        if not stopwords_exist:
            print('Error: Stopwords\' file doesn\'t exist!')

tokenizers = { key : value for key, value in globals().items() if isinstance(value, Tokenizer) }
parser = argparse.ArgumentParser()
parser.add_argument('input', type = str, help = 'Filename or directory with files to index')
parser.add_argument('output', type = str, help = 'Filename of the file with the indexer result')
parser.add_argument('tokenizer', choices = list(tokenizers.keys()), type = str, help = 'Indicates which tokenizer the indexer must use')
parser.add_argument('-s', '--stopwords', type = str, help = 'Filename of the stopwords list (ignored if tokenizer is "simple_tokenizer")', default = 'stopwords.txt')
parser.add_argument('-m', '--memory', type = int, help = 'Percentage of max memory used in the process', default = 20)

if __name__ == '__main__':
    main()