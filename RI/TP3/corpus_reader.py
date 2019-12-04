class CorpusReader:
    def __init__(self, file):
        self.file = file

    def items(self):
        if type(self.file) == str:
            self.file = open(self.file, 'r', encoding = 'iso-8859-1')
        current, pmid, read = str(), None, False
        for line in self.file:
            if len(line) >= 5 and line[4] == '-':
                if line[:4] == 'PMID':
                    if pmid is not None:
                        yield (pmid, current)
                    pmid = line[5:].strip()
                    current, read = str(), False
                else:
                    read = line[:2] == 'TI'
                    if read:
                        current += line[5:]
            elif read:
                current += line
        if pmid is not None:
            yield (pmid, current)
        self.file.close()