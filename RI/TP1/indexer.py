
class Indexer:

    def __init__(self):
        self.terms = {}  # {string : {doc_id : [index1, index2]}}

    def update(self, doc_id, terms): #terms = list
        for i, term in terms:
            if term in self.terms:
                if doc_id in self.terms[term]:
                    #self.terms[term][doc_id] += 1
                    self.terms[term][doc_id].append(i)
                else:
                    #self.terms[term][doc_id] = 1
                    self.terms[term][doc_id] = [i]
            else:
                self.terms[term] = {doc_id : [i]}

    def __repr__(self):
        return str(self.terms)
