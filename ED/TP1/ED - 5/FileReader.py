from collections import OrderedDict
from model import TaxiEvent
import re

class FileReader:


    def __init__(self, file):
        self.file = file
        self.list_taxis = []


    def taxifilereader(self):

        taxi_pos = None
        list_append = self.list_taxis.append

        with open(self.file) as file:
            for line in file:
                _, _, id, segment, _, _, dt  = re.split(r'\t+', line.strip().rstrip('\t'))
                list_append(TaxiEvent(segment, id, dt))
