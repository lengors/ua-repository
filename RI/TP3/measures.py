from tokenization import Tokenizer, tokenizer, simple_tokenizer
from ranker import Ranker
from index import Index
import math, rules

def precision(documents, relevance):
    if len(documents) == 0:
        return 0
    return sum(int(document in relevance) for document in documents) / len(documents)

def recall(documents, relevance):
    return sum(int(document in relevance) for document in documents) / len(relevance)

def fmeasure(P, R):
    if P == 0 and R == 0:
        return 0
    return 2 * P * R / (R + P)

def averagep(documents, relevance):
    if len(documents) == 0:
        return 0
    total = 0
    relevant = 0
    for i, document in enumerate(documents):
        relevant += int(document in relevance)
        total += relevant / (i + 1)
    return total / len(documents)

def ndcg(documents, relevance):
    if len(documents) == 0:
        return 0
    dcg = sum(relevance[document] / math.log2(i + 1) if i != 0 else relevance[document] for i, document in enumerate(documents) if document in relevance)
    idcg = sum(relevance / math.log2(i + 1) if i != 0 else relevance for i, relevance in enumerate(sorted(relevance.values(), key = lambda x: -x)))
    return dcg / idcg