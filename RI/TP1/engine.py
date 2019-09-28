from tokenization import tokenizer, simple_tokenizer
from corpus_reader import CorpusReader
from Stemmer import Stemmer
import sys, os

def load(filename):
    if os.path.isfile(filename):
        return open(filename)
    return None

if len(sys.argv) > 1:
    file = load(sys.argv[1])
    if file is not None:
        stopwords_file = load('stopwords.txt')
        if stopwords_file is not None:
            stemmer = Stemmer('english')
            corpus_reader = CorpusReader(file)
            stopwords = [ word for word in stopwords_file ]
            for pmid, document in corpus_reader.documents.items():
                print('ID: {}'.format(pmid))
                tokens = simple_tokenizer.tokenize(document)
                tokens = [ stemmer.stemWord(token) for token in tokens if token not in stopwords ]
                print(tokens)
                print()
        else:
            print('Error: Stopwords\' file doesn\'t exist!')
    else:
        print('Error: File doesn\'t exist!')
else:
    print('Usage: python engine.py [filename]')