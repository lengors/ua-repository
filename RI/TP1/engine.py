from tokenization import tokenizer, simple_tokenizer
from corpus_reader import CorpusReader
from Stemmer import Stemmer
from indexer import Indexer
import sys, os
import collections

def load(filename):
    if os.path.isfile(filename):
        return open(filename)
    return None

def write_file(filename, od):
    with open(filename, 'w') as file:
        for key in od:
            file.write(key)
            sec_dic = od[key]
            for k in sec_dic:
                file.write(" , " + str(k) + " - " + str(len(sec_dic[k])))
            file.write("\n")



if len(sys.argv) > 2:
    directory = sys.argv[1]
    output = sys.argv[2]
    indexer = Indexer()
    if os.path.exists(directory):
        stopwords_file = load('stopwords.txt')
        if stopwords_file is not None:
            stemmer = Stemmer('english')
            for filename in os.listdir(directory):
                file = open(os.path.join(directory, filename))
                corpus_reader = CorpusReader(file)
                stopwords = [ word.strip() for word in stopwords_file ]
                for pmid, document in corpus_reader.documents.items():
                    tokens = enumerate(tokenizer.tokenize(document))
                    tokens = [ (i,stemmer.stemWord(token)) for i, token in tokens if token not in stopwords ]
                    indexer.update(pmid, tokens)
               
        else:
            print('Error: Stopwords\' file doesn\'t exist!')
    else:
        print('Error: File doesn\'t exist!')
    od = collections.OrderedDict(sorted(indexer.terms.items()))
    
    write_file(output, od)
    
else:
    print('Usage: python engine.py [filename]')

