from prime_generator import generate_primes
import random, math

class BloomFilter:

    def __init__(self, m,  k = 5):      # k = num de hash functions, rel relação entre numero de palavras e tamanho do filtro
        self.k = k
        self.m = m
        self.primes = list()
        self.storage = [ 0 ] * m
        self.primes = generate_primes(self.k << 1, start = 3)
        random.shuffle(self.primes)

    def contains(self, value):
        for i in range(self.k):
            if self.storage[self.__hash(value, i) % self.m] == 0:
                return False
        return True

    def extend(self, values):
        count = 0
        for value in values:
            count += self.insert(value)
        return count

    def insert(self, value):
        if self.contains(value):
            return 0
        for i in range(self.k):
            self.storage[self.__hash(value, i) % self.m] = 1
        return 1

    def __hash(self, string, index):
        hash = self.primes[index]
        prime = self.primes[self.k + index]
        for character in string:
            hash = hash * prime + ord(character)
        return hash

    def __repr__(self):
        return "n = " + str(self.n) + " ; f = " + str(self.f)

    def __len__(self):
        return round(- (self.m / self.k) * math.log(1 - sum(self.storage) / self.m))

    @property
    def f(self):
        return sum(self.storage) / self.m
