class Count:

    def __init__(self):
        self.count = 0
        self.pos = []

    def add(self, pos):
        self.count += 1
        self.pos.append(pos)

    def __repr__(self):
        return str((self.count, str(self.pos)))

class Indexer:

    def __init__(self):
        self.terms = {}  # string : [docs]

    def add(self, term, doc_id, index):
        self.terms[term][doc_id].add(index)

    def create(self, term, doc_id, index):
        self.terms[term][doc_id] = Count()
        self.terms[term][doc_id].add(index)


    def create_f_scratch(self, term, doc_id, index):
        self.terms[term] = {doc_id : Count()}
        self.terms[term][doc_id] = Count()
        self.terms[term][doc_id].add(index)


    def update(self, doc_id, terms): #terms = list
        for i, term in terms:
            if term in self.terms:
                if doc_id in self.terms[term]:
                    #self.terms[term][doc_id] += 1
                    self.add(term, doc_id, i)
                else:
                    #self.terms[term][doc_id] = 1
                    self.create(term, doc_id, i)
            else:
                #self.terms[term] = {doc_id : 1}
                self.create_f_scratch(term, doc_id, i)

    def __repr__(self):
        return str(self.terms)
