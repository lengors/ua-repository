import random

class Counter:
    def __init__(self):
        self.reset()

    def get(self):
        return self.count

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

class ProbabilisticCounter(Counter):
    def __init__(self, a = 2):
        super().__init__()
        self._probability = 1 / a
        self._a = a
    
    def get(self):
        return super().get() * self._a

    def increment(self):
        if random.random() < self._probability:
            self.count += 1

class LogarithmicCounter(ProbabilisticCounter):
    def get(self):
        b = self._a - 1
        return (self._a ** self.count - b) / b

    def increment(self):
        if random.random() < self._probability ** self.count:
            self.count += 1