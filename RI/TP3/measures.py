from tokenization import Tokenizer
from ranker import Ranker
from index import Index
import math

def precision(documents, relevance):
    pass

def recall(documents, relevance):
    pass

def fmeasure(P, R):
    return 2 * P * R / (R + P)

def averagep(documents, relevance):
    total = 0
    relevant = 0
    for i, document in enumerate(documents):
        relevant += int(document in relevance)
        total += relevant / (i + 1)
    return total / len(documents)

def ndcg(documents, relevance):
    dcg = sum(relevance[document] / math.log2(i + 1) for i, document in enumerate(documents) if document in relevance)
    idcg = sum(relevance / math.log2(i + 1) for i, relevance in enumerate(sorted(relevance.values(), key = lambda x: -x)))
    return dcg / idcg