"""class CorpusReader:
    def __init__(self, file):
        self.documents, read = dict(), False
        for line in file:
            parts = None
            if len(line.strip()) == 0:
                continue
            if '-' in line:
                parts = line.split('-')
                if parts[0] != 'TI':
                    read = False
                if parts[0] == 'PMID':
                    pmid = parts[1].strip()
                    self.documents[pmid] = str()
                if parts[0].strip() == 'TI':
                    read = True
            if read:
                sentence = line if parts is None else '-'.join(parts[1:])
                self.documents[pmid] += sentence"""

class CorpusReader:
    def __init__(self, file):
        self.load(file)

    def __load(self, file):
        current, pmid = str(), None
        self.documents, read = dict(), False
        for line in file:
            if len(line) >= 5 and line[4] == '-':
                if line[:4] == 'PMID':
                    if pmid is not None:
                        self.documents[pmid] = current
                    pmid = line[5:].strip()
                    current, read = str(), False
                else:
                    read = line[:2] == 'TI'
                    if read:
                        current += line[5:]
            elif read:
                current += line
        if pmid is not None:
            self.documents[pmid] = current

    def load(self, file):
        if type(file) == str:
            with open(file, 'r') as fin:
                self.__load(fin)
        else:
            self.__load(fin)