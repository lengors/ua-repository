import math, random

def is_prime(number):
    if number == 1 or number == 2:
        return number == 2
    if number % 2 == 0:
        return False
    for i in range(3, math.ceil(math.sqrt(number))):
        if number % i == 0:
            return False
    return True

def is_prime2(number, count = 1000):
    if number <= 0:
        return False
    if number <= 3:
        return number != 1
    if number % 2 == 0:
        return False
    for i in range(count):
        value = random.randint(2, number - 2)
        if (value ** (number - 1)) % number != 1:
            return False
    return True

for i in range(1, 50):
    print(i, is_prime2(i, 5))