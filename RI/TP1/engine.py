from tokenization import tokenizer, simple_tokenizer
from corpus_reader import CorpusReader
import sys

if len(sys.argv) > 1:
    with open(sys.argv[1]) as file:
        corpus_reader = CorpusReader(file)
        for pmid, document in corpus_reader.documents.items():
            print('ID: {}'.format(pmid))
            print(simple_tokenizer.tokenize(document))
            print()
else:
    print('Usage: python exercise_2_1.py [filename]')