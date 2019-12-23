from .Dimension import Dimension

class RoadSegment(int, Dimension):
    @staticmethod
    def make(id):
        return RoadSegment(id)