import random
from math import sqrt, ceil

class BloomFilter:

    def __init__(self, rel = 8,  k = 5):      # k = num de hash functions, rel relação entre numero de palavras e tamanho do filtro
        self.rel = rel
        self.k = k
        self.primes = list()
        for i in range(2 * self.k):
            self.primes.append(self.__gen_prime(0, 50, self.primes))
        


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

    def __gen_prime(self, min_range, max_range, non_options = list()):
        lista = list()
        for i in range(min_range, max_range):
            if self.__is_prime(i) and not i in non_options:
                lista.append(i)

        return random.choice(lista)

    def __hashf(self, string, index):
        soma = self.primes[index]
        for pos in string:
            soma = soma * self.primes[self.k + index] * ord(pos)

        return soma % self.m

    def __repr__(self):
        return "n = " + str(self.n) + " ; f = " + str(self.f)

    def __len__(self):
        return ceil( self.bf.count(1) / self.k)
