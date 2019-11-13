from collections import OrderedDict
from RoadSegment import RoadSegment
from model import TaxiEvent
import re

class FileReader:


    def __init__(self, file):
        self.file = file
        self.list_roads = []
        self.list_taxis = []


    def taxifilereader(self):

        taxi_pos = None
        list_append = self.list_taxis.append

        with open(self.file) as file:
            for line in file:
                _, _, id, segment, _, _, dt  = re.split(r'\t+', line.strip().rstrip('\t'))
                list_append(TaxiEvent(segment, id, dt))


    def roadfilereader(self):

        road = None
        list_append = self.list_roads.append

        with open(self.file) as file:
            for line in file:
                road_args = re.split(r'\t+', line.rstrip('\t'))
                road = RoadSegment(road_args[0], road_args[1], road_args[2], road_args[3], road_args[4], road_args[5])
                list_append(road)
