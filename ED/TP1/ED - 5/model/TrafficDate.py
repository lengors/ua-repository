from .Dimension import Dimension
from datetime import date

class TrafficDate(date, Dimension):
    @property
    def weekday(self):
        return super().weekday()

    @staticmethod
    def make(dt : date):
        return TrafficDate(dt.year, dt.month, dt.day)