import os
from segment_index import segments_info
from math import sqrt

class Ranking:


    def __init__(self,  index_folder):
        self.index_folder = index_folder

    def find_term_in_index(self, term):
        for key, (word_init, word_final) in segments_info.items():
            if term > word_init and term < word_final:
                return key

    def normalize(self, query):
        val = query.values()
        aux = sqrt(sum(list(map(lambda x : x ** 2, val))))
        query = {key : value / aux for key, value in query.items()}
        return query

    def compare(self, query, doc):
        value = 0
        
        for term in query:
            if term in doc:
                value += float(query[term]) * float(doc[term])
        
        return value

    def rank(self, query):
        terms = query.split(" ")
        docs = dict()               # {doc : {term}
        q = dict()
        for term in terms:
            term = term.lower()
            segment = self.find_term_in_index(term)
            with open(os.path.join(self.index_folder, segment)) as file:
                for line in file:
                    line = line.strip()
                    if line.split(":")[0] == term:
                        term, value = line.split(':', 1)
                        idf, *val = value.split(';')
                        if not term in q:
                            q[term] = float(idf) * query.lower().count(term)
                        for v in val:
                            doc, *shit = v.split(":")
                            tfidf = shit[0]
                            if not doc in docs:
                                docs[doc] = dict()
                            docs[doc][term] = tfidf
        
        q = self.normalize(q)
        scores = dict()
        for doc in docs:
            scores[doc] = self.compare(q, docs[doc])
        scores = sorted(scores.items(), key=lambda x: -x[1])
        return scores


if __name__ == "__main__":
    r = Ranking("index")
    scores = r.rank("Generating transgenic mice")
    print(scores)



