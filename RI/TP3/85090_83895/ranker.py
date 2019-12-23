import rules, utils
from index import Index
from utils import timeit
from corpus_reader import CorpusReader
from tokenization import tokenizer, simple_tokenizer, Tokenizer
import os, shutil, math, pprint, collections, argparse, itertools

class Ranker:
    def __init__(self,  index : Index):
        self.index = index

    def rank(self, query):
        query_vector = dict()
        documents_vectors = dict()
        query = self.index.tokenizer.tokenize(query)
        for term in query:
            result = self.index.lazyget(term, None)
            if result is not None:
                idf, documents = result
                query_vector.setdefault(term, idf * query.count(term))
                for pmid, (weight, _) in documents.items():
                    document_vector = documents_vectors.setdefault(pmid, {})
                    document_vector.setdefault(term, weight)
        
        # normalize
        norm = math.sqrt(sum(map(lambda x: x * x, query_vector.values())))
        query_vector = { key : value / norm for key, value in query_vector.items() }

        # comparsion
        scores = dict()
        for pmid, document_vector in documents_vectors.items():
            scores[pmid] = sum(weight * document_vector.get(term, 0) for term, weight in query_vector.items())
        return collections.OrderedDict(sorted(scores.items(), key = lambda x: -x[1]))

if __name__ == '__main__':
    tokenizers = { key : value for key, value in globals().items() if isinstance(value, Tokenizer) }

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type = str, help = 'Query to rank')
    parser.add_argument('-f', '--file', type = str, help = 'File with queries to rank')
    parser.add_argument('documents', type = str, help = 'Filename or directory with documents')
    parser.add_argument('model', type = str, help = 'Filename (without extension) of the index model')
    parser.add_argument('tokenizer', choices = list(tokenizers.keys()), type = str, help = 'Indicates which tokenizer the ranker must use')
    parser.add_argument('-s', '--stopwords', type = str, help = 'Filename of the stopwords list (ignored if tokenizer is "simple_tokenizer")', default = 'stopwords.txt')
    args = parser.parse_args()

    filenames = utils.get_filenames(args.documents)
    files_exist = len(filenames) != 0
    stopwords_exist = os.path.isfile(args.stopwords)
    has_file = os.path.isfile(args.file) if args.file else True
    model_exist = os.path.isfile('{}.csv'.format(args.model)) and os.path.isfile('{}.idx'.format(args.model))
    if files_exist and model_exist and stopwords_exist and has_file:
        used_tokenizer = tokenizers[args.tokenizer]
        if used_tokenizer.has_rule(rules.stopping):
            used_tokenizer.make_rule(rules.stopping, args.stopwords)
        index = Index.segment_on_load(args.model, tokenizer = used_tokenizer)
        ranker = Ranker(index)

        queries = []
        if args.query:
            queries.append(args.query)
        if args.file:
            with open(args.file, 'r') as fin:
                queries.extend([ line.strip().split('\t')[1] for line in fin ])

        result = {}
        queries = { query : collections.OrderedDict(itertools.islice(ranker.rank(query).items(), 10)) for query in queries }

        for filename in filenames:
            for pmid, document in CorpusReader(filename).items():
                toremove = list()
                for query, scores in queries.items():
                    score = scores.pop(pmid, None)
                    if score is not None:
                        if len(scores) == 0:
                            toremove.append(query)
                        result_scores = result.setdefault(query, [])
                        result_scores.append((document, score))
                for query in toremove:
                    queries.pop(query)
                if len(queries) == 0:
                    break
            else: # Continues if the inner loop DIDN'T break!
                continue
            break
 
        for query in result.keys():
            result[query] = sorted(result[query], key = lambda x: -x[1])
        pprint.pprint(result)
        shutil.rmtree('index')
    else:
        if not files_exist:
            print('Error: File or directory (with files) with documents doesn\'t exist!')
        if not model_exist:
            print('Error: Index model doesn\'t exist or is incomplete!')
        if not stopwords_exist:
            print('Error: Stopwords\' file doesn\'t exist!')
        if not has_file:
            print('Error: Specified file with queries doesn\'t exist!')

    '''
    tokenizer.make_rule(rules.stopping, 'stopwords.txt')
    index = Index.segment_on_load('output', tokenizer = tokenizer)
    ranker = Ranker(index)

    (scores, time) = timeit(ranker.rank, 'Transgenic mice')
    print('Time:', time)

    documents = list()
    scores = collections.OrderedDict([ (pmid, score) for pmid, score in scores.items() if score >= 0.7 ])
    
    for filename in utils.get_filenames('..\\TP1\\samples'):
        corpus_reader = CorpusReader(filename)
        for pmid, document in corpus_reader.items():
            score = scores.get(pmid)
            if score is not None:
                documents.append((document, score))

    pprint.pprint(sorted(documents, key = lambda x: -x[1]))

    shutil.rmtree('index')
    '''