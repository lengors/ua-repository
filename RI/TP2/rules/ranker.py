import math

class DocumentCount:
    def __init__(self, count : int, idf):
        count = self.count = 0 if count is None else count
        self.weight = 0 if count == 0 else (1 + math.log10(count)) * idf

    def save(self):
        return '{}'.format(self.weight)

class Document:
    def __init__(self, positions : list, idf):
        positions = self.positions = [] if positions is None else positions
        self.weight = 0 if len(positions) == 0 else (1 + math.log10(len(positions))) * idf

    def save(self):
        return '{}{}'.format(self.weight, '' if len(self.positions) == 0 else ':{}'.format(','.join([ str(position) for position in self.positions ])))

class Term:
    def __init__(self, doc_index : dict, documents : set, default : type):
        self.length = len(doc_index)
        self.idf = math.log10(len(documents) / self.length)
        self.doc_index = { pmid : default(doc_index.get(pmid), self.idf) for pmid in documents }

    def __len__(self):
        return self.length

    def save(self):
        return ':{};{}'.format(self.idf, ';'.join([ '{}:{}'.format(pmid, doc.save()) for pmid, doc in self.doc_index.items() ]))

def ranker(indexer):
    default = Document if type(indexer._Indexer__tokenize) == indexer._Indexer__PositionableTokenize else DocumentCount
    for term, doc_index in indexer.terms.items():
        indexer.terms[term] = Term(doc_index, indexer.documents, default)