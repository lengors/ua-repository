# from TaxiPosition import TaxiPosition
from .Dimension import Dimension

class Taxi(int, Dimension):
    @staticmethod
    def make(id):
        return Taxi(id)