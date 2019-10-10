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
        file.write(''.join([ '{}{}\n'.format(key, ''.join([ ' , {} - {}'.format(k, len(v)) for k, v in sec_dic.items() ])) for key, sec_dic in od.items() ]))

def one_document(od):
    terms = []
    for term in od:
        if len(terms) == 10:
            break
        if len(od[term]) == 1:
            terms.append(term)
    return terms

def highest_frequency(od):
    lista = []
    for i in range(10):
        maior = 0
        for term in od:
            if len(od[term]) > maior and term not in lista:
                maior = len(od[term])
                termo = term
        lista.append(termo)
    return lista

if len(sys.argv) > 2:
    directory = sys.argv[1]
    output = sys.argv[2]
    indexer = Indexer()
    if os.path.exists(directory):
        stopwords_file = load('stopwords.txt')
        if stopwords_file is not None:
            stemmer = Stemmer('english')
            stopwords = [ word.strip() for word in stopwords_file ]
            for filename in os.listdir(directory):
                file = open(os.path.join(directory, filename))
                corpus_reader = CorpusReader(file)
                for pmid, document in corpus_reader.documents.items():
                    tokens = enumerate(simple_tokenizer.tokenize(document))
                    tokens = [ (i,stemmer.stemWord(token)) for i, token in tokens if token not in stopwords ]
                    indexer.update(pmid, tokens)
               
        else:
            print('Error: Stopwords\' file doesn\'t exist!')
    else:
        print('Error: File doesn\'t exist!')
    od = collections.OrderedDict(sorted(indexer.terms.items()))
    one_doc = one_document(od)
    print(one_doc)
    print("----")
    print(highest_frequency(od))
    write_file(output, od)
    
else:
    print('Usage: python engine.py [filename]')

