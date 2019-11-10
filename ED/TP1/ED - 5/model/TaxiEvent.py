from .TrafficDate import TrafficDate
from .TrafficTime import TrafficTime
from datetime import datetime
from .Taxi import Taxi

class TaxiEvent:

    def __init__(self, segment, taxi, dt : datetime):
        self.segment = segment
        self.taxi = Taxi.get(taxi)
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        self.date = TrafficDate.get(dt.date())
        self.time = TrafficTime.get(dt.time())

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return '{}'.format(self.segment)

    @staticmethod
    def get_type(value):
        if value == 'taxi':
            return Taxi
        elif value == 'date':
            return TrafficDate
        elif value == 'time':
            return TrafficTime
        return None
