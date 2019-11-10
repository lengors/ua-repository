# from TaxiPosition import TaxiPosition
from .Registable import Registable

class Taxi(int, Registable):
    @staticmethod
    def make(id):
        return Taxi(id)