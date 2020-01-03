def generate_primes(count, start = 2):
    if count == 0:
        return [ ]
    start = max(start, 2)
    primes = set([ 2 ])
    prime, lastprime = 3, 2
    while lastprime < start:
        for value in primes:
            if prime % value == 0:
                break
        else:
            lastprime = prime
            primes.add(prime)
        prime += 2
    result = [ lastprime ]
    prime = lastprime + int(lastprime != 2) + 1
    while len(result) < count:
        for value in primes:
            if prime % value == 0:
                break
        else:
            primes.add(prime)
            result.append(prime)
        prime += 2
    return result