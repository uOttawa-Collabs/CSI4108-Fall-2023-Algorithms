def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def prime_generator():
    n = 2
    yield n

    n = 3
    while True:
        if is_prime(n):
            yield n
        n += 2


def prime_factorize(n):
    if n < 1:
        return []

    if n == 1:
        return [(1, 1)]

    factors = []
    generator = prime_generator()

    for p in generator:
        t = 0

        while n % p == 0:
            n /= p
            t += 1

        if t > 0:
            factors.append((p, t))

        if p >= n:
            break

    return factors
