from .Dimension import Dimension
from datetime import time

class TrafficTime(time, Dimension):
    @property
    def timestamp(self):
        return self.second + self.minute * 60 + self.hour * 1440

    @staticmethod
    def make(dt : time):
        return TrafficTime(dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)