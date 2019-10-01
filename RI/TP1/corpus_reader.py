class CorpusReader:
    def __init__(self, file):
        self.documents = dict()
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
                self.documents[pmid] += sentence