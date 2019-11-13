import random, math

class Counter:
    def __init__(self, a = 2):
        self.probability = 1 / a
        self.count = 0
        self._a = a
    
    def get(self):
        return self.count * self._a

    def increment(self):
        if random.random() < self.probability:
            self.count += 1

    def reset(self):
        self.count = 0

class LogarithmicCounter(Counter):
    def get(self):
        b = self._a - 1
        return (self._a ** self.count - b) / b

    def increment(self):
        if random.random() < self.probability ** self.count:
            self.count += 1

    def reset(self):
        self.count = 0

if __name__ == '__main__':
    total = 0
    counters = []
    amount, count = 10000, 10000
    counter = LogarithmicCounter(2)
    for i in range(amount):
        counter.reset()
        for j in range(count):
            counter.increment()
        total += counter.get()
        counters.append(counter.count)
    print(total / amount)
    for i in set(sorted(counters)):
        c = counters.count(i)
        print('counter value: {:02} - {:5} times - {:07.3f}%'.format(i, c, c * 100 / len(counters)))