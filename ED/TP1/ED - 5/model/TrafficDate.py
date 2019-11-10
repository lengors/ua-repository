from .Registable import Registable
from datetime import date

class TrafficDate(date, Registable):
    @property
    def weekday(self):
        return super().weekday()

    @staticmethod
    def make(dt : date):
        return TrafficDate(dt.year, dt.month, dt.day)