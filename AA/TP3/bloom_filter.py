import random
from math import sqrt

class BloomFilter:

    def __init__(self, rel = 8,  k = 5):      # k = num de hash functions
        self.rel = rel
        self.k = k
        self.primes = [ self.__gen_prime(100, 500) for i in range(self.k) ]


    def extend(self, lista):
        self.__initialize(len(lista))
        for ele in lista:
            ele = ele.strip()
            self.__add(ele)
        self.__calc_f()


    def contains(self, element):
        for i in range(self.k):
            index = self.__hashf(element, i)
            if self.bf[index] == 0:
                return False
        return True

    def __initialize(self, n):
        self.n = n
        self.m = self.rel * self.n
        self.bf = [ 0 for i in range(self.m) ]

    def __add(self, element):
        for i in range(self.k):
            index = self.__hashf(element, i)
            if self.bf[index] == 0:
                self.bf[index] = 1

    def __calc_f(self):
        soma = 0
        for ele in self.bf:
            soma += 1 if ele == 1 else 0
        self.f = soma / self.m

    def __is_prime(self, n):
        if n % 2 == 0:
            return False

        for i in range(3, n):
            if n % i == 0:
                return False
        return True

    def __gen_prime(self, min_range, max_range):
        lista = list()
        for i in range(min_range, max_range):
            if self.__is_prime(i):
                lista.append(i)

        return random.choice(lista)

    def __hashf(self, string, index):
        soma = 0
        for pos in string:
            soma += ord(pos) * self.primes[index]

        return soma % self.m

    def __repr__(self):
        return "n = " + str(self.n) + " ; f = " + str(self.f)
