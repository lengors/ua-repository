from .TaxiEvent import TaxiEvent

class Group:
    def __init__(self, model, *by):
        if len(by) == 0:
            self.events = list(model.events)
        else:
            self.events = (TaxiEvent.get_type(by[0]), dict())
            events = model.events if isinstance(model.events, list) else model.events[1].values()
            for event in events:
                _, object = self.events
                for i, dimension in enumerate(by):
                    value = getattr(event, dimension)
                    _, object = object.setdefault(value, (TaxiEvent.get_type(by[i - 1]), list() if i == len(by) - 1 else dict()))
                object.append(event)

    def average(self, *values):
        if len(values) == 0:
            return Group.avg(self.events)
        elif len(values) == 1:
            return Group.avg(self.events[1].get(values[0]))
        else:
            return [ Group.avg(self.events[1].get(value)) for value in values ]

    @staticmethod
    def avg(events):
        event_type, events = events
        if isinstance(events, list):
            return len(set([ event.segment for event in events ]))
        return sum([ Group.avg(event) for event in events.values() ]) / event_type.length()

class Model(Group):
    def __init__(self, events : list):
        self.events = events

    def group(self, *by):
        return Group(self, *by)