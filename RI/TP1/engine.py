from tokenization import tokenizer, simple_tokenizer
from corpus_reader import CorpusReader
from Stemmer import Stemmer
from indexer import Indexer
import sys, os

def load(filename):
    if os.path.isfile(filename):
        return open(filename)
    return None

if len(sys.argv) > 1:
    file = load(sys.argv[1])
    indexer = Indexer()
    if file is not None:
        stopwords_file = load('stopwords.txt')
        if stopwords_file is not None:
            stemmer = Stemmer('english')
            corpus_reader = CorpusReader(file)
            stopwords = [ word.strip() for word in stopwords_file ]
            #print(stopwords)
            for pmid, document in corpus_reader.documents.items():
                #print('ID: {}'.format(pmid))
                tokens = enumerate(simple_tokenizer.tokenize(document))
                tokens = [ (i,stemmer.stemWord(token)) for i, token in tokens if token not in stopwords ]
                indexer.update(pmid, tokens)
                #print(tokens)
                #print()
        else:
            print('Error: Stopwords\' file doesn\'t exist!')
    else:
        print('Error: File doesn\'t exist!')
    print(indexer)
else:
    print('Usage: python engine.py [filename]')

