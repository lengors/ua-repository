

class CorpusReader:

    def __init__(self, filename):
        self.filename = filename
        self.dic = {}           # PMID : [word, word1, word2] in TI field


    def process(self):
        file = open(self.filename)
        pmid = ""
        read = False
        for line in file:
            if line == "":
                continue
            if "-" in line:
                l = line.split("-")
                if l[0] != "TI":
                    read = False
                if l[0] == "PMID":
                    pmid = l[1].strip()
                    self.dic[pmid] = []
                if l[0].strip() == "TI":
                    read = True
                    
            
            if read:
                try:
                    l = line.split("-")
                    for word in l[1].split(" "):
                        self.dic[pmid].append(word.strip())
                    
                except:
                    for word in line.strip().split(" "):
                        self.dic[pmid].append(word.strip())
            




a = CorpusReader("2004_TREC_ASCII_MEDLINE_1_sample")
a.process()
print(a.dic)