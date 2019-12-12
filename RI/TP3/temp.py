from measures import *
import pprint, shutil
import collections
import itertools
import pprint

if __name__ == '__main__':
    with open('queries.relevance.txt') as fin:
        lines = [ line.strip().split('\t') for line in fin ]

    relevances = dict()
    for queryid, pmid, relevance in lines:
        relevance = float(relevance)
        query = relevances.setdefault(queryid, {})
        query.setdefault(pmid, relevance + 1 - int(relevance == 2) * 2)

    tokenizer.make_rule(rules.stopping, 'stopwords.txt')
    index = Index.segment_on_load('output', tokenizer = tokenizer)
    ranker = Ranker(index)

    with open('queries.txt', 'r') as fin:
        queries = [ tuple(line.strip().split('\t')) for line in fin ]

    length = max(len(query) for qid, query in queries)
    queries = { query : ranker.rank(query[1]) for query in queries }

    formatter_header = '{:2}   {:>14}   {:>14}   {:>14}   {:>14}   {:>14}'
    formatter_body = '{:02d}   {:>14.3f}   {:>14.3f}   {:>14.3f}   {:>14.3f}   {:>14.3f}'

    for i in [ 10, 20, 50 ]:
        print('Top-{}'.format(i))
        print(formatter_header.format('', 'Precision', 'Recall', 'F-Measure', 'Avg. Precision', 'NDCG'))
        ap = ar = af = aa = an = 0
        for query, ranking in sorted(queries.items(), key = lambda item: int(item[0][0])):
            relevance = relevances[query[0]]
            documents = collections.OrderedDict(itertools.islice(ranking.items(), i))
            p = precision(documents, relevance)
            r = recall(documents, relevance)
            f = fmeasure(p, r)
            a = averagep(documents, relevance)
            n = ndcg(documents, relevance)

            ap += p
            ar += r
            af += f
            aa += a
            an += n

            print(formatter_body.format(int(query[0]), p, r, f, a, n))

        print()
        print('Top-{} - Average'.format(i))
        print(formatter_header.format('', 'Precision', 'Recall', 'F-Measure', 'Avg. Precision', 'NDCG'))
        print(formatter_body.format(int(query[0]), ap / len(queries), ar / len(queries), af / len(queries), aa / len(queries), an / len(queries)))
        print()

    shutil.rmtree('index')