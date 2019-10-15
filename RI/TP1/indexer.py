class Indexer:
    def __init__(self):
        self.terms = {}  # {string : {doc_id : [index1, index2]}}

    def update(self, doc_id, terms): #terms = list
        for i, term in terms:
            term_docs = self.terms.setdefault(term, { })
            doc_occurrences = term_docs.setdefault(doc_id, [ ])
            doc_occurrences.append(i)

    def __repr__(self):
        return str(self.terms)
